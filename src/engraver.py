import sys
import os 
import importlib.metadata

def addobjectat(score, x, y, obj):
    score[y] = score[y][:x] + obj + score[y][x+1:]
    return score

def clearobjectat(score, x, w):
    for y in range(len(score)):
        replacement = ""
        if y % 2 == 0: replacement = " " * w
        else: replacement = "-" * w
        score[y] = score[y][:x] + replacement + score[y][x+w:]
    return score

def addnoteat(score, x, y, dur, hasdot):
    if dur in ["4n", "8n"]:
        notehead = "●"
    elif dur == "2n":
        notehead = "○"
    elif dur == "1n":
        notehead = "🞇"
    score = addobjectat(score, x, y, notehead)
    # stems
    if dur in ["8n", "4n", "2n"]:
        score = addstemfornoteat(score, x, y)
    # flags
    if dur == "8n":
        score = addflagfornoteat(score, x, y)
    if hasdot: # dotted note
        score = addobjectat(score, x+1, y, ".")
    return score

def addrestat(score, x, dur, hasdot):
    # eighth and quarter note rests above middle line
    if dur == "8n":
        obj = "𝄾"
        y = 4
    elif dur == "4n":
        obj = "𝄽"
        y = 4
    # half rests on middle line
    elif dur == "2n": 
        obj = "𝄼"
        y = 5
    # whole notes below middle line
    elif dur == "1n":
        obj = "𝄻"
        y = 6
    else: return
    score = addobjectat(score, x, y, obj)
    if hasdot: return addobjectat(score, x+1, y, ".")
    else: return score
    

def addstemfornoteat(score, x, y):
    step = 0
    if y < 5: # stem down
        step = 1
    else: # stem up
        step = -1
    for i in range(1,4):
        thisline = y + (i * step)
        score[thisline] = score[thisline][:x+1] + "|" + score[thisline][x+2:]
    return score
        
def addflagfornoteat(score, x, y):
    step = 0
    dir = 0
    flag = "╮"
    if y < 5: # left
        step = 3
        dir = 0
    else: # right
        step = -3
        dir = 2
    score[y+step] = score[y+step][:x+dir] + flag + score[y+step][x+dir+1:]
    return score

def clearandprintscore(score, lf, lall):
    os.system('cls' if os.name == 'nt' else 'clear')
    for m in range(len(score)):
        printbar(score[m], m, lf, lall)

def printbar(measure, num, lf, lall):
    if num == 0:
        print(str(num+1))
        for l in range(len(measure)):
            print(lf[l] + measure[l])
    else:
        print("\n\n\n" + str(num+1))
        for l in range(len(measure)):
            print(lall[l] + measure[l])
    return measure

def main():
    # sys.argv = ["engraver", "--version"] # for debugging
    clef = None 
    timesig = None
    keysig = None
    barinput = None
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help"]: # show help screen
            sys.exit("engraver: the basic CL sheet music engraving tool nobody asked for\n\nUsage:\n    engraver new (treble|bass) (4/4|3/4|2/4|12/8|9/8|6/8|3/8) (C|F|Bb|Eb|Ab|Db|Gb|Cb|G|D|A|E|B|F#|C#) <number_of_bars>\n    engraver new\n    engraver -h | --help\n    engraver --version\n\nOptions:\n    -h --help      Show this screen.\n    --version      Show version.\n\nAdding objects:\n    Notes:\n        <pitch> <duration> [.]\n    Rests:\n        r <duration> [.]\n    Accidentals:\n        (f|s|n) <pitch>\n\nTreble clef pitches: d4|e4|f4|g4|a4|b4|c5|d5|e5|f5|g5\nBass clef pitches: f2|g2|a2|b2|c3|d3|e3|f3|g3|a3|b3\nDurations: 1n|2n|4n|8n")
        elif sys.argv[1] == "--version":
            sys.exit(importlib.metadata.version("engraver"))
        elif len(sys.argv) < 6:
            sys.exit("Not enough arguments.  engraver -h for more information.")
        else:
            clef = sys.argv[2]
            timesig = sys.argv[3]
            keysig = sys.argv[4]
            barinput = sys.argv[5]
    # clef
    treble = ["           ^        ", "|----------%+-------", "|         +:+       ", "|----------+#-------", "|        =@*        ", "|-------%#**--------", "|      ++:##*%)     ", "|------(*:=-:-+-----", "|        -==*:      ", "|--------:=.=-------", "        #*:+        "]
    bass = ["                    ", "--------------------", "     @@@@@@@  @     ", "----@@@@--@@@@@@----", "     @@@@ @@@@@     ", "----------@@@@@@----", "         @@@        ", "-------@@@----------", "    @@@             ", "--------------------", "                    "]
    clefwidth = len(treble[0])
    myclef = None
    while myclef == None:     
        if not clef:
            clef = input("Which clef? (treble or bass, q to quit): ")
        if clef == "treble":
            myclef = treble
        elif clef == "bass":
            myclef = bass
        elif clef == "q":
            sys.exit()
        else:
            clef = None # bad input, make sure we ask again

    # time signature
    twofour = ["     XXX    ","----X---X---","       XX   ","-----XX-----","    XXXXX   ","------------","        X   ","------X-X---","    XXXXXX  ","--------X---","        X   "]
    threefour = ["    XXXX    ", "--------X---", "     XXX    ", "--------X---", "    XXXX    ", "------------", "        X   ", "------X-X---", "    XXXXXX  ", "--------X---", "        X   "]
    fourfour = ["        X   ", "------X-X---", "    XXXXXX  ", "--------X---", "        X   ", "------------", "        X   ", "------X-X---", "    XXXXXX  ", "--------X---", "        X   "]
    threeeight = ["     XXXX   ","---------X--","      XXX   ","---------X--","     XXXX   ","------------","     XXX    ","----X---X---","     XXX    ","----X---X---","    XXXXX   "]
    sixeight = ["     XXXX   ","----X-------","    X XXX   ","----XX---X--","     XXXX   ","------------","     XXX    ","----X---X---","     XXX    ","----X---X---","    XXXXX   "]
    nineeight = ["      XXX   ","-----X---X--","      XXXX  ","---------X--","      XXX   ","------------","     XXX    ","----X---X---","     XXX    ","----X---X---","    XXXXX   "]
    twelveeight = ["  X   XXX   ","-XX--X---X--","  X    XX   ","--X---XX----"," XXX XXXXX  ","------------","     XXX    ","----X---X---","     XXX    ","----X---X---","    XXXXX   "]
    timesigwidth = len(threefour[0])
    mytimesig = None
    while mytimesig == None:
        if not timesig: 
            timesig = input("Which time signature? (4/4 or 3/4, q to quit): ")
        if timesig == "4/4":
            mytimesig = fourfour
        elif timesig == "3/4":
            mytimesig = threefour
        elif timesig == "2/4":
            mytimesig = twofour
        elif timesig == "3/8":
            mytimesig = threeeight
        elif timesig == "6/8":
            mytimesig = sixeight
        elif timesig == "9/8":
            mytimesig = nineeight
        elif timesig == "12/8":
            mytimesig = twelveeight
        elif timesig == "q":
            sys.exit()
        else:
            timesig = None # bad input, make sure we ask again
        
    # key signature
    symbols = { "s": "♯", "f": "♭", "n": "♮" }
    flatindicestreble = [5, 2, 6, 3, 7, 4, 8]
    flatindicesbass = [7, 4, 8, 5, 2, 6, 3]
    sharpindicestreble = [1, 4, 0, 3, 6, 2, 5]
    sharpindicesbass = [3, 6, 2, 5, 1, 4, 7]
    flatkeys = { "F":1, "Bb":2, "Eb":3, "Ab":4, "Db":5, "Gb":6, "Cb":7 }
    sharpkeys = { "G":1, "D":2, "A":3, "E":4, "B":5, "F#":6, "C#":7 }
    keysigwidth = 0
    while keysigwidth == 0:
        if not keysig:
            keysig = input("Which key signature? (e.g. Eb, q to quit): ")
        if keysig in flatkeys:
            myflats = (flatindicestreble if clef == "treble" else flatindicesbass)[0:flatkeys[keysig]] 
            keysigwidth = len(myflats) * 3
        elif keysig in sharpkeys:
            mysharps = (sharpindicestreble if clef == "treble" else sharpindicesbass)[0:sharpkeys[keysig]]
            keysigwidth = len(mysharps) * 3
        elif keysig == "C":
            keysigwidth = 1
        elif keysig == "q":
            sys.exit()
        else:
            keysig = None # bad input, make sure we ask again
    ksspaces = " " * keysigwidth
    kslines = "-" * keysigwidth
    mykeysig = [ksspaces, kslines, ksspaces, kslines, ksspaces, kslines, ksspaces, kslines, ksspaces, kslines, ksspaces]
    kspointer = 1
    if keysig in flatkeys:
        for i in myflats:
            mykeysig = addobjectat(mykeysig, kspointer, i, symbols["f"])
            kspointer += 3
    elif keysig in sharpkeys:
        for i in mysharps:
            mykeysig = addobjectat(mykeysig, kspointer, i, symbols["s"])
            kspointer += 3

    # base score lines
    notewidth = 8
    timesignums = timesig.split("/")
    slotsperbar = int(timesignums[0]) * 8 // int(timesignums[1]) # for now, number of eighth notes per bar
    barwidth = notewidth * slotsperbar
    bars = 0
    while bars == 0:
        if not barinput:
            barinput = input("How many bars? (e.g. 2, q to quit): ")
        if barinput == "q":
            sys.exit()
        elif barinput.isdigit() and int(barinput) > 0:
            bars = int(barinput)
        else:
            barinput = None # bad input, make sure we ask again
    outsidespaces = (" " * (barwidth-1) + " ") + "\r" 
    spaces = (" " * (barwidth-1) + "︱") + "\r" 
    lines = ("-" * (barwidth-1) + "︱") + "\r"
    def onebar():
        return [outsidespaces, lines, spaces, lines, spaces, lines, spaces, lines, spaces, lines, outsidespaces]
    score = []
    for i in range(bars):
        score.append(onebar())
    leftfirstlineblob = [a + b + c for a, b, c in zip(myclef, mytimesig, mykeysig)]
    leftothersblob = [a + c for a, c in zip(myclef, mykeysig)]

    clearandprintscore(score, leftfirstlineblob, leftothersblob)
    
    next = ""
    durations = ["8n", "4n", "2n", "1n"]
    treblenotes = ["g5", "f5", "e5", "d5", "c5", "b4", "a4", "g4", "f4", "e4", "d4"]
    bassnotes = ["b3", "a3", "g3", "f3", "e3", "d3", "c3", "b2", "a2", "g2", "f2"]
    xpointer = 2
    if clef == "treble":
        notes = treblenotes
    elif clef == "bass":
        notes = bassnotes
    
    commandstack = []
    barnum = 0
    # object add section - loops until bars are full or user quit
    while barnum < bars: 
        os.system('cls' if os.name == 'nt' else 'clear')
        printbar(score[barnum], barnum, leftfirstlineblob, leftothersblob)
        
        while xpointer < len(score[barnum][0]): # until current bar full
            next = input("Add object? (e.g. g4 8n) q to quit: ")
            nextls = next.split()
            spacingmult = 1
            dotspace = False
            if next == "q":
                sys.exit()
            elif nextls[0] in notes: # contains note info
                if len(nextls) < 2:
                    print("No duration info, try again")
                    continue
                if len(nextls) > 2 and nextls[2] == ".": # dotted note
                    dotspace = True
                score[barnum] = addnoteat(score[barnum], xpointer, notes.index(nextls[0]), nextls[1], dotspace)
                commandstack.append([x for x in nextls]+[xpointer]) # add command and x to stack
                spacingmult = int(8 * (1.5 if dotspace else 1) // int(nextls[1][0]))
                xpointer += notewidth * spacingmult
            elif nextls[0] == "r": # contains rest info
                if len(nextls) < 2 or nextls[1] not in durations:
                    print("rest needs duration, try again")
                    continue
                else:
                    if len(nextls) > 2 and nextls[2] == ".": # dotted rest
                        dotspace = True
                    score[barnum] = addrestat(score[barnum], xpointer, nextls[1], dotspace)
                    commandstack.append([x for x in nextls]+[xpointer]) # add command and x to stack
                    spacingmult = int(8 * (1.5 if dotspace else 1) // int(nextls[1][0]))
                    xpointer += notewidth * spacingmult
            elif nextls[0] in symbols: # contains accidental info
                if len(nextls) < 2 or nextls[1] not in notes:
                    print("accidental needs pitch, try again")
                    continue
                else:
                    score[barnum] = addobjectat(score[barnum], xpointer-2, notes.index(nextls[1]), symbols[nextls[0]])
                    commandstack.append([x for x in nextls]+[xpointer]) # add command and x to stack
            elif nextls[0] == "d": # delete last object added
                lastcommand = commandstack.pop()
                xpointer = lastcommand[-1]
                commandhead = lastcommand[0]
                deleteatx = xpointer
                if commandhead in ["s", "f", "n"]: deleteatx -= 2
                score[barnum] = clearobjectat(score[barnum], deleteatx, notewidth)
            else:
                print("input not valid, double-check and try again")
                continue
            
            os.system('cls' if os.name == 'nt' else 'clear')
            printbar(score[barnum], barnum, leftfirstlineblob, leftothersblob)
        moveon = None
        while moveon == None:
            moveoninput = input("Move on to next bar, or redo bar " + str(barnum+1) + "? (next | redo) q to quit:")
            if moveoninput == "q":
                sys.exit()
            elif moveoninput == "next":
                moveon = True
            elif moveoninput == "redo":
                moveon = False
            else:
                print("invalid input, please type 'next', 'redo', or 'q':")
        if moveon:
            barnum += 1
            xpointer = 2
        else:
            score[barnum] = onebar()
            xpointer = 2
    clearandprintscore(score, leftfirstlineblob, leftothersblob)
    sys.exit()
    # print(commandstack) # for debugging
# main() # for debugging
if __name__ == "engraver":
    main()