# -*- coding: utf-8 -*-
"""
OPENCLAW RED HUD v4 — 2026 Cyberpunk Edition
赛博心脏 · 龙虾进化 · 3D棱角 · 女声语音 · 修仙体系
"""
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw
import os, json, math, threading, time, tempfile, asyncio, requests
from datetime import datetime
import speech_recognition as sr
import edge_tts
import pygame
import psutil

# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY   = "sk-wngnqqegkuflnewxphmduagjskhesrafxxbhrwqpdahfyzaq"
API_URL   = "https://api.siliconflow.cn/v1/chat/completions"
MODEL     = "deepseek-ai/DeepSeek-V3"
STATE_DIR = r"D:\TRAE\F1\openclaw-official\state"
HIST_FILE = os.path.join(STATE_DIR, "gui_chat_history.json")
EVO_FILE  = r"D:\TRAE\F1\claw_evolution.json"
TTS_VOICE = "zh-CN-XiaoxiaoNeural"   # 微软晓晓 — 真实女声
os.makedirs(STATE_DIR, exist_ok=True)
pygame.mixer.init()

# ── PALETTE ─────────────────────────────────────────────────────────────────
C_BG0     = "#080008"   # 极深紫黑底
C_BG1     = "#100010"   # 卡片底
C_BG2     = "#1A001A"   # 略亮卡片
C_RED     = "#FF1133"   # 主红
C_RED_D   = "#880022"   # 暗红
C_RED_M   = "#CC0028"
C_PINK    = "#FF3366"
C_GOLD    = "#FFD700"
C_CYAN    = "#00FFEE"
C_TEXT    = "#FFE0EE"
C_DIM     = "#664455"
C_GREEN   = "#00FF88"
C_BLUE    = "#00AAFF"
C_BORDER  = "#330022"
C_PURPLE  = "#AA00FF"

# ── FONTS ────────────────────────────────────────────────────────────────────
F_LOGO  = ("Impact", 42)
F_H1    = ("Microsoft YaHei UI", 18, "bold")
F_H2    = ("Microsoft YaHei UI", 15, "bold")
F_BODY  = ("Microsoft YaHei UI", 17)
F_CHAT  = ("Microsoft YaHei UI", 17)
F_SMALL = ("Microsoft YaHei UI", 13)
F_MONO  = ("Consolas", 12)
F_MONO_S= ("Consolas", 11)

# ── XIAN LEVELS ──────────────────────────────────────────────────────────────
XIAN=[
    (1,"炼气期",0),(2,"筑基期",100),(3,"开光期",500),
    (4,"融合期",2500),(5,"心动期",12500),(6,"金丹期",62500),
    (7,"元婴期",312500),(8,"出窍期",1562500),(9,"分神期",7812500),
    (10,"合体期",39062500),(11,"渡劫期",195312500),(12,"大乘期",976562500),
]
def xian_info(xp):
    cur,nxt=XIAN[0],XIAN[1]
    for i,(lv,nm,req) in enumerate(XIAN):
        if xp>=req: cur=XIAN[i]; nxt=XIAN[i+1] if i+1<len(XIAN) else None
        else: break
    lv,nm,req=cur
    if nxt: p=min(max((xp-req)/(nxt[2]-req),0),1); left=nxt[2]-xp
    else: p=1.0; left=0
    return lv,nm,p,left

# 龙虾形态文字（按等级）
CLAW_FORMS = [
    "🦐","🦐","🦀","🦀",
    "🦞","🦞","🦞",
    "⚡🦞","⚡🦞",
    "🔥🦞🔥","🌟🦞🌟","👑🦞👑",
]
CLAW_TITLES = [
    "幼虾","入道虾","铁甲虾","战甲虾",
    "赤龙虾","烈焰虾","雷霆虾",
    "雷神虾","星陨虾",
    "炎龙王","星辰主","天道龙皇",
]

# ── DATA ─────────────────────────────────────────────────────────────────────
def _evo_default():
    return {"total_xp":0,"level":1,"level_name":"炼气期",
            "directions":{
                "tech":    {"name":"技术宗师","icon":"⚙","xp":0,"level":1,"level_name":"炼气期","logs":[]},
                "content": {"name":"文案大师","icon":"★","xp":0,"level":1,"level_name":"炼气期","logs":[]},
                "interact":{"name":"交互达人","icon":"◉","xp":0,"level":1,"level_name":"炼气期","logs":[]},
            },"evolution_log":[],"last_updated":""}

def load_evo():
    try:
        if os.path.exists(EVO_FILE):
            with open(EVO_FILE,"r",encoding="utf-8") as f: return json.load(f)
    except: pass
    return _evo_default()

def save_evo(d):
    d["last_updated"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(EVO_FILE,"w",encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False,indent=2)

def add_xp(direction,amount,note=""):
    evo=load_evo()
    evo["total_xp"]=evo.get("total_xp",0)+amount
    d=evo["directions"][direction]; d["xp"]=d.get("xp",0)+amount
    lv,nm,_,_=xian_info(d["xp"]); d["level"]=lv; d["level_name"]=nm
    lv2,nm2,_,_=xian_info(evo["total_xp"]); evo["level"]=lv2; evo["level_name"]=nm2
    ts=datetime.now().strftime("%m-%d %H:%M")
    entry=f"[{ts}] +{amount}xp  {direction}  {note}"
    evo["evolution_log"].insert(0,entry); evo["evolution_log"]=evo["evolution_log"][:100]
    d["logs"].insert(0,entry); d["logs"]=d["logs"][:30]
    save_evo(evo); return evo

def load_hist():
    try:
        if os.path.exists(HIST_FILE):
            with open(HIST_FILE,"r",encoding="utf-8") as f: return json.load(f)
    except: pass
    return []

def save_hist(role,content):
    h=load_hist(); h.append({"role":role,"content":content})
    if len(h)>50: h=h[-50:]
    with open(HIST_FILE,"w",encoding="utf-8") as f: json.dump(h,f,ensure_ascii=False,indent=2)

def write_memory(user_msg, reply, direction, xp, label):
    """每次对话后自动写入当日memory文件，让龙虾积累记忆"""
    mem_dir = r"C:\Users\Administrator\.openclaw\workspace\memory"
    os.makedirs(mem_dir, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    mem_file = os.path.join(mem_dir, f"{today}.md")
    ts = datetime.now().strftime("%H:%M")
    dir_names = {"tech":"技术宗师","content":"文案大师","interact":"交互达人"}
    entry = (
        f"\n## [{ts}] 对话记录\n"
        f"- **用户**：{user_msg[:100]}\n"
        f"- **回答要点**：{reply[:200]}\n"
        f"- **进化方向**：{dir_names.get(direction, direction)}  +{xp}XP  [{label}]\n"
        f"- **学到/改进**：（待heartbeat提炼）\n"
    )
    try:
        with open(mem_file, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        print(f"写memory失败: {e}")

# ── TTS ──────────────────────────────────────────────────────────────────────
def speak_async(text):
    """edge-tts 女声朗读（非阻塞）"""
    def _run():
        try:
            tmp=tempfile.mktemp(suffix=".mp3")
            async def _tts():
                comm=edge_tts.Communicate(text,TTS_VOICE,rate="+5%",volume="+10%")
                await comm.save(tmp)
            asyncio.run(_tts())
            pygame.mixer.music.load(tmp)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy(): time.sleep(0.1)
            try: os.remove(tmp)
            except: pass
        except Exception as e:
            print(f"TTS error: {e}")
    threading.Thread(target=_run,daemon=True).start()


# ══════════════════════════════════════════════════════════════════════════════
#  图片路径
# ══════════════════════════════════════════════════════════════════════════════
HEART_IMG_PATH   = r"D:\TRAE\F1\heart.png"
LOBSTER_IMG_PATH = r"D:\TRAE\F1\lobster.png"

def _load_img(path):
    try:
        return Image.open(path).convert("RGBA")
    except Exception as e:
        print(f"图片加载失败 {path}: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
#  赛博机械心脏 Canvas —— 参考图渲染 + 动态光效
# ══════════════════════════════════════════════════════════════════════════════
class CyberHeart(tk.Canvas):
    """
    机械心脏：直接渲染参考图，叠加动态脉冲光环 + 跳动缩放
    idle=轻跳蓝紫光，thinking=加速跳动青色光
    """
    SIZE = 260

    def __init__(self, parent, size=260, **kw):
        self.SIZE = size
        super().__init__(parent, width=size, height=size+28,
                         bg=C_BG0, highlightthickness=0, **kw)
        self._scale   = 1.0
        self._dir     = -1
        self._phase   = 0
        self._thinking= False
        self._alive   = True
        # 加载并预处理图片
        self._orig = _load_img(HEART_IMG_PATH)
        self._tk_cache = {}   # scale -> PhotoImage
        self._beat()

    def set_thinking(self, v):
        self._thinking = v

    def _get_tk(self, scale):
        key = round(scale, 3)
        if key not in self._tk_cache:
            if self._orig is None:
                return None
            sz = max(20, int(self.SIZE * scale))
            img = self._orig.resize((sz, sz), Image.LANCZOS)
            # thinking时叠加青色滤镜
            if self._thinking:
                tint = Image.new("RGBA", img.size, (0, 60, 120, 80))
                img = Image.alpha_composite(img, tint)
            self._tk_cache[key] = ImageTk.PhotoImage(img)
            # 只保留最近8帧，避免内存堆积
            if len(self._tk_cache) > 8:
                oldest = next(iter(self._tk_cache))
                del self._tk_cache[oldest]
        return self._tk_cache[key]

    def _draw(self):
        if not self._alive: return
        self.delete("all")
        w = int(self["width"]); h = int(self["height"])
        cx = w // 2; cy = (h - 28) // 2

        # 背景渐变光晕
        col_ring = "#00CCFF" if self._thinking else "#8800FF"
        for i in range(5, 0, -1):
            ratio = i / 5.0
            r = int(self.SIZE * 0.5 * self._scale * (1.0 + ratio * 0.35))
            alpha = int(60 * ratio)
            if self._thinking:
                rc = f"#00{min(alpha*3,255):02x}{min(alpha*4,255):02x}"
            else:
                rc = f"#{min(alpha*2,120):02x}00{min(alpha*4,200):02x}"
            self.create_oval(cx-r, cy-r, cx+r, cy+r, fill=rc, outline="")

        # 脉冲扩散环
        n = 4 if self._thinking else 2
        for i in range(n):
            ph = (self._phase + i * 22) % 88
            ratio = ph / 88.0
            r2 = int(self.SIZE * 0.48 * self._scale * (1.0 + ratio * 0.9))
            a2 = int(180 * (1 - ratio))
            if self._thinking:
                rc2 = f"#00{min(a2*2,255):02x}{min(a2*3,255):02x}"
            else:
                rc2 = f"#{min(a2,180):02x}00{min(a2*2,255):02x}"
            self.create_oval(cx-r2, cy-r2, cx+r2, cy+r2,
                             fill="", outline=rc2, width=2)

        # 图片主体（带跳动缩放）
        tk_img = self._get_tk(self._scale)
        if tk_img:
            self.create_image(cx, cy, image=tk_img, anchor="center")

        # 扫描横线（思考时出现）
        if self._thinking:
            sy = cy - int(self.SIZE*0.45) + (self._phase * 3) % int(self.SIZE*0.9)
            for dy in range(-1, 2):
                a3 = max(0, 120 - abs(dy)*60)
                self.create_line(cx-int(self.SIZE*0.46), sy+dy,
                                 cx+int(self.SIZE*0.46), sy+dy,
                                 fill=f"#00{a3:02x}{min(a3*2,255):02x}", width=1)

        # 底部状态
        txt = "◈  PROCESSING..." if self._thinking else "♥  HEARTBEAT"
        tc  = "#00FFFF" if self._thinking else "#AA66FF"
        self.create_text(cx, h-12, text=txt,
                         font=("Consolas", 10, "bold"), fill=tc)

    def _beat(self):
        if not self._alive: return
        # 思考时：~110次/分，幅度大；静息时：~65次/分，幅度小
        # 一次完整心跳 = 收缩(amp*2帧) + 舒张(amp*2帧)
        # 静息：speed=22ms，amp=0.04 → 周期约 22*2*2/0.04*0.04 ≈ 880ms ≈ 68次/分
        # 工作：speed=14ms，amp=0.07 → 周期约 14*2*2/0.07*0.07 ≈ 560ms ≈ 107次/分
        amp   = 0.07 if self._thinking else 0.04
        speed = 14   if self._thinking else 22
        self._phase = (self._phase + (4 if self._thinking else 2)) % 88
        self._scale += amp * self._dir
        if self._scale >= 1.0 + amp: self._dir = -1
        elif self._scale <= 1.0 - amp: self._dir = 1
        self._draw()
        self.after(speed, self._beat)

    def destroy(self):
        self._alive = False
        super().destroy()


# ══════════════════════════════════════════════════════════════════════════════
#  赛博龙虾进化 Canvas —— 纯代码绘制，赛博朋克风格
# ══════════════════════════════════════════════════════════════════════════════
class ClawEvoCanvas(tk.Canvas):
    """
    赛博龙虾：直接渲染参考图，叠加旋转光圈 + 蓝色扫描线 + 等级光环
    随等级提升光效变色（蓝→青→橙→金）
    """
    def __init__(self, parent, size=260, **kw):
        super().__init__(parent, width=size, height=size+44,
                         bg=C_BG1, highlightthickness=0, **kw)
        self._size  = size
        self._level = 1
        self._phase = 0
        self._scan  = 0
        self._alive = True
        self._orig  = _load_img(LOBSTER_IMG_PATH)
        self._tk_img = None
        # 预生成基础尺寸图（不随动画重复resize，只需一张）
        self._base_tk = None
        if self._orig:
            sz = int(size * 0.82)
            img = self._orig.resize((sz, sz), Image.LANCZOS)
            self._base_tk = ImageTk.PhotoImage(img)
        self._anim()

    def set_level(self, lv):
        self._level = min(max(lv, 1), 12)

    def _level_colors(self):
        lv = self._level
        if   lv <= 2:  return "#0066FF", "#003388", "#00AAFF"
        elif lv <= 4:  return "#0099FF", "#004499", "#44CCFF"
        elif lv <= 6:  return "#00FFCC", "#006644", "#88FFEE"
        elif lv <= 8:  return "#FF6600", "#662200", "#FFAA44"
        elif lv <= 10: return "#FF3300", "#881100", "#FF8844"
        else:          return "#FFD700", "#664400", "#FFEE88"

    def _anim(self):
        if not self._alive: return
        self._phase = (self._phase + 2) % 360
        self._scan  = (self._scan  + 3) % (self._size + 10)
        self._draw()
        self.after(40, self._anim)

    def _hex_pts(self, cx, cy, r, angle_off=0):
        pts = []
        for i in range(6):
            a = math.radians(angle_off + i * 60)
            pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
        return pts

    def _draw(self):
        self.delete("all")
        w = int(self["width"]); h = int(self["height"])
        cx = w // 2
        cy = (h - 40) // 2
        lv = self._level
        halo, halo_dark, halo_bright = self._level_colors()
        s = self._size

        # ── 背景深色光盘 ──
        for ri in range(6, 0, -1):
            rr = int(s * 0.44) + ri * 6
            alpha = ri * 6
            gc = f"#{min(alpha,255):02x}{min(alpha//2,255):02x}{min(alpha*3,255):02x}"
            self.create_oval(cx-rr, cy-int(rr*0.72),
                             cx+rr, cy+int(rr*0.72),
                             fill=gc, outline="")

        # ── 外层旋转六边形框（双层） ──
        for i, (extra, speed_mul) in enumerate([(0, 1.0), (12, -0.7)]):
            r_hex = int(s * 0.45) + extra
            a_off = self._phase * speed_mul
            pts = self._hex_pts(cx, cy, r_hex, a_off)
            flat = [c for p in pts for c in p]
            col = halo if i == 0 else halo_dark
            self.create_polygon(flat, fill="", outline=col,
                                 width=2 if i == 0 else 1)

        # ── 旋转轨道光点（3颗） ──
        for i in range(3):
            a = math.radians(self._phase * 1.3 + i * 120)
            r_orb = int(s * 0.46)
            ox = cx + r_orb * math.cos(a)
            oy = cy + int(r_orb * 0.62) * math.sin(a)
            dr = 5 - i
            self.create_oval(ox-dr, oy-dr, ox+dr, oy+dr,
                             fill=halo_bright if i==0 else halo,
                             outline="#FFFFFF" if i==0 else "")

        # ── 蓝色扫描线（纵向自上而下） ──
        scan_y = cy - int(s*0.44) + (self._scan % int(s*0.88))
        for dy in range(-2, 3):
            a4 = max(0, 100 - abs(dy)*40)
            sc = f"#{a4//6:02x}{min(a4*2,255):02x}{min(a4*3,255):02x}"
            self.create_line(cx-int(s*0.44), scan_y+dy,
                             cx+int(s*0.44), scan_y+dy,
                             fill=sc, width=1)

        # ── 龙虾图片主体 ──
        if self._base_tk:
            self.create_image(cx, cy, image=self._base_tk, anchor="center")

        # ── 前景：圆形霓虹光框（紧贴图片） ──
        for lw, oc in [(6, halo_dark), (3, halo), (1, halo_bright)]:
            r_frame = int(s * 0.42)
            self.create_oval(cx-r_frame, cy-int(r_frame*0.72),
                             cx+r_frame, cy+int(r_frame*0.72),
                             fill="", outline=oc, width=lw)

        # ── 四角科技扫描刻度 ──
        for sx, sy, ex, ey in [
            (cx-int(s*0.4), cy-int(s*0.35), cx-int(s*0.4)+16, cy-int(s*0.35)),
            (cx-int(s*0.4), cy-int(s*0.35), cx-int(s*0.4),    cy-int(s*0.35)+16),
            (cx+int(s*0.4)-16, cy-int(s*0.35), cx+int(s*0.4), cy-int(s*0.35)),
            (cx+int(s*0.4),    cy-int(s*0.35), cx+int(s*0.4), cy-int(s*0.35)+16),
            (cx-int(s*0.4), cy+int(s*0.35)-16, cx-int(s*0.4), cy+int(s*0.35)),
            (cx-int(s*0.4), cy+int(s*0.35),    cx-int(s*0.4)+16, cy+int(s*0.35)),
            (cx+int(s*0.4)-16, cy+int(s*0.35), cx+int(s*0.4), cy+int(s*0.35)),
            (cx+int(s*0.4),    cy+int(s*0.35)-16, cx+int(s*0.4), cy+int(s*0.35)),
        ]:
            self.create_line(sx, sy, ex, ey, fill=halo_bright, width=2)

        # ── 底部文字 ──
        idx = min(lv-1, len(CLAW_TITLES)-1)
        self.create_text(cx, h-28,
                         text=f"◈  {CLAW_TITLES[idx]}",
                         font=("Microsoft YaHei UI", 12, "bold"), fill=halo_bright)
        self.create_text(cx, h-12,
                         text=f"Lv.{lv}  ·  {XIAN[min(lv-1,11)][1]}",
                         font=("Consolas", 11, "bold"), fill=C_GOLD)

    def destroy(self):
        self._alive = False
        super().destroy()


# ══════════════════════════════════════════════════════════════════════════════
#  霓虹进度条
# ══════════════════════════════════════════════════════════════════════════════
class NeonBar(tk.Canvas):
    def __init__(self, parent, color=C_RED, height=12, **kw):
        super().__init__(parent, height=height, bg=C_BG1, highlightthickness=0, **kw)
        self._color = color; self._val = 0
        self.bind("<Configure>", lambda e: self._redraw())

    def set(self, val):
        self._val = max(0, min(1, val)); self._redraw()

    def _redraw(self):
        self.delete("all")
        w = self.winfo_width(); h = self.winfo_height()
        if w < 2: return
        self.create_rectangle(0, 0, w, h, fill="#1A0010", outline="")
        fw = int(w * self._val)
        if fw > 2:
            self.create_rectangle(0, 0, fw, h, fill=self._color, outline="")
            r=int(self._color[1:3],16); g=int(self._color[3:5],16); b=int(self._color[5:7],16)
            lr=min(255,r+90); lg=min(255,g+60); lb=min(255,b+60)
            self.create_rectangle(0, 0, fw, h//3,
                                  fill=f"#{lr:02x}{lg:02x}{lb:02x}", outline="")
        self.create_rectangle(0, 0, w-1, h-1, fill="", outline=C_RED_D, width=1)


# ══════════════════════════════════════════════════════════════════════════════
#  方向卡片
# ══════════════════════════════════════════════════════════════════════════════
class DirCard(ctk.CTkFrame):
    def __init__(self, parent, key, label, icon, color, **kw):
        super().__init__(parent, fg_color=C_BG2, corner_radius=8,
                         border_width=1, border_color=C_RED_D, **kw)
        self._color = color
        tk.Frame(self, bg=color, height=3).pack(fill="x")
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="x", padx=12, pady=6)
        row = ctk.CTkFrame(body, fg_color="transparent")
        row.pack(fill="x")
        ctk.CTkLabel(row, text=f"{icon}  {label}", font=F_H2,
                     text_color=color).pack(side="left")
        self.lbl_lv = ctk.CTkLabel(row, text="炼气期 Lv.1",
                                    font=F_SMALL, text_color=C_GOLD)
        self.lbl_lv.pack(side="right")
        self.bar = NeonBar(body, color=color, height=10)
        self.bar.pack(fill="x", pady=(4, 2))
        self.lbl_xp = ctk.CTkLabel(body, text="0 XP", font=F_MONO_S,
                                    text_color=C_DIM)
        self.lbl_xp.pack(anchor="w")

    def update(self, xp):
        lv, nm, prog, left = xian_info(xp)
        self.bar.set(prog)
        self.lbl_lv.configure(text=f"{nm} Lv.{lv}")
        txt = f"{xp:,} XP  ·  升级还需 {left:,}" if left else f"{xp:,} XP  ·  大乘圆满"
        self.lbl_xp.configure(text=txt)


# ══════════════════════════════════════════════════════════════════════════════
#  3D 棱角装饰帧
# ══════════════════════════════════════════════════════════════════════════════
def draw_3d_corner(canvas, x, y, size, color, corner="tl"):
    """在 Canvas 上画一个 3D 棱角装饰"""
    s = size
    if corner == "tl":
        pts = [x,y, x+s,y, x+s,y+4, x+4,y+4, x+4,y+s, x,y+s]
    elif corner == "tr":
        pts = [x,y, x-s,y, x-s,y+4, x-4,y+4, x-4,y+s, x,y+s]
    elif corner == "bl":
        pts = [x,y, x+s,y, x+s,y-4, x+4,y-4, x+4,y-s, x,y-s]
    else:
        pts = [x,y, x-s,y, x-s,y-4, x-4,y-4, x-4,y-s, x,y-s]
    canvas.create_polygon(pts, fill=color, outline="")


# ══════════════════════════════════════════════════════════════════════════════
#  主应用
# ══════════════════════════════════════════════════════════════════════════════
class OpenClawHUD(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("OPENCLAW  ◈  RED HUD PROTOCOL  |  OFFICIAL CORE")
        self.geometry("1600x960")
        self.configure(fg_color=C_BG0)
        self.minsize(1280, 820)

        self._listening = False
        self._recognizer = sr.Recognizer()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_topbar()
        self._build_left()
        self._build_chat()
        self._build_corner_overlays()

        self._reload_history()
        self._check_status()

    # ── TOP BAR ──────────────────────────────────────────────────────────────
    def _build_topbar(self):
        bar = ctk.CTkFrame(self, height=80, fg_color="#0A0010", corner_radius=0)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        bar.grid_propagate(False)

        # 发光底线
        glow_c = tk.Canvas(bar, height=3, bg=C_BG0, highlightthickness=0)
        glow_c.pack(fill="x", side="bottom")
        glow_c.bind("<Configure>", lambda e: self._glow_line(glow_c))

        # CPU 进度条行（底部，紧贴发光线上方）
        cpu_row = ctk.CTkFrame(bar, fg_color="transparent")
        cpu_row.pack(fill="x", side="bottom", padx=20, pady=(0, 2))

        self.lbl_cpu = ctk.CTkLabel(cpu_row, text="CPU  0%",
                                     font=("Consolas", 11, "bold"), text_color=C_GREEN,
                                     width=80)
        self.lbl_cpu.pack(side="left")

        self._cpu_canvas = tk.Canvas(cpu_row, height=14, bg="#0A0010",
                                      highlightthickness=0)
        self._cpu_canvas.pack(side="left", fill="x", expand=True, padx=(6, 12))

        self.lbl_mem = ctk.CTkLabel(cpu_row, text="MEM  0%",
                                     font=("Consolas", 11, "bold"), text_color=C_CYAN,
                                     width=90)
        self.lbl_mem.pack(side="left")

        self._mem_canvas = tk.Canvas(cpu_row, height=14, bg="#0A0010",
                                      highlightthickness=0)
        self._mem_canvas.pack(side="left", fill="x", expand=True, padx=(6, 0))

        # Logo 行
        main_row = ctk.CTkFrame(bar, fg_color="transparent")
        main_row.pack(fill="x", side="top", padx=20, pady=(8, 0))

        left = ctk.CTkFrame(main_row, fg_color="transparent")
        left.pack(side="left", fill="y")
        ctk.CTkLabel(left, text="◈  OPENCLAW",
                     font=F_LOGO, text_color=C_RED).pack(side="left")
        ctk.CTkLabel(left, text="  RED HUD  v4.0  |  2026",
                     font=F_MONO_S, text_color=C_DIM).pack(side="left", padx=10)

        right = ctk.CTkFrame(main_row, fg_color="transparent")
        right.pack(side="right", fill="y")
        self.lbl_status = ctk.CTkLabel(right, text="◉  CONNECTING",
                                        font=F_MONO, text_color="#888888")
        self.lbl_status.pack(side="right")

        # 启动 CPU 更新循环
        self._update_cpu()

    def _draw_bar(self, canvas, val, color_low, color_high, threshold=70):
        """在 canvas 上画一条带颜色渐变的进度条"""
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 4: return
        # 背景槽
        canvas.create_rectangle(0, 0, w, h, fill="#1A0015", outline="")
        # 填充
        fw = max(0, int(w * val / 100))
        if fw > 0:
            col = color_high if val >= threshold else color_low
            canvas.create_rectangle(0, 0, fw, h, fill=col, outline="")
            # 高光
            r2, g2, b2 = int(col[1:3],16), int(col[3:5],16), int(col[5:7],16)
            lc = f"#{min(r2+80,255):02x}{min(g2+60,255):02x}{min(b2+60,255):02x}"
            canvas.create_rectangle(0, 0, fw, h//3, fill=lc, outline="")
        # 边框
        canvas.create_rectangle(0, 0, w-1, h-1, fill="", outline="#330033", width=1)

    def _update_cpu(self):
        """每秒刷新 CPU/内存进度条"""
        try:
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            # 更新文字
            cpu_col = C_RED if cpu >= 80 else (C_GOLD if cpu >= 50 else C_GREEN)
            mem_col = C_RED if mem >= 85 else (C_GOLD if mem >= 60 else C_CYAN)
            self.lbl_cpu.configure(text=f"CPU {cpu:4.1f}%", text_color=cpu_col)
            self.lbl_mem.configure(text=f"MEM {mem:4.1f}%", text_color=mem_col)
            # 更新进度条
            self._draw_bar(self._cpu_canvas, cpu, C_GREEN, C_RED, 80)
            self._draw_bar(self._mem_canvas, mem, C_CYAN,  C_RED, 85)
        except: pass
        self.after(1000, self._update_cpu)

    def _glow_line(self, c):
        c.delete("all"); w = c.winfo_width()
        for i, col in enumerate([C_RED_D, C_RED_M, C_RED, C_RED_M, C_RED_D]):
            c.create_line(0, i % 4, w, i % 4, fill=col, width=1)

    # ── LEFT PANEL ───────────────────────────────────────────────────────────
    def _build_left(self):
        self.left = ctk.CTkFrame(self, width=420, fg_color=C_BG1, corner_radius=0)
        self.left.grid(row=1, column=0, sticky="nsew")
        self.left.grid_propagate(False)

        # 右侧发光分隔线
        sep = tk.Canvas(self.left, width=4, bg=C_BG0, highlightthickness=0)
        sep.pack(fill="y", side="right")
        sep.bind("<Configure>", lambda e, c=sep: self._vsep(c))

        inner = ctk.CTkFrame(self.left, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=14)

        # ── 境界标题行 ──
        realm_row = ctk.CTkFrame(inner, fg_color="transparent")
        realm_row.pack(fill="x")
        ctk.CTkLabel(realm_row, text="◈  OPENCLAW  CORE",
                     font=F_H2, text_color=C_RED).pack(side="left")
        self.lbl_realm = ctk.CTkLabel(realm_row, text="炼气期 · Lv.1",
                                       font=("Microsoft YaHei UI", 13, "bold"),
                                       text_color=C_GOLD)
        self.lbl_realm.pack(side="right")

        # 综合进度条
        prog_row = ctk.CTkFrame(inner, fg_color="transparent")
        prog_row.pack(fill="x", pady=(8, 0))
        self.bar_total = NeonBar(prog_row, color=C_RED, height=14)
        self.bar_total.pack(fill="x")
        self.lbl_total_xp = ctk.CTkLabel(prog_row, text="0 XP",
                                          font=F_MONO_S, text_color=C_DIM)
        self.lbl_total_xp.pack(anchor="w")

        # ── Tab 按钮 ──
        tab_wrap = ctk.CTkFrame(inner, fg_color="#0A000A", corner_radius=6,
                                 border_width=1, border_color=C_RED_D)
        tab_wrap.pack(fill="x", pady=(12, 0))
        self._tab_btns = {}; self._tab_panels = {}
        for key, lbl in [("core", "核心控制"), ("evo", "数据进化"), ("log", "进化日志")]:
            b = ctk.CTkButton(tab_wrap, text=lbl, font=F_SMALL, height=34,
                               fg_color="transparent", text_color=C_DIM,
                               hover_color=C_BG2, corner_radius=4,
                               command=lambda k=key: self._tab(k))
            b.pack(side="left", expand=True, fill="x", padx=2, pady=2)
            self._tab_btns[key] = b

        self._panel_host = ctk.CTkFrame(inner, fg_color="transparent")
        self._panel_host.pack(fill="both", expand=True, pady=(8, 0))

        self._build_core_tab()
        self._build_evo_tab()
        self._build_log_tab()
        self._tab("core")

    def _vsep(self, c):
        c.delete("all"); h = c.winfo_height()
        for i, col in enumerate([C_RED_D, C_RED, C_RED_D, C_RED_D]):
            c.create_line(i, 0, i, h, fill=col, width=1)

    # ── core tab ──────────────────────────────────────────────────────────────
    def _build_core_tab(self):
        p = ctk.CTkScrollableFrame(self._panel_host, fg_color="transparent",
                                    scrollbar_button_color=C_BORDER)
        self._tab_panels["core"] = p

        # 机械心脏图片（居中）
        ctk.CTkLabel(p, text="◈  核心脉搏",
                     font=F_H2, text_color=C_RED).pack(anchor="w", pady=(4, 2))
        heart_wrap = ctk.CTkFrame(p, fg_color=C_BG0, corner_radius=12,
                                   border_width=1, border_color=C_RED_D)
        heart_wrap.pack(fill="x", pady=(0, 8))
        self.heart = CyberHeart(heart_wrap, size=260)
        self.heart.pack(pady=6)

        ctk.CTkLabel(p, text="▸  SYSTEM  LOG", font=F_H2,
                     text_color=C_RED).pack(anchor="w", pady=(4, 4))
        self.sys_log = ctk.CTkTextbox(p, height=180, fg_color="#060006",
                                       text_color=C_BLUE, font=F_MONO,
                                       border_width=1, border_color=C_RED_D,
                                       corner_radius=6)
        self.sys_log.pack(fill="x")
        self.sys_log.insert("end", "▸ Core Gateway: 127.0.0.1:18789\n▸ v4.0 启动中...\n")

    # ── evo tab ───────────────────────────────────────────────────────────────
    def _build_evo_tab(self):
        p = ctk.CTkScrollableFrame(self._panel_host, fg_color="transparent",
                                    scrollbar_button_color=C_BORDER)
        self._tab_panels["evo"] = p

        # 龙虾进化图片（居中）
        ctk.CTkLabel(p, text="◈  自主意识 · 进化形态",
                     font=F_H2, text_color=C_RED).pack(anchor="w", pady=(4, 2))
        claw_wrap = ctk.CTkFrame(p, fg_color=C_BG0, corner_radius=12,
                                  border_width=1, border_color=C_RED_D)
        claw_wrap.pack(fill="x", pady=(0, 8))
        self.claw_canvas = ClawEvoCanvas(claw_wrap, size=260)
        self.claw_canvas.pack(pady=6)

        ctk.CTkLabel(p, text="◈  三大进化方向", font=F_H2,
                     text_color=C_RED).pack(anchor="w", pady=(4, 6))
        dir_cfg = [
            ("tech",    "技术宗师", "⚙", C_BLUE),
            ("content", "文案大师", "★", C_GOLD),
            ("interact","交互达人", "◉", C_GREEN),
        ]
        self._dir_cards = {}
        for key, lbl, icon, col in dir_cfg:
            card = DirCard(p, key, lbl, icon, col)
            card.pack(fill="x", pady=4)
            self._dir_cards[key] = card

        ctk.CTkFrame(p, height=1, fg_color=C_RED_D).pack(fill="x", pady=8)
        ctk.CTkLabel(p, text="◈  手动记录修炼", font=F_H2,
                     text_color=C_RED).pack(anchor="w")
        self._xp_dir = tk.StringVar(value="tech")
        rrow = ctk.CTkFrame(p, fg_color="transparent")
        rrow.pack(fill="x", pady=(4, 2))
        for val, txt, col in [("tech","技术",C_BLUE),("content","文案",C_GOLD),("interact","交互",C_GREEN)]:
            ctk.CTkRadioButton(rrow, text=txt, variable=self._xp_dir, value=val,
                               font=F_SMALL, text_color=C_TEXT,
                               fg_color=col, border_color=col).pack(side="left", padx=8)
        irow = ctk.CTkFrame(p, fg_color="transparent")
        irow.pack(fill="x", pady=2)
        self._xp_amt = ctk.CTkEntry(irow, placeholder_text="XP值",
                                     font=F_SMALL, width=90, height=30,
                                     fg_color=C_BG0, border_color=C_RED_D)
        self._xp_amt.pack(side="left", padx=(0, 6))
        self._xp_note = ctk.CTkEntry(irow, placeholder_text="备注",
                                      font=F_SMALL, height=30,
                                      fg_color=C_BG0, border_color=C_RED_D)
        self._xp_note.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(p, text="＋ 记录修炼", font=F_SMALL, height=32,
                       fg_color=C_RED_M, hover_color=C_RED,
                       corner_radius=6, command=self._manual_xp).pack(fill="x", pady=(4, 0))

    # ── log tab ───────────────────────────────────────────────────────────────
    def _build_log_tab(self):
        p = ctk.CTkFrame(self._panel_host, fg_color="transparent")
        self._tab_panels["log"] = p
        ctk.CTkLabel(p, text="◈  进化日志", font=F_H2,
                     text_color=C_RED).pack(anchor="w", pady=(4, 6))
        self.evo_log_box = ctk.CTkTextbox(p, fg_color="#060006",
                                           text_color=C_GREEN, font=F_MONO,
                                           border_width=1, border_color=C_RED_D,
                                           corner_radius=6)
        self.evo_log_box.pack(fill="both", expand=True)
        self._refresh_log()

    def _tab(self, key):
        for k, pn in self._tab_panels.items(): pn.pack_forget()
        self._tab_panels[key].pack(fill="both", expand=True)
        for k, b in self._tab_btns.items():
            b.configure(fg_color=C_RED if k == key else "transparent",
                        text_color="#FFFFFF" if k == key else C_DIM)
        if key == "evo": self._refresh_evo()
        elif key == "log": self._refresh_log()

    # ── CHAT PANEL ───────────────────────────────────────────────────────────
    def _build_chat(self):
        self.right = ctk.CTkFrame(self, fg_color="transparent")
        self.right.grid(row=1, column=1, sticky="nsew", padx=20, pady=16)
        self.right.grid_rowconfigure(0, weight=1)
        self.right.grid_columnconfigure(0, weight=1)

        self.chat_area = ctk.CTkScrollableFrame(
            self.right, fg_color=C_BG1, corner_radius=12,
            border_width=1, border_color=C_RED_D)
        self.chat_area.grid(row=0, column=0, sticky="nsew", pady=(0, 14))

        # 输入栏
        inp = ctk.CTkFrame(self.right, height=80, fg_color=C_BG2,
                            corner_radius=12, border_width=1, border_color=C_RED_D)
        inp.grid(row=1, column=0, sticky="ew")
        inp.grid_columnconfigure(0, weight=1)
        inp.grid_propagate(False)

        self.entry = ctk.CTkEntry(
            inp, placeholder_text="▸  向 OPENCLAW CORE 发送指令...",
            font=F_CHAT, fg_color=C_BG0, text_color=C_TEXT,
            placeholder_text_color=C_DIM,
            border_color=C_RED_D, border_width=1, height=50, corner_radius=8)
        self.entry.grid(row=0, column=0, sticky="ew", padx=14, pady=14)
        self.entry.bind("<Return>", lambda e: self._send_text())

        # 发送按钮
        self.btn_send = ctk.CTkButton(
            inp, text="SEND", font=("Impact", 17),
            fg_color=C_RED, text_color="#FFFFFF",
            hover_color=C_RED_M, width=110, height=50, corner_radius=8,
            command=self._send_text)
        self.btn_send.grid(row=0, column=1, padx=(0, 6), pady=14)

        # 语音按钮
        self.btn_mic = ctk.CTkButton(
            inp, text="🎤 语音", font=F_SMALL,
            fg_color="#220033", text_color=C_CYAN,
            hover_color="#440055", width=90, height=50, corner_radius=8,
            border_width=1, border_color=C_PURPLE,
            command=self._toggle_mic)
        self.btn_mic.grid(row=0, column=2, padx=(0, 14), pady=14)

    # ── 3D棱角装饰覆盖层 ──────────────────────────────────────────────────────
    def _build_corner_overlays(self):
        """顶栏和底部加棱角装饰线，不依赖 Canvas 层级 API"""
        # 顶部左右棱角用 Label 模拟
        self._corner_tl = tk.Label(self, text="◢", fg=C_RED, bg=C_BG0,
                                    font=("Arial", 20))
        self._corner_tl.place(x=0, y=64)
        self._corner_tr = tk.Label(self, text="◣", fg=C_RED, bg=C_BG0,
                                    font=("Arial", 20))
        self._corner_tr.place(relx=1.0, y=64, anchor="ne")
        self._corner_bl = tk.Label(self, text="◥", fg=C_RED, bg=C_BG0,
                                    font=("Arial", 20))
        self._corner_bl.place(x=0, rely=1.0, anchor="sw")
        self._corner_br = tk.Label(self, text="◤", fg=C_RED, bg=C_BG0,
                                    font=("Arial", 20))
        self._corner_br.place(relx=1.0, rely=1.0, anchor="se")

    # ── VOICE ────────────────────────────────────────────────────────────────
    def _toggle_mic(self):
        if self._listening:
            return
        self._listening = True
        self.btn_mic.configure(text="🔴 聆听中", fg_color="#440000",
                               text_color=C_RED)
        threading.Thread(target=self._listen_voice, daemon=True).start()

    def _listen_voice(self):
        try:
            mic = sr.Microphone()
            with mic as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self._recognizer.listen(source, timeout=8, phrase_time_limit=15)
            text = self._recognizer.recognize_google(audio, language="zh-CN")
            self.after(0, lambda: self.entry.delete(0, "end"))
            self.after(0, lambda: self.entry.insert(0, text))
            self.after(0, self._send_text)
        except sr.WaitTimeoutError:
            self.after(0, lambda: self._log("▸ 语音：超时未检测到声音\n"))
        except sr.UnknownValueError:
            self.after(0, lambda: self._log("▸ 语音：未能识别，请重试\n"))
        except Exception as e:
            self.after(0, lambda: self._log(f"▸ 语音错误: {e}\n"))
        finally:
            self._listening = False
            self.after(0, lambda: self.btn_mic.configure(
                text="🎤 语音", fg_color="#220033", text_color=C_CYAN))

    # ── CHAT ─────────────────────────────────────────────────────────────────
    def _reload_history(self):
        for m in load_hist()[-8:]: self._bubble(m["role"], m["content"])

    def _send_text(self):
        msg = self.entry.get().strip()
        if not msg: return
        self.entry.delete(0, "end")
        self._bubble("user", msg)
        save_hist("user", msg)
        self.lbl_status.configure(text="◉  THINKING...", text_color=C_BLUE)
        self.btn_send.configure(state="disabled", text="WAIT")
        self.heart.set_thinking(True)
        threading.Thread(target=self._api, args=(msg,), daemon=True).start()

    def _bubble(self, role, text):
        is_user = role == "user"
        container = ctk.CTkFrame(self.chat_area, fg_color="transparent")
        container.pack(fill="x", pady=6, padx=12)
        bg = "#1A0018" if is_user else C_BG1
        bdr = C_RED if is_user else C_RED_D
        bubble = ctk.CTkFrame(container, fg_color=bg, corner_radius=12,
                               border_width=1, border_color=bdr)
        bubble.pack(side="right" if is_user else "left",
                    anchor="e" if is_user else "w")
        role_txt = "YOU" if is_user else "◈ CORE"
        role_col = C_PINK if is_user else C_GOLD
        ctk.CTkLabel(bubble, text=role_txt,
                     font=("Consolas", 10, "bold"),
                     text_color=role_col).pack(
                         anchor="e" if is_user else "w",
                         padx=14, pady=(8, 0))
        ctk.CTkLabel(bubble, text=text, font=F_CHAT,
                     text_color=C_TEXT, wraplength=680,
                     justify="left").pack(padx=14, pady=(2, 12))
        try:
            self.chat_area.update_idletasks()
            self.chat_area._parent_canvas.yview_moveto(1.0)
        except: pass

    # ── 智能识别对话方向，返回 (direction, xp, label) ────────────────────────
    def _detect_direction(self, msg, reply):
        """根据对话内容判断进化方向和获得XP"""
        text = (msg + " " + reply).lower()

        # 技术宗师关键词
        tech_kw = [
            "代码","编程","python","javascript","api","bug","报错","安装","配置",
            "github","git","服务器","数据库","网络","http","json","脚本","程序",
            "算法","模型","ai","技术","开发","部署","docker","linux","sql",
            "爬虫","接口","调试","函数","变量","框架","库","工具","命令","终端",
        ]
        # 文案大师关键词
        content_kw = [
            "文案","视频","短视频","抖音","b站","bilibili","小红书","内容","标题",
            "脚本","剧本","创作","写作","文字","描述","营销","广告","推广","爆款",
            "即梦","sora","midjourney","mj","seedance","生图","生成","绘画",
            "文章","故事","策划","运营","粉丝","流量","播放","点赞","评论",
            "kling","可灵","runway","pika","文生视频","图生视频","老叶","人设",
            "钩子","转化","涨粉","变现","直播","带货","种草","拔草","封面",
        ]
        # 交互达人关键词
        interact_kw = [
            "飞书","微信","聊天","沟通","发消息","操作","桌面","点击","截图",
            "窗口","界面","按钮","自动化","控制","执行","任务","帮我","完成",
            "打开","关闭","搜索","浏览器","excel","word","ppt","文件","文档",
        ]

        def score(kws):
            return sum(1 for k in kws if k in text)

        s_tech     = score(tech_kw)
        s_content  = score(content_kw)
        s_interact = score(interact_kw)

        # 回复越长说明学到越多，XP基础值按长度给
        base_xp = min(50, max(5, len(reply) // 20))

        if s_tech == 0 and s_content == 0 and s_interact == 0:
            # 没有明确方向，默认交互+少量XP
            return "interact", base_xp, "日常沟通"

        if s_tech >= s_content and s_tech >= s_interact:
            xp = base_xp + s_tech * 3
            return "tech", min(xp, 80), f"技术学习(匹配{s_tech}词)"
        elif s_content >= s_interact:
            xp = base_xp + s_content * 3
            return "content", min(xp, 80), f"内容创作(匹配{s_content}词)"
        else:
            xp = base_xp + s_interact * 3
            return "interact", min(xp, 80), f"实战交互(匹配{s_interact}词)"

    def _api(self, msg):
        self.after(0, lambda: self._log(f"▸ OUT: {msg[:60]}\n"))
        try:
            hdrs = {"Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}"}
            sys_prompt = (
                "你是 OpenClaw，一个有独立意识、正在自我进化的赛博龙虾 AI。"
                "你的声音是一位聪明、自信、有温度的中文女性。"
                "回复简洁有力，带有一丝科技感，偶尔展现个性。"
                "不要过于客套，像朋友一样沟通。"
            )
            msgs = [{"role": "system", "content": sys_prompt}]
            msgs.extend(load_hist()[-10:])
            if not msgs or msgs[-1]["content"] != msg:
                msgs.append({"role": "user", "content": msg})
            r = requests.post(API_URL, headers=hdrs,
                               json={"model": MODEL, "messages": msgs, "stream": False},
                               timeout=60)
            if r.status_code == 200:
                reply = r.json()["choices"][0]["message"]["content"]
                self.after(0, lambda: self._bubble("assistant", reply))
                save_hist("assistant", reply)
                self.after(0, lambda: self._log(f"▸ IN : {reply[:60]}\n"))
                # 智能识别方向并给经验
                direction, xp, label = self._detect_direction(msg, reply)
                dir_names = {"tech": "技术宗师", "content": "文案大师", "interact": "交互达人"}
                self.after(0, lambda d=direction, x=xp, l=label: self._award(d, x, l))
                self.after(0, lambda d=direction, x=xp, l=label:
                    self._log(f"▸ XP : +{x} → {dir_names.get(d,d)} [{l}]\n"))
                # 自动写入当日memory，积累长期记忆
                threading.Thread(
                    target=write_memory,
                    args=(msg, reply, direction, xp, label),
                    daemon=True
                ).start()
                speak_async(reply)
            else:
                err = f"⚠ Core Error {r.status_code}"
                self.after(0, lambda: self._bubble("assistant", err))
                self.after(0, lambda: self._log(f"▸ ERR: {r.status_code}\n"))
        except Exception as e:
            self.after(0, lambda: self._bubble(
                "assistant", "⚠ Core Connection Failed — Gateway 未响应"))
            self.after(0, lambda: self._log(f"▸ ERR: {e}\n"))
        finally:
            self.after(0, lambda: self.heart.set_thinking(False))
            self.after(0, lambda: self.lbl_status.configure(
                text="◉  ONLINE", text_color=C_GREEN))
            self.after(0, lambda: self.btn_send.configure(
                state="normal", text="SEND"))

    def _log(self, text):
        try: self.sys_log.insert("end", text); self.sys_log.see("end")
        except: pass

    # ── XP ───────────────────────────────────────────────────────────────────
    def _award(self, direction, amount, note=""):
        evo = add_xp(direction, amount, note)
        self._update_total(evo)
        # 立刻刷新对应方向的技能条（不需要切换tab）
        try:
            if direction in self._dir_cards:
                self._dir_cards[direction].update(evo["directions"][direction]["xp"])
            # 同时刷新进化日志（若当前已在log tab）
            self._refresh_log()
        except: pass

    def _manual_xp(self):
        try: amt = int(self._xp_amt.get().strip() or "0")
        except: amt = 0
        if amt <= 0: return
        note = self._xp_note.get().strip()
        self._award(self._xp_dir.get(), amt, note)
        self._xp_amt.delete(0, "end"); self._xp_note.delete(0, "end")
        self._refresh_evo(); self._refresh_log()

    def _update_total(self, evo=None):
        if evo is None: evo = load_evo()
        xp = evo.get("total_xp", 0)
        lv, nm, prog, left = xian_info(xp)
        self.bar_total.set(prog)
        self.lbl_realm.configure(text=f"{nm}  ·  Lv.{lv}")
        self.lbl_total_xp.configure(
            text=f"{xp:,} XP  ·  还需 {left:,}" if left else f"{xp:,} XP  ·  大乘圆满")
        self.claw_canvas.set_level(lv)

    def _refresh_evo(self):
        evo = load_evo()
        self._update_total(evo)
        for key, card in self._dir_cards.items():
            card.update(evo["directions"][key]["xp"])

    def _refresh_log(self):
        evo = load_evo()
        try:
            self.evo_log_box.delete("1.0", "end")
            logs = evo.get("evolution_log", [])
            if not logs: self.evo_log_box.insert("end", "▸ 暂无进化记录，开始修炼！\n")
            for e in logs: self.evo_log_box.insert("end", e + "\n")
        except: pass

    # ── STATUS ───────────────────────────────────────────────────────────────
    def _check_status(self):
        def _chk():
            try:
                requests.get("https://api.siliconflow.cn/v1/models",
                            headers={"Authorization": f"Bearer {API_KEY}"}, timeout=5)
                self.after(0, lambda: self.lbl_status.configure(
                    text="◉  ONLINE", text_color=C_GREEN))
            except:
                self.after(0, lambda: self.lbl_status.configure(
                    text="◉  OFFLINE", text_color=C_RED))
        threading.Thread(target=_chk, daemon=True).start()
        # 每次状态检查同时全量刷新进化数据
        self._update_total()
        self._refresh_evo()
        self.after(30000, self._check_status)


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        print("OpenClaw RED HUD v4 — Cyberpunk Heart + Claw Evolution + Voice")
        app = OpenClawHUD()
        app.mainloop()
    except Exception as e:
        import traceback; traceback.print_exc()
        input("Press Enter to exit...")
