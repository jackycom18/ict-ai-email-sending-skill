# SendmailSkills — Agent 发邮件技能

让 AI 智能体（Agent）通过 SMTP 协议自动发送邮件。用户只需填写邮箱账号和授权码，即可让 Agent 自动撰写并发送邮件。

## 特性

- ✅ **零第三方依赖**：仅用 Python 标准库 `smtplib` + `email`
- ✅ **多邮箱支持**：QQ / 163 / 126 / 新浪 / Gmail，自动识别 SMTP 服务器与端口
- ✅ **多账号路由**：可配置多个邮箱，按发件人自动切换
- ✅ **纯文本 + HTML 邮件**：支持富文本正文
- ✅ **抄送/密送/附件**：完整的邮件发送能力
- ✅ **清晰错误提示**：授权码错误、服务器连接失败等自动识别

## 快速开始

### 1. 获取授权码

| 邮箱 | 如何获取授权码 |
|------|----------------|
| QQ | 设置 → 账户 → 开启「POP3/SMTP服务」→ 生成授权码 |
| 163 / 126 | 设置 → POP3/SMTP/IMAP → 开启 SMTP → 生成授权码 |
| 新浪 | 设置 → 客户端 POP3/SMTP → 开启 → 获取授权码 |
| Gmail | 开启两步验证 → 生成「应用专用密码」 |

> ⚠️ 授权码 ≠ 登录密码，请务必使用授权码/应用专用密码。

### 2. 配置账号

```bash
cp config/accounts.example.json config/accounts.json
```

编辑 `config/accounts.json`，填入邮箱账号和授权码：

```json
{
  "accounts": [
    {
      "name": "我的QQ邮箱",
      "provider": "qq",
      "user": "yourname@qq.com",
      "auth_code": "你的授权码",
      "from_name": "张三"
    }
  ]
}
```

### 3. 发送邮件

**CLI 方式：**

```bash
python scripts/send_mail.py \
  --config config/accounts.json \
  --to "receiver@example.com" \
  --subject "会议通知" \
  --body "明天下午 3 点开会"
```

**Python 模块方式：**

```python
from scripts.send_mail import send_email

result = send_email(
    config_path="config/accounts.json",
    to="receiver@example.com",
    subject="会议通知",
    body="明天下午 3 点开会",
)
print(result)
```

## 目录结构

```
SendmailSkills/
├── SKILL.md                       # 技能定义（Agent 读取）
├── README.md                      # 使用说明
├── config/
│   ├── accounts.example.json      # 配置文件模板
│   └── accounts.json              # 你的配置（已 gitignore，不提交）
└── scripts/
    └── send_mail.py               # 核心发送脚本
```

## 支持的邮箱

| provider | 邮箱 | SMTP 服务器 | 端口 |
|----------|------|-------------|------|
| qq | QQ 邮箱 | smtp.qq.com | 587 |
| 163 | 163 邮箱 | smtp.163.com | 465 |
| 126 | 126 邮箱 | smtp.126.com | 465 |
| sina | 新浪邮箱 | smtp.sina.com | 465 |
| gmail | Gmail | smtp.gmail.com | 587 |
| custom | 自定义 | 自定义 host/port | 自定义 |

## 安全说明

- 授权码保存在本地 `config/accounts.json`，该文件已加入 `.gitignore`，不会被提交到仓库
- 请勿将 `accounts.json` 上传到任何公开平台

## 许可证

MIT
