# testing tkinter, for docs see: 
#   https://tkdocs.com/tutorial/index.html
#   http://effbot.org/tkinterbook/canvas.htm
#
import tkinter
import random

print("Drag balls with mouse:")

class Globals:
  root = tkinter.Tk()
  root.title("Elastics")  
  canvas_width=1000
  canvas_height=800
  canvas = tkinter.Canvas(root, width=canvas_width, height=canvas_height)
  canvas.config(bg="black")
  canvas.pack()
  canvas.focus_set()
  time=0
  balls=[]
  mouse_holds_ball=None

class Ball:
  size=20
  
  def __init__(self,x,y):
    self.x=x
    self.y=y
    self.vx=0
    self.vy=0

  def sqaure_distance(self,mx,my):
    dx=self.x-mx           # difference in x
    dy=self.y-my           # difference in y
    return dx*dx+dy*dy # Pythagoras

def closest_ball(mx,my):
  closest=None
  min_distance=None
  for i in Globals.balls:
    sd=i.sqaure_distance(mx,my)
    if min_distance is None or sd<min_distance:
      min_distance=sd
      closest=i
  return closest
  
def move_balls():
  gravity=3
  force=0.1
  air_resistance=0.9
  for i in range(1,len(Globals.balls)-1):
    b=Globals.balls[i]
    fx=Globals.balls[i-1].x-b.x + Globals.balls[i+1].x-b.x
    fy=Globals.balls[i-1].y-b.y + Globals.balls[i+1].y-b.y
    fy+=gravity
    if True:#not b is Globals.mouse_holds_ball:
      b.vx+= fx*force
      b.vy+= fy*force
      b.x+= b.vx
      b.y+= b.vy
      b.vx*=air_resistance
      b.vy*=air_resistance

def draw_balls():
  for i in range(len(Globals.balls)):
    Globals.canvas.create_oval(Globals.balls[i].x-Ball.size, Globals.balls[i].y-Ball.size, \
                               Globals.balls[i].x+Ball.size, Globals.balls[i].y+Ball.size, \
                               fill=None, outline="white", width=6)
    if i+1<len(Globals.balls):
      Globals.canvas.create_line(Globals.balls[i  ].x, Globals.balls[i  ].y, \
                                 Globals.balls[i+1].x, Globals.balls[i+1].y, \
                                 fill="white", width=4)

def mouse_button(event):
  Globals.mouse_holds_ball=closest_ball(event.x,event.y)
  Globals.mouse_holds_ball.x=event.x
  Globals.mouse_holds_ball.y=event.y
  
def mouse_release(event):
  #print("Mouse release:",event)
  Globals.mouse_holds_ball=None
  
def mouse_motion(event):
  #print("Mouse motion:",event)
  if not Globals.mouse_holds_ball is None:
    Globals.mouse_holds_ball.x=event.x
    Globals.mouse_holds_ball.y=event.y
  
def time_step():
  Globals.canvas.delete("all") # remove all previous drawings
  Globals.time+=1
  move_balls()
  draw_balls()
  Globals.root.after(10, time_step)
    
def add_balls(n):
  for i in range(n):
    Globals.balls.append(Ball(i*Globals.canvas_width/(n-1), Globals.canvas_height*1/3))
 
def main():
  Globals.root.update()
  Globals.root.bind('<Button>',mouse_button)
  Globals.root.bind('<ButtonRelease>',mouse_release)
  Globals.root.bind('<Motion>',mouse_motion)

  add_balls(20)
  
  Globals.root.after(100, time_step)
  Globals.root.mainloop()

if __name__ == "__main__":
    main()
