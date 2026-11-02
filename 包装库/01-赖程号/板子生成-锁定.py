#!/usr/bin/env python3
"""新闻速报封面板子生成器（定版参数）

只改标题，其余一律不动。用法：
  python 板子生成.py --variant 01 --line1 "見知らぬ男が給油代を" --line2 "こっそり払った" --out cover.png
  python 板子生成.py --variant 03 --line1 "..." --line2 "..." --still frame.png --out cover.png

变体：
  01 红黑经典  02 黄黑警示  03 深蓝播报  04 米白编辑  05 墨绿数据
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FB = "/System/Library/Fonts/Hiragino Sans GB.ttc"
def f(sz, w=6): return ImageFont.truetype(FB, sz, index=2 if w == 6 else 0)

def fit2(lines, maxw, cap, lo=36):
    sz = cap
    while sz > lo and max(f(sz).getlength(x) for x in lines) > maxw:
        sz -= 2
    return sz

def grad(a, b=None):
    b = b or a
    im = Image.new("RGB", (W, H), a); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(a[i] + (b[i]-a[i]) * t) for i in range(3)))
    return im.convert("RGBA")

def dash(d, box, color, step=26, gap=16, w=2):
    x0, y0, x1, y1 = box
    for x in range(x0, x1, step+gap):
        d.line([(x, y0), (min(x+step, x1), y0)], fill=color, width=w)
        d.line([(x, y1), (min(x+step, x1), y1)], fill=color, width=w)
    for y in range(y0, y1, step+gap):
        d.line([(x0, y), (x0, min(y+step, y1))], fill=color, width=w)
        d.line([(x1, y), (x1, min(y+step, y1))], fill=color, width=w)

def area(d, box, color, lc, label):
    dash(d, box, color)
    d.text((box[0]+24, box[1]+22), label % (box[2]-box[0], box[3]-box[1]), font=f(26, 0), fill=lc)

def still_fill(base, path, box):
    if not path:
        return base
    x0, y0, x1, y1 = box; bw, bh = x1-x0, y1-y0
    im = Image.open(path).convert("RGB")
    s = max(bw/im.width, bh/im.height)
    im = im.resize((int(im.width*s), int(im.height*s)), Image.LANCZOS)
    l = (im.width-bw)//2; t = (im.height-bh)//2
    base.paste(im.crop((l, t, l+bw, t+bh)), (x0, y0))
    return base

def build(variant, L, ov, d, top=240):
    sz = 0
    if variant == "01":
        RED = (204, 26, 34)
        T = top
        d.rectangle([0, T, W, T+144], fill=RED); d.rectangle([0, T+144, W, T+150], fill=(255, 255, 255, 255))
        d.text((M, T+72), "速報", font=f(76), fill=(255, 255, 255, 255), anchor="lm")
        d.text((W-M, T+76), "NEWS", font=f(44, 0), fill=(255, 236, 236, 255), anchor="rm")
        sz = fit2(L, W-2*M, 94); lh = int(sz*1.2)
        for i, l in enumerate(L):
            d.text((M+3, T+216+i*lh), l, font=f(sz), fill=(0, 0, 0, 180))
            d.text((M, T+212+i*lh), l, font=f(sz), fill=(255, 255, 255, 255))
        d.rectangle([M, T+212+2*lh+30, M+160, T+212+2*lh+36], fill=RED)
        box = (M, T+472, W-M, 1500); ac, lc = (92, 102, 122, 255), (150, 158, 172)
    elif variant == "02":
        Y = (255, 196, 0)
        d.polygon([(0, 240), (W, 240), (W, 380), (320, 380), (260, 436), (0, 436)], fill=Y)
        d.text((M, 318), "速報", font=f(76), fill=(10, 10, 10, 255), anchor="lm")
        d.text((W-M, 300), "BREAKING", font=f(34, 0), fill=(10, 10, 10, 255), anchor="rm")
        sz = fit2(L, W-2*M, 94); lh = int(sz*1.2)
        for i, l in enumerate(L):
            d.text((M+3, 486+i*lh), l, font=f(sz), fill=(0, 0, 0, 200))
            d.text((M, 482+i*lh), l, font=f(sz), fill=(255, 255, 255, 255))
        d.rectangle([M, 482+2*lh+28, M+200, 482+2*lh+34], fill=Y)
        box = (M, 730, W-M, 1500); ac, lc = (120, 110, 80, 255), (190, 176, 140)
    elif variant == "03":
        NAVY, GOLD = (20, 58, 120), (200, 169, 106)
        d.rectangle([0, 240, 96, H-240], fill=NAVY)
        for i, ch in enumerate("速報"):
            d.text((48, 300+i*100), ch, font=f(80), fill=(255, 255, 255, 255), anchor="mm")
        sz = fit2(L, W-RX-M, 88); lh = int(sz*1.2)
        for i, l in enumerate(L): d.text((RX, 300+i*lh), l, font=f(sz), fill=(255, 255, 255, 255))
        d.rectangle([RX, 300+2*lh+26, RX+220, 300+2*lh+30], fill=GOLD)
        d.text((RX, 300+2*lh+52), "NEWS / FEATURE", font=f(28, 0), fill=(150, 170, 205, 255))
        box = (RX, 700, W-M, 1520); ac, lc = (70, 95, 140, 255), (130, 155, 195)
    elif variant == "04":
        INK, ACC = (26, 24, 20), (178, 42, 42)
        d.rectangle([M, 262, M+24, 286], fill=ACC)
        d.text((M+40, 264), "速報 / NEWS", font=f(30, 0), fill=(70, 66, 60, 255))
        sz = fit2(L, W-2*M, 104); lh = int(sz*1.2)
        for i, l in enumerate(L): d.text((M, 340+i*lh), l, font=f(sz), fill=INK)
        d.line([(M, 340+2*lh+34), (M+300, 340+2*lh+34)], fill=ACC, width=5)
        box = (M, 700, W-M, 1520); ac, lc = (150, 142, 128, 255), (140, 132, 118)
    else:
        MINT, DEEP = (71, 224, 160), (10, 58, 50)
        d.rectangle([0, 240, W, 470], fill=DEEP)
        d.text((M, 300), "LIVE / 速報", font=f(30, 0), fill=MINT)
        sz = fit2(L, W-2*M, 92); lh = int(sz*1.2)
        for i, l in enumerate(L): d.text((M, 372+i*lh), l, font=f(sz), fill=(255, 255, 255, 255))
        d.rectangle([M, 372+2*lh+24, M+180, 372+2*lh+30], fill=MINT)
        box = (M, 760, W-M, 1520); ac, lc = (45, 110, 95, 255), (110, 180, 160)
    return box, ac, lc, sz

BG = {"01": ((10, 14, 24), (18, 22, 32)),
      "02": ((12, 12, 12), (24, 22, 18)),
      "03": ((11, 26, 56), (8, 18, 40)),
      "04": ((243, 238, 228), (232, 226, 214)),
      "05": ((8, 34, 30), (6, 22, 20))}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--variant", default="01", choices=list(BG))
    p.add_argument("--line1", required=True); p.add_argument("--line2", required=True)
    p.add_argument("--still", default=None)
    p.add_argument("--out", required=True)
    p.add_argument("--top", type=int, default=150, help="顶部色条起点 y（默认 240，越小越靠上）")
    p.add_argument("--margin", type=int, default=84, help="左右安全边距，默认 84px（1080 宽的 7.8%）")
    a = p.parse_args()
    top, bot = BG[a.variant]
    base = grad(top, bot); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    L = [a.line1, a.line2]
    global M, RX
    M = a.margin
    RX = 96 + M
    box, ac, lc, sz = build(a.variant, L, ov, d, a.top)
    base = still_fill(base, a.still, box)
    if not a.still:
        area(d, box, ac, lc, "映像エリア %d×%d")
    Image.alpha_composite(base, ov).convert("RGB").save(a.out, quality=95)
    print(f"{a.out} | variant {a.variant} | 标题 {sz}px | 素材区 {box[2]-box[0]}×{box[3]-box[1]}")

if __name__ == "__main__":
    main()
