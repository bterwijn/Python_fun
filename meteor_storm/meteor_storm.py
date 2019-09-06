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
air_resistance=0.995

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
    min_speed=1
    max_speed=3
    self.speed=random.uniform(min_speed,max_speed)
    r=(self.speed-min_speed)/(max_speed-min_speed)
    self.posrad=PosRad(x,y,6+10-r*10)

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
    self.speed=0.02
    self.vx=0
    self.vy=0

  def time_step(self):
    if keyboard.is_down("Left"):
      self.vx-=self.speed
      canvas.create_line(self.posrad.x+self.posrad.rad   , self.posrad.y,
                         self.posrad.x+self.posrad.rad+20, self.posrad.y, fill="red", width=10)
    if keyboard.is_down("Right"):
      self.vx+=self.speed
      canvas.create_line(self.posrad.x-self.posrad.rad   , self.posrad.y,
                         self.posrad.x-self.posrad.rad-20, self.posrad.y, fill="red", width=10)
    if keyboard.is_down("Up"):
      self.vy-=self.speed
      canvas.create_line(self.posrad.x , self.posrad.y+self.posrad.rad,
                         self.posrad.x , self.posrad.y+self.posrad.rad+20, fill="red", width=10)
    if keyboard.is_down("Down"):
      self.vy+=self.speed
      canvas.create_line(self.posrad.x , self.posrad.y-self.posrad.rad,
                         self.posrad.x , self.posrad.y-self.posrad.rad-20, fill="red", width=10)
    self.vx-=0.01 # wind
    self.posrad.x+=self.vx
    self.posrad.y+=self.vy
    self.vx*=air_resistance
    self.vy*=air_resistance
    if self.posrad.x<0:
      self.posrad.x=0
      self.vx*=-1
    if self.posrad.y<0:
      self.posrad.y=0
      self.vy*=-1
    if self.posrad.x>canvas.winfo_width():
      self.posrad.x=canvas.winfo_width()
      self.vx*=-1
    if self.posrad.y>canvas.winfo_width()-self.posrad.rad*10:
      self.posrad.y=canvas.winfo_width()-self.posrad.rad*10
      self.vy*=-1
  
  def draw(self,canvas):
    canvas.create_oval(self.posrad.x-self.posrad.rad, self.posrad.y-self.posrad.rad, \
                       self.posrad.x+self.posrad.rad, self.posrad.y+self.posrad.rad, \
                       fill="black", outline="white")

  def collision_detect(self,meteors):
    for i in meteors:
      if self.posrad.in_collision(i.posrad):
        explosions.append(Explosion(i.posrad.x,i.posrad.y))
        meteors.remove(i)
        self.vx-=3

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
