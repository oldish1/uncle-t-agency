import subprocess, sys

SRC = "/root/.claude/uploads/ddc88798-d0a7-593c-ba8a-2954c94de9c4/101f09ac-VID-20261119-WA0052.mp4"
OUT = sys.argv[1]
ASS = sys.argv[2]

# kept source ranges (cut lead silence, the pause at 34s, trailing silence)
A = (0.45, 33.95)
B = (35.2, 57.7)
def out_t(s):
    return s - A[0] if s <= A[1] else (A[1] - A[0]) + (s - B[0])
TOTAL = out_t(B[1])

# punch-in segments (source time boundaries, zoom)
cuts = [A[0], 6.3, 12.2, 18.0, 23.7, 29.6, A[1], B[0], 40.9, 46.5, 50.5, B[1]]
zooms = [1.0, 1.14, 1.0, 1.14, 1.22, 1.0, None, 1.0, 1.0, 1.0, 1.12]

chunks = [
 (0.6, 6.3, "Hello everybody, hello everybody! So I've been getting lots of questions regarding the"),
 (6.3, 12.2, "competition. So like, follow, comment, share, tag"),
 (12.2, 18.0, "as much as you can. The most consistent"),
 (18.0, 23.7, "person will most likely have a chance to win. You do stand a"),
 (23.7, 29.6, "chance to win highlights, toner, Nanoplastia. If you don't"),
 (29.6, 33.9, "want the Nanoplastia, you can do a Botox for the curly ladies"),
 (35.3, 40.9, "So yeah, it's this post over here guys. Comment, share,"),
 (40.9, 46.5, "like, follow as much as you can. The competition ends next week, the"),
 (46.5, 50.5, "28th, and then the winner will be announced"),
]
GOLD = {"COMPETITION","WIN","WIN.","HIGHLIGHTS,","TONER,","NANOPLASTIA.","NANOPLASTIA,","BOTOX","28TH,","LIKE,","FOLLOW,","COMMENT,","SHARE,","TAG","SHARE,","CONSISTENT","COMPETITION."}

def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

ev = []
for s, e, text in chunks:
    words = text.upper().split()
    groups, g = [], []
    for w in words:
        g.append(w)
        if len(g) == 3 or w[-1] in ",.!?":
            groups.append(g); g = []
    if g: groups.append(g)
    total_chars = sum(len(" ".join(x)) for x in groups)
    t = s
    for grp in groups:
        d = (e - s) * len(" ".join(grp)) / total_chars
        txt = " ".join(("{\\c&H4FC6F2&}" + w + "{\\c&HFFFFFF&}") if w in GOLD else w for w in grp)
        ev.append(f"Dialogue: 1,{ts(out_t(t))},{ts(out_t(t+d))},Cap,,0,0,0,,{{\\fscx70\\fscy70\\t(0,90,\\fscx100\\fscy100)}}{txt}")
        t += d

def card(s, e, style, text, fade=(150, 150)):
    ev.append(f"Dialogue: 2,{ts(s)},{ts(e)},{style},,0,0,0,,{{\\fad({fade[0]},{fade[1]})}}{text}")

G = "{\\c&H4FC6F2&}"; W = "{\\c&HFFFFFF&}"
card(0, 3.2, "Hook", f"WIN A R1,500\\N{G}HAIR MAKEOVER", (0, 200))
card(out_t(6.3), out_t(18.0), "Top", f"{{\\fs44}}HOW TO ENTER\\N{{\\fs54}}{G}FOLLOW · SHARE TO YOUR STORY\\NTAG A FRIEND · COMMENT \"DONE\"")
card(out_t(23.7), out_t(33.9), "Top", f"{{\\fs44}}THE PRIZE\\N{{\\fs62}}{G}HIGHLIGHTS + TONER\\N+ NANOPLASTIA\\N{W}{{\\fs40}}or Botox for curly hair")
card(out_t(40.9), out_t(50.5), "Top", f"{{\\fs44}}WINNER ANNOUNCED\\N{{\\fs72}}{G}28 NOVEMBER")
card(out_t(50.5), TOTAL, "End", f"{{\\fs46}}{G}CHALES HAIR BOUTIQUE{W}\\N{{\\fs36}}Oakdale, Bellville\\N\\N{{\\fs40}}Enter on this post. Winner announced 28 November\\N\\N{{\\fs44}}Book on WhatsApp\\N{{\\fs64}}{G}071 429 6057{W}\\N{{\\fs36}}chaleshairboutique.co.za", (300, 0))

head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter ExtraBold,76,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,6,3,2,60,60,470,1
Style: Hook,Inter ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,7,4,8,50,50,150,1
Style: Top,Inter ExtraBold,58,&H00FFFFFF,&H00FFFFFF,&HB4140F0C,&HB4140F0C,0,0,0,0,100,100,1,0,3,22,0,2,70,70,700,1
Style: End,Inter ExtraBold,44,&H00FFFFFF,&H00FFFFFF,&H40140F0C,&H40140F0C,0,0,0,0,100,100,1,0,3,34,0,5,70,70,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(ASS, "w").write(head + "\n".join(ev) + "\n")

# video graph
pre = ("[0:v]split[raw][fl];[fl]crop=256:342:14:72,scale=480:642:flags=lanczos[flyer];[raw]delogo=x=2:y=452:w=104:h=116:enable='lt(t,3.75)',"
       "delogo=x=466:y=762:w=108:h=108:enable='gte(t,3.25)',"
       "hflip,scale=1080:1920:flags=lanczos[base];[base][flyer]overlay=574:135:enable='between(t,37.68,45.58)',unsharp=5:5:0.6,"
       "eq=contrast=1.07:saturation=1.12:gamma=0.98,colorbalance=rs=0.03:bs=-0.03,"
       "vignette=PI/5")
pieces = [(cuts[i], cuts[i+1], zooms[i]) for i in range(len(zooms)) if zooms[i]]
n = len(pieces)
g = [pre + f",split={n}" + "".join(f"[v{i}]" for i in range(n))]
g.append("[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,asplit=2[aa][ab]")
for i, (s, e, z) in enumerate(pieces):
    cw, ch = int(1080 / z) // 2 * 2, int(1920 / z) // 2 * 2
    x = (1080 - cw) // 2; y = int((1920 - ch) * 0.3)
    g.append(f"[v{i}]trim={s}:{e},setpts=PTS-STARTPTS,crop={cw}:{ch}:{x}:{y},scale=1080:1920:flags=lanczos,setsar=1[p{i}]")
g.append("".join(f"[p{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,ass={ASS},fade=t=out:st={TOTAL-0.4:.2f}:d=0.4[vout]")
g.append(f"[aa]atrim={A[0]}:{A[1]},asetpts=PTS-STARTPTS[a1];[ab]atrim={B[0]}:{B[1]},asetpts=PTS-STARTPTS[a2];[a1][a2]concat=n=2:v=0:a=1,afade=t=out:st={TOTAL-0.5:.2f}:d=0.5[aout]")
cmd = ["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", ";".join(g),
       "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "19",
       "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", OUT]
subprocess.run(cmd, check=True)
print("done", round(TOTAL, 2))
