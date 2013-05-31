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
meta = ['round','roundleg','straight','crossbar','ucRound']
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
        hweight = int(60)
        roundWidth=int(font["round"].box[2])
        roundLegWidth=int(font["roundleg"].box[2])
        descender = font.info.descender
        xheight = font.info.xHeight
        ascender = font.info.ascender
        capheight = font.info.capHeight
        overshoot = abs(int(font["round"].box[1]))
        strtRM = font['straight'].rightMargin
        rndRM = font['round'].rightMargin
        rndlgRM = font['roundleg'].rightMargin
        buildG = ['D','E','F','H','I','L','O','T','a','b','c','d','e','f','h','i','l','m','n','o','p','q','t','u','v','space','straightX','straightD','ucStraight','ucCrossbar']

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
        sX.rightMargin=strtRM
        sX.leftMargin=0
        sX.mark = (1,.7,0,1)


        #building an uppercase vertical by scaling the lowercase straight by 10% and moving top 2 points down
        ucStraight = font['ucStraight']
        ucStraight.appendGlyph(font['straight'])
        pts = [0,0]
        ptsW = [0,0]
        for contour in ucStraight:
            for point in contour.points:
                if point == contour.points[0]:
                    pts[0] = point
                    pts[1] = point
                    ptsW[0] = point
                    ptsW[1] = point
                if point.y > pts[0].y:
                    pts[1] = pts[0]
                    pts[0] = point
                elif point.y >= pts[1].y:
                    pts[1] = point
                if point.x > ptsW[0].y:
                    ptsW[1] = ptsW[0]
                    ptsW[0] = point
                elif point.x >= ptsW[1].x:
                    ptsW[1] = point
        pts[0].y -= (ascender - capheight)
        pts[1].y -= (ascender - capheight)
        ptsW[0].x = int(ptsW[0].x*1.1)
        ptsW[1].x = int(ptsW[1].x*1.1)
        for contour in sX:
            contour.update()     
        ucStraight.mark = (1,.7,0,1)
        ucStraightWidth = ptsW[0].x
        if font['round'].rightMargin !=0:
            ucStraight.rightMargin = int((font['ucRound'].rightMargin * font['straight'].rightMargin) / font['round'].rightMargin)

        ucCrossbar = font['ucCrossbar']
        ucCrossbar.appendComponent('crossbar', (0,0),(1.4, 1.1))
        ucCrossbar.mark = (1,.7,0,1)
        ucCrossWidth = int(font['ucCrossbar'].box[2]) + int(font['ucCrossbar'].box[0])
                
        #building a descender straight by moving the two lowest points of the straight up
        sD = font['straightD']
        sD.appendGlyph(font['straight'],(0,-(ascender-xheight)))
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
        sD.leftMargin=0
        sD.mark = (1,.7,0,1)
        
        
        #Proper glyph construction starts here ****
        
        space = font['space']
        space.width = roundWidth

        a = font['a']
        a.appendComponent('round',(roundWidth,0),(-1,1))
        a.appendComponent('straightX',(roundWidth+offset-font['round'].leftMargin-weight/2,0))
        a.leftMargin=rndRM
        a.rightMargin=strtRM
        
        b = font['b']
        b.appendComponent('straight')
        b.appendComponent('round',(weight/2+offset-font['round'].leftMargin,0))
        b.rightMargin=rndRM
        b.leftMargin=strtRM
        
        c = font['c']
        c.appendComponent('round',(0,xheight),(-1,-1))
        c.leftMargin=font['round'].rightMargin
        c.rightMargin=font['round'].rightMargin - 20

        d = font['d']
        d.appendComponent('round',(roundWidth,int(font["round"].box[3])-overshoot),(-1,-1))
        d.appendComponent('straight',(roundWidth+offset-font['round'].leftMargin-weight/2,0))
        d.rightMargin=font['straight'].rightMargin
        d.leftMargin=font['round'].rightMargin

        e = font['e']
        e.appendComponent('crossbar',(weight,xheight-(xheight/3)))
        e.appendComponent('c')
        e.rightMargin=font['round'].rightMargin - 20
        e.leftMargin=font['round'].rightMargin
        

        f = font['f']
        f.appendComponent('straightX')
        f.appendComponent('roundleg',(roundLegWidth,ascender-xheight),(-1,1))
        f.appendComponent('crossbar',(-weight/2,xheight))
        f.leftMargin=font['straight'].rightMargin - weight/2
        f.rightMargin=-50
        
        p = font['p']
        p.appendComponent('straightD')
        p.appendComponent('round',(weight/2+offset-font['round'].leftMargin,0))
        p.rightMargin=font['round'].rightMargin
        p.leftMargin=font['straight'].rightMargin

        q = font['q']
        q.appendComponent('round',(roundWidth,int(font["round"].box[3])-overshoot),(-1,-1))
        q.appendComponent('straightD',(roundWidth+offset-font['round'].leftMargin-weight/2,0))
        q.rightMargin=font['straight'].rightMargin
        q.leftMargin=font['round'].rightMargin

        o = font['o']
        o.appendComponent('round',(roundWidth,xheight),(-1,-1))
        o.appendComponent('round',(roundWidth+offset,0))
        o.rightMargin=font['round'].rightMargin
        o.leftMargin=font['round'].rightMargin

        
        h = font['h']
        h.appendComponent('straight')
        h.appendComponent('roundleg',(weight+offset,0))
        h.rightMargin=font['roundleg'].rightMargin
        h.leftMargin=font['straight'].rightMargin
        
        i = font['i']
        i.appendComponent('straightX')
        i.rightMargin=font['straight'].rightMargin
        i.leftMargin=font['straight'].rightMargin
        
        l = font['l']
        l.appendComponent('straight')
        l.rightMargin=font['straight'].rightMargin
        l.leftMargin=font['straight'].rightMargin
        
        
        n = font['n']
        n.appendComponent('straightX')
        n.appendComponent('roundleg',(weight+offset,0))
        n.rightMargin=font['roundleg'].rightMargin
        n.leftMargin=font['straight'].rightMargin
        
        m = font['m']
        m.appendComponent('straightX')
        m.appendComponent('roundleg',(weight+offset*3,0))
        m.appendComponent('roundleg',(weight+font['roundleg'].box[2]+offset*10,0))
        m.rightMargin=font['roundleg'].rightMargin
        m.leftMargin=font['straight'].rightMargin

        t = font['t']
        t.appendComponent('roundleg',(roundLegWidth,xheight),(-1,-1))
        t.appendComponent('straightX',(0,xheight/3))
        t.appendComponent('crossbar',(-weight/2,xheight))
        t.leftMargin=font['straight'].rightMargin - weight/2
        t.rightMargin=0
        
        u = font['u']
        u.appendComponent('n',(0,xheight),(-1,-1))
        u.rightMargin = n.leftMargin
        u.leftMargin = n.rightMargin

        v = font['v']
        A = (int((n.box[2]-n.rightMargin)/2),-overshoot)
        B = (int(n.box[2]-n.rightMargin+weight*0.33),xheight)
        abSlp = mySlope(A[0],A[1],B[0],B[1])
        bhSlp = nSlope(abSlp)
        Hx = B[0] - math.cos(math.atan(abs(bhSlp))) * weight * 0.85
        Hy = B[1] + math.sin(math.atan(abs(bhSlp))) * weight * 0.85
        Hx = B[0] - math.cos(math.atan(abs(bhSlp))) * weight * 0.5
        Hy = B[1] + math.sin(math.atan(abs(bhSlp))) * weight * 0.5
        hYinter = yIntercept(Hx,Hy,abSlp)
        C = (int((B[1] - hYinter)/abSlp), B[1])
        E = (int((A[0]-(C[0]-A[0]))+weight*0.5),xheight)
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
        
        D = font ['D']
        D.appendComponent('ucStraight',(weight+offset,0))
        D.appendComponent('ucRound',(roundWidth+weight+offset,0))
        D.rightMargin = font['ucRound'].rightMargin
        D.leftMargin = ucStraight.rightMargin
        
        E = font['E']
        E.appendComponent('ucStraight',(weight+offset,0))
        E.appendComponent('ucCrossbar',(weight+offset+(weight/2),(capheight)),(0.9,1))
        E.appendComponent('ucCrossbar',(weight+offset+(weight/2),(capheight/2)+ hweight),(0.7,1))
        E.appendComponent('ucCrossbar',(weight+offset+(weight/2),hweight))
        E.rightMargin = ucStraight.rightMargin -15
        E.leftMargin = ucStraight.rightMargin
        
        F = font['F']
        F.appendComponent('ucStraight',(weight+offset,0))
        F.appendComponent('ucCrossbar',(weight+offset+(weight/2),(capheight)),(0.9,1))
        F.appendComponent('ucCrossbar',(weight+offset+(weight/2),(capheight/2)+ hweight),(0.7,1))
        F.rightMargin = ucStraight.rightMargin -15
        F.leftMargin = ucStraight.rightMargin
                
        H = font['H']
        H.appendComponent('ucStraight',(weight+offset,0))
        H.appendComponent('ucCrossbar',(weight+offset+(weight/2),(capheight/2)+hweight))
        H.appendComponent('ucStraight', ((ucCrossWidth+weight+offset),0),(1,1))
        H.rightMargin = ucStraight.rightMargin
        H.leftMargin = ucStraight.rightMargin

        I = font['I']
        I.appendComponent('ucStraight',(weight+offset,0))
        I.rightMargin = ucStraight.rightMargin
        I.leftMargin = ucStraight.rightMargin
        
        L = font['L']
        L.appendComponent('ucStraight',(weight+offset,0))
        L.appendComponent('ucCrossbar',(weight+offset+(weight/2),hweight),(0.9,1))
        L.rightMargin = ucStraight.rightMargin -15
        L.leftMargin = ucStraight.rightMargin
        
        O = font['O']
        O.appendComponent('ucRound',(roundWidth,capheight),(-1,-1))
        O.appendComponent('ucRound',(roundWidth+offset,0))
        O.rightMargin = font['ucRound'].rightMargin
        O.leftMargin = font['ucRound'].rightMargin

        T = font['T']
        T.appendComponent('ucStraight')
        T.appendComponent('ucCrossbar',(ucStraightWidth/2 - ucCrossWidth*1.3/2,capheight),(1.3,1))       
        T.rightMargin = 0
        T.leftMargin = 0
        
        
        for glyph in buildG:
            for comp in font[glyph].components:
                comp.decompose()
            for cont in font[glyph]:
                cont.clockwise = True
        
        mySorted = buildG + meta
        font.glyphOrder = mySorted
        print 'Font created.'