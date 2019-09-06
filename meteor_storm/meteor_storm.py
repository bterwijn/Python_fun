# testing tkinter, for docs see: 
#   https://tkdocs.com/tutorial/index.html
#   http://effbot.org/tkinterbook/canvas.htm
#
import tkinter as tk
import random

# globals
root = tk.Tk()
root.title("Meteor Storm")  
canvas_width=1000
canvas_height=800
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.config(bg="black")
canvas.pack()
canvas.focus_set()
time=0
meteors=[] 
explosions=[]
max_time_explosion=50

def rgb(r,g,b):
  return "#%02x%02x%02x" % (r,g,b)

class Keyboard:

  def __init__(self):
    self.keys={}

  def key_down(self,key):
    self.keys[key]=1;
    
  def key_up(self,key):
    self.keys[key]=0;

  def is_down(self,key):
    if key in self.keys:
      return self.keys[key]==1
    return False
    
class PosRad:

  def __init__(self,x,y,rad):
    self.x=x
    self.y=y
    self.rad=rad

  def add(dx,dy):
    self.x+=dx
    self.y+=dy

  def in_collision(self,p2):
    dx=self.x-p2.x     # difference in x
    dy=self.y-p2.y     # difference in y
    sr=self.rad+p2.rad # sum of radia
    return dx*dx+dy*dy<sr*sr # Pythagoras

class Explosion:

  def __init__(self,x,y):
    self.posrad=PosRad(x,y,200)
    self.time=0

  def time_step(self):
    self.time+=1
    if self.time>max_time_explosion:
      explosions.remove(self)

  def draw(self,canvas):
    for i in range(20):
      length=int(self.posrad.rad*self.time/max_time_explosion)
      x2=random.randint(-length,length)
      y2=random.randint(-length,length)
      color=""
      if random.randint(0,2)==0:
        color="orange"
      else:
        color="red"
      canvas.create_line(self.posrad.x,   self.posrad.y,
                         self.posrad.x+x2,self.posrad.y+y2, fill=color, width=2)
          
class Meteor:

  def __init__(self,x,y):
    self.posrad=PosRad(x,y,10)
    self.speed=random.uniform(1,3)

  def time_step(self):
    self.posrad.x-=self.speed
    if self.posrad.x<0:
      meteors.remove(self)
    
  def draw(self,canvas):
    canvas.create_oval(self.posrad.x-self.posrad.rad, self.posrad.y-self.posrad.rad, \
                       self.posrad.x+self.posrad.rad, self.posrad.y+self.posrad.rad, \
                       fill="red", outline="white")

class Ship:

  def __init__(self,x,y):
    self.posrad=PosRad(x,y,20)
    self.speed=1

  def time_step(self):
    if keyboard.is_down("Left"):
      self.posrad.x-=self.speed
    if keyboard.is_down("Right"):
      self.posrad.x+=self.speed
    if keyboard.is_down("Up"):
      self.posrad.y-=self.speed
    if keyboard.is_down("Down"):
      self.posrad.y+=self.speed
  
  def draw(self,canvas):
    canvas.create_oval(self.posrad.x-self.posrad.rad, self.posrad.y-self.posrad.rad, \
                       self.posrad.x+self.posrad.rad, self.posrad.y+self.posrad.rad, \
                       fill="black", outline="white")

  def collision_detect(self,meteors):
    for i in meteors:
      if self.posrad.in_collision(i.posrad):
        explosions.append(Explosion(i.posrad.x,i.posrad.y))
        meteors.remove(i)


# globals
keyboard=Keyboard()
ship=Ship(canvas_width/2,canvas_height/2)
    
def time_step():
    global time
    canvas.delete("all") # remove all previous drawings
    if random.randint(0,50)==0:
      meteors.append( Meteor(canvas.winfo_width(),random.randint(0,canvas.winfo_height())) )
    ship.time_step()
    ship.draw(canvas)      
    for i in meteors:
      i.time_step()
      i.draw(canvas)
    for i in explosions:
      i.time_step()
      i.draw(canvas)
    ship.collision_detect(meteors)
    time+=1
    root.after(2, time_step)

def key_down(e):
    keyboard.key_down(e.keysym)
    #print('down',e.keysym)
def key_up(e):
    keyboard.key_up(e.keysym)
    #print('up',e.keysym)
    
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
root.after(50, time_step)
root.update()
root.mainloop()
