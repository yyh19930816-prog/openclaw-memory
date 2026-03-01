# 🦞 OpenClaw 龙虾记忆备份

> 这里保存着龙虾（OpenClaw AI）和 Cursor AI 助手的所有记忆与进化数据。
> 自动备份，防止换电脑后失忆。

## 📁 目录结构

```
openclaw-memory/
├── workspace/
│   ├── MEMORY.md          # 龙虾长期记忆（重要教训、偏好、技能）
│   ├── AGENTS.md          # 龙虾行为指令
│   ├── HEARTBEAT.md       # 定期自我进化任务
│   ├── TOOLS.md           # 龙虾技能手册
│   ├── SOUL.md            # 龙虾灵魂设定
│   └── memory/            # 每日对话日记
│       ├── 2026-02-26.md
│       └── 2026-03-01.md
├── hud/
│   └── claw_gui_red.py    # HUD 桌面界面代码
├── cursor-transcripts/    # Cursor 对话历史摘要
├── claw_evolution.json    # 进化等级/经验值数据
└── README.md              # 本文件
```

## 🔄 恢复方法（换电脑后）

1. Clone 这个仓库到新电脑
2. 把 `workspace/` 里的文件复制到 `C:\Users\你的用户名\.openclaw\workspace\`
3. 把 `hud\claw_gui_red.py` 复制到 `D:\TRAE\F1\`
4. 把 `claw_evolution.json` 复制到 `D:\TRAE\F1\`
5. 把 `cursor-transcripts/` 里最新的 `.jsonl` 文件内容贴给 Cursor AI，记忆立刻恢复

## ⏰ 备份时间

最后备份：自动更新
