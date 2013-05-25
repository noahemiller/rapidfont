from robofab.world import CurrentGlyph,CurrentFont
from robofab.interface.all.dialogs import AskString, Message
import sys, math

font = CurrentFont()

#trigonometry helper functions
def mySlope(px,py,qx,qy):
    theSlope = 0
    if px == qx and py == qy:
        sys.exit('Error: trying to calculate slope from single point')
    elif px == qx:
        theSlope = float("+inf")
    elif py == qy:
        theSlope = 0
    else:
        theSlope = float((qy - py)) / float((qx - px))
    return theSlope

def yIntercept(px, py, mp):
    yInter = py - mp * px
    return yInter
    
def nSlope(mp):
    normal = -1 / mp
    return normal
    
def lineX(mp, cp, mq, cq):
    if mp == mq:
        sys.exit('Error: trying to calculate intersect of parallels')
    elif cp == cq:
        lineX = (0, cp)
    else:
        myX = int((cp - cq) / (mq - mp))
        myY = int(mp * myX + cp)
        lineX = [myX, myY]
    return lineX

#testing to make sure the required components are present
meta = ['round','roundleg','straight']
for glyph in meta:
    if glyph not in font:
        #we exit here ... possibly expand to create blank component glyphs and promt user to create contours.
        sys.exit('Required component not found. Please use the fontBuilder.ufo supplied with this script.')
    elif len(font[glyph]) == 0:
        sys.exit('Required component ' + glyph + ' has no content. Please add contours to ' + glyph)
        

offset = AskString("Offset components by how many units??")
if offset == None:
    offset = 0
if offset or offset == 0:
    try:
        offset = int(offset)
    except ValueError:
        Message("Numbers only.")
    else:
        weight = int(font["straight"].box[2])
        roundWidth=int(font["round"].box[2])
        descender = font.info.descender
        xheight = font.info.xHeight
        ascender = font.info.ascender
        overshoot = abs(int(font["round"].box[1]))
        buildG = ['a','b','c','d','h','i','l','m','n','o','p','q','u','v','space','straightX','straightD']

        for glyph in buildG:
            font.newGlyph(glyph)
            
        #building an x-height straight by moving the two highest points of the straight down
        sX = font['straightX']
        sX.appendGlyph(font['straight'])
        pts = [0,0]
        for contour in sX:
            for point in contour.points:
                if point == contour.points[0]:
                    pts[0] = point
                    pts[1] = point
                if point.y > pts[0].y:
                    pts[1] = pts[0]
                    pts[0] = point
                elif point.y >= pts[1].y:
                    pts[1] = point
        pts[0].y -= (ascender - xheight)
        pts[1].y -= (ascender - xheight)
        for contour in sX:
            contour.update()
        sX.rightMargin=font['straight'].rightMargin
        sX.leftMargin=font['straight'].leftMargin
        sX.mark = (1,.7,0,1)
        
        #building a descender straight by moving the two lowest points of the straight up
        sD = font['straightD']
        sD.appendGlyph(font['straight'])
        sD.move((0,-(ascender-xheight)))
        pts = [0,0]
        for contour in sD:
            for point in contour.points:
                if point == contour.points[0]:
                    pts[0] = point
                    pts[1] = point
                if point.y < pts[0].y:
                    pts[1] = pts[0]
                    pts[0] = point
                elif point.y <= pts[1].y:
                    pts[1] = point
        if pts[0].y < descender:
            pts[1].y += abs(pts[0].y - descender)
            pts[0].y += abs(pts[0].y - descender)
        for contour in sD:
            contour.update()
        sD.rightMargin=font['straight'].rightMargin
        sD.leftMargin=font['straight'].leftMargin
        sD.mark = (1,.7,0,1)

        space = font['space']
        space.width = roundWidth

        a = font['a']
        a.appendGlyph(font['round'])
        a.scale((-1,1))
        a.move((roundWidth,0))
        a.appendComponent('straightX',(roundWidth+offset-font['round'].leftMargin-weight/2,0))
        a.leftMargin=font['round'].rightMargin
        a.rightMargin=font['straight'].rightMargin
        
        b = font['b']
        b.appendComponent('straight')
        b.appendComponent('round',(weight/2+offset-font['round'].leftMargin,0))
        b.rightMargin=font['round'].rightMargin
        b.leftMargin=font['straight'].rightMargin
        
        c = font['c']
        c.appendGlyph(font['round'])
        c.scale((-1,1))
        c.leftMargin=font['round'].rightMargin
        c.rightMargin=font['round'].rightMargin - 10

        d = font['d']
        d.appendGlyph(font['round'])
        d.scale((-1,1))
        d.move((roundWidth,0))
        d.appendComponent('straight',(roundWidth+offset-font['round'].leftMargin-weight/2,0))
        d.rightMargin=font['straight'].rightMargin
        d.leftMargin=font['round'].rightMargin

        p = font['p']
        p.appendComponent('straightD')
        p.appendComponent('round',(weight/2+offset-font['round'].leftMargin,0))
        p.rightMargin=font['round'].rightMargin
        p.leftMargin=font['straight'].rightMargin

        q = font['q']
        q.appendGlyph(font['round'])
        q.scale((-1,1))
        q.move((roundWidth,0))
        q.appendComponent('straightD',(roundWidth+offset-font['round'].leftMargin-weight/2,0))
        q.rightMargin=font['straight'].rightMargin
        q.leftMargin=font['round'].rightMargin

        o = font['o']
        o.appendGlyph(font['round'])
        o.scale((-1,-1))
        o.move((roundWidth,xheight))
        o.appendComponent('round',(roundWidth+offset,0))
        o.rightMargin=font['round'].rightMargin
        o.leftMargin=font['round'].rightMargin
        
        h = font['h']
        h.appendGlyph(font['straight'])
        h.appendComponent('roundleg',(weight+offset,0))
        h.rightMargin=font['roundleg'].rightMargin
        h.leftMargin=font['straight'].rightMargin
        
        i = font['i']
        i.appendGlyph(font['straightX'])
        i.rightMargin=font['straight'].rightMargin
        i.leftMargin=font['straight'].rightMargin
        
        l = font['l']
        l.appendGlyph(font['straight'])
        l.rightMargin=font['straight'].rightMargin
        l.leftMargin=font['straight'].rightMargin
        
        
        n = font['n']
        n.appendGlyph(font['straightX'])
        n.appendComponent('roundleg',(weight+offset,0))
        n.rightMargin=font['roundleg'].rightMargin
        n.leftMargin=font['straight'].rightMargin
        
        m = font['m']
        m.appendGlyph(font['straightX'])
        m.appendComponent('roundleg',(weight+offset*3,0))
        m.appendComponent('roundleg',(weight+font['roundleg'].box[2]+offset*10,0))
        m.rightMargin=font['roundleg'].rightMargin
        m.leftMargin=font['straight'].rightMargin
        
        v = font['v']
        A = (int((n.box[2]-n.rightMargin)/2),-overshoot)
        B = (int(n.box[2]-n.rightMargin+weight*0.33),xheight)
        abSlp = mySlope(A[0],A[1],B[0],B[1])
        bhSlp = nSlope(abSlp)
        Hx = B[0] - math.cos(math.atan(abs(bhSlp))) * weight * 0.85
        Hy = B[1] + math.sin(math.atan(abs(bhSlp))) * weight * 0.85
        hYinter = yIntercept(Hx,Hy,abSlp)
        C = (int((B[1] - hYinter)/abSlp), B[1])
        E = (int((A[0]-(C[0]-A[0]))*1.05),xheight)
        F = (A[0]-(B[0]-A[0]),xheight)
        cYinter = yIntercept(C[0],C[1],abSlp)
        eYinter = yIntercept(E[0],E[1],-abSlp)
        D = lineX(abSlp,cYinter,-abSlp,eYinter)
        D[1] = int(D[1] - weight*0.05)
        pen = v.getPen()
        pen.moveTo(A)
        pen.lineTo(B)
        pen.lineTo(C)
        pen.lineTo(D)
        pen.lineTo(E)
        pen.lineTo(F)
        pen.closePath()
        v.update()
        v.leftMargin = 0
        v.rightMargin = 0
        
        for glyph in buildG:
            for comp in font[glyph].components:
                comp.decompose()
            for cont in font[glyph]:
                cont.clockwise = True
                
        u = font['u']
        u.appendGlyph(font['n'])
        u.scale((-1,-1))
        u.move((0,xheight))
        u.rightMargin = n.leftMargin
        u.leftMargin = n.rightMargin
        
        mySorted = buildG + meta
        font.glyphOrder = mySorted
        print 'Font created.'