# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 18:14:31 2020

@author: keyvan
"""
import tkinter as tk
from math import sin, cos, radians, exp, sqrt
from random import randint

class Main(tk.Frame):
    def __init__(self, fenetre, **kwargs):
        tk.Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill=tk.BOTH, expand=True)
        self.sim = Simulation(self)
        

class Simulation(tk.Canvas):
    def __init__(self,parent):
        
        self.canvasSizeX = 800
        self.sizeX = self.canvasSizeX*2
        self.transX = int(self.canvasSizeX)/2
        
        self.canvasSizeY = 480
        self.sizeY = self.canvasSizeY*2
        self.transY = int(self.canvasSizeY)/2
        
        self.parent = parent
        
        super().__init__(
            parent,background="#00008c",height=self.canvasSizeY,width=self.canvasSizeX)
        self.pack(fill=tk.BOTH, side="left", expand=True)
    
        self.config(cursor="none")
    
        self.windsNumber = 20**2
        self.winds = [Wind(1/sqrt(self.windsNumber)*i+10,int(45 /self.windsNumber*i)) for i in range(self.windsNumber)]
        
        self.x0 = self.canvasSizeX*1/2+self.transX 
        self.y0 = self.canvasSizeY*3/4+self.transY
        self.boat = Boat(self.x0,self.y0, 0)
        
        self.bouees = [Bouee(500,540),Bouee(1100,340)]
        
        self.tag_bind("oright","<ButtonPress-1>", lambda event : self.boat.rotate(True))
        self.tag_bind("oleft","<ButtonPress-1>", lambda event : self.boat.rotate(False))
        
        self.tag_bind("sright","<ButtonPress-1>", lambda event : self.boat.trim(True))
        self.tag_bind("sleft","<ButtonPress-1>", lambda event : self.boat.trim(False))
        
        self.tag_bind("close","<Button-1>",close)
        
        self.bind("<ButtonPress-1>",self.onPress)
        self.bind("<Motion>",self.onMove)
        self.bind("<ButtonRelease-1>", self.onRelease)      
        
        self.isMoving = False
    
        self.drawSim()
        

        
    def onPress(self, event):
        self.initalTrans = (self.transX,self.transY)
        self.initialMove = (event.x,event.y)
        self.isMoving = True
        return
    
    def onMove(self, event):
        self.move = (event.x,event.y)
        return
    
    def onRelease(self, event):
        self.isMoving = False
        self.boat.stopAll(event)
        
    def drawSim(self):
        self.update()
                
        self.canvasSizeX = self.winfo_width()
        self.canvasSizeY = self.winfo_height()
        
        for bouee in self.bouees:
            bouee.draw(self)
        
        if self.isMoving:
            newTx = self.initalTrans[0] + (self.initialMove[0]-self.move[0])
            newTy = self.initalTrans[1] + (self.initialMove[1]-self.move[1])
            self.transX = newTx if newTx <= self.sizeX-self.canvasSizeX and newTx >= 0 else self.transX
            self.transY = newTy if newTy <= self.sizeY-self.canvasSizeY and newTy >= 0 else self.transY
        
        
        self.boat.draw(self)
        try :
            self.boat.move(self.winds[int(self.boat.x/self.sizeX*sqrt(self.windsNumber)) + int(self.boat.y/self.sizeY*sqrt(self.windsNumber))*int(sqrt(self.windsNumber))])
        except:
            self.boat.move(self.winds[int(self.boat.x/self.sizeX*sqrt(self.windsNumber)) + int(self.boat.y/self.sizeY*sqrt(self.windsNumber))*int(sqrt(self.windsNumber))])
        
        x1 = -60
        y1 = -60
        s = 30
        l = 25
        
        try :
            self.delete(self.t)
        except AttributeError:
            pass
        self.t = self.create_text(self.canvasSizeX+x1-4,self.canvasSizeY+y1-15,text=str(self.boat.wO)+"°",anchor=tk.CENTER,fill="white",font=('Times', '12'))

        
        #orientation
        self.delete("oright")
        self.delete("oleft")
        self.create_polygon(self.canvasSizeX+x1,self.canvasSizeY+y1,self.canvasSizeX+x1,self.canvasSizeY+y1+s,self.canvasSizeX+x1+l,self.canvasSizeY+y1+s/2,fill="white",tags="oright")    
        x2 = x1-10
        y2 = y1
        self.create_polygon(self.canvasSizeX+x2,self.canvasSizeY+y2,self.canvasSizeX+x2,self.canvasSizeY+y2+s,self.canvasSizeX+x2-l,self.canvasSizeY+y2+s/2,fill="white",tags="oleft")

        
        #sail
        x3 = -x1
        y3 = y1
        self.delete("sleft")
        self.delete("sright")
        self.create_polygon(x3,self.canvasSizeY+y3,x3,self.canvasSizeY+y3+s,x3-l,self.canvasSizeY+y3+s/2,fill="white",tags="sleft")    
        x4 = x3+10
        y4 = y3
        self.create_polygon(x4,self.canvasSizeY+y4,x4,self.canvasSizeY+y4+s,x4+l,self.canvasSizeY+y4+s/2,fill="white",tags="sright")
        
        
        self.delete("close")
        self.create_line(self.canvasSizeX-20, 10, self.canvasSizeX-10,20,width=2,tags="close",fill="white")
        self.create_line(self.canvasSizeX-10, 10, self.canvasSizeX-20,20,width=2,tags="close",fill="white")

        
                
        for i,wind in enumerate(self.winds):
            wind.draw(self,self.sizeX/sqrt(self.windsNumber)*(i%sqrt(self.windsNumber))+wind.rx,self.sizeY/sqrt(self.windsNumber)*(i-i%sqrt(self.windsNumber))/sqrt(self.windsNumber)+wind.ry,self.sizeX/sqrt(self.windsNumber)+wind.rx,self.sizeY/sqrt(self.windsNumber)+wind.ry)
        
        
        self.after(40,self.drawSim)
        
    
    

class Wind():
    def __init__(self, _force, _orientation):
        self.force = _force
        self.orientation = _orientation
        self.l = self.force
        self.d = 0
        self.rx = randint(-5, 5)
        self.ry = randint(-5, 5)
        self.t = randint(10,50)
        self.s = 0
        
    def draw(self, canvas,x,y,sx,sy):
        canvas.delete(self.d)
        
        xD1 = x+sx/2+self.s*sin(radians(self.orientation)) - canvas.transX
        yD1 = y+sy/2+self.s*cos(radians(self.orientation)) - canvas.transY
        
        xD2 = x+sx/2+(self.s+self.l)*sin(radians(self.orientation)) - canvas.transX
        yD2 = y+sy/2+(self.s+self.l)*cos(radians(self.orientation)) - canvas.transY
        
        if (xD1 >= 0 or xD2 >= 0) and (xD1 <= canvas.canvasSizeX or xD2 <= canvas.canvasSizeX) and (yD1 >= 0 or yD2 >= 0) and (yD1 <= canvas.canvasSizeY or yD2 <= canvas.canvasSizeY):
            if self.s <= self.t:
                self.d = canvas.create_line(xD1,yD1,xD2,yD2,fill="white")
            elif self.s < self.t+30:
                a = int(-255/30*(self.s-self.t)+255)
                b = int(-255/30*(self.s-self.t)+255)
                c = 139
                c = '#%02x%02x%02x' % (a, b, c)                
                self.d = canvas.create_line(xD1,yD1,xD2,yD2,fill=c)
        self.s += 1/10*self.force
        if self.s >= self.t+25:
            self.s = 0
            self.t = randint(50,200)
        
class Boat():
    def __init__(self, _posx, _posy, _orientation):
        self.x = _posx
        self.y = _posy
        self.o = _orientation
        self.reglage = 20
        self.sail = self.reglage
        self.coef = 0.08
        self.ds = 0
        self.db = 0
        self.rotating = False
        self.rotatingRight = False
        self.trimming = False
        self.trimmingRight = False
        
    def getCoef(self,o,s):
        return self.getSailCoef(o-s)*exp(-0.5*self.getSailCoef(o-s)*((1/60)*o-2)**2)/5
    
    def getSailCoef(self,s):
        return exp(-0.5*((1/20)*s-1)**2)
        
    def draw(self, canvas):
        l = 25
        canvas.update()
        canvas.delete(self.ds)
        canvas.delete(self.db)

        xD = self.x - canvas.transX
        yD= self.y - canvas.transY

        self.db = canvas.create_line(xD,yD,xD-l*sin(radians(self.o)),yD-l*cos(radians(self.o)),width=5,fill="white")
        self.ds = canvas.create_line(xD-(l-5)*sin(radians(self.o)),yD-(l-5)*cos(radians(self.o)),xD-(l-5)*sin(radians(self.o))+(l-5)*sin(radians(self.o+self.sail)),yD-(l-5)*cos(radians(self.o))+(l-5)*cos(radians(self.o+self.sail)),width=3,fill="red")
    
    def move(self, wind):
        self.wO = (self.o-wind.orientation)%360

        if self.wO < 180:
            self.sail = -self.reglage
            self.coef = self.getCoef(self.wO,abs(self.sail))
        else:
            self.sail = self.reglage
            self.coef = self.getCoef(360-self.wO,abs(self.sail))
       
        if self.rotating:
            if self.rotatingRight:
                self.o -= 2
            else:
                self.o += 2
            self.o = self.o%360
            
        if self.trimming:
            if self.trimmingRight and self.reglage >= 5 and self.reglage <= 115 :
                self.reglage += 5 if self.reglage == self.sail else -5
            elif self.reglage <= 115 and not self.trimmingRight and self.reglage >= 5:
                self.reglage += -5 if self.reglage == self.sail else 5
            if self.reglage == 0:
                self.reglage = 5
            elif self.reglage == 120:
                self.reglage = 115
        
        self.x -= wind.force * sin(radians(self.o)) * self.coef
        self.y -= wind.force * cos(radians(self.o)) * self.coef
        
    def rotate(self, _right):
        self.rotating = True
        self.rotatingRight = _right
        
    def stopAll(self,event):
        self.rotating = False
        self.trimming = False
    
    def trim(self, _right):
        self.trimming = True
        self.trimmingRight = _right
            
        
class Bouee():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.s = 5
        self.d = 0
        
    def draw(self, canvas):
        canvas.delete(self.d)
        self.d = canvas.create_oval(self.x - self.s - canvas.transX, self.y-self.s - canvas.transY, self.x+self.s - canvas.transX, self.y+self.s - canvas.transY, fill="yellow", outline="yellow")
        
def close(event):
    root.destroy()
    print("Closed")
root = tk.Tk()
#root.wm_attributes('-fullscreen','true')
main = Main(root)
main.mainloop()