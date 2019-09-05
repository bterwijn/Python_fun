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
    
class Pos:

  def __init__(self,x,y):
    self.x=x
    self.y=y

  def add(dx,dy):
    self.x+=dx
    self.y+=dy

class Meteor:

  def __init__(self,x,y):
    self.pos=Pos(x,y)
    self.radius=10
    self.speed=random.uniform(1,3)

  def time_step(self):
    self.pos.x-=self.speed
    if self.pos.x<0:
      meteors.remove(self)
    
  def draw(self,canvas):
    canvas.create_oval(self.pos.x-self.radius, self.pos.y-self.radius, \
                       self.pos.x+self.radius, self.pos.y+self.radius, \
                       fill="red", outline="white")

class Ship:

  def __init__(self,x,y):
    self.pos=Pos(x,y)
    self.radius=20
    self.speed=1

  def time_step(self):
    if keyboard.is_down("Left"):
      self.pos.x-=self.speed
    if keyboard.is_down("Right"):
      self.pos.x+=self.speed
    if keyboard.is_down("Up"):
      self.pos.y-=self.speed
    if keyboard.is_down("Down"):
      self.pos.y+=self.speed
  
  def draw(self,canvas):
    canvas.create_oval(self.pos.x-self.radius, self.pos.y-self.radius, \
                       self.pos.x+self.radius, self.pos.y+self.radius, \
                       fill="black", outline="white")

# globals
keyboard=Keyboard()
ship=Ship(canvas_width/2,canvas_height/2)
    
def time_step():
    global time
    canvas.delete("all") # remove all previous drawings
    if random.randint(0,50)==0:
      meteors.append( Meteor(canvas.winfo_width(),random.randint(0,canvas.winfo_height())) )
      #print(len(meteors))
    ship.time_step()
    ship.draw(canvas)      
    for i in meteors:
      i.time_step()
      i.draw(canvas)
    time+=1
    root.after(2, time_step)

def key_up(e):
    keyboard.key_up(e.keysym)
    print('up',e.keysym)
def key_down(e):
    keyboard.key_down(e.keysym)
    print('down',e.keysym)
    
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
root.after(50, time_step)
root.update()
root.mainloop()
