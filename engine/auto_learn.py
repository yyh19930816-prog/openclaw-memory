# -*- coding: utf-8 -*-
"""
OpenClaw Auto-Learn Engine v2.0 - Meituan
Every 5 minutes: search real GitHub repos, learn skills, write to EvoMap + shared brain
GH_TOKEN must be set via environment variable or local config file
"""
import requests, json, os, sys, time, random, base64
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

API_KEY  = os.environ.get("OPENCLAW_API_KEY", "sk-wngnqqegkuflnewxphmduagjskhesrafxxbhrwqpdahfyzaq")
API_URL  = "https://api.siliconflow.cn/v1/chat/completions"
MODEL    = "deepseek-ai/DeepSeek-V3"
WS       = os.path.expanduser(r"~\.openclaw\workspace")
LOG_FILE = os.path.expanduser(r"~\.openclaw\auto_learn_meituan.log")
EVO_FILE = os.path.expanduser(r"~\.openclaw\claw_evolution.json")
MEITUAN_REPO  = "yyh19930816-prog/openclaw-memory"
INTERVAL_MINUTES = 5

# Token从本地配置文件读取（不写入代码）
_cfg_path = os.path.expanduser(r"~\.openclaw\.env")
_GH_TOKEN = ""
if os.path.exists(_cfg_path):
    for _line in open(_cfg_path, encoding="utf-8"):
        if _line.startswith("GH_TOKEN="):
            _GH_TOKEN = _line.strip().split("=", 1)[1]
if not _GH_TOKEN:
    _GH_TOKEN = os.environ.get("GH_TOKEN", "")
GH_HEADERS = {"Authorization": f"token {_GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}

os.makedirs(WS, exist_ok=True)
os.makedirs(os.path.join(WS, "memory"), exist_ok=True)

LEARN_TOPICS = {
    "tech": [
        "Python moviepy batch video processing with subtitle overlay",
        "SiliconFlow image and video generation API complete tutorial",
        "Python requests automated content publishing to social platforms",
        "GitHub Actions daily scheduled AI content generation automation",
        "DeepSeek V3 prompt engineering for high-quality copywriting",
        "Python PIL Pillow batch social media image generation",
        "AI short video script generation structured output pipeline",
        "Python subprocess safe system command execution best practices",
    ],
    "content": [
        "2026 AI side hustle viral content formula: hook + value + CTA structure",
        "AI tool review video script template: 3-minute golden structure",
        "Xiaohongshu AI content creation: automated workflow from topic to publish",
        "Douyin AI tools account viral topic database: high traffic ideas",
        "AI generated comparison content: before/after showcase techniques",
        "AI side income from 0 to 10k monthly: real case content strategy",
        "Video thumbnail design: key elements for AI generated high-CTR covers",
        "Brand persona building: how AI maintains consistent creator style",
    ],
    "interact": [
        "Python desktop AI assistant with modern tkinter UI design",
        "edge-tts Python high quality text-to-speech complete solution",
        "Windows desktop notification API Python implementation",
        "PyAutoGUI automated browser content publishing script",
        "customtkinter beautiful AI tool GUI interface design",
        "Python clipboard monitor with AI auto-processing",
        "Screenshot plus AI analysis intelligent content review Python",
        "Speech recognition plus AI reply real-time conversation assistant",
    ]
}

LEARNED_THIS_RUN = set()

def log(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

def ask_ai(prompt, system=None):
    if system is None:
        system = (
            "You are Meituan, OpenClaw AI content expert. "
            "Give concise, practical learning notes with code examples. "
            "Format: bullet points + core code block + one-line summary. 400-600 words in Chinese."
        )
    hdrs = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    try:
        r = requests.post(API_URL, headers=hdrs, json={
            "model": MODEL,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "stream": False, "max_tokens": 900
        }, timeout=60)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        return f"[API error {r.status_code}]"
    except Exception as e:
        return f"[Request failed: {e}]"

def search_github_repo(keywords):
    url = f"https://api.github.com/search/repositories?q={requests.utils.quote(keywords)}&sort=stars&per_page=5"
    try:
        r = requests.get(url, headers=GH_HEADERS, timeout=15)
        if r.status_code == 200:
            items = r.json().get("items", [])
            return items[0] if items else None
    except:
        pass
    return None

def read_repo_readme(repo_full_name):
    try:
        r = requests.get(f"https://api.github.com/repos/{repo_full_name}/readme", headers=GH_HEADERS, timeout=15)
        if r.status_code == 200:
            return base64.b64decode(r.json()["content"]).decode("utf-8", errors="replace")[:3000]
    except:
        pass
    return None

def gh_read_file(repo, path):
    r = requests.get(f"https://api.github.com/repos/{repo}/contents/{path}", headers=GH_HEADERS, timeout=10)
    if r.status_code == 200:
        data = r.json()
        return base64.b64decode(data["content"]).decode("utf-8", errors="replace"), data["sha"]
    return None, None

def gh_write_file(repo, path, content, sha=None, msg="update"):
    payload = {"message": msg, "content": base64.b64encode(content.encode("utf-8")).decode()}
    if sha:
        payload["sha"] = sha
    r = requests.put(f"https://api.github.com/repos/{repo}/contents/{path}", headers=GH_HEADERS, json=payload, timeout=15)
    return r.status_code in (200, 201)

def gh_append_line(repo, path, new_line, default_header=""):
    existing, sha = gh_read_file(repo, path)
    if existing is None:
        existing = default_header
    return gh_write_file(repo, path, existing + new_line, sha, msg=f"Meituan write {datetime.now().strftime('%H:%M')}")

def add_evo_xp(direction, xp, note):
    try:
        for path in [EVO_FILE, r"D:\TRAE\F1\claw_evolution.json"]:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    evo = json.load(f)
                evo["total_xp"] = evo.get("total_xp", 0) + xp
                d = evo.setdefault("directions", {}).setdefault(direction, {"xp": 0, "level": 1})
                d["xp"] = d.get("xp", 0) + xp
                ts = datetime.now().strftime("%m-%d %H:%M")
                entry = f"[{ts}] +{xp}xp {direction} Meituan:{note}"
                evo.setdefault("evolution_log", []).insert(0, entry)
                evo["evolution_log"] = evo["evolution_log"][:100]
                evo["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(evo, f, ensure_ascii=False, indent=2)
                log(f"  [XP] +{xp} to {direction} ({note[:25]})")
                return
    except Exception as e:
        log(f"  [XP write failed] {e}")

def learn_one(direction):
    topics = LEARN_TOPICS[direction]
    available = [t for t in topics if t not in LEARNED_THIS_RUN]
    if not available:
        available = topics
    topic = random.choice(available)
    LEARNED_THIS_RUN.add(topic)

    log(f"[{direction.upper()}] Learning: {topic[:50]}")

    kw = topic.split(":")[0][:40]
    repo = search_github_repo(kw)
    if repo:
        repo_name = repo["full_name"]
        stars = repo["stargazers_count"]
        readme = read_repo_readme(repo_name)
        source = f"GitHub:{repo_name}(star:{stars})"
        if readme:
            prompt = (
                f"I studied GitHub repo {repo_name} (stars:{stars}), related to topic: {topic}\n\n"
                f"README excerpt:\n{readme[:2500]}\n\n"
                f"Please extract 3-5 core knowledge points with runnable code snippets in Chinese, "
                f"focusing on practical value for AI content creators."
            )
        else:
            prompt = f"Please explain in detail with practical code examples (in Chinese): {topic}"
    else:
        source = "AI direct learning"
        prompt = f"Please explain in detail with practical code examples (in Chinese): {topic}"

    result = ask_ai(prompt)
    if "[API error" in result or "[Request failed" in result:
        log(f"  Failed: {result}")
        return False

    log(f"  Done, length: {len(result)} chars, source: {source}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = datetime.now().strftime("%Y-%m-%d")

    # Write local daily memory
    mem_file = os.path.join(WS, "memory", f"{today}.md")
    try:
        with open(mem_file, "a", encoding="utf-8") as f:
            f.write(f"\n## [{datetime.now().strftime('%H:%M')}] GitHub Learn - {direction}\n**{topic}**\nSource: {source}\n\n{result[:400]}\n---\n")
    except Exception as e:
        log(f"  Local write failed: {e}")

    # Write GitHub MEITUAN_LOG (for Wukong to audit)
    log_line = f"| {now} | GitHub learn | learn_from_github | topic:{topic[:30]}, source:{source[:30]} | done |\n"
    gh_append_line(
        MEITUAN_REPO, "shared/MEITUAN_LOG.md", log_line,
        default_header="# Meituan Work Log (for Wukong audit)\n\n| time | task | tool | result | status |\n|------|------|------|--------|--------|\n"
    )

    # Write GitHub SHARED_BRAIN (Wukong can read)
    brain_entry = f"\n### [Meituan-{direction}] {topic[:40]} ({now})\n**Source**: {source}\n\n{result}\n\n---\n"
    gh_append_line(
        MEITUAN_REPO, "shared/SHARED_BRAIN.md", brain_entry,
        default_header="# OpenClaw Shared Brain\n\n---\n"
    )

    # Add XP
    xp = min(20 + len(result) // 25, 100)
    add_evo_xp(direction, xp, topic[:20])

    log(f"  [Done] +{xp}XP, GitHub synced")
    return True

def learn_cycle():
    log(f"\n{'='*55}")
    log(f"Meituan Auto-Learn v2.0 cycle at {datetime.now().strftime('%H:%M')}")
    log(f"{'='*55}")
    direction = random.choice(["tech", "content", "interact"])
    ok = learn_one(direction)
    log(f"Cycle done: {'success' if ok else 'failed'}, next in {INTERVAL_MINUTES} min")

if __name__ == "__main__":
    log("Meituan Auto-Learn Engine v2.0 started")
    log(f"Interval: every {INTERVAL_MINUTES} minutes")
    log(f"Mode: Real GitHub repo search + AI synthesis")
    log(f"Output: EvoMap XP + GitHub Shared Brain + local memory")
    learn_cycle()
    while True:
        time.sleep(INTERVAL_MINUTES * 60)
        learn_cycle()