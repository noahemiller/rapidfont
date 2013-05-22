from robofab.world import CurrentGlyph,CurrentFont
from robofab.interface.all.dialogs import AskString, Message



offset = AskString("Offset components by how many units??")
if offset == None:
    offset = 0
if offset or offset == 0:
    try:
        offset = int(offset)
    except ValueError:
        Message("Numbers only.")
    else:
        font = CurrentFont()
        weight = int(font["straight"].box[2])
        roundWidth=int(font["round"].box[2])
        descender = font.info.descender
        xheight = font.info.xHeight
        ascender = font.info.ascender
        buildG = ['b','d','p','q','o','h','i','l','n','m','u','test']

        for glyph in buildG:
            font.newGlyph(glyph)
            
       
        
        b = font['b']
        b.appendComponent('straight')
        b.appendComponent('round',(weight+offset-font['round'].leftMargin,0))
        b.rightMargin=font['round'].rightMargin
        b.leftMargin=font['straight'].rightMargin

        d = font['d']
        d.appendGlyph(font['round'])
        d.scale((-1,1))
        d.move((roundWidth,0))
        d.appendComponent('straight',(roundWidth+offset-font['round'].leftMargin,0))
        d.rightMargin=font['straight'].rightMargin
        d.leftMargin=font['round'].rightMargin

        p = font['p']
        p.appendComponent('straight',(0,descender))
        p.appendComponent('round',(weight+offset-font['round'].leftMargin,0))
        p.rightMargin=font['round'].rightMargin
        p.leftMargin=font['straight'].rightMargin

        q = font['q']
        q.appendGlyph(font['round'])
        q.scale((-1,1))
        q.move((roundWidth,0))
        q.appendComponent('straight',(roundWidth+offset-font['round'].leftMargin,descender))
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
        i.appendGlyph(font['straight'])
        i.move((0,(xheight-ascender)))
        i.rightMargin=font['straight'].rightMargin
        i.leftMargin=font['straight'].rightMargin
        
        l = font['l']
        l.appendGlyph(font['straight'])
        l.rightMargin=font['straight'].rightMargin
        l.leftMargin=font['straight'].rightMargin
        
        
        n = font['n']
        n.appendGlyph(font['straight'])
        n.move((0,(xheight-ascender)))
        n.appendComponent('roundleg',(weight+offset,0))
        n.rightMargin=font['roundleg'].rightMargin
        n.leftMargin=font['straight'].rightMargin
        
        m = font['m']
        m.appendGlyph(font['straight'])
        m.move((0,(xheight-ascender)))
        m.appendComponent('roundleg',(weight+offset*3,0))
        m.appendComponent('roundleg',(weight+font['roundleg'].box[2]+offset*10,0))
        m.rightMargin=font['roundleg'].rightMargin
        m.leftMargin=font['straight'].rightMargin
        
        
        for glyph in buildG:
            for comp in font[glyph].components:
                comp.decompose()
            for cont in font[glyph]:
                cont.clockwise = True
                
        u = font['u']
        u.appendGlyph(font['n'])
        u.scale((-1,-1))
        u.move((0,500))
        u.rightMargin = n.leftMargin
        u.leftMargin = n.rightMargin

