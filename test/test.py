# testing tkinter, for docs see: 
#   https://tkdocs.com/tutorial/index.html
#   http://effbot.org/tkinterbook/canvas.htm
#
import tkinter as tk
import random

root = tk.Tk()
root.title("My Game")  
canvas_width=1000
canvas_height=800
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.config(bg="black")
canvas.pack()
canvas.focus_set()
time=0

def rgb(r,g,b):
  return "#%02x%02x%02x" % (r,g,b)

def time_step():
    global time
    if time%500==0:
        canvas.delete("all") # remove all previous drawings
    else:
        color=rgb(random.randint(0,255), \
                  random.randint(0,255), \
                  random.randint(0,255)) 
        shape=random.randint(0,3)
        if shape==0:
            x1=random.randint(0,canvas.winfo_width())
            y1=random.randint(0,canvas.winfo_height())
            x2=random.randint(0,canvas.winfo_width())
            y2=random.randint(0,canvas.winfo_height())
            canvas.create_line(x1, y1, x2, y2, fill=color, width=4)
        elif shape==1:
            width =random.randint(30,100)
            height=random.randint(30,100)
            x1=random.randint(0,canvas.winfo_width() -width )
            y1=random.randint(0,canvas.winfo_height()-height)
            canvas.create_oval(x1, y1, x1+width, y1+height, fill=color, outline="white")
        elif shape==2:
            width =random.randint(30,100)
            height=random.randint(30,100)
            x1=random.randint(0,canvas.winfo_width() -width )
            y1=random.randint(0,canvas.winfo_height()-height)
            canvas.create_rectangle(x1, y1, x1+width, y1+height, fill=color, outline="white")
    time+=1
    root.after(2, time_step)
    
root.after(10, time_step)
root.update()
root.mainloop()
