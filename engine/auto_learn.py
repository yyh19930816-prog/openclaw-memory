# -*- coding: utf-8 -*-
"""
OpenClaw Auto-Learn Engine v3.0 - Meituan
Every 5 min: search REAL GitHub repos, read actual README, AI extracts notes.
NO HALLUCINATION: if no real repo found, skip the cycle entirely.
Token loaded from local ~/.openclaw/.env file, never hardcoded.
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
        "python video automation moviepy",
        "python social media automation post",
        "github actions scheduled automation",
        "python image generation pillow",
        "python web scraping content",
        "python text to speech edge tts",
        "python api wrapper siliconflow",
        "python subprocess automation windows",
    ],
    "content": [
        "viral content formula hook engagement",
        "youtube shorts script template",
        "xiaohongshu content strategy automation",
        "tiktok ai content creation tool",
        "ai copywriting generator tool",
        "video thumbnail generator python",
        "social media scheduler python",
        "content calendar automation ai",
    ],
    "interact": [
        "python desktop gui tkinter modern",
        "python speech recognition offline",
        "python windows notification toast",
        "python clipboard monitor automation",
        "python screen capture ocr",
        "python hotkey global keyboard",
        "python system tray app",
        "python voice assistant windows",
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
            "You MUST only use information from the provided GitHub README. "
            "Do NOT invent features, code, or claims not present in the source. "
            "Reply in Chinese, 400-600 words, with bullet points and code blocks."
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

def search_real_github_repo(keywords):
    """
    Search GitHub for a real repo. Returns dict with name/stars/url/readme
    or None if nothing usable found.
    NEVER falls back to AI imagination.
    """
    kw = keywords.strip()[:50]
    url = f"https://api.github.com/search/repositories?q={requests.utils.quote(kw)}&sort=stars&per_page=5"
    try:
        r = requests.get(url, headers=GH_HEADERS, timeout=15)
        if r.status_code != 200:
            log(f"  [GitHub search failed] HTTP {r.status_code}")
            return None
        items = r.json().get("items", [])
        if not items:
            log(f"  [GitHub] No results for: {kw}")
            return None
        for repo in items[:3]:
            repo_name = repo["full_name"]
            stars = repo["stargazers_count"]
            repo_url = repo["html_url"]
            readme_r = requests.get(
                f"https://api.github.com/repos/{repo_name}/readme",
                headers=GH_HEADERS, timeout=15
            )
            if readme_r.status_code == 200:
                readme = base64.b64decode(readme_r.json()["content"]).decode("utf-8", errors="replace")
                readme = readme[:4000]
                log(f"  [Real repo found] {repo_name} star:{stars} {repo_url}")
                return {"name": repo_name, "stars": stars, "url": repo_url, "readme": readme}
        log(f"  [GitHub] Repos found but no README available, skipping")
        return None
    except Exception as e:
        log(f"  [GitHub error] {e}")
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

    log(f"[{direction.upper()}] Searching GitHub for: {topic}")

    repo = search_real_github_repo(topic)
    if not repo:
        log(f"  [SKIP] No real GitHub repo found for '{topic}'. Not recording to avoid hallucination.")
        return False, None

    repo_name = repo["name"]
    stars = repo["stars"]
    repo_url = repo["url"]
    readme = repo["readme"]
    source = f"GitHub:{repo_name}(star:{stars}) {repo_url}"

    # AI must only use the actual README content
    result = ask_ai(
        f"以下是GitHub仓库 **{repo_name}**（⭐{stars}）的真实README原文：\n\n"
        f"```\n{readme}\n```\n\n"
        f"请严格基于上面的README内容，用中文提炼：\n"
        f"1. 这个项目解决什么问题（1-2句，来自README）\n"
        f"2. 核心功能/知识点3-5条（直接来自README）\n"
        f"3. 安装/使用代码示例（优先引用README原文代码）\n"
        f"4. 适合什么人使用\n\n"
        f"⚠️ 严禁编造README中没有的功能或代码。"
    )

    if "[API error" in result or "[Request failed" in result:
        log(f"  [AI failed] {result}")
        return False, None

    log(f"  [Done] {len(result)} chars extracted from {repo_name}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = datetime.now().strftime("%Y-%m-%d")

    # 1. Write local daily memory
    mem_file = os.path.join(WS, "memory", f"{today}.md")
    try:
        with open(mem_file, "a", encoding="utf-8") as f:
            f.write(
                f"\n## [{datetime.now().strftime('%H:%M')}] Real GitHub Learn - {direction}\n"
                f"**Repo**: [{repo_name}]({repo_url}) ⭐{stars}\n"
                f"**Topic**: {topic}\n\n"
                f"{result[:400]}\n---\n"
            )
    except Exception as e:
        log(f"  Local write failed: {e}")

    # 2. Write MEITUAN_LOG on GitHub (verifiable by Wukong)
    log_line = (
        f"| {now} | GitHub real learn | learn_from_github | "
        f"repo:[{repo_name}]({repo_url}) star:{stars} topic:{topic[:25]} | done |\n"
    )
    gh_append_line(
        MEITUAN_REPO, "shared/MEITUAN_LOG.md", log_line,
        default_header=(
            "# Meituan Work Log (Wukong audits this)\n\n"
            "| time | task | tool | result | status |\n"
            "|------|------|------|--------|--------|\n"
        )
    )

    # 3. Write SHARED_BRAIN with real source link
    brain_entry = (
        f"\n### [Meituan-{direction}] {topic[:40]} ({now})\n"
        f"**Real source**: [{repo_name}]({repo_url}) ⭐{stars}\n\n"
        f"{result}\n\n---\n"
    )
    gh_append_line(
        MEITUAN_REPO, "shared/SHARED_BRAIN.md", brain_entry,
        default_header="# OpenClaw Shared Brain\n\n---\n"
    )

    # 4. Add XP (only for real learning)
    xp = min(20 + len(result) // 25, 100)
    add_evo_xp(direction, xp, topic[:20])

    log(f"  [Recorded] +{xp}XP | source: {source[:70]}")
    return True, source

def learn_cycle():
    log(f"\n{'='*55}")
    log(f"Meituan Auto-Learn v3.0 at {datetime.now().strftime('%H:%M')}")
    log(f"{'='*55}")
    direction = random.choice(["tech", "content", "interact"])
    ok, source = learn_one(direction)
    if ok:
        log(f"Cycle OK: learned from {source[:60]}")
    else:
        log(f"Cycle SKIPPED (no real GitHub repo found, no hallucination recorded)")
    log(f"Next cycle in {INTERVAL_MINUTES} min")

if __name__ == "__main__":
    log("Meituan Auto-Learn Engine v3.0 started")
    log(f"Interval: every {INTERVAL_MINUTES} minutes")
    log(f"Mode: STRICT - only real GitHub repos, no AI imagination")
    log(f"Output: EvoMap XP + GitHub logs with verifiable source links")
    learn_cycle()
    while True:
        time.sleep(INTERVAL_MINUTES * 60)
        learn_cycle()