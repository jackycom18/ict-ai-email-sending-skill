# Agent办公实践邮件发送Skill实践

## 实践信息

- 日期：2026-10-27
- 赛题：基于 AI 开发者空间的 Agent 办公实践邮件发送 Skill 实践
- 工作目录：`C:\Users\Xzj13\Desktop\pro\email-sending-skill-practice`
- 运行环境：Windows 11、Python 3.14.6
- 云资源费用：0 元

## 一、实践目标

本次实践安装邮件发送 Skill，配置 SMTP 发件账号，构造包含中文主题、
正文及附件的邮件，并验证 Agent 从自然语言办公需求到邮件发送调用的
完整流程。

## 二、安装邮件发送 Skill

按实验手册执行：

```text
帮我安装“https://gitcode.com/agent-best-practices/SendmailSkills.git”项目中的技能。
```

Agent 克隆并检查仓库后确认：

- Skill 名称：`sendmail`
- 来源：`https://gitcode.com/agent-best-practices/SendmailSkills.git`
- 使用提交：`ea4a3ac8d0f873ea288b9e4ec905e29d965d0e5b`
- 依赖：Python 标准库 `smtplib` 和 `email`，无第三方运行时依赖

Skill 已整理到 `skills/sendmail/`，包括：

```text
skills/sendmail/
├── SKILL.md
├── README.md
├── config/accounts.example.json
└── scripts/send_mail.py
```

## 三、邮箱授权码与安全配置

手册要求使用邮箱 SMTP 授权码，而不是网页登录密码。对应服务商如下：

| 邮箱 | SMTP 服务器 | 端口 |
|---|---|---|
| QQ | smtp.qq.com | 587 |
| 163 / 126 | smtp.163.com / smtp.126.com | 465 |
| 新浪 | smtp.sina.com | 465 |
| Gmail | smtp.gmail.com | 587 |

本次实践使用免费的一次性 Ethereal 测试邮箱完成真实 SMTP 投递，
没有获取或使用用户的个人邮箱授权码。账号配置使用以下模板：

```json
{
  "accounts": [
    {
      "name": "校园通知邮箱",
      "provider": "163",
      "user": "yourname@163.com",
      "auth_code": "你的邮箱授权码",
      "from_name": "校园通知助手"
    }
  ]
}
```

真实配置应保存为 `skills/sendmail/config/accounts.json`。该项目文件已加入
`.gitignore`，不会提交到公开仓库。

## 四、自然语言办公需求

模拟用户需求：

```text
给名单里的所有同学发送课程成绩通知。
```

示例名单 `data/recipients.csv`：

| 姓名 | 邮箱 | 课程 | 成绩 |
|---|---|---|---|
| 张三 | student01@example.com | 云计算基础 | 95 |
| 李四 | student02@example.com | 云计算基础 | 92 |
| 王五 | student03@example.com | 云计算基础 | 88 |

Agent 识别到“发送邮件”请求后加载 `sendmail` Skill，并执行以下工作流：

1. 读取收件人姓名、邮箱、课程和成绩。
2. 按每位学生生成个性化正文。
3. 从本地配置选择发件账号及 SMTP 参数。
4. 构造 MIME 邮件并执行 SMTP 登录、投递。
5. 汇总成功与失败清单。

个性化正文示例：

```text
张三同学：

你的《云计算基础》课程成绩为 95 分。
请登录教学系统查看详细评语。

校园通知助手
```

## 五、邮件发送调用

单封通知的命令形式：

```powershell
python skills/sendmail/scripts/send_mail.py `
  --config skills/sendmail/config/accounts.json `
  --to "student01@example.com" `
  --subject "课程成绩通知" `
  --body "张三同学，你的课程成绩为 95 分。" `
  --attachment "data/通知明细.txt"
```

Skill 返回结构：

```json
{
  "ok": true,
  "message": "邮件已发送至 student01@example.com"
}
```

真实发送验证使用：

```powershell
python -X utf8 scripts/send_ethereal_demo.py
```

执行结果：

```json
{
  "status": "sent",
  "provider": "Ethereal Email",
  "smtp_host": "smtp.ethereal.email",
  "smtp_port": 587,
  "subject": "课程成绩通知 - ICT 1.14",
  "attachment": "课程成绩通知.txt"
}
```

官方 Skill 返回“邮件已发送”，说明 SMTP 登录与投递成功。一次性测试账号
在使用后未写入仓库，报告中已隐藏邮箱地址和全部凭据。

如果授权码错误、网络不可达、收件人为空或附件不存在，Skill 会停止发送
并返回可读的中文错误，避免误报成功。

## 六、验证结果

执行：

```powershell
python -X utf8 -m unittest tests.test_sendmail_skill -v
```

结果：

```text
Ran 2 tests in 0.026s

OK
```

验证内容包括：

- 空收件人被拦截。
- SMTP SSL 发送路径被正确调用。
- 登录用户名与授权码来自配置。
- 信封发件人和收件人正确。
- 中文主题和正文正确写入 MIME。
- 附件名称和内容正确加入 MIME。

自动化测试使用内存 SMTP 传输替身，不消耗云资源；另外通过 Ethereal
一次性测试邮箱完成了一次真实 SMTP 投递，两种验证均不会泄露授权码。

## 七、注意事项

1. QQ、163、126、新浪邮箱必须使用 SMTP 授权码。
2. Gmail 必须使用应用专用密码。
3. Outlook/微软邮箱需 OAuth2，不在本 Skill 支持范围内。
4. 大批量发送时增加延时，避免触发邮箱服务商风控。
5. 记录每封邮件的发送结果，失败项人工复核后重试。
6. 一次性测试账号仅用于本次验证，真实办公发送仍需用户自己的授权码。

## 八、归档结果

最终作品目录：

```text
Agent办公实践邮件发送Skill实践作品/
├── Agent办公实践邮件发送Skill实践.md
└── readme.md
```

两份文件已按实验手册要求命名并完成归档。
