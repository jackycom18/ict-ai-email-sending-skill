# 代码地图

> 最后更新：2026-10-27

## 总体结构

```text
email-sending-skill-practice/
├── skills/sendmail/             官方邮件发送 Skill
├── tests/                       SMTP 发送路径测试
├── data/recipients.csv          个性化通知示例
├── docs/                        项目备忘、代码地图与设计
├── reports/                     测试记录
└── Agent办公实践邮件发送Skill实践作品/
```

## 逐文件核心内容

### `skills/sendmail/scripts/send_mail.py`

- 用途：加载账号配置、构造 MIME 邮件并通过 SMTP 发送。
- 关键入口：`send_email()`、`_resolve_account()`、`_split_addresses()`。
- 注意：授权码来自本地 `accounts.json`，该文件不进入版本库。

### `tests/test_sendmail_skill.py`

- 用途：验证输入校验与 SMTP SSL 发送路径。
- 数据流：临时配置与附件 → 官方 `send_email()` → 内存 SMTP 替身 → MIME 断言。
- 注意：测试不连接外部邮箱，不读取真实授权码。

### `data/recipients.csv`

- 用途：演示姓名、邮箱、课程与成绩的个性化通知来源。
