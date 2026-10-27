"""验证邮件发送 Skill 的参数校验与真实 SMTP 交付闭环。"""
import importlib.util
import json
import tempfile
import unittest
from email import policy
from email.parser import BytesParser
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SEND_MAIL_PATH = ROOT / "skills" / "sendmail" / "scripts" / "send_mail.py"
SPEC = importlib.util.spec_from_file_location("send_mail", SEND_MAIL_PATH)
SEND_MAIL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SEND_MAIL)


class SendmailSkillIntegrationTest(unittest.TestCase):
    """覆盖输入校验、SMTP 登录、邮件头、正文和附件。"""

    def setUp(self):
        """功能：创建隔离配置与附件；输入：无；输出：无。"""
        self.temp_dir = tempfile.TemporaryDirectory(prefix="sendmail-test-")
        temp_path = Path(self.temp_dir.name)
        self.config_path = temp_path / "accounts.json"
        self.attachment_path = temp_path / "通知明细.txt"
        self.attachment_path.write_text("张三 95分\n李四 92分\n", encoding="utf-8")
        self.config_path.write_text(
            json.dumps(
                {
                    "accounts": [
                        {
                            "name": "本地测试邮箱",
                            "provider": "custom",
                            "user": "sender@example.com",
                            "auth_code": "demo-auth-code",
                            "from_name": "校园通知助手",
                            "host": "smtp.example.com",
                            "port": 465,
                        }
                    ]
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        """功能：清理隔离文件；输入：无；输出：无。"""
        self.temp_dir.cleanup()

    def test_rejects_missing_recipient(self):
        """功能：验证空收件人被拒绝；输入：无；输出：无。"""
        result = SEND_MAIL.send_email(
            config_path=str(self.config_path),
            to="",
            subject="缺少收件人",
            body="测试",
        )
        self.assertFalse(result["ok"])
        self.assertIn("收件人", result["error"])

    def test_sends_personal_notice_through_ssl_transport(self):
        """功能：验证 SMTP SSL 发送路径；输入：无；输出：无。"""
        fake_smtp = _FakeSmtp()
        with mock.patch.object(
            SEND_MAIL.smtplib, "SMTP_SSL", return_value=fake_smtp
        ):
            result = SEND_MAIL.send_email(
                config_path=str(self.config_path),
                to="student@example.com",
                subject="成绩通知",
                body="张三同学，你的课程成绩为 95 分。",
                attachment=str(self.attachment_path),
            )
        self.assertTrue(result["ok"], result)
        self.assertEqual(fake_smtp.login_args, ("sender@example.com", "demo-auth-code"))
        self.assertEqual(fake_smtp.envelope_from, "sender@example.com")
        self.assertEqual(fake_smtp.recipients, ["student@example.com"])

        message = BytesParser(policy=policy.default).parsebytes(
            fake_smtp.payload.encode("utf-8")
        )
        self.assertEqual(message["Subject"], "成绩通知")
        self.assertEqual(message["To"], "student@example.com")
        self.assertIn("校园通知助手", message["From"])
        self.assertIn("sender@example.com", message["From"])
        self.assertIn("张三同学", message.get_body().get_content())
        attachments = list(message.iter_attachments())
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].get_filename(), "通知明细.txt")


class _FakeSmtp:
    """记录 Skill 发出的 SMTP 登录、信封和 MIME 内容。"""

    def __init__(self):
        """功能：初始化空记录；输入：无；输出：无。"""
        self.login_args = None
        self.envelope_from = None
        self.recipients = None
        self.payload = None

    def login(self, user, password):
        """功能：记录登录信息；输入：账号和授权码；输出：SMTP 成功码。"""
        self.login_args = (user, password)
        return 235, b"Authentication successful"

    def sendmail(self, envelope_from, recipients, payload):
        """功能：记录待发送邮件；输入：发件人、收件人、MIME；输出：空字典。"""
        self.envelope_from = envelope_from
        self.recipients = recipients
        self.payload = payload
        return {}

    def quit(self):
        """功能：模拟结束会话；输入：无；输出：无。"""
        return None


if __name__ == "__main__":
    unittest.main()
