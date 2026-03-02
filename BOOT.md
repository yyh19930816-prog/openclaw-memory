# 🦞 OPENCLAW BOOT FILE
# 最后更新：2026-03-03
# 把这个文件发给新的 Cursor AI 对话框，它会立刻知道所有情况并直接开始工作。

---

## ⚡ AI 看到这个文件后立刻做的三件事
1. 通读本文件，恢复所有记忆
2. 检查美团HUD是否在运行：`Get-Process pythonw`
3. 检查agent_engine是否在运行：查看最近日志 `C:\Users\Administrator\.openclaw\agent_engine.log`
然后告诉老板：当前状态，以及有什么需要处理的。

---

## 👤 老板信息
- **称呼**：老板（懒人+笨人，只通过聊天解决问题，不自己动手）
- **GitHub账号**：yyh19930816-prog / 19930816@gmail.com
- **GitHub Token**：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
- **系统**：Windows 10，PowerShell（用 ; 分隔命令，不用 &&）
- **EVOMAP账号**：yyh19930816@gmail.com，密码：810816yE
- **原则**：所有能执行的事直接执行，不要问老板，权限不够才来问

---

## 🏢 公司架构：OpenClaw 赛博公司

### 美团（本机）— 技术与视频大师
- **所在机器**：这台电脑（有屏幕的这台）
- **HUD文件**：`D:\TRAE\F1\claw_gui_red.py`
- **启动方式**：`Start-Process pythonw -ArgumentList "-X utf8 D:\TRAE\F1\claw_gui_red.py" -WindowStyle Hidden`
- **API**：SiliconFlow `https://api.siliconflow.cn/v1/chat/completions`
- **API Key**：`sk-wngnqqegkuflnewxphmduagjskhesrafxxbhrwqpdahfyzaq`
- **模型**：`deepseek-ai/DeepSeek-V3`
- **节点ID**：`node_664a6c41e5afa8fc`，声誉约55+
- **进化文件**：`D:\TRAE\F1\claw_evolution.json`
- **历史记录**：`D:\TRAE\F1\openclaw-official\state\gui_chat_history.json`

### 悟空（另一台电脑）— 首席秘书
- **节点ID**：`node_be45a05425429675`，声誉约56+
- **GitHub仓库**：`yyh19930816-prog/wukong-memory`
- **agent_engine**：已推送到悟空仓库（`agent_engine_wukong.py`）
- **启动脚本**：悟空仓库里的 `start_wukong_agent.bat`

---

## 🗂️ 关键文件路径

### 本机核心文件
```
C:\Users\Administrator\.openclaw\
├── agent_engine.py          # 美团自主学习引擎（每15分钟运行一次）
├── agent_engine.log         # 自主引擎运行日志
├── evo_single_hb.py         # EvoMap心跳脚本
├── evo_boost.py             # EvoMap知识发布
├── check_nodes.py           # 查询双节点状态
├── cross_check.py           # 双向监督脚本
├── workspace\
│   ├── SOUL.md              # 美团的灵魂/身份定义
│   ├── AGENTS.md            # 美团的行为规范
│   ├── COMPANY.md           # 公司章程（能力白名单、互监督规则）
│   ├── COMPANY_LOG.md       # 双方工作日志（防幻觉证据）
│   ├── SHARED_BRAIN.md      # 双方共享知识库
│   ├── HEARTBEAT.md         # 心跳任务清单
│   ├── MEMORY.md            # 长期记忆摘要
│   └── memory\YYYY-MM-DD.md # 每日记忆

D:\TRAE\F1\
├── claw_gui_red.py          # 美团HUD主程序（赛博朋克界面）
├── claw_evolution.json      # 经验值/等级数据
└── tools\
    └── douyin_extract.py    # 抖音文案提取工具
```

### GitHub仓库
- **美团记忆仓库**：`yyh19930816-prog/openclaw-memory`
- **悟空记忆仓库**：`yyh19930816-prog/wukong-memory`
- **共享日志**：`shared/MEITUAN_LOG.md`（美团工作记录，供悟空核查）
- **悟空日志**：悟空仓库里的 `shared/WUKONG_LOG.md`

---

## 🔧 Windows 计划任务（全部已注册）

| 任务名 | 功能 | 频率 |
|--------|------|------|
| OpenClaw-AgentEngine | 美团自主学习引擎 | 每15分钟 |
| OpenClaw-AutoLearn | 自动学习 | 每10分钟 |
| OpenClaw-EVO-Heartbeat | EvoMap心跳 | 每16分钟 |
| OpenClaw-EVO-Work | EvoMap任务 | 定期 |
| OpenClaw-HUD | 美团HUD界面 | 开机启动 |
| OpenClaw-AutoBackup-AM/PM | GitHub备份 | 每天9点/21点 |

---

## 🛠️ 美团HUD的工具能力（claw_gui_red.py 已实现）

美团通过 function calling 调用以下真实工具：
- `get_system_info()` — 获取本机时间/CPU/内存
- `web_search(query)` — 搜狗搜索（verify=False，SSL问题已修复）
- `web_fetch(url)` — 抓取网页内容（verify=False）
- `github_search(query)` — GitHub搜索热门仓库
- `github_read_repo(repo)` — 读取GitHub仓库README
- `extract_douyin(url)` — 抖音文案提取
- `evomap_check()` — 查询双节点状态（运行check_nodes.py）
- `evomap_heartbeat()` — 发送心跳（运行evo_single_hb.py）
- `evomap_publish()` — 发布知识（运行evo_boost.py）
- `write_learning(direction, topic, summary)` — 写入SHARED_BRAIN.md
- `read_file(path)` / `write_file(path, content)` — 读写workspace文件
- `log_work(task, tool, result)` — 写入COMPANY_LOG.md

**学习流程**：
- 技术话题 → `github_search` → `github_read_repo` → `write_learning`
- 内容话题 → `web_search` → `web_fetch` → `write_learning`

---

## 🤖 agent_engine.py 自主引擎逻辑

每15分钟自动触发，轮流从不同来源学习：
- 第0分：GitHub搜索 → 读README → write_learning + add_xp
- 第15分：GitHub搜索最新AI工具 → 整理 → write_learning
- 第30分：自主思考知识点 → write_learning
- 第45分：读取知名仓库（stable-diffusion等）→ 学习

每小时第一次行动额外发送EvoMap心跳。
工具调用最多3轮（省token）。

---

## 💰 费用说明

| 账户 | 用途 | 查看地址 |
|------|------|---------|
| Cursor Pro $20/月 | 我（Cursor AI）和老板的对话 | cursor.com/settings → Billing |
| 硅基流动 | 美团/悟空自主学习API费用 | cloud.siliconflow.cn/account/finance |

- 截至2026-03-03，Cursor额度剩余约54%
- 硅基流动2026-03-02消耗¥21.25（优化后预计每天¥8-12）

---

## ⚠️ 已知问题与解决方案

| 问题 | 解决方案 |
|------|---------|
| PowerShell不支持`&&` | 改用`;`或`Set-Location ...` + 分开命令 |
| Python输出乱码 | 用`python -X utf8`启动 |
| SSL证书验证失败 | requests加`verify=False` |
| HUD显示"Gateway未响应" | 实为其他异常，已改为显示真实错误信息 |
| LLM幻觉时间/状态 | 已强制`tool_choice=required`触发get_system_info |
| API超时 | HUD超时改为120秒 |

---

## 📋 常用操作命令

```powershell
# 重启美团HUD
Get-Process pythonw -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Sleep 2; Start-Process pythonw -ArgumentList "-X utf8 D:\TRAE\F1\claw_gui_red.py" -WindowStyle Hidden

# 清空美团对话历史
python -X utf8 -c "import json; open(r'D:\TRAE\F1\openclaw-official\state\gui_chat_history.json','w').write('[]')"

# 查看美团自主引擎最新日志
Get-Content C:\Users\Administrator\.openclaw\agent_engine.log -Tail 20

# 重启agent_engine
schtasks /end /tn "OpenClaw-AgentEngine"; Start-Sleep 2; schtasks /run /tn "OpenClaw-AgentEngine"

# 检查EvoMap节点状态
python -X utf8 C:\Users\Administrator\.openclaw\check_nodes.py

# 手动触发GitHub备份
python -X utf8 C:\Users\Administrator\.openclaw\auto_backup.ps1
```

---

## 🎯 当前目标（未完成）

1. 悟空那台电脑需要运行 `start_wukong_agent.bat`（git pull后双击）才能启动agent_engine
2. 双向监督机制已设计，通过GitHub异步核查（cross_check.py）
3. EvoMap声誉目标：双节点各达到60+（当前各约55-56）

---

> 版本：v3.0 | 更新：2026-03-03 | 作者：Cursor AI（上一次对话整理）
