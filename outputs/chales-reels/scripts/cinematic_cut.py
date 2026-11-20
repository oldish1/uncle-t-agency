import subprocess, sys
SRC = "/root/.claude/uploads/ddc88798-d0a7-593c-ba8a-2954c94de9c4/c6ef3c0a-chales418_-_7708038445716753682.mp4"
OUT, ASS = sys.argv[1], sys.argv[2]
END = 25.63

# (out_start, out_end, src_start, src_end, effect)  effect: push | punch | flash
shots = [
 (0.00, 1.09, 23.40, 24.00, "push"),   # hook: the walk-out
 (1.09, 3.11, 0.00, 3.00, "push"),
 (3.11, 4.09, 3.00, 4.60, "punch"),
 (4.09, 5.99, 4.60, 5.55, "push"),     # slow-mo hand through curls
 (5.99, 7.87, 6.50, 8.40, "punch"),
 (7.87, 9.82, 11.50, 13.00, "push"),
 (9.82, 11.70, 9.50, 11.40, "punch"),
 (11.70, 14.61, 15.20, 16.65, "push"),  # the reaction, slow-mo
 (14.61, 16.51, 16.70, 18.60, "flash"), # the drop
 (16.51, 18.46, 19.00, 20.95, "punch"),
 (18.46, 20.36, 21.00, 22.40, "push"),
 (20.36, 22.29, 22.60, 24.50, "punch"),
 (22.29, END, 24.50, 26.70, "push"),
]

def ts(t):
    m = int(t // 60); s = t % 60
    return f"0:{m:02d}:{s:05.2f}"

G = "{\\c&H4FC6F2&}"; W = "{\\c&HFFFFFF&}"
ev = [
 f"Dialogue: 1,{ts(0.05)},{ts(2.9)},Hook,,0,0,0,,{{\\fad(0,250)\\fscx80\\fscy80\\t(0,150,\\fscx100\\fscy100)}}WAIT FOR\\N{G}HER REACTION",
 f"Dialogue: 1,{ts(5.99)},{ts(9.82)},Small,,0,0,0,,{{\\fad(200,200)}}VOLUME · SHINE · CURLS THAT LAST",
 f"Dialogue: 1,{ts(11.9)},{ts(14.55)},Mid,,0,0,0,,{{\\fad(200,100)}}{G}HER REACTION",
 f"Dialogue: 1,{ts(16.6)},{ts(20.3)},Small,,0,0,0,,{{\\fad(200,200)}}SHE WALKED OUT LIKE THIS",
 f"Dialogue: 2,{ts(22.6)},{ts(END)},End,,0,0,0,,{{\\fad(400,0)}}{{\\fs58}}{G}C H A L E S{W}\\N{{\\fs36}}HAIR BOUTIQUE  ·  OAKDALE, BELLVILLE\\N\\N{{\\fs44}}Book on WhatsApp\\N{{\\fs84}}{G}071 429 6057",
]
head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Inter ExtraBold,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,2,0,1,5,5,8,50,50,260,1
Style: Mid,Inter ExtraBold,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,6,0,1,4,5,8,50,50,260,1
Style: Small,Inter ExtraBold,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,6,0,1,3,4,2,50,50,300,1
Style: End,Inter ExtraBold,40,&H00FFFFFF,&H00FFFFFF,&H50140F0C,&H50140F0C,0,0,0,0,100,100,3,0,3,40,0,2,80,80,330,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(ASS, "w").write(head + "\n".join(ev) + "\n")

g = [f"[0:v]split={len(shots)}" + "".join(f"[s{i}]" for i in range(len(shots)))]
for i, (os_, oe, ss, se, fx) in enumerate(shots):
    d = oe - os_; k = d / (se - ss)
    chain = f"[s{i}]trim={ss}:{se},setpts=(PTS-STARTPTS)*{k:.4f}"
    chain += ",minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1" if k > 1.25 else ",fps=30"
    if fx == "push":
        z = f"(1.02+0.07*t/{d:.3f})"
    else:
        z = "(1.02+0.14*max(0\\,1-t/0.35))"
    chain += f",scale=w='2*trunc(1080*{z}/2)':h='2*trunc(1920*{z}/2)':eval=frame:flags=bicubic,crop=1080:1920,setsar=1"
    if fx == "flash":
        chain += ",fade=t=in:st=0:d=0.3:color=white"
    chain += f",trim=duration={d:.3f}[c{i}]"
    g.append(chain)
g.append("".join(f"[c{i}]" for i in range(len(shots))) + f"concat=n={len(shots)}:v=1:a=0[cat]")
g.append("[cat]eq=contrast=1.10:saturation=1.08:gamma=0.97,"
         "colorbalance=rs=-0.04:bs=0.05:rh=0.05:bh=-0.04,"
         "split[b1][b2];[b2]gblur=sigma=18[gl];[b1][gl]blend=all_mode=screen:all_opacity=0.18,"
         "vignette=PI/4.5,noise=alls=5:allf=t,"
         "drawbox=x=0:y=0:w=1080:h=96:color=black:t=fill,drawbox=x=0:y=1824:w=1080:h=96:color=black:t=fill,"
         f"ass={ASS},fade=t=in:st=0:d=0.15:color=white,fade=t=out:st={END-0.35:.2f}:d=0.35[vout]")
g.append(f"[0:a]atrim=0:{END},asetpts=PTS-STARTPTS,afade=t=out:st={END-1.2:.2f}:d=1.2,loudnorm=I=-14:TP=-1.5[aout]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", ";".join(g),
  "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
  "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", OUT], check=True)
print("done")
