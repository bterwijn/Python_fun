# testing tkinter, for docs see: 
#   https://tkdocs.com/tutorial/index.html
#   http://effbot.org/tkinterbook/canvas.htm
#
import tkinter as tk
import random

print("Drag balls with mouse:")

root = tk.Tk()
root.title("Elastics")  
canvas_width=1000
canvas_height=800
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
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
  for i in balls:
    sd=i.sqaure_distance(mx,my)
    if min_distance is None or sd<min_distance:
      min_distance=sd
      closest=i
  return closest
  
def move_balls():
  gravity=3
  force=0.1
  air_resistance=0.9
  for i in range(1,len(balls)-1):
    b=balls[i]
    fx=balls[i-1].x-b.x + balls[i+1].x-b.x
    fy=balls[i-1].y-b.y + balls[i+1].y-b.y
    fy+=gravity
    if not b is mouse_holds_ball:
      b.vx+= fx*force
      b.vy+= fy*force
      b.x+= b.vx
      b.y+= b.vy
      b.vx*=air_resistance
      b.vy*=air_resistance

def draw_balls():
  for i in range(len(balls)):
    canvas.create_oval(balls[i].x-Ball.size, balls[i].y-Ball.size, \
                       balls[i].x+Ball.size, balls[i].y+Ball.size, \
                       fill=None, outline="white", width=6)
    if i+1<len(balls):
      canvas.create_line(balls[i  ].x, balls[i  ].y, \
                         balls[i+1].x, balls[i+1].y, \
                         fill="white", width=4)

def mouse_button(event):
  global mouse_holds_ball
  mouse_holds_ball=closest_ball(event.x,event.y)
  mouse_holds_ball.x=event.x
  mouse_holds_ball.y=event.y
  
def mouse_release(event):
  global mouse_holds_ball
  #print("Mouse release:",event)
  mouse_holds_ball=None
  
def mouse_motion(event):
  global mouse_holds_ball
  #print("Mouse motion:",event)
  if not mouse_holds_ball is None:
    mouse_holds_ball.x=event.x
    mouse_holds_ball.y=event.y
  
nr_balls=20
for i in range(nr_balls):
  balls.append(Ball(i*canvas_width/(nr_balls-1), canvas_height*1/3))

def time_step():
    global time
    canvas.delete("all") # remove all previous drawings
    time+=1
    move_balls()
    draw_balls()
    root.after(10, time_step)

root.update()
root.bind('<Button>',mouse_button)
root.bind('<ButtonRelease>',mouse_release)
root.bind('<Motion>',mouse_motion)
root.after(100, time_step)
root.mainloop()
