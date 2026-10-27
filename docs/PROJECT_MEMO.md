# 项目：Agent 办公实践邮件发送 Skill

> 最后更新：2026-10-27

## 项目总览

- 目标：完成 ICT 云赛道 1.14 并提交作品。
- 技术栈：Python 3.14 标准库、SMTP、MIME。
- 运行：`python -X utf8 -m unittest tests.test_sendmail_skill -v`
- 入口：`skills/sendmail/scripts/send_mail.py`

## 环境配置

- 系统：Windows 11
- Python：3.14.6
- 第三方运行时依赖：无
- 官方 Skill：`ea4a3ac8d0f873ea288b9e4ec905e29d965d0e5b`
- 真实邮箱配置：本地 `skills/sendmail/config/accounts.json`，已忽略

## 当前状态

- 已完成：官方 Skill 安装与源码归档、示例名单、测试和安全说明。
- 正在进行：生成比赛归档文件并提交。
- 下一步：推送 GitHub 仓库，提交 ICT 1.14。
- 风险：没有用户邮箱授权码，不能合法发送到外部真实邮箱。

## 需求与约定

- 默认只使用免费资源。
- 最终作品目录仅保留两个指定 Markdown 文件。
- 不在聊天、代码、日志或仓库中保存真实授权码。
- 自写函数注释必须包含功能、输入、输出。

## 待办

- [x] 安装官方 Skill 并记录来源
- [x] 完成发送路径测试
- [x] 生成两份归档文件
- [ ] 创建公开仓库并提交比赛

## 版本历史

- 2026-10-27：安装官方 Skill，建立测试和项目文档。
- 2026-10-27：完成归档，准备提交。
