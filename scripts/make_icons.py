# Draws the scales-of-justice icon at every size Android needs (no image library required).
import zlib, struct, os
BG=(13,90,71); FG=(255,255,255)
def shape(X,Y):
    if 248<=X<=264 and 150<=Y<=380: return True
    if 180<=X<=332 and 372<=Y<=392: return True
    if 214<=X<=298 and 356<=Y<=374: return True
    if (X-256)**2+(Y-138)**2<=16**2: return True
    if 130<=X<=382 and 166<=Y<=180: return True
    for ax,bx in ((140,100),(140,180),(372,332),(372,412)):
        t=(Y-178)/112
        if 0<=t<=1 and abs(X-(ax+(bx-ax)*t))<=4.5: return True
    for cx in (140,372):
        if 288<=Y<=318 and (X-cx)**2+(Y-288)**2<=48**2: return True
    return False
def draw(size,path,k=1.0,bg=True,round_mask=False,radius=0.0):
    s=size/512.0; raw=bytearray(); c=(size-1)/2
    for y in range(size):
        raw.append(0)
        for x in range(size):
            if round_mask and (x-c)**2+(y-c)**2>(size/2)**2: raw+=b'\0\0\0\0'; continue
            if radius:
                R=size*radius; cx=min(max(x,R),size-1-R); cy=min(max(y,R),size-1-R)
                if (x-cx)**2+(y-cy)**2>R*R: raw+=b'\0\0\0\0'; continue
            n=sum(shape(((x+dx)/s-256)/k+256,((y+dy)/s-265)/k+265) for dx in (.25,.75) for dy in (.25,.75))
            a=n/4
            if bg: raw+=bytes((*[round(BG[i]*(1-a)+FG[i]*a) for i in range(3)],255))
            else: raw+=bytes((255,255,255,round(255*a)))
    ch=lambda t,d: struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    os.makedirs(os.path.dirname(path),exist_ok=True)
    open(path,'wb').write(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',size,size,8,6,0,0,0))+ch(b'IDAT',zlib.compress(bytes(raw),9))+ch(b'IEND',b''))
res='android/app/src/main/res'
for d,m in (('mdpi',1),('hdpi',1.5),('xhdpi',2),('xxhdpi',3),('xxxhdpi',4)):
    draw(int(48*m),f'{res}/mipmap-{d}/ic_launcher.png',k=0.95,radius=0.2)
    draw(int(48*m),f'{res}/mipmap-{d}/ic_launcher_round.png',k=0.9,round_mask=True)
    draw(int(108*m),f'{res}/mipmap-{d}/ic_launcher_foreground.png',k=0.72,bg=False)
    draw(int(24*m),f'{res}/drawable-{d}/ic_stat_notify.png',k=1.25,bg=False)
print('icons ok')
