# Goal game
import tkinter
import random
import math

print("Two player game, bump balls in your goal to score. Keys:")
print(" player 1: 'z'        turn left")
print("         : 'x'        turn right")
print("         : 'f'        move forward")
print("         : 'x'        brake")
print("         : 'f'        shoot")
print(" player 2: 'm'        turn left")
print("         : ','        turn right")
print("         : ';'        move forward")
print("         : '.'        brake")
print("         : '''        shoot")
print("Some keyboards can't handle many simultaneous keystrokes.")
print("Search 'keyboard rollover' for details.")

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

class Globals:
  root = tkinter.Tk()
  root.title("Goal")  
  canvas_width=1000
  canvas_height=800
  canvas = tkinter.Canvas(root, width=canvas_width, height=canvas_height)
  canvas.config(bg="black")
  canvas.pack()
  canvas.focus_set()
  time=0
  players=[]
  balls=[]
  bullets=[]
  goals=[]
  keyboard=Keyboard()

def polar_to_cartesian(angle, distance):
  cx = math.cos(angle) * distance
  cy = math.sin(angle) * distance
  return cx,cy
  
class Speed:
  air_resistance=0.98
  
  def __init__(self,vx,vy):
    self.x=vx
    self.y=vy

  def add_polar(self,angle,size):
    cx,cy=polar_to_cartesian(angle,size)
    self.x+=cx
    self.y+=cy

  def air_resits(self):
    self.x*=Speed.air_resistance
    self.y*=Speed.air_resistance

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
  return obj.posrad.x<0 or obj.posrad.x>Globals.canvas.winfo_width()

def is_in_horizontal_border_collision(obj):
  return obj.posrad.y<0 or obj.posrad.y>Globals.canvas.winfo_height()

def is_in_collision(obj1,obj2):
  dx=obj1.posrad.x   - obj2.posrad.x    # difference in x
  dy=obj1.posrad.y   - obj2.posrad.y    # difference in y
  sr=obj1.posrad.rad + obj2.posrad.rad  # sum of radia
  return dx*dx+dy*dy<sr*sr              # collision when distance is smaller than sum radia

def check_object_collisions(obj1,obj_lists):
  for obj_list in obj_lists:
    for obj2 in obj_list:
      if obj1!=obj2 and is_in_collision(obj1,obj2):
        return (obj1,obj2)
  return (None,None)

def check_border_collisions(obj):
  if is_in_horizontal_border_collision(obj):
    return (obj,"Horizontal_Border")
  if is_in_vertical_border_collision(obj):
    return (obj,"Vertical_Border")
  return (None,None)

def check_collisions(obj1,obj_lists):
  o1,o2=check_object_collisions(obj1,obj_lists)
  if o1==None:
    o1,o2=check_border_collisions(obj1)
  return (o1,o2)

def is_collision_free(obj1,obj_lists):
  o1,o2=check_collisions(obj1,obj_lists)
  return o1==None

def check_and_handle_collisions(obj1,obj_lists):
  o1,o2=check_collisions(obj1,obj_lists)
  if o1!=None:
    o1.posrad.move(o1.speed,-1)
    if o2=="Horizontal_Border":
      o1.speed.y*=-1;
    elif o2=="Vertical_Border":
      o1.speed.x*=-1;
    else:
      speed_swap(o1,o2)
      if o1.__class__.__name__=="Ball" and \
         o2.__class__.__name__=="Goal":
        o2.score()
        if o1 in Globals.balls:
          Globals.balls.remove(o1)
      if o1.__class__.__name__=="Bullet":
        if o1 in Globals.bullets:
          Globals.bullets.remove(o1)
      if o2.__class__.__name__=="Bullet":
        if o2 in Globals.bullets:
          Globals.bullets.remove(o2)

class Player:
  init_size=20
  pointer_length=1.8
  steer_speed=0.05
  forward_speed=0.20
  brake_factor=0.97
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

  def forward(self):
    self.speed.add_polar(self.angle,Player.forward_speed)

  def brake(self):
    self.speed.multipy(Player.brake_factor)
    
  def time_step(self):
    self.speed.air_resits()
    self.posrad.move(self.speed)
    check_and_handle_collisions(self,[Globals.players,Globals.balls,Globals.bullets])

  def shoot(self):
    if Globals.time>self.last_shoot_time+Player.shoot_time:
      self.last_shoot_time=Globals.time
      bvx,bvy=polar_to_cartesian(self.angle,1)
      length=self.posrad.rad * Player.pointer_length
      bullet=Bullet(self.posrad.x + bvx*length, \
                    self.posrad.y + bvy*length, \
                    self.speed.x  + bvx*Player.bullet_speed, \
                    self.speed.y  + bvy*Player.bullet_speed, \
                    self.color)
      Globals.bullets.append(bullet)
      check_and_handle_collisions(bullet,[Globals.players,Globals.balls])

  def draw(self):
    Globals.canvas.create_oval(self.posrad.x-self.posrad.rad, self.posrad.y-self.posrad.rad, \
                               self.posrad.x+self.posrad.rad, self.posrad.y+self.posrad.rad, \
                               fill=None, outline=self.color, width=6)
    cx,cy=polar_to_cartesian(self.angle, self.posrad.rad * Player.pointer_length)
    Globals.canvas.create_line(self.posrad.x,                               self.posrad.y,                               \
                               self.posrad.x + cx, self.posrad.y + cy, \
                               fill=self.color, width=6)

class Ball:
  size=10

  def __init__(self,x,y):
    self.posrad=PosRad(x,y,Ball.size)
    self.speed=Speed(0,0)

  def time_step(self):
    self.speed.air_resits()
    self.posrad.move(self.speed)
    check_and_handle_collisions(self,[Globals.players,Globals.balls,Globals.bullets,Globals.goals])

  def draw(self):
    Globals.canvas.create_oval(self.posrad.x-self.posrad.rad, self.posrad.y-self.posrad.rad, \
                               self.posrad.x+self.posrad.rad, self.posrad.y+self.posrad.rad, \
                               fill=None, outline="white", width=6)

class Goal:
  initial_size=70
  mark_height=14
  mark_spacing=8
  explosion_rad=25

  def __init__(self,x,y,color):
    self.posrad=PosRad(x,y,Goal.initial_size)
    self.speed=Speed(0,0)
    self.color=color
    self.goal_count=0
    self.goal_time=0

  def time_step(self):
    self.speed.x=0
    self.speed.y=0
    self.goal_time-=1

  def score(self):
    self.goal_count+=1
    self.posrad.rad*=0.9
    self.goal_time=Goal.explosion_rad

  def draw(self):
    Globals.canvas.create_oval(self.posrad.x-self.posrad.rad, self.posrad.y-self.posrad.rad, \
                       self.posrad.x+self.posrad.rad, self.posrad.y+self.posrad.rad, \
                       fill=None, outline=self.color, width=8)
    h=Goal.mark_height
    w=Goal.mark_spacing
    for i in range(self.goal_count):
      Globals.canvas.create_line(self.posrad.x + (.5+i-self.goal_count/2)*w, self.posrad.y-h, \
                         self.posrad.x + (.5+i-self.goal_count/2)*w, self.posrad.y+h, \
                         fill="red", width=4)
    if self.goal_time>0:
      t=(Goal.explosion_rad-self.goal_time)*4
      Globals.canvas.create_oval(self.posrad.x-self.posrad.rad-t, self.posrad.y-self.posrad.rad-t, \
                         self.posrad.x+self.posrad.rad+t, self.posrad.y+self.posrad.rad+t, \
                         fill=None, outline="red", width=4)

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
      Globals.bullets.remove(self)
    else:
      self.posrad.move(self.speed)
      check_and_handle_collisions(self,[Globals.players,Globals.balls])

  def draw(self):
    Globals.canvas.create_oval(self.posrad.x-self.posrad.rad, self.posrad.y-self.posrad.rad, \
                       self.posrad.x+self.posrad.rad, self.posrad.y+self.posrad.rad, \
                       fill=None, outline=self.color, width=4)
      
def process_keyboard_state():
  if Globals.keyboard.is_down("z"):
    Globals.players[0].steer(-1)
  if Globals.keyboard.is_down("x"):
    Globals.players[0].steer(+1)
  if Globals.keyboard.is_down("f"):
    Globals.players[0].forward()
  if Globals.keyboard.is_down("c"):
    Globals.players[0].brake()
  if Globals.keyboard.is_down("g"):
    Globals.players[0].shoot()
    
  if Globals.keyboard.is_down("m"):
    Globals.players[1].steer(-1)
  if Globals.keyboard.is_down("comma"):
    Globals.players[1].steer(+1)
  if Globals.keyboard.is_down("semicolon"):
    Globals.players[1].forward()
  if Globals.keyboard.is_down("period"):
    Globals.players[1].brake()
  if Globals.keyboard.is_down("apostrophe"):
    Globals.players[1].shoot()

def add_balls(n):
  for i in range(n):
    while True:
      x=random.randint(0,Globals.canvas_width)
      y=random.randint(0,Globals.canvas_height)
      b=Ball(x,y)
      if is_collision_free(b,[Globals.players,Globals.balls,Globals.goals]):
        Globals.balls.append(b)
        break

def key_down(e):
    Globals.keyboard.key_down(e.keysym)
    #print('down:',e.keysym)
def key_up(e):
    Globals.keyboard.key_up(e.keysym)
    #print('up:',e.keysym)
    
def time_step():
    Globals.canvas.delete("all") # remove all previous drawings
    process_keyboard_state()
    for obj_list in [Globals.goals,Globals.players,Globals.balls,Globals.bullets]:
      for obj in obj_list:
        obj.time_step()
        obj.draw()
    Globals.time+=1
    Globals.root.after(10, time_step)

def main():
  Globals.root.bind("<KeyPress>", key_down)
  Globals.root.bind("<KeyRelease>", key_up)
  Globals.root.update()
  
  Globals.players.append(Player(Globals.canvas_width*1/3, \
                                Globals.canvas_height/2,0      ,"blue"))
  Globals.players.append(Player(Globals.canvas_width*2/3, \
                                Globals.canvas_height/2,math.pi,"green"))
  Globals.goals.append(Goal(Goal.initial_size*3, \
                            Globals.canvas_height/2,"blue"))
  Globals.goals.append(Goal(Globals.canvas_width-Goal.initial_size*3, \
                            Globals.canvas_height/2,"green"))
  add_balls(10)
  
  Globals.root.after(100, time_step)
  Globals.root.mainloop()

if __name__ == "__main__":
    main()
