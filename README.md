# Agent 办公实践邮件发送 Skill

本项目对应华为 ICT 2026 云赛道实践赛第 14 题：
“基于 AI 开发者空间的 Agent 办公实践邮件发送 Skill 实践”。

项目复用官方 `SendmailSkills` 的邮件发送实现，使用 Python 标准库
`smtplib` 和 `email` 完成纯文本、HTML、抄送、密送与附件发送。

## 目录

- `skills/sendmail/`：官方邮件发送 Skill、脚本和配置模板。
- `data/recipients.csv`：成绩通知示例名单。
- `tests/`：参数校验与 SMTP SSL 发送路径验证。
- `scripts/send_ethereal_demo.py`：一次性测试邮箱的真实 SMTP 投递演示。
- `Agent办公实践邮件发送Skill实践作品/`：比赛要求的两份归档文件。

## 配置

复制配置模板：

```powershell
Copy-Item skills/sendmail/config/accounts.example.json skills/sendmail/config/accounts.json
```

在本地 `accounts.json` 中填写邮箱地址和邮箱授权码。该文件已被
`.gitignore` 排除，禁止提交到公开仓库。QQ、163、126、新浪邮箱使用
SMTP 授权码，Gmail 使用应用专用密码。

## 发送

```powershell
python skills/sendmail/scripts/send_mail.py `
  --config skills/sendmail/config/accounts.json `
  --to "student@example.com" `
  --subject "课程成绩通知" `
  --body "张三同学，你的课程成绩为 95 分。" `
  --attachment "data/通知明细.txt"
```

## 验证

```powershell
python -X utf8 -m unittest tests.test_sendmail_skill -v
```

测试覆盖空收件人拦截、SMTP SSL 调用、认证参数、信封收件人、
中文主题、正文和附件。仓库内没有保存任何真实邮箱授权码。

真实 SMTP 投递演示：

```powershell
python -X utf8 scripts/send_ethereal_demo.py
```

脚本创建免费的一次性 Ethereal 测试邮箱，通过官方 Skill 发送邮件，
并在 `reports/ethereal-delivery.json` 写入不含凭据的发送结果。
