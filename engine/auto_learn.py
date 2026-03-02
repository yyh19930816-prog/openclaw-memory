# -*- coding: utf-8 -*-
"""
OpenClaw 自学引擎 v1.0
让龙虾真正主动学习——调用 AI 生成学习内容并写入记忆文件
三大方向每次各学一个课题，结果写入 MEMORY.md / TOOLS.md / 每日日记
"""
import requests, json, os, sys, time, random
from datetime import datetime

# ── CONFIG ────────────────────────────────────────────────────
API_KEY  = "sk-wngnqqegkuflnewxphmduagjskhesrafxxbhrwqpdahfyzaq"
API_URL  = "https://api.siliconflow.cn/v1/chat/completions"
MODEL    = "deepseek-ai/DeepSeek-V3"
WS       = r"C:\Users\Administrator\.openclaw\workspace"
EVO_FILE = r"D:\TRAE\F1\claw_evolution.json"
MEM_FILE = os.path.join(WS, "MEMORY.md")
TOOLS_FILE = os.path.join(WS, "TOOLS.md")
os.makedirs(os.path.join(WS, "memory"), exist_ok=True)

# ── 三大方向学习课题库（每次随机抽一题，避免重复）──────────────
TOPICS = {
    "tech": [
        "搜索并总结：2026年最值得关注的3个AI开源项目，说明用途和GitHub地址",
        "总结：Python调用SiliconFlow API的最佳实践，包括流式输出、错误重试、并发控制",
        "分析：Cursor AI与TRAE的核心差异，哪个更适合中国独立开发者，给出结论",
        "总结：Windows任务自动化最常用的5个PowerShell技巧，附代码示例",
        "搜索并总结：即梦AI、Seedance、Kling三个视频生成工具的最新API使用方法",
        "总结：如何用Python实现桌面自动化（pyautogui/pywinauto），附3个实用示例",
        "分析：2026年国内最好用的向量数据库方案，对比ChromaDB/Milvus/Qdrant",
        "总结：LLM Prompt Engineering最新最佳实践，提高AI回复质量的5个核心技巧",
        "搜索：飞书开放平台API最新文档，总结如何用Python发送消息和文件",
        "总结：Agent工具调用(Function Calling)的实现原理和代码模板",
        "分析：RAG(检索增强生成)的完整实现流程，给出Python代码框架",
        "总结：2026年最流行的AI视频脚本生成提示词模板，分析爆款规律",
    ],
    "content": [
        "分析：抖音最近100万+播放量AI创业类视频的标题规律，总结5个可复用公式",
        "生成：以'老叶'人设（AI创业/沈阳/犀利风格）写3个不同风格的短视频开场白",
        "分析：小红书爆款笔记的标题结构，总结数字+痛点+解决方案的写法规律",
        "生成：5个适合即梦AI生成的赛博朋克风格视频提示词（中英双语）",
        "总结：B站科技区百万播放UP主的内容策略，提炼3个核心套路",
        "生成：老叶人设的30天内容日历，每天一个短视频主题，覆盖AI创业/工具/干货",
        "分析：爆款视频的BGM选择规律，总结情绪节奏与内容类型的匹配关系",
        "生成：10个抖音AI工具类视频的钩子开场白（前3秒吸引眼球的文案）",
        "总结：视频文案的AIDA结构（注意/兴趣/欲望/行动）在短视频中的具体应用",
        "分析：即梦AI生成高质量视频的最佳提示词结构，总结镜头语言关键词",
        "生成：老叶风格的AI日报模板（每天分享1个AI工具，犀利评价+使用建议）",
        "分析：2026年AI创业赛道最火的3个内容方向，给出具体选题建议",
    ],
    "interact": [
        "总结：飞书机器人API的完整调用流程，Python代码实现自动发消息",
        "设计：一个桌面AI助手的完整交互流程图，包括语音唤醒/任务执行/结果反馈",
        "总结：pyautogui实现Windows桌面自动化的10个最常用操作，附代码",
        "分析：如何让AI更好地理解用户意图，总结意图识别的5个关键技术点",
        "设计：龙虾HUD的下一版升级方案，列出3个最有价值的新功能及实现思路",
        "总结：Windows语音识别API与Google Speech Recognition的对比，哪个更适合中文",
        "分析：如何实现AI与用户的多轮对话记忆管理，总结上下文压缩的最佳实践",
        "设计：一个自动化工作流，让龙虾每天自动：读邮件→总结→发飞书通知",
        "总结：edge-tts最自然的中文语音参数设置，对比5个不同声音效果",
        "分析：如何让桌面AI助手感知用户状态（忙碌/空闲/专注），调整交互方式",
        "设计：龙虾的任务管理系统，让它能记住未完成任务并在下次对话时提醒",
        "总结：2026年最好的中文语音合成方案对比，哪个最接近真人",
    ]
}

# 每个方向今天已学的课题（避免重复）
LEARNED_TODAY = {"tech": set(), "content": set(), "interact": set()}

def ask_ai(prompt, system_prompt=None):
    """调用SiliconFlow API获取学习内容"""
    if system_prompt is None:
        system_prompt = (
            "你是OpenClaw龙虾AI，正在进行主动自学。"
            "请给出具体、实用、有深度的学习总结。"
            "格式要求：用中文，分点清晰，包含具体例子或代码片段，长度300-600字。"
            "结尾用一句话说明：这个知识对老板（AI创业者）最有用的地方是什么。"
        )
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "max_tokens": 1000
    }
    try:
        r = requests.post(API_URL, headers=headers, json=data, timeout=60)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"[API错误 {r.status_code}]"
    except Exception as e:
        return f"[网络错误: {e}]"

def add_xp(direction, amount, note=""):
    """给对应方向加经验值"""
    try:
        if not os.path.exists(EVO_FILE):
            return
        with open(EVO_FILE, "r", encoding="utf-8") as f:
            evo = json.load(f)
        evo["total_xp"] = evo.get("total_xp", 0) + amount
        d = evo["directions"][direction]
        d["xp"] = d.get("xp", 0) + amount
        ts = datetime.now().strftime("%m-%d %H:%M")
        entry = f"[{ts}] +{amount}xp  {direction}  {note}"
        evo.setdefault("evolution_log", []).insert(0, entry)
        evo["evolution_log"] = evo["evolution_log"][:100]
        d.setdefault("logs", []).insert(0, entry)
        d["logs"] = d["logs"][:30]
        evo["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(EVO_FILE, "w", encoding="utf-8") as f:
            json.dump(evo, f, ensure_ascii=False, indent=2)
        print(f"  [XP] +{amount} → {direction} [{note}]")
    except Exception as e:
        print(f"  [XP错误] {e}")

def append_to_file(filepath, content):
    """安全追加内容到文件"""
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"  [写文件错误] {filepath}: {e}")

def write_daily_log(direction, topic, result):
    """写入每日日记"""
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")
    daily_file = os.path.join(WS, "memory", f"{today}.md")
    dir_names = {"tech": "技术宗师", "content": "文案大师", "interact": "交互达人"}
    content = f"""
## [{now}] 自学记录 · {dir_names.get(direction, direction)}
**课题**：{topic}
**学习内容摘要**：
{result[:400]}...
---
"""
    append_to_file(daily_file, content)

def write_to_memory(direction, topic, result):
    """把有价值的内容写入MEMORY.md"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    dir_names = {"tech": "技术宗师", "content": "文案大师", "interact": "交互达人"}
    section = f"""
### [{dir_names.get(direction, direction)}] {topic[:40]} ({now})
{result[:600]}

"""
    # 找到对应方向的章节插入
    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            mem = f.read()
        # 追加到文件末尾
        append_to_file(MEM_FILE, section)
    except:
        append_to_file(MEM_FILE, section)

def write_to_tools(direction, topic, result):
    """把技能类内容写入TOOLS.md"""
    now = datetime.now().strftime("%Y-%m-%d")
    dir_names = {"tech": "技术宗师", "content": "文案大师", "interact": "交互达人"}
    content = f"""
### [{topic[:30]}] 自学于{now}
- **方向**：{dir_names.get(direction, direction)}
- **核心内容**：
{result[:500]}

"""
    append_to_file(TOOLS_FILE, content)

def learn_one(direction):
    """执行一次单方向学习"""
    dir_names = {"tech": "[TECH] 技术宗师", "content": "[CONTENT] 文案大师", "interact": "[INTERACT] 交互达人"}
    topics = TOPICS[direction]

    # 随机选一个今天没学过的课题
    available = [t for t in topics if t not in LEARNED_TODAY[direction]]
    if not available:
        LEARNED_TODAY[direction].clear()
        available = topics
    topic = random.choice(available)
    LEARNED_TODAY[direction].add(topic)

    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {dir_names[direction]} 开始学习")
    print(f"课题：{topic[:50]}...")
    print(f"{'='*60}")

    result = ask_ai(topic)

    if "[API错误" in result or "[网络错误" in result:
        print(f"  ❌ 学习失败: {result}")
        return False

    print(f"  ✅ 学习完成，内容长度: {len(result)} 字")
    print(f"  预览: {result[:100]}...")

    # 写入各记忆文件
    write_daily_log(direction, topic, result)
    write_to_memory(direction, topic, result)

    # 技能类内容额外写入TOOLS.md
    if direction in ("tech", "interact"):
        write_to_tools(direction, topic, result)

    # 把核心结论写进MEMORY.md顶部（1句话，随时可查）
    summarize_to_memory(direction, topic, result)

    # 加经验值（真正学习给更多XP）
    xp = min(30 + len(result) // 30, 120)
    add_xp(direction, xp, f"主动学习: {topic[:20]}")

    return True

def summarize_to_memory(direction, topic, result):
    """把本轮最重要的1句话结论写进MEMORY.md顶部，方便龙虾随时调用"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    dir_names = {"tech": "技术宗师", "content": "文案大师", "interact": "交互达人"}
    # 让AI提炼一句话结论
    summary_prompt = f"把以下学习内容提炼成1句话（不超过50字）的核心结论，直接输出结论，不要任何前缀：\n\n{result[:500]}"
    one_line = ask_ai(summary_prompt, "你是信息提炼专家，只输出一句话结论，不超过50字。")
    if "[API错误" in one_line or "[网络错误" in one_line:
        one_line = result[:80]
    
    entry = f"- [{now}][{dir_names.get(direction,'?')}] {one_line.strip()}\n"
    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        # 插入到文件顶部的"最新学习摘要"区域
        marker = "## 🧠 自动学习摘要（最新在前）\n"
        if marker in content:
            content = content.replace(marker, marker + entry)
        else:
            content = marker + entry + "\n---\n\n" + content
        with open(MEM_FILE, "w", encoding="utf-8") as f:
            f.write(content)
    except:
        append_to_file(MEM_FILE, entry)

def learn_cycle():
    """一轮完整学习：三个方向各学一次"""
    print(f"\n{'#'*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始新一轮自学循环")
    print(f"{'#'*60}")

    results = {}
    for direction in ["tech", "content", "interact"]:
        ok = learn_one(direction)
        results[direction] = ok
        if ok:
            time.sleep(8)  # 避免API限流，稍微等一下

    success = sum(1 for v in results.values() if v)
    print(f"\n本轮学习完成: {success}/3 个方向成功")
    print(f"下一轮将在 {INTERVAL_MINUTES} 分钟后开始")
    return success

# ── 主循环 ─────────────────────────────────────────────────────
INTERVAL_MINUTES = 10  # 每10分钟学一轮（一天约144轮，每轮3方向=432次学习）

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    print("=" * 60)
    print("[OPENCLAW] Auto-Learn Engine started")
    print(f"   Interval: every {INTERVAL_MINUTES} minutes")
    print(f"   Per cycle: tech + content + interact x1 each")
    print(f"   Output: MEMORY.md / TOOLS.md / daily diary")
    print("=" * 60)

    # 启动时立刻学一轮
    learn_cycle()

    # 然后按间隔持续循环
    while True:
        time.sleep(INTERVAL_MINUTES * 60)
        learn_cycle()
