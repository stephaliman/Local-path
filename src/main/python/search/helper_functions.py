import logging, fractions
from search.search_classes import XslotTypes
from lexicon.module_classes import TimingInterval, TimingPoint

def articulatordisplaytext(arts, phase):
    k = arts[0] # hand, arm, or leg
    if arts[1][1] and not arts[1][2]:
        todisplay = k + " " + str(1)
    elif arts[1][2] and not arts[1][1]:
        todisplay = k + " " + str(2)
    elif arts[1][1] and arts[1][2]:
        
        todisplay = "Both " + k.lower() + "s"
        if phase == 1:
            todisplay += " in phase"
        elif phase == 2:
            todisplay += " out of phase"
        elif phase == 3:
            todisplay += " connected"
        elif phase == 4:
            todisplay += " connected, in phase"
    return todisplay

def phonlocsdisplaytext(phonlocs):
    todisplay = []
    if phonlocs.phonologicalloc:
        if phonlocs.majorphonloc:
            todisplay.append("Maj. phonological locn")
        if phonlocs.minorphonloc:
            todisplay.append("Min. phonological locn")
        else:
            todisplay.append("Phonological locn")
    if phonlocs.phoneticloc:
        todisplay.append("Phonetic locn")
    return todisplay

def loctypedisplaytext(loctype):
    todisplay = []
    if loctype.body:
       todisplay.append("Body")
    elif loctype.signingspace:
        txt = "Signing space"
        if loctype.bodyanchored:
            txt += " (body anchored)"
        elif loctype.purelyspatial:
            txt += " (purely spatial)"
        todisplay.append(txt)
    return todisplay

def signtypedisplaytext(specslist):
    
    specs = [s[0] for s in specslist]
    disp = []
    if 'Unspecified' in specs:
        disp.append('Unspecified')
    if '1h' in specs:
        oneh = []
        for s in ['1h.moves', '1h.no mvmt']:
            if s in specs:
                oneh.append(s)
        if len(oneh) > 0:
            disp.extend(oneh)
        else:
            disp.append('1h')

    if '2h' in specs:
        twoh = []
        for s in ['same HCs', 'different HCs', 'maintain contact', 'contact not maintained', 'bilaterally symmetric', 'not bilaterally symmetric', 'neither moves']:
            if ('2h.' + s) in specs:
                twoh.append('2h.' + s)
        if '2h.only 1 moves' in specs:
            only1moves = []
            for s in ['H1 moves', 'H2 moves']:
                if ('2h.only 1 moves.' + s) in specs:
                    only1moves.append('2h.only ' + s)
            if len(only1moves) > 0:
                twoh.extend(only1moves)
            else:
                twoh.append('2h.one hand moves')
        if '2h.both move' in specs:
            bothmove = []
            for s in ['move differently', 'move similarly']:
                if ('2h.both move.' + s) in specs:
                    bothmove.append('2h.hands ' + s)
            if len(bothmove) > 0:
                twoh.extend(bothmove)
            else:
                twoh.append('2h.both move')     
        if (len(twoh) > 0):
            disp.extend(twoh)
        else:
            disp.append('2h')

    return disp

# TODO
def module_matches_xslottype(timingintervals, targetintervals, xslottype, xslotstructure):
    # logging.warning(timingintervals)
    if xslottype == XslotTypes.IGNORE:
        return True
    
    if xslottype == XslotTypes.CONCRETE:
        return timingintervals == targetintervals

    if xslottype == XslotTypes.ABSTRACT_WHOLE:
        targetint = targetintervals[0] # only one selection is possible: either startpt, endpt, or whole sign.
        if targetint.iswholesign() and timingintervals[0].iswholesign():
            return True
        # match if occurring during start of sign
        elif targetint.ispoint() and targetint.startpoint == TimingPoint(1, 0):
            for t in timingintervals:
                if t.startpoint == TimingPoint(1, 0) or t.startpoint == TimingPoint(0, 0):
                    return True
            return False
        # match if occurring during end of sign
        elif targetint.ispoint() and targetint.startpoint == TimingPoint(1, 1):
            # xslotstructure's additionalfraction is 0 if there are no additionalfractions, but the TimingPoint object will have fraction 1
            frac = 1 if xslotstructure.additionalfraction == 0 else xslotstructure.additionalfraction
            # xslotstructure's number is the number of whole xslots, but the TimingPoint object also couts partial xslots
            num = xslotstructure.number if frac == 1 else xslotstructure.number + 1
            endpoint = TimingPoint(num, frac)
            for t in timingintervals:
                if t.endpoint == endpoint or t.endpoint == TimingPoint(0, 1):
                    return True
            return False
        else:
            return False


    if xslottype == XslotTypes.ABSTRACT_XSLOT:
        for targetint in targetintervals:
            if targetint.ispoint():
                for t in timingintervals:
                    if targetint.startpoint.fractionalpart == t.startpoint.fractionalpart:
                        return True
            else:
                for t in timingintervals:
                    if targetint.startpoint.fractionalpart == t.startpoint.fractionalpart and targetint.endpoint.fractionalpart == t.endpoint.fractionalpart:
                        return True

            
        return False



        