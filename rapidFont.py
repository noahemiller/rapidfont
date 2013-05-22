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
        weight = int(font["B"].box[2])
        roundWidth=int(font["A"].box[2])
        descender = font.info.descender
        buildG = ['b','d','p','q','o','h','i','l','n','m','u']

        for glyph in buildG:
            font.newGlyph(glyph)

        b = font['b']
        b.appendComponent('B')
        b.appendComponent('A',(weight+offset-font['A'].leftMargin,0))
        b.rightMargin=font['A'].rightMargin
        b.leftMargin=font['B'].rightMargin

        d = font['d']
        d.appendGlyph(font['A'])
        d.scale((-1,1))
        d.move((roundWidth,0))
        d.appendComponent('B',(roundWidth+offset-font['A'].leftMargin,0))
        d.rightMargin=font['B'].rightMargin
        d.leftMargin=font['A'].rightMargin

        p = font['p']
        p.appendComponent('B',(0,descender))
        p.appendComponent('A',(weight+offset-font['A'].leftMargin,0))
        p.rightMargin=font['A'].rightMargin
        p.leftMargin=font['B'].rightMargin

        q = font['q']
        q.appendGlyph(font['A'])
        q.scale((-1,1))
        q.move((roundWidth,0))
        q.appendComponent('B',(roundWidth+offset-font['A'].leftMargin,descender))
        q.rightMargin=font['B'].rightMargin
        q.leftMargin=font['A'].rightMargin

        o = font['o']
        o.appendGlyph(font['A'])
        o.scale((-1,1))
        o.move((roundWidth,0))
        o.appendComponent('A',(roundWidth+offset,0))
        o.rightMargin=font['A'].rightMargin
        o.leftMargin=font['A'].rightMargin
        
        h = font['h']
        h.appendGlyph(font['B'])
        h.appendComponent('C',(weight+offset,0))
        h.rightMargin=font['C'].rightMargin
        h.leftMargin=font['B'].rightMargin
        
        i = font['i']
        i.appendGlyph(font['B'])
        i.scale((1,0.666))
        i.rightMargin=font['B'].rightMargin
        i.leftMargin=font['B'].rightMargin
        
        l = font['l']
        l.appendGlyph(font['B'])
        l.rightMargin=font['B'].rightMargin
        l.leftMargin=font['B'].rightMargin
        
        
        n = font['n']
        n.appendGlyph(font['B'])
        n.scale((1,0.666))
        n.appendComponent('C',(weight+offset,0))
        n.rightMargin=font['C'].rightMargin
        n.leftMargin=font['B'].rightMargin
        
        m = font['m']
        m.appendGlyph(font['B'])
        m.scale((1,0.666))
        m.appendComponent('C',(weight+offset*3,0))
        m.appendComponent('C',(weight+font['C'].box[2]+offset*10,0))
        m.rightMargin=font['C'].rightMargin
        m.leftMargin=font['B'].rightMargin
        
        
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

