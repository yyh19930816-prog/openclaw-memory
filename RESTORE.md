# 🦞 OpenClaw 记忆恢复卡
> 换电脑后，把这整个文件的内容贴给 Cursor AI，它就能立刻恢复所有记忆。

---

## 👤 用户信息
- **称呼**：老板（懒人+笨人，只通过聊天解决问题，不自己动手）
- **GitHub**：yyh19930816-prog
- **备份仓库**：https://github.com/yyh19930816-prog/openclaw-memory（私有）
- **系统**：Windows 10，PowerShell

## 🦞 龙虾（OpenClaw）是什么
- 本机运行的 AI 助手，有桌面 HUD 界面（赛博朋克风格）
- HUD 文件：`D:\TRAE\F1\claw_gui_red.py`
- 使用 SiliconFlow API，模型：`deepseek-ai/DeepSeek-V3`
- API Key：`sk-wngnqqegkuflnewxphmduagjskhesrafxxbhrwqpdahfyzaq`
- 有女声语音输出（晓晓）、语音输入功能

## 📁 关键文件路径
| 文件 | 路径 |
|------|------|
| 长期记忆 | `C:\Users\Administrator\.openclaw\workspace\MEMORY.md` |
| 每日日记 | `C:\Users\Administrator\.openclaw\workspace\memory\YYYY-MM-DD.md` |
| 行为指令 | `C:\Users\Administrator\.openclaw\workspace\AGENTS.md` |
| 技能手册 | `C:\Users\Administrator\.openclaw\workspace\TOOLS.md` |
| 心跳任务 | `C:\Users\Administrator\.openclaw\workspace\HEARTBEAT.md` |
| 进化数据 | `D:\TRAE\F1\claw_evolution.json` |
| 自动备份 | `C:\Users\Administrator\.openclaw\auto_backup.ps1`（每天09:00自动运行）|

## 🧬 龙虾当前进化状态（2026-03-01）
- **总经验**：237 XP，Lv.2
- **技术宗师**：0 XP，Lv.1（刚起步）
- **文案大师**：127 XP，Lv.2（主攻方向）
- **交互达人**：110 XP，Lv.2
- **修仙等级体系**：练气→筑基→金丹→元婴→化神→渡劫→大乘，每级经验是上一级的5倍

## 🎯 老板的核心需求
1. **文案+视频大师**：抖音/小红书/B站爆款内容，调用即梦AI/Seedance/Kling生成视频
2. **绝对禁止**：wan2.2视频模型（效果差还贵，花了24元没结果）
3. **老叶人设**：AI创业、沈阳本地、犀利风格
4. **懒人原则**：所有能执行的任务直接做，不需要用户动手，只有真正缺权限才问

## 💬 沟通偏好
- 直接说结果，不要啰嗦
- 不喜欢"好的我记住了"——被纠正时要直接写文件
- 喜欢简洁有力的回复，带一丝科技感
- 遇到问题直接解决，不要列一堆选项让老板选

## 🔧 重要技术记忆
- OpenClaw 网关：`D:\TRAE\F1\openclaw-official\`，端口 18789
- 配置文件：`C:\Users\Administrator\.openclaw\openclaw.json`（不能有 web.search/web.brave 字段，否则崩溃）
- HUD 启动：`python D:\TRAE\F1\claw_gui_red.py`
- 守护脚本：`D:\TRAE\F1\watchdog.ps1`

## ⚠️ 重要教训
- wan2.2 视频模型：绝对不用，效果差还贵
- openclaw.json 里不能有非法字段（web.search/web.brave）
- HUD 启动慢，要等10秒以上再检查进程

## 🔄 恢复步骤（换电脑后）
1. 从 GitHub 仓库 clone 文件恢复到对应路径
2. 安装依赖：`pip install customtkinter pillow requests SpeechRecognition edge-tts pygame psutil`
3. 把本文件内容贴给新电脑的 Cursor AI
4. AI 立刻恢复所有记忆，继续工作

---
*最后更新：2026-03-01 | 自动备份每天09:00运行*
