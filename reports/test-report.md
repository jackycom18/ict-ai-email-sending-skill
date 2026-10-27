# 邮件发送 Skill 验证报告

- 日期：2026-10-27
- 命令：`python -X utf8 -m unittest tests.test_sendmail_skill -v`
- 结果：退出码 0，2 项测试通过

覆盖内容：

1. 缺少收件人时拒绝发送并返回中文错误。
2. SMTP SSL 发送路径使用配置中的服务器、端口、邮箱和授权码。
3. 信封发件人、收件人、中文主题、正文和附件均正确构造。

安全说明：测试使用内存中的 SMTP 传输替身，不向外部邮箱发送邮件，
也不会读取或保存真实授权码。

## 真实 SMTP 投递

- 命令：`python -X utf8 scripts/send_ethereal_demo.py`
- 测试服务：Ethereal Email（免费一次性测试邮箱）
- SMTP：`smtp.ethereal.email:587`
- 结果：发送成功，包含中文主题和附件
- 脱敏记录：`reports/ethereal-delivery.json`
