

from msvcrt import getch
from colorama import Back, Fore, init
import threading
import random
import cursor
import queue
import time
import sys
import os
    
    
init(autoreset=True)

''' Derived From ansiescapes(Deprecated) '''
def _(s): return s;
ESC = '\u001B['
def cursorTo(x, y = None):

  return _(ESC + str(y + 1) + ';' + str(x + 1) + 'H');

''' ------------------------------------ '''


class Controls:
    def __init__(self):
        self.q = queue.Queue(maxsize=1)
        self.t = threading.Thread(target=self.arrowKeys, args=(self.q,))

    def start(self):
        self.t.start()

    def stop(self):
        self.t.join()

    def get(self):
        if not self.q.empty():
            return self.q.get()
        return b''
    
    def arrowKeys(self, q):
        while 1:
            ch = getch()
            q.put(ch)

class Cursor:
    def __init__(self):
        pass

    def hide(self):
        cursor.hide()

    def show(self):
        cursor.show()

    def draw(self, color, x, y, text=' '):
        print(cursorTo(x, y) + color + text, end = '')

    def goto(self, x, y):
        print(cursorTo(x, y), end = '')

    def clear(self):
        print("\033[2J", end='')

class Enemy:
    def __init__(self, cursor):
        self.cursor = cursor
        self.y = 0
        self.x = random.randint(0, 118)

    def draw(self):
        self.cursor.draw(Back.LIGHTRED_EX, self.x, self.y)
        self.y += random.choice([1, 1,1, 2, 2])
        
class Powerup:
    def __init__(self, cursor):
        self.cursor = cursor
        self.y = 0
        self.x = random.randint(0, 118)
        self.add = random.randint(50, 300)
        self.spent = False
        self.effect = random.choice(["score", "small", "large"])

    def draw(self):
        if self.effect == "score":
            self.cursor.draw(Back.LIGHTBLUE_EX, self.x, self.y)
        elif self.effect == "small":
            self.cursor.draw(Back.LIGHTGREEN_EX, self.x, self.y)
        elif self.effect == "large":
            self.cursor.draw(Back.CYAN, self.x, self.y)
        self.y += 1

class player:
    def __init__(self, cursor, controls):
        self.cursor = cursor
        self.controls = controls

        self.px = 0
        self.py = 12

        self.seffect = False
        self.leffect = False
        self.blinkout = False
        self.startime = 0
        self.score = 0

    def draw(self):
        self.cursor.draw(Back.CYAN, self.px, self.py)
        if not self.seffect or (self.blinkout and self.startime %2 ==1):
            self.cursor.draw(Back.CYAN, self.px+1, self.py)
            self.cursor.draw(Back.CYAN, self.px+2, self.py)
            self.cursor.draw(Back.CYAN, self.px, self.py+1)
            self.cursor.draw(Back.CYAN, self.px+1, self.py+1)
            self.cursor.draw(Back.CYAN, self.px+2, self.py+1)
        if self.leffect:
            if self.blinkout and self.startime %2 == 1:
                self.cursor.draw(Back.CYAN, self.px+3, self.py)
                self.cursor.draw(Back.CYAN, self.px+4, self.py)
                self.cursor.draw(Back.CYAN, self.px+5, self.py)
                self.cursor.draw(Back.CYAN, self.px+3, self.py+1)
                self.cursor.draw(Back.CYAN, self.px+4, self.py+1)
                self.cursor.draw(Back.CYAN, self.px+5, self.py+1)
                self.cursor.draw(Back.CYAN, self.px+1, self.py+2)
                self.cursor.draw(Back.CYAN, self.px+2, self.py+2)
                self.cursor.draw(Back.CYAN, self.px+3, self.py+2)
                self.cursor.draw(Back.CYAN, self.px+4, self.py+2)
                self.cursor.draw(Back.CYAN, self.px+5, self.py+2)
                self.cursor.draw(Back.CYAN, self.px, self.py+2)
            elif self.blinkout:
                pass
            else:
                self.cursor.draw(Back.CYAN, self.px+3, self.py)
                self.cursor.draw(Back.CYAN, self.px+4, self.py)
                self.cursor.draw(Back.CYAN, self.px+5, self.py)
                self.cursor.draw(Back.CYAN, self.px+3, self.py+1)
                self.cursor.draw(Back.CYAN, self.px+4, self.py+1)
                self.cursor.draw(Back.CYAN, self.px+5, self.py+1)
                self.cursor.draw(Back.CYAN, self.px+1, self.py+2)
                self.cursor.draw(Back.CYAN, self.px+2, self.py+2)
                self.cursor.draw(Back.CYAN, self.px+3, self.py+2)
                self.cursor.draw(Back.CYAN, self.px+4, self.py+2)
                self.cursor.draw(Back.CYAN, self.px+5, self.py+2)
                self.cursor.draw(Back.CYAN, self.px, self.py+2)

        if self.leffect or self.seffect:
            self.startime += 1

        if self.startime >= 50:
            self.blinkout = True
        if self.startime == 58:
            self.leffect = False
            self.seffect = False
            self.blinkout = False
            self.startime = 0

        self.score += 1

    def move(self, a):
        self.px += a

    def collide(self, esold, powerups):
        self.esold = esold
        self.powerups = powerups
        b = 0
        for e in self.esold:
            if e.x == self.px or e.x == self.px+1 or e.x == self.px+2:
                if e.y == 12 or e.y == 13:
                    if not self.leffect and not self.seffect:
                        b = 1
                        break
            if e.x == self.px and b == 0:
                if e.y == 12 and self.seffect:
                    b = 1
                    break
        if b:
            return False

        colp = []

        for p in powerups:
            if p.x == self.px or p.x == self.px+1 or p.x == self.px+2:
                if p.y == 12 or p.y == 13:
                    if p.effect == "score":
                        self.score += p.add
                    if p.effect == "small" and not self.leffect:
                        self.seffect = True
                        self.startime = 0
                    if p.effect == "large" and not self.seffect:
                        self.leffect = True
                        self.startime = 0
                    p.spent = True
                    

        return powerups


class dummy:
    def __init__(self):
        self.px = 0
        self.py = 0

class Game:
    def __init__(self):
        self.cursor = Cursor()
        self.controls = Controls()
        self.controls.start()

        self.es = []
        self.esold = []

        self.powerups = []

        
    def run(self, dif, pl2=True):
        self.cursor.clear()
        if dif == "easy":
            self.es = [Enemy(self.cursor) for i in range(5)]
        elif dif == "medium":
            self.es = [Enemy(self.cursor) for i in range(10)]
        elif dif == "hard":
            self.es = [Enemy(self.cursor) for i in range(15)]
        elif dif == "insane":
            self.es = [Enemy(self.cursor) for i in range(20)]
        elif dif == "impossible":
            self.es = [Enemy(self.cursor) for i in range(35)]

        self.esold = []

        self.powerups = []

        if pl2:
            p1 = player(self.cursor, self.controls)
            p2 = player(self.cursor, self.controls)
            p2.px = 115
        else:
            p1 = player(self.cursor, self.controls)
        
        while 1:
            self.cursor.draw(Back.BLACK, 0, 30, text="Score: "+str(p1.score))
            if pl2:
                self.cursor.draw(Back.BLACK, 110, 30, text="Score: "+str(p2.score))

            p1.draw()
            if pl2: p2.draw()
                

            for e in self.es:
                e.draw()

            for e in self.esold:
                e.draw()
                                                                                           
            for p in self.powerups:
                p.draw()

            self.powerups = p1.collide(self.esold, self.powerups)
            if self.powerups is False:
                if pl2:
                    p2.score += 200
                break
            if pl2:
                self.powerups = p2.collide(self.esold, self.powerups)
                if self.powerups is False:
                    p1.score += 200
                    break
         
            self.doEnemies()
            self.doPowerups()
            time.sleep(0.009)
            self.cursor.clear()

            if pl2:
                self.doControls(p1, p2)
            else:
                self.doControls(p1, dummy())

        self.cursor.clear()

        if pl2:
            playagain = self.options2(p1.score, sc2=p2.score)
        else:
            playagain = self.options2(p1.score)
        if playagain == "e":
            self.cursor.clear()
            return
        elif playagain == "pa":
            self.cursor.clear()
            dif, c = self.options()
            return self.run(dif, c)

    def doEnemies(self):
        howmany = 0
        d = []
        d2 = []
        for e in self.es:
            if e.y >= 18:
                d.append(e)
            if e.y >= 8:
                howmany += 1
                self.esold.append(e)
                d.append(e)
                
        for e in self.esold:
            if e.y >= 18:
                d2.append(e)

        for i in d2:
            self.esold.remove(i)

        for i in d:
            self.es.remove(i)

        for i in range(howmany):
            self.es.append(Enemy(self.cursor))

    def doPowerups(self):
        d = []
        for p in self.powerups:
            if p.spent == True:
                d.append(p)
            if p.y >= 18:
                d.append(p)

        for i in d:
            self.powerups.remove(i)

        if not random.randint(0, 9):
            self.powerups.append(Powerup(self.cursor))
            

    def doControls(self, p1, p2):
        ch = self.controls.get()

        a = b'a'
        d = b'd'
        
        if ch == a:
            p1.px -= 1
        if ch == d:
            p1.px += 1
        if ch == b'j':
            p2.px -= 1
        if ch == b'l':
            p2.px += 1

        width = 3

        if p1.px < 0:
            p1.px = 0
        if p1.px > 118-width:
            p1.px = 118-width
        if p2.px < 0:
            p2.px = 0
        if p2.px > 118-width:
            p2.px = 118-width

    def options(self):
        curchoice = 0
        a = ''
        a2 = ''
        b = ''
        b2 = ''
        c = ''
        c2 = ''
        d = ''
        d2 = ''
        e = ''
        e2 = ''
        f = ''
        f2 = ''
        g = ''
        g2 = ''
        h = ''
        h2 = ''
        choice = 0
        choice2 = 5
        while 1:
            if curchoice == 0 or choice == 0:
                a = Back.LIGHTGREEN_EX
                a2 = Fore.BLACK
            else:
                a = ''
                a2 = Fore.LIGHTGREEN_EX
            if curchoice == 1 or choice == 1:
                b = Back.GREEN
                b2 = Fore.BLACK
            else:
                b = ''
                b2 = Fore.GREEN
            if curchoice == 2 or choice == 2:
                c = Back.WHITE
                c2 = Fore.BLACK
            else:
                c = ''
                c2 = Fore.WHITE
            if curchoice == 3 or choice == 3:
                d = Back.RED
                d2 = Fore.BLACK
            else:
                d = ''
                d2 = Fore.RED
            if curchoice == 4 or choice == 4:
                e = Back.LIGHTRED_EX
                e2 = Fore.BLACK
            else:
                e = ''
                e2 = Fore.LIGHTRED_EX
            if curchoice == 5 or choice2 == 5:
                f = Back.CYAN
                f2 = Fore.BLACK
            else:
                f = ''
                f2 = Fore.CYAN
            if curchoice == 6 or choice2 == 6:
                g = Back.BLUE
                g2 = Fore.BLACK
            else:
                g = ''
                g2 = Fore.BLUE
            if curchoice == 7:
                h = Back.WHITE
                h2 = Fore.BLACK
            else:
                h = ''
                h2 = Fore.WHITE
                
            self.cursor.draw(a+a2, 1, 1, text="EASY")
            self.cursor.draw(b+b2, 1, 2, text="MEDIUM")
            self.cursor.draw(c+c2, 1, 3, text="HARD")
            self.cursor.draw(d+d2, 1, 4, text="INSANE")
            self.cursor.draw(e+e2, 1, 5, text="IMPOSSIBLE")
            self.cursor.draw(f+f2, 1, 7, text="1 Player")
            self.cursor.draw(g+g2, 1, 8, text="2 Player")
            self.cursor.draw(h+h2, 1, 10, text="play")
            time.sleep(0.009)
            self.cursor.clear()

            ch = self.controls.get()
            if ch == b'w':
                curchoice -= 1
            if ch == b's':
                curchoice += 1

            if ch == b'e':
                if curchoice <= 4:
                    choice = curchoice
                if curchoice <= 6 and curchoice > 4:
                    choice2 = curchoice
                if curchoice == 7:
                    dif = ["easy", "medium", "hard", "insane", "impossible"][choice]
                    if choice2 == 5:
                        c = False
                    else:
                        c = True
                    return dif, c

            if curchoice < 0:
                curchoice = 0
            if curchoice > 7:
                curchoice = 7

    def options2(self, score, sc2=None):
        curchoice = 0
        a = ''
        a2 = ''
        b = ''
        b2 = ''
        while 1:
            if curchoice == 0:
                a = Back.LIGHTGREEN_EX
                a2 = Fore.BLACK
            else:
                a = ''
                a2 = Fore.LIGHTGREEN_EX
            if curchoice == 1:
                b = Back.LIGHTRED_EX
                b2 = Fore.BLACK
            else:
                b = ''
                b2 = Fore.LIGHTRED_EX

            if sc2 == None:
                print("===================")
                print("YOU LOST!!!")
                print("FINAL SCORE: "+str(score))
                print("===================")
            else:
                print("======================")
                if sc2 >score:
                    print("Player 2 won!")
                else:
                    print("Player 1 won!")

                print("Player 1's final score:", score)
                print("Player 2's final score:", sc2)
                print("======================")

            self.cursor.draw(a+a2, 1, 6, text="Menu")
            self.cursor.draw(b+b2, 1, 7, text="Exit")
            time.sleep(0.009)
            self.cursor.clear()

            ch = self.controls.get()
            if ch == b'w':
                curchoice -= 1
            if ch == b's':
                curchoice += 1

            if ch == b'e':
                if curchoice == 0:
                    return "pa"
                if curchoice == 1:
                    return "e"


            if curchoice < 0:
                curchoice = 0
            if curchoice > 4:
                curchoice = 4
'''
class playerChoice:
    def __init__(self, d="/playerdata"):
        self.dir = d
        self.cursor = Cursor()
        self.controls = Controls()

    def newplayer(

    def getplayer(self):
        pass'''
        

game = Game()
dif, c = game.options()
game.run(dif, c)



















