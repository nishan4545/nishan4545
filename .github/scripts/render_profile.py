"""Original profile animation generator; requires Python and Pillow.

Run: python .github/scripts/render_profile.py
On Linux, set PROFILE_FONT_DIR to a directory with DejaVuSans*.ttf fonts.
Generated assets are local: no animation service or API key is required.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import os

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
W, S = 1200, 2
NAVY, WHITE, MUTED = (9,15,29), (235,242,255), (142,161,190)
CYAN, BLUE, VIOLET, AMBER = (93,229,215), (99,163,255), (176,150,255), (248,196,113)
FONT_CACHE = {}

def font(size, bold=False, mono=False):
    key=(size,bold,mono)
    if key in FONT_CACHE: return FONT_CACHE[key]
    directory=Path(os.environ.get('PROFILE_FONT_DIR','C:/Windows/Fonts'))
    names=['consola.ttf','DejaVuSansMono.ttf'] if mono else (['segoeuib.ttf','DejaVuSans-Bold.ttf'] if bold else ['segoeui.ttf','DejaVuSans.ttf'])
    for name in names:
        if (directory/name).exists():
            FONT_CACHE[key]=ImageFont.truetype(str(directory/name),round(size*S))
            return FONT_CACHE[key]
    raise RuntimeError('Set PROFILE_FONT_DIR to a TrueType font directory.')

def xy(values): return tuple(round(v*S) for v in values)
def txt(d,pos,value,size=18,color=WHITE,bold=False,mono=False,anchor=None):
    d.text(xy(pos),value,fill=color,font=font(size,bold,mono),anchor=anchor)
def rounded(d,box,fill,outline=None,radius=12,width=1):
    d.rounded_rectangle(xy(box),radius=round(radius*S),fill=fill,outline=outline,width=round(width*S))
def line(d,points,color,width=1):
    d.line([xy(p) for p in points],fill=color,width=round(width*S),joint='curve')
def dot(d,pos,r,color):
    x,y=pos; d.ellipse(xy((x-r,y-r,x+r,y+r)),fill=color)
def blend(a,b,t): return tuple(round(x*(1-t)+y*t) for x,y in zip(a,b))

def background(height):
    small=Image.new('RGB',(300,max(1,height//4))); px=small.load()
    for y in range(small.height):
        for x in range(small.width):
            a=math.exp(-(((x-240)/90)**2+((y-12)/65)**2))
            b=math.exp(-(((x-150)/100)**2+((y-100)/70)**2))
            px[x,y]=(int(9+16*a),int(15+9*a+8*b),int(29+30*a+10*b))
    img=small.resize((W*S,height*S),Image.Resampling.BICUBIC)
    rounded(ImageDraw.Draw(img),(.5,.5,W-1,height-1),None,(43,55,77),22)
    return img

def path_point(points,progress):
    lengths=[math.dist(a,b) for a,b in zip(points,points[1:])]
    target=(progress%1)*sum(lengths)
    for i,length in enumerate(lengths):
        if target<=length:
            t=target/length
            return tuple(a+(b-a)*t for a,b in zip(points[i],points[i+1]))
        target-=length
    return points[-1]

def signal(d,points,progress,color):
    for offset,r,strength in [(.035,4,.14),(.021,4,.28),(.010,4,.5),(0,4,1)]:
        dot(d,path_point(points,progress-offset),r,blend((30,43,63),color,strength))

def save_animation(name,frames,durations):
    # One shared palette keeps the stationary background and text stable.
    samples=Image.new('RGB',(W,frames[0].height*4))
    for i,idx in enumerate([0,len(frames)//4,len(frames)//2,3*len(frames)//4]):
        samples.paste(frames[idx],(0,i*frames[0].height))
    palette=samples.quantize(colors=224,method=Image.Quantize.MEDIANCUT)
    out=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    out[0].save(ASSETS/name,save_all=True,append_images=out[1:],duration=durations,loop=0,optimize=True,disposal=1)
    frames[len(frames)//3].save(ASSETS/name.replace('.gif','-preview.png'))
    print(name, f'{(ASSETS/name).stat().st_size/1024:.0f} KB', f'{len(out)} frames',flush=True)

def hero():
    height=410; base=background(height); d=ImageDraw.Draw(base)
    for x in range(658,1180,26):
        for y in range(32,390,26): dot(d,(x,y),.7,(43,54,77))
    rounded(d,(42,31,340,64),(18,31,47),(42,62,77),16)
    dot(d,(61,47),3,CYAN)
    txt(d,(76,37),'NISHAN4545 / DEVELOPER',13,CYAN,mono=True)
    txt(d,(39,83),'NISHAN',82,WHITE,bold=True)
    txt(d,(44,192),'FULL STACK + AI',28,CYAN,bold=True)
    txt(d,(44,243),'From interfaces to intelligence.',23)
    txt(d,(44,280),'React. Services. Models. Connected.',17,MUTED)
    for x,label,width in [(44,'BUILD',90),(146,'INTEGRATE',126),(284,'REFINE',99)]:
        rounded(d,(x,337,x+width,370),(16,28,43),(43,61,78),8)
        txt(d,(x+15,345),label,12,MUTED,mono=True)
    cx,cy=930,205
    for r in [80,119,156]: d.ellipse(xy((cx-r,cy-r,cx+r,cy+r)),outline=(46,59,84),width=2)
    wires=[([(690,100),(748,100),(748,177),(875,177)],BLUE),
           ([(1154,85),(1081,85),(1081,177),(985,177)],VIOLET),
           ([(689,318),(766,318),(766,239),(875,239)],CYAN),
           ([(1151,329),(1088,329),(1088,239),(985,239)],AMBER)]
    for points,col in wires:
        line(d,points,blend(NAVY,col,.35),2); dot(d,points[0],5,col)
    for x,y,label,col in [(673,68,'UI',BLUE),(1115,53,'API',VIOLET),(672,336,'AI',CYAN),(1108,347,'DATA',AMBER)]:
        txt(d,(x,y),label,13,col,mono=True)
    frames=[]
    for n in range(64):
        t=n/64; img=base.copy(); d=ImageDraw.Draw(img)
        for i,(points,col) in enumerate(wires): signal(d,points,t+i*.25,col)
        for i,(r,col) in enumerate([(80,BLUE),(119,VIOLET),(156,CYAN)]):
            a=2*math.pi*(t*(1 if i%2==0 else -1)+i*.33)
            pos=(cx+r*math.cos(a),cy+r*math.sin(a))
            dot(d,pos,7,blend(NAVY,col,.3)); dot(d,pos,3,col)
        pulse=(1+math.sin(t*2*math.pi))/2
        rounded(d,(869,145,991,267),(15,25,44),blend((60,83,108),CYAN,.3+.5*pulse),25,2)
        line(d,[(913,187),(892,206),(913,225)],WHITE,4)
        line(d,[(947,187),(968,206),(947,225)],WHITE,4)
        line(d,[(938,181),(924,231)],CYAN,4)
        txt(d,(930,289),'IDEA → SYSTEM',12,MUTED,mono=True,anchor='mm')
        frames.append(img.resize((W,height),Image.Resampling.LANCZOS))
    save_animation('hero.gif',frames,100)

def workflow():
    height=176; base=background(height); d=ImageDraw.Draw(base)
    txt(d,(27,15),'THE LAYERS I WORK ACROSS',11,MUTED,mono=True)
    nodes=[(27,'01','INTERFACES','React · HTML · CSS',BLUE),
           (325,'02','SERVICES','Node.js · FastAPI',VIOLET),
           (623,'03','DOCUMENT AI','OCR · Model routing',CYAN),
           (921,'04','DELIVERY','AWS · Docker · Git',AMBER)]
    paths=[]
    for i,(x,number,title,subtitle,col) in enumerate(nodes):
        rounded(d,(x,48,x+251,149),(15,25,42),(43,59,82),13)
        txt(d,(x+17,64),number,13,col,mono=True)
        txt(d,(x+17,89),title,18,WHITE,bold=True)
        txt(d,(x+17,119),subtitle,13,MUTED)
        if i<3:
            points=[(x+254,98),(x+294,98)]
            line(d,points,(55,70,92),2); paths.append(points)
    frames=[]
    for n in range(48):
        img=base.copy(); d=ImageDraw.Draw(img); t=n/48
        for i,points in enumerate(paths): signal(d,points,t*2-i*.2,[BLUE,VIOLET,CYAN][i])
        for i,(x,_,__,___,col) in enumerate(nodes):
            strength=.25+.6*(.5+.5*math.sin(2*math.pi*(t-i*.25)))
            line(d,[(x+18,148),(x+233,148)],blend((27,40,58),col,strength),2)
        frames.append(img.resize((W,height),Image.Resampling.LANCZOS))
    save_animation('workflow.gif',frames,110)

def focus():
    height=200; base=background(height); d=ImageDraw.Draw(base)
    for i,col in enumerate([(243,130,130),(242,199,114),(107,205,162)]): dot(d,(28+i*19,25),4,col)
    txt(d,(99,16),'nishan / focus',13,MUTED,mono=True)
    line(d,[(20,46),(1180,46)],(36,49,69))
    txt(d,(30,69),'current_focus',15,CYAN,mono=True)
    txt(d,(30,153),'FULL STACK DEVELOPMENT  /  PRACTICAL AI',12,MUTED,mono=True)
    frames=[]; durations=[]
    for message in ['Full-stack applications.','Backend microservices.','AI document processing.','Cloud deployment.']:
        for k in range(0,len(message)+1,2):
            img=base.copy(); d=ImageDraw.Draw(img); value=message[:k]
            txt(d,(30,98),'> '+value,27,WHITE,mono=True)
            width=d.textlength('> '+value,font=font(27,mono=True))/S
            rounded(d,(32+width,101,45+width,128),CYAN,radius=1)
            frames.append(img.resize((W,height),Image.Resampling.LANCZOS)); durations.append(75)
        for blink in range(4):
            img=base.copy(); d=ImageDraw.Draw(img)
            txt(d,(30,98),'> '+message,27,WHITE,mono=True)
            width=d.textlength('> '+message,font=font(27,mono=True))/S
            if blink%2==0: rounded(d,(32+width,101,45+width,128),CYAN,radius=1)
            frames.append(img.resize((W,height),Image.Resampling.LANCZOS)); durations.append(430)
    save_animation('focus.gif',frames,durations)

def button():
    (ASSETS/'linkedin.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="218" height="42" viewBox="0 0 218 42">
<rect x=".5" y=".5" width="217" height="41" rx="10" fill="#101c2d" stroke="#33465f"/>
<rect x="14" y="12" width="18" height="18" rx="3" fill="#63a3ff"/>
<text x="23" y="25.5" fill="#09101d" font-family="Arial,sans-serif" font-size="14" font-weight="bold" text-anchor="middle">in</text>
<text x="45" y="26" fill="#edf3ff" font-family="Arial,sans-serif" font-size="13" font-weight="bold">LET'S CONNECT</text>
<path d="M188 26L198 16M189 16h9v9" fill="none" stroke="#5de5d7" stroke-width="1.6"/>
</svg>''',encoding='utf-8')

if __name__=='__main__': hero(); workflow(); focus(); button()
