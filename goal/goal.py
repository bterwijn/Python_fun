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
brake_factor=0.97
players=[]
balls=[]
bullets=[]

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

class Speed:

  def __init__(self,vx,vy):
    self.x=vx
    self.y=vy

  def add_polar(self,angle,size):
    self.x+=math.cos(angle)*size
    self.y+=math.sin(angle)*size

  def air_resits(self):
    self.x*=air_resistance
    self.y*=air_resistance
    
  def multipy(self,m):
    self.x*=m
    self.y*=m
  
def speed_swap(obj1,obj2):
  temp=obj1.speed
  obj1.speed=obj2.speed
  obj2.speed=temp
  rad_ratio=obj2.posrad.rad/obj1.posrad.rad
  obj1.speed.multipy(rad_ratio)
  obj2.speed.multipy(1/rad_ratio)
  
class PosRad:

  def __init__(self,x,y,rad):
    self.x=x
    self.y=y
    self.rad=rad

  def move(self,speed,direction=1):
    self.x+=speed.x*direction
    self.y+=speed.y*direction
  
def is_in_vertical_border_collision(obj):
  return obj.posrad.x<0 or obj.posrad.x>canvas.winfo_width()
    
def is_in_horizontal_border_collision(obj):
  return obj.posrad.y<0 or obj.posrad.y>canvas.winfo_height()

def square_distance(obj1,obj2):
  dx=obj1.posrad.x - obj2.posrad.x   # difference in x
  dy=obj1.posrad.y - obj2.posrad.y   # difference in y
  return dx*dx+dy*dy                 # Pythagoras
    
def is_in_collision(obj1,obj2):
  sr=obj1.posrad.rad + obj2.posrad.rad    # sum of radia
  return square_distance(obj1,obj2)<sr*sr # collision when distance is smaller than sum radia

def collide_border(obj1):
  pass
  #if obj1.__class__.__name__=="Bullet":
  #  dynamic_objs.remove(obj1)

def collide_dynamic(obj1,obj2):
  if obj1.__class__.__name__=="Bullet":
    #if obj1 in bullets:
    bullets.remove(obj1)
  if obj2.__class__.__name__=="Bullet":
    #if obj2 in bullets:
    bullets.remove(obj2)
    
def check_and_handle_border_collisions(obj):
  if is_in_horizontal_border_collision(obj):
    obj.posrad.move(obj.speed,-1)
    obj.speed.y*=-1;
    collide_border(obj)
  if is_in_vertical_border_collision(obj):
    obj.posrad.move(obj.speed,-1)
    obj.speed.x*=-1;
    collide_border(obj)
    
def check_and_handle_dynamic_collisions(obj1,obj_lists):
  for obj_list in obj_lists:
    for obj2 in obj_list:
      if obj1!=obj2 and is_in_collision(obj1,obj2):
        obj1.posrad.move(obj1.speed,-1)
        speed_swap(obj1,obj2)
        collide_dynamic(obj1,obj2)

def check_and_handle_collisions(obj1,obj_lists):
  check_and_handle_border_collisions(obj1)
  check_and_handle_dynamic_collisions(obj1,obj_lists)

class Player:
  init_size=20
  pointer_length=1.8
  steer_speed=0.05
  forward_speed=0.20
  shoot_time=20
  bullet_speed=8
  
  def __init__(self,x,y,a,color):
    self.posrad=PosRad(x,y,Player.init_size)
    self.speed=Speed(0,0)
    self.angle=a
    self.color=color
    self.last_shoot_time=0
    
  def steer(self,direction):
    self.angle+=direction*Player.steer_speed

  def add_speed(self,size):
    self.speed.add_polar(self.angle,size)
    
  def time_step(self):
    self.speed.air_resits()
    self.posrad.move(self.speed)
    check_and_handle_collisions(self,[players,balls,bullets])

  def shoot(self):
    if time>self.last_shoot_time+Player.shoot_time:
      self.last_shoot_time=time
      bx=math.cos(self.angle)
      by=math.sin(self.angle)
      length=self.posrad.rad * Player.pointer_length
      bullet=Bullet(self.posrad.x+bx*length, \
                                 self.posrad.y+by*length, \
                                 self.speed.x+bx*Player.bullet_speed, \
                                 self.speed.y+by*Player.bullet_speed, \
                                 self.color)
      bullets.append(bullet)
      check_and_handle_collisions(bullet,[players,balls])
    
  def draw(self):
    canvas.create_oval(self.posrad.x-self.posrad.rad, self.posrad.y-self.posrad.rad, \
                       self.posrad.x+self.posrad.rad, self.posrad.y+self.posrad.rad, \
                       fill=None, outline=self.color, width=4)
    length=self.posrad.rad * Player.pointer_length
    canvas.create_line(self.posrad.x,                           self.posrad.y,                           \
                       self.posrad.x + math.cos(self.angle)*length, self.posrad.y + math.sin(self.angle)*length, \
                       fill=self.color, width=4)
class Ball:
  size=10

  def __init__(self,x,y):
    self.posrad=PosRad(x,y,Ball.size)
    self.speed=Speed(0,0)

  def time_step(self):
    self.speed.air_resits()
    self.posrad.move(self.speed)
    check_and_handle_collisions(self,[players,balls,bullets])
    
  def draw(self):
    canvas.create_oval(self.posrad.x-self.posrad.rad, self.posrad.y-self.posrad.rad, \
                       self.posrad.x+self.posrad.rad, self.posrad.y+self.posrad.rad, \
                       fill=None, outline="white", width=4)
class Bullet:
  size=4
  life_time=200
  
  def __init__(self,x,y,vx,vy,color):
    self.posrad=PosRad(x,y,Bullet.size)
    self.speed=Speed(vx,vy)
    self.color=color
    self.time=0

  def time_step(self):
    self.time+=1
    if self.time>Bullet.life_time:
      bullets.remove(self)
    else:
      self.posrad.move(self.speed)
      check_and_handle_collisions(self,[players,balls])
    
  def draw(self):
    canvas.create_oval(self.posrad.x-self.posrad.rad, self.posrad.y-self.posrad.rad, \
                       self.posrad.x+self.posrad.rad, self.posrad.y+self.posrad.rad, \
                       fill=None, outline=self.color, width=4)
  
# globals
keyboard=Keyboard()
player1=Player(canvas_width*1/3,canvas_height/2,0      ,"blue")
player2=Player(canvas_width*2/3,canvas_height/2,math.pi,"green")
players.append(player1)
players.append(player2)

for i in range(10):
  x=random.randint(0,canvas_width)
  y=random.randint(0,canvas_width)
  balls.append(Ball(x,y))

def handle_keyboard_state():
  if keyboard.is_down("z"):
    player1.steer(-1)
  if keyboard.is_down("x"):
    player1.steer(+1)
  if keyboard.is_down("f"):
    player1.add_speed(Player.forward_speed)
  if keyboard.is_down("c"):
    player1.speed.multipy(brake_factor)
  if keyboard.is_down("g"):
    player1.shoot()
  if keyboard.is_down("comma"):
    player2.steer(-1)
  if keyboard.is_down("period"):
    player2.steer(+1)
  if keyboard.is_down("apostrophe"):
    player2.add_speed(Player.forward_speed)
  if keyboard.is_down("slash"):
    player2.speed.multipy(brake_factor)
  if keyboard.is_down("Return"):
    player2.shoot()
    
def time_step():
    global time
    canvas.delete("all") # remove all previous drawings
    handle_keyboard_state()
    for obj_list in [players,balls,bullets]:
      for obj in obj_list:
        obj.time_step()
        obj.draw()
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
