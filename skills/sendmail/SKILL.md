---
name: sendmail
description: "支持 Agent 通过 SMTP 协议自动发送邮件。用户只需配置邮箱账号与授权码（QQ/163/126/新浪/Gmail），即可让 AI 智能体自动撰写并发送邮件。"
version: "1.0.0"
metadata:
  dependencies:
    - "./scripts/send_mail.py"
    - "./config/accounts.example.json"
---

# Sendmail — Agent 发邮件技能

## 角色定位

你是**邮件发送执行器**，负责将用户或上游 Agent 的邮件意图转化为真实的邮件发送操作。本技能封装了 SMTP 邮件发送的完整流程，用户只需预先配置好邮箱账号与授权码，即可让 AI 智能体自动发送邮件。

## 核心能力

- 通过 SMTP 协议发送纯文本 / HTML 邮件
- 支持多个常用邮箱服务商（QQ、163、126、新浪、Gmail）
- 自动识别发件人账号对应的 SMTP 服务器与端口（无需用户手动填 host/port）
- 支持多账号配置，按发件人自动路由到对应邮箱
- 提供清晰的错误提示（认证失败、服务器连接失败、收件人缺失等）

## 环境要求

- Python >= 3.7（仅依赖标准库 `smtplib`、`email`，无需安装第三方包）

---

## 配置说明（用户操作）

### 第一步：获取邮箱授权码

| 邮箱 | SMTP 服务器 | 端口 | 授权码获取方式 |
|------|-------------|------|----------------|
| QQ 邮箱 | smtp.qq.com | 587 | 设置 → 账户 → 开启「POP3/SMTP 服务」→ 生成授权码 |
| 163 邮箱 | smtp.163.com | 465 | 设置 → POP3/SMTP/IMAP → 开启 SMTP → 生成授权码 |
| 126 邮箱 | smtp.126.com | 465 | 同 163 |
| 新浪邮箱 | smtp.sina.com | 465 | 设置 → 客户端 POP3/SMTP → 开启 → 获取授权码 |
| Gmail | smtp.gmail.com | 587 | 开启两步验证 → 生成「应用专用密码」 |

> ⚠️ **重要**：授权码 ≠ 登录密码。QQ/163/126/新浪必须使用授权码；Gmail 必须使用「应用专用密码」。
> ⚠️ Outlook/微软邮箱不支持（需 OAuth2），请使用上述邮箱。

### 第二步：填写配置文件

将 `config/accounts.example.json` 复制为 `config/accounts.json`，填入你的邮箱账号和授权码：

```json
{
  "accounts": [
    {
      "name": "我的QQ邮箱",
      "provider": "qq",
      "user": "yourname@qq.com",
      "auth_code": "你的QQ邮箱授权码",
      "from_name": "张三"
    },
    {
      "name": "我的163邮箱",
      "provider": "163",
      "user": "yourname@163.com",
      "auth_code": "你的163邮箱授权码",
      "from_name": "张三"
    }
  ]
}
```

- `provider` 可选：`qq` / `163` / `126` / `sina` / `gmail` / `custom`
- `custom` 时需额外提供 `host` 和 `port` 字段
- 如果 `from_name` 为空，将使用邮箱地址作为发件人名称

---

## 执行方式

### 方式一：CLI 命令行直接发送

```bash
python scripts/send_mail.py \
  --config config/accounts.json \
  --from yourname@qq.com \
  --to "receiver@example.com" \
  --subject "会议通知" \
  --body "明天下午 3 点开会" \
  [--html] \
  [--cc "cc@example.com"] \
  [--bcc "bcc@example.com"] \
  [--attachment "/path/to/file.pdf"]
```

### 方式二：作为 Python 模块被 Agent 调用

```python
from scripts.send_mail import send_email

result = send_email(
    config_path="config/accounts.json",
    from_addr="yourname@qq.com",   # 可选，不传则用第一个账号
    to="receiver@example.com",
    subject="会议通知",
    body="明天下午 3 点开会",
    is_html=False,
)
print(result)  # {"ok": True, "message": "邮件已发送至 receiver@example.com"}
```

### 方式三：Agent 对话式调用

当用户在对话中说「帮我发邮件给 xxx」，Agent 应：
1. 确认发件人（用户配置的哪个邮箱账号）
2. 确认收件人、主题、正文
3. 调用本技能执行发送

---

## 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `config_path` | string | 是 | 配置文件路径（accounts.json） |
| `from_addr` | string | 否 | 发件人邮箱（不传则用配置文件第一个账号） |
| `to` | string/list | 是 | 收件人邮箱（多个用逗号分隔或传列表） |
| `subject` | string | 是 | 邮件主题 |
| `body` | string | 是 | 邮件正文 |
| `is_html` | bool | 否 | 正文是否为 HTML，默认 false |
| `cc` | string | 否 | 抄送 |
| `bcc` | string | 否 | 密送 |
| `attachment` | string | 否 | 附件文件路径 |

## 返回值

```json
{"ok": true, "message": "邮件已发送至 receiver@example.com"}
```

失败时返回 `{"ok": false, "error": "错误原因"}`。

---

## 错误处理

| 错误 | 原因 | 处理 |
|------|------|------|
| SMTPAuthenticationError | 授权码错误 | 提示用户重新获取授权码（非登录密码） |
| SMTPConnectError | 服务器/端口错误 | 检查网络、服务器地址 |
| 收件人为空 | 未提供 to | 提示补充收件人 |
| 账号未配置 | config 里无匹配发件人 | 提示先配置账号 |

---

## 安全提示

- 授权码保存在本地 `config/accounts.json`，请勿提交到公开仓库（已加入 .gitignore）
- 发送前应让 Agent 确认收件人、主题、正文无误，避免误发
