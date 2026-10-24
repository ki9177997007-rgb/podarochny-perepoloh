#!/usr/bin/env python3
"""Generate an original animated 9:16 product explainer with moving vector objects.

No stock footage, false product claims or text-only slides. Needs Pillow, numpy, ffmpeg.
"""
from pathlib import Path
import math, subprocess, tempfile, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'media'/'powerbank-vs-charger-motion.mp4'
W,H,FPS,DURATION=432,768,24,12
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def clamp(x): return max(0,min(1,x))
def smooth(x):
    x=clamp(x)
    return x*x*(3-2*x)
def centered(d,x,y,s,size=22,color='white',bold=True):
    f=ImageFont.truetype(BOLD if bold else FONT,size)
    b=d.textbbox((0,0),s,font=f)
    d.text((x-(b[2]-b[0])/2,y),s,font=f,fill=color)
def bank(d,x,y,t):
    x,y=int(x),int(y)
    d.rounded_rectangle((x+11,y+15,x+156,y+266),radius=30,fill='#0b071a')
    d.rounded_rectangle((x,y,x+145,y+251),radius=27,fill='#ff557e',outline='#ffb2c4',width=3)
    d.rounded_rectangle((x+14,y+13,x+128,y+230),radius=21,fill='#f34471')
    d.rounded_rectangle((x+34,y+73,x+111,y+115),radius=13,fill='#312346')
    for i in range(3):
        d.rounded_rectangle((x+45+i*20,y+86,x+58+i*20,y+101),radius=3,fill='#64f4c3' if i<=int((t*1.1)%3) else '#6b5f80')
    d.rounded_rectangle((x+45,y+17,x+96,y+26),radius=4,fill='#3a294c')
def phone(d,x,y,level):
    x,y=int(x),int(y)
    d.rounded_rectangle((x+8,y+14,x+130,y+254),radius=25,fill='#090517')
    d.rounded_rectangle((x,y,x+122,y+240),radius=24,fill='#e8e6f5',outline='white',width=3)
    d.rounded_rectangle((x+8,y+8,x+114,y+232),radius=18,fill='#251c43')
    d.rounded_rectangle((x+41,y+11,x+81,y+17),radius=3,fill='#070514')
    bx,by=x+28,y+103
    d.rounded_rectangle((bx,by,bx+66,by+50),radius=8,outline='white',width=3)
    d.rectangle((bx+5,by+5,bx+5+int(56*clamp(level)),by+45),fill='#58e8be')
    d.rectangle((bx+67,by+18,bx+71,by+33),fill='white')
def charger(d,x,y,t):
    x,y=int(x),int(y)
    d.rounded_rectangle((x+8,y+13,x+165,y+207),radius=29,fill='#0b071a')
    d.rounded_rectangle((x,y,x+156,y+194),radius=26,fill='#f4eefb',outline='white',width=3)
    d.rounded_rectangle((x+15,y+15,x+140,y+175),radius=22,fill='#dbd0ea')
    d.rounded_rectangle((x+57,y+78,x+103,y+93),radius=7,fill='#32264c')
    d.rectangle((x+42,y-33,x+57,y+3),fill='#b9b7c7')
    d.rectangle((x+99,y-33,x+114,y+3),fill='#b9b7c7')
    a=4*math.sin(t*6)
    d.ellipse((x+68+a,y+117,x+82+a,y+131),fill='#ff557e')
def cable(d,x1,y1,x2,y2,t):
    pts=[]
    for i in range(51):
        a=i/50
        pts.append((x1+(x2-x1)*a,y1+(y2-y1)*a+math.sin(a*math.pi)*95))
    d.line(pts,fill='#0c081b',width=14,joint='curve')
    d.line(pts,fill='#ebd8f8',width=7,joint='curve')
    for j in range(3):
        x,y=pts[int(((t*.38+j/3)%1)*50)]
        d.ellipse((x-7,y-7,x+7,y+7),fill='#5cf4bf')
def background():
    im=Image.new('RGB',(W,H));p=im.load()
    for y in range(H):
        q=y/H
        for x in range(W):
            r=math.hypot((x-W*.7)/W,(y-H*.28)/H)
            g=max(0,1-r*2)
            p[x,y]=(int(30+34*g+10*q),int(22+16*g+6*q),int(53+37*g+10*q))
    return im
BG=background()
def frame(t):
    im=BG.copy();d=ImageDraw.Draw(im)
    for i in range(12):
        x=(i*89+20+14*math.sin(t*.6+i))%W
        y=(i*139+30+20*math.cos(t*.4+i))%H
        r=2+i%3
        d.ellipse((x-r,y-r,x+r,y+r),fill='#684c85')
    d.rounded_rectangle((25,34,407,79),radius=22,fill='#39284e')
    centered(d,W/2,47,'ПОДАРОЧНЫЙ ПЕРЕПОЛОХ',17)
    if t<4.25:
        p=smooth(t/.75)
        bank(d,-170+202*p,285+7*math.sin(t*2),t)
        phone(d,284+180*(1-p),312+8*math.sin(t*1.7),.16+.70*smooth((t-.7)/2.8))
        if p>.4:cable(d,176,472,286,506,t)
        centered(d,W/2,145,'ПАУЭРБАНК',35)
        centered(d,W/2,196,'Когда розетки рядом нет',19,'#f5dcea',False)
    elif t<8.4:
        q=t-4.25;p=smooth(q/.8)
        charger(d,35-195*(1-p),345+8*math.sin(q*2),q)
        phone(d,274+180*(1-p),305+7*math.sin(q*1.8),.22+.70*smooth((q-.5)/2.7))
        if p>.4:cable(d,193,485,276,502,q)
        centered(d,W/2,145,'СЕТЕВАЯ ЗАРЯДКА',27)
        centered(d,W/2,196,'Когда есть розетка',19,'#f5dcea',False)
    else:
        q=t-8.4
        bank(d,20+9*math.sin(q*1.6),322,t)
        charger(d,254+9*math.cos(q*1.6),360,t)
        d.rounded_rectangle((170,406,260,462),radius=22,fill='#ff557e')
        centered(d,215,415,'ИЛИ',25)
        centered(d,W/2,150,'ЧТО ПОДАРИТЬ?',33)
        centered(d,W/2,205,'Выбирай по привычкам',18,'#f5dcea',False)
    d.rounded_rectangle((26,670,406,729),radius=19,fill='#ff557e')
    centered(d,W/2,685,'ГИД НА САЙТЕ →',22)
    return im
def audio(path):
    sr=24000;samples=np.zeros(sr*DURATION)
    notes=[220,277.18,329.63,293.66,246.94,329.63,369.99,329.63,220,277.18,329.63,440]
    for sec,hz in enumerate(notes):
        t=np.arange(sr)/sr
        env=np.minimum(1,t*7)*np.minimum(1,(1-t)*4)
        samples[sec*sr:(sec+1)*sr]=env*(.12*np.sin(2*np.pi*hz*t)+.04*np.sin(4*np.pi*hz*t))
    with wave.open(str(path),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr)
        f.writeframes((np.clip(samples,-1,1)*32767).astype('<i2').tobytes())
def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        wav=Path(td)/'music.wav';audio(wav)
        cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(wav),'-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',str(OUT)]
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        try:
            for i in range(FPS*DURATION):p.stdin.write(frame(i/FPS).tobytes())
        finally:p.stdin.close()
        if p.wait()!=0:raise RuntimeError('ffmpeg encoding failed')
    print('Rendered',OUT,OUT.stat().st_size,'bytes')
if __name__=='__main__':main()
