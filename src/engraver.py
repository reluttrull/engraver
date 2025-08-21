import sys
import os 

def addobjectat(score, x, y, nh):
    score[y] = score[y][:x] + nh + score[y][x+1:]
    return score

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

def main():
    # clef
    treble = ["           ^        ", "|----------%+-------", "|         +:+       ", "|----------+#-------", "|        =@*        ", "|-------%#**--------", "|      ++:##*%)     ", "|------(*:=-:-+-----", "|        -==*:      ", "|--------:=.=-------", "        #*:+        "]
    bass = ["                    ", "--------------------", "     @@@@@@@  @     ", "----@@@@--@@@@@@----", "     @@@@ @@@@@     ", "----------@@@@@@----", "         @@@        ", "-------@@@----------", "    @@@             ", "--------------------", "                    "]
    clefwidth = len(treble[0])
    myclef = None
    while myclef == None:     
        clef = input("Which clef? (treble or bass, q to quit): ")
        if clef == "treble":
            myclef = treble
        elif clef == "bass":
            myclef = bass
        elif clef == "q":
            sys.exit()

    # time signature
    threefour = ["    XXXX    ", "--------X---", "     XXX    ", "--------X---", "    XXXX    ", "------------", "        X   ", "------X-X---", "    XXXXXX  ", "--------X---", "        X   "]
    fourfour = ["        X   ", "------X-X---", "    XXXXXX  ", "--------X---", "        X   ", "------------", "        X   ", "------X-X---", "    XXXXXX  ", "--------X---", "        X   "]
    timesigwidth = len(threefour[0])
    mytimesig = None
    while mytimesig == None:
        timesig = input("Which time signature? (4/4 or 3/4, q to quit): ")
        if timesig == "4/4":
            mytimesig = fourfour
        elif timesig == "3/4":
            mytimesig = threefour
        elif timesig == "q":
            sys.exit()
        
    # key signature
    symbols = {
    "s": "♯",
    "f": "♭",
    "n": "♮"
    }
    flatindicestreble = [5, 2, 6, 3, 7, 4, 8]
    flatindicesbass = [7, 4, 8, 5, 2, 6, 3]
    sharpindicestreble = [1, 4, 0, 3, 6, 2, 5]
    sharpindicesbass = [3, 6, 2, 5, 1, 4, 7]
    flatkeys = {
        "F":1,
        "Bb":2,
        "Eb":3,
        "Ab":4,
        "Db":5,
        "Gb":6,
        "Cb":7
    }
    sharpkeys = {
        "G":1,
        "D":2,
        "A":3,
        "E":4,
        "B":5,
        "F#":6,
        "C#":7
    }
    keysigwidth = 0
    while keysigwidth == 0:
        keysig = input("Which key signature? (e.g. Eb, q to quit): ")
        if keysig in flatkeys:
            myflats = (flatindicestreble if clef == "treble" else flatindicesbass)[0:flatkeys[keysig]] 
            keysigwidth = len(myflats) * 3
        elif keysig in sharpkeys:
            mysharps = (sharpindicestreble if clef == "treble" else sharpindicesbass)[0:sharpkeys[keysig]]
            keysigwidth = len(mysharps) * 3
        elif keysig == "q":
            sys.exit()
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
    slotsperbar = int(timesig[0]) * 2 # for now, number of eighth notes per bar
    barwidth = notewidth * slotsperbar
    bars = 0
    while bars == 0:
        barinput = input("How many bars? (e.g. 2, q to quit): ")
        if barinput == "q":
            sys.exit()
        elif barinput.isdigit() and int(barinput) > 0:
            bars = int(barinput)
    outsidespaces = ((" " * (barwidth-1) + " ") * bars) + "\r" 
    spaces = ((" " * (barwidth-1) + "|") * bars) + "\r" 
    lines = (("-" * (barwidth-1) + "|") * bars) + "\r"
    score = [outsidespaces, lines, spaces, lines, spaces, lines, spaces, lines, spaces, lines, outsidespaces]
    score = [a + b + c + d for a, b, c, d in zip(myclef, mytimesig, mykeysig, score)]

    for line in score:
        print(line)
    next = ""
    treblenotes = ["g5", "f5", "e5", "d5", "c5", "b4", "a4", "g4", "f4", "e4", "d4"]
    bassnotes = ["b3", "a3", "g3", "f3", "e3", "d3", "c3", "b2", "a2", "g2", "f2"]
    notebuffer = 2
    xpointer = clefwidth + timesigwidth + keysigwidth + notebuffer
    if clef == "treble":
        notes = treblenotes
    elif clef == "bass":
        notes = bassnotes
    while next != "q" and xpointer < len(score[0]):
        next = input("Add object? (e.g. g4 8n) q to quit: ")
        nextls = next.split()
        spacingmult = 1
        if nextls[0] in notes: # contains note info
            if len(nextls) < 2:
                print("No duration info, try again")
                continue
            if nextls[1] in ["4n", "8n"]:
                notehead = "●"
            elif nextls[1] == "2n":
                notehead = "○"
            elif nextls[1] == "1n":
                notehead = "🞇"
            score = addobjectat(score, xpointer, notes.index(nextls[0]), notehead)
            if nextls[1] in ["8n", "4n", "2n"]:
                score = addstemfornoteat(score, xpointer, notes.index(nextls[0]))
            if nextls[1] == "8n":
                score = addflagfornoteat(score, xpointer, notes.index(nextls[0]))
            spacingmult = 8 // int(nextls[1][0])
            xpointer += notewidth * spacingmult
        elif nextls[0] in symbols:
            if len(nextls) < 2 or nextls[1] not in notes:
                print("accidental needs pitch, try again")
                continue
            else:
                score = addobjectat(score, xpointer-2, notes.index(nextls[1]), symbols[nextls[0]])
        else:
            print("input not valid, double-check and try again")
            continue
    for line in score:
        print(line)
main() # for debugging
if __name__ == "engraver":
    main()