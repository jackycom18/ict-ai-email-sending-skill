"""通过一次性测试邮箱执行真实 SMTP 邮件发送演示。"""
import json
import subprocess
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEND_MAIL = ROOT / "skills" / "sendmail" / "scripts" / "send_mail.py"
REPORT = ROOT / "reports" / "ethereal-delivery.json"


def create_test_account() -> dict:
    """功能：创建免费 Ethereal 测试账号；输入：无；输出：账号与 SMTP 配置。"""
    request = urllib.request.Request(
        "https://api.nodemailer.com/user",
        data=json.dumps(
            {"requestor": "Huawei ICT 1.14 Agent practice", "version": "1.0"}
        ).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "ICT-Practice/1.0"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def run_demo() -> dict:
    """功能：真实发送测试邮件并生成脱敏报告；输入：无；输出：发送报告字典。"""
    account = create_test_account()
    with tempfile.TemporaryDirectory(prefix="ict-mail-") as temp_dir:
        temp_path = Path(temp_dir)
        config_path = temp_path / "accounts.json"
        attachment_path = temp_path / "课程成绩通知.txt"
        attachment_path.write_text(
            "张三,云计算基础,95\n李四,云计算基础,92\n",
            encoding="utf-8",
        )
        config_path.write_text(
            json.dumps(
                {
                    "accounts": [
                        {
                            "name": "Ethereal 测试邮箱",
                            "provider": "custom",
                            "user": account["user"],
                            "auth_code": account["pass"],
                            "from_name": "校园通知助手",
                            "host": account["smtp"]["host"],
                            "port": account["smtp"]["port"],
                        }
                    ]
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                str(SEND_MAIL),
                "--config",
                str(config_path),
                "--to",
                account["user"],
                "--subject",
                "课程成绩通知 - ICT 1.14",
                "--body",
                "张三同学，你的《云计算基础》课程成绩为 95 分。",
                "--attachment",
                str(attachment_path),
            ],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "SMTP 发送失败")
    return {
        "date": datetime.now(timezone.utc).isoformat(),
        "status": "sent",
        "provider": "Ethereal Email",
        "smtp_host": account["smtp"]["host"],
        "smtp_port": account["smtp"]["port"],
        "recipient": account["user"].replace(account["user"].split("@")[0], "***"),
        "subject": "课程成绩通知 - ICT 1.14",
        "attachment": "课程成绩通知.txt",
        "skill_output": result.stdout.strip().replace(
            account["user"], "***@ethereal.email"
        ),
    }


def main() -> None:
    """功能：执行真实发送并保存报告；输入：无；输出：无。"""
    report = run_demo()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
