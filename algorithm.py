import PIL
from PIL import Image
import math
import random

class Rect:
    left: int
    right: int
    down: int
    top: int
    def __init__(self, left, right, down, top):
        self.left = left
        self.right = right
        self.down = down
        self.top = top

class Chunk:
    rect: Rect
    totalr: int
    totalg: int
    totalb: int
    def __init__(self, rect, tr, tg, tb):
        self.rect = rect
        self.totalr = tr
        self.totalg = tg
        self.totalb = tb

def rand01(acc = 100):
    r = random.randint(0, acc)
    return r/acc

def edit_chunk(img: Image.Image, rect: Rect, total: tuple[int, int, int], colored: bool = True):
    r, g, b = total[0], total[1], total[2]
    rr, gg, bb = r*r, g*g, b*b
    white = math.sqrt(rr + gg + bb)
    addr, addg, addb = 0, 0, 0
    KOEF = 1.4
    MAXCOLOR = 20
    WHITECOLOR = 60
    if (colored):
        if (rr > KOEF*(gg + bb)):
            addr = math.sqrt(rr - gg - bb)
        elif (gg > KOEF*(rr + bb)):
            addg = math.sqrt(gg - rr - bb)
        elif (bb > KOEF*(rr + gg)):
            addb = math.sqrt(bb - rr - gg)

    while (white > 0):
        for y in range(rect.down, rect.top):
            for x in range(rect.left, rect.right):
                color = list(img.getpixel((x,y)))
                rand = rand01()
                crand = rand01()
                
                w = int(rand * WHITECOLOR)
                color[0] += w
                color[1] += w
                color[2] += w
                white -= w
                
                if (addr > 0):
                    c = int(crand * MAXCOLOR)
                    color[0] += c
                    addr -= c
                elif (addg > 0):
                    c = int(crand * MAXCOLOR)
                    color[1] += c
                    addg -= c
                if (addb > 0):
                    c = int(crand * MAXCOLOR)
                    color[2] += c
                    addb -= c
                
                color[0] = min(255, color[0])
                color[1] = min(255, color[1])
                color[2] = min(255, color[2])
            
                img.putpixel( (x,y), tuple(color))
                
                if (white <= 0):
                    break
            if (white <= 0):
                break
            
    


def alg(image: Image.Image, chunksize: int) -> Image.Image:
    (xsize, ysize) = image.size
    img = Image.new("RGB", (xsize, ysize))
    chx = xsize//chunksize
    if (xsize - chx*chunksize > 0):
        chx += 1
    chy = ysize//chunksize
    if (ysize - chy*chunksize > 0):
        chy += 1
        
    chunks = [ [0 for j in range(chx)] for i in range(chy) ]
    
    x, y = 0, 0
    xold, yold = 0, 0
    cx, cy = 0, 0
    totalr, totalg, totalb = 0, 0, 0
    
    while (1):
        # doing smth...
        color = image.getpixel((x,y))
        totalr, totalg, totalb = totalr + color[0], totalg + color[1], totalb + color[2]
        # done smth 
        x += 1
        if (x%chunksize == 0 or x == xsize):
            y += 1
            if (y%chunksize == 0 or y == ysize):
                # ...
                chunks[cy][cx] = Chunk(Rect(xold, x, yold, y), totalr, totalg, totalb)
                totalr, totalg, totalb = 0, 0, 0
                # chunk done
                
                xold += chunksize
                cx += 1
                if (xold >= xsize):
                    xold = 0
                    yold += chunksize
                    if (yold >= ysize):
                        break
                    cx, cy = 0, cy+1
                    
                y = yold
            x = xold
    
    KOEF = 0.1
    for ly in range(chy):
        for lx in range(chx):
            chunk = chunks[ly][lx]
            r, g, b = int(KOEF*chunk.totalr), int(KOEF*chunk.totalg), int(KOEF*chunk.totalb)
            try:
                chunks[chy-1][chx].totalr += r
                chunks[chy-1][chx].totalg += g
                chunks[chy-1][chx].totalb += b
                chunk.totalr -= r
                chunk.totalg -= g
                chunk.totalb -= b
            except: pass
            
            try:
                chunks[chy+1][chx].totalr += r
                chunks[chy+1][chx].totalg += g
                chunks[chy+1][chx].totalb += b
                chunk.totalr -= r
                chunk.totalg -= g
                chunk.totalb -= b
            except: pass
            
            try:
                chunks[chy][chx-1].totalr += r
                chunks[chy][chx-1].totalg += g
                chunks[chy][chx-1].totalb += b
                chunk.totalr -= r
                chunk.totalg -= g
                chunk.totalb -= b
            except: pass
            
            try:
                chunks[chy][chx+1].totalr += r
                chunks[chy][chx+1].totalg += g
                chunks[chy][chx+1].totalb += b
                chunk.totalr -= r
                chunk.totalg -= g
                chunk.totalb -= b
            except: pass
    
    for ly in range(chy):
        for lx in range(chx):
            chunk = chunks[ly][lx]
            edit_chunk(img, chunk.rect, (chunk.totalr, chunk.totalg, chunk.totalb), True)
                        
    return img