from pathlib import Path
from PIL import Image, ImageDraw
from render_profile import txt, line, dot, save_animation, S, xy

INK=(36,50,75); BLUE=(53,107,234); MUTED=(100,113,138)
def render(mobile=False):
 w,h=(600,260) if mobile else (1200,240)
 base=Image.new('RGB',(w*S,h*S),'white'); d=ImageDraw.Draw(base)
 txt(d,(w/2,48 if mobile else 40),"Hi, I'm Nishan.",49 if mobile else 62,INK,True,anchor='mt')
 txt(d,(w/2,122 if mobile else 131),'FULL STACK DEVELOPER',17 if mobile else 18,BLUE,mono=True,anchor='mt')
 line(d,[(w/2-170,h-24),(w/2+170,h-24)],(228,235,248),1)
 phrases=['Interfaces. Systems. Intelligence.','React. Backend services. Applied AI.']
 frames=[]
 for n in range(100):
  im=base.copy(); d=ImageDraw.Draw(im)
  phase=n%50; phrase=phrases[n//50]; count=min(len(phrase),round(phase/27*len(phrase)))
  display=phrase[:count]
  txt(d,(w/2,165 if mobile else 174),display+(" |" if phase%12<7 else "  "),16,MUTED,mono=True,anchor='mt')
  x=w/2-170+(n/99)*340
  dot(d,(x,h-24),3,BLUE)
  frames.append(im.resize((w,h),Image.Resampling.LANCZOS))
 name='hero-mobile.gif' if mobile else 'hero.gif'
 save_animation(name,frames,85)
 frames[40].save(Path(__file__).resolve().parents[2]/'assets'/name.replace('.gif','-preview.png'))
if __name__=='__main__':
 render();render(True)
