# Goal game
import tkinter as tk
import random
import math

# globals
root = tk.Tk()
root.title("Goal")  
canvas_width=1000
canvas_height=800
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.config(bg="black")
canvas.pack()
canvas.focus_set()
time=0
air_resistance=0.98
balls=[]
players=[]

class Keyboard:

  def __init__(self):
    self.keys={}

  def key_down(self,key):
    self.keys[key]=True;
    
  def key_up(self,key):
    self.keys[key]=False;

  def is_down(self,key):
    if key in self.keys:
      return self.keys[key]
    return False
    
class PosRadSpeed:

  def __init__(self,x,y,rad,vx,vy):
    self.x=x
    self.y=y
    self.rad=rad
    self.vx=vx
    self.vy=vy

  def move(self,direct=1):
    self.x+=self.vx*direct
    self.y+=self.vy*direct

  def air_resits(self):
    self.vx*=air_resistance
    self.vy*=air_resistance
    
  def bounce_border(self):
    if self.x<0:
      self.x=0
      self.vx*=-1
    if self.y<0:
      self.y=0
      self.vy*=-1
    if self.x>canvas.winfo_width():
      self.x=canvas.winfo_width()
      self.vx*=-1
    if self.y>canvas.winfo_height():
      self.y=canvas.winfo_height()
      self.vy*=-1
      
  def is_in_collision(self,p2):
    dx=self.x-p2.x     # difference in x
    dy=self.y-p2.y     # difference in y
    sr=self.rad+p2.rad # sum of radia
    return dx*dx+dy*dy<sr*sr # Pythagoras

  def swap_speed(self,p2):
    temp=self.vx
    self.vx=p2.vx
    p2.vx=temp
    temp=self.vy
    self.vy=p2.vy
    p2.vy=temp
    
  def handle_collision(self,p2):
    self.move(-1)
    p2.move(-1)
    self.swap_speed(p2)
      
  def check_and_handle_collision(self,p2):
    if self.is_in_collision(p2):
      self.handle_collision(p2)

def collision_detect(obj):
    for i in players:
      if i!=obj:
        obj.prs.check_and_handle_collision(i.prs)
    for i in balls:
      if i!=obj:
        obj.prs.check_and_handle_collision(i.prs)
      
# class Explosion:
#   size=200
#   max_time_explosion=20
#   nr_lines=20
  
#   def __init__(self,x,y):
#     self.posrad=PosRadSpeed(x,y,Explosion.size)
#     self.time=0

#   def time_step(self):
#     self.time+=1
#     if self.time>Explosion.max_time_explosion:
#       explosions.remove(self)

#   def draw(self,canvas):
#     for i in range(Explosion.nr_lines):
#       length=int(self.posrad.rad*self.time/Explosion.max_time_explosion)
#       x2=random.randint(-length,length)
#       y2=random.randint(-length,length)
#       color=""
#       if random.randint(0,2)==0:
#         color="orange"
#       else:
#         color="red"
#       canvas.create_line(self.posrad.x,   self.posrad.y,
#                          self.posrad.x+x2,self.posrad.y+y2, fill=color, width=2)

class Ball:
  size=10

  def __init__(self,x,y):
    self.prs=PosRadSpeed(x,y,Ball.size,0,0)

  def time_step(self):
    self.prs.air_resits()
    self.prs.move()
    self.prs.bounce_border()
    collision_detect(self)
    
  def draw(self):
    canvas.create_oval(self.prs.x-self.prs.rad, self.prs.y-self.prs.rad, \
                       self.prs.x+self.prs.rad, self.prs.y+self.prs.rad, \
                       fill=None, outline="white", width=4)
class Player:
  init_size=20
  pointer_length=1.8
  steer_speed=0.05
  forward_speed=0.17
  backward_speed=0.09
  
  def __init__(self,x,y,a,color):
    self.prs=PosRadSpeed(x,y,Player.init_size,0,0)
    self.a=a
    self.color=color
    
  def steer(self,direction):
    self.a+=direction*Player.steer_speed

  def add_speed(self,s):
    self.prs.vx+=math.cos(self.a)*s
    self.prs.vy+=math.sin(self.a)*s
    
  def time_step(self):
    self.prs.air_resits()
    self.prs.move()
    self.prs.bounce_border()
    collision_detect(self)
      
  def draw(self):
    canvas.create_oval(self.prs.x-self.prs.rad, self.prs.y-self.prs.rad, \
                       self.prs.x+self.prs.rad, self.prs.y+self.prs.rad, \
                       fill=None, outline=self.color, width=4)
    length=self.prs.rad * Player.pointer_length
    canvas.create_line(self.prs.x,                           self.prs.y,                           \
                       self.prs.x + math.cos(self.a)*length, self.prs.y + math.sin(self.a)*length, \
                       fill=self.color, width=4)
      
# globals
keyboard=Keyboard()
players.append(Player(canvas_width*1/3,canvas_height/2,0      ,"blue"))
players.append(Player(canvas_width*2/3,canvas_height/2,math.pi,"green"))

for i in range(10):
  x=random.randint(0,canvas_width)
  y=random.randint(0,canvas_width)
  balls.append(Ball(x,y))

def handle_keyboard_state():
  if keyboard.is_down("z"):
    players[0].steer(-1)
  if keyboard.is_down("x"):
    players[0].steer(+1)
  if keyboard.is_down("f"):
    players[0].add_speed(Player.forward_speed)
  if keyboard.is_down("c"):
    players[0].add_speed(-Player.backward_speed)
  if keyboard.is_down("comma"):
    players[1].steer(-1)
  if keyboard.is_down("period"):
    players[1].steer(+1)
  if keyboard.is_down("apostrophe"):
    players[1].add_speed(Player.forward_speed)
  if keyboard.is_down("slash"):
    players[1].add_speed(-Player.backward_speed)

def time_step():
    global time
    canvas.delete("all") # remove all previous drawings
    handle_keyboard_state()
    for i in players:
      i.time_step()
      i.draw()
    for i in balls:
      i.time_step()
      i.draw()
    time+=1
    root.after(10, time_step)

def key_down(e):
    keyboard.key_down(e.keysym)
    #print('down:',e.keysym)
def key_up(e):
    keyboard.key_up(e.keysym)
    #print('up:',e.keysym)
    
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
root.after(100, time_step)
root.update()
root.mainloop()
