# testing tkinter, for docs see: 
#   https://tkdocs.com/tutorial/index.html
#   http://effbot.org/tkinterbook/canvas.htm
#
import tkinter
import random

root = tkinter.Tk()  # create root window
root.title("My Game")

# create canvas to draw on
canvas_width  = 1000
canvas_height =  800
canvas = tkinter.Canvas(root, width=canvas_width, height=canvas_height)
canvas.config(bg="black")
canvas.pack() # pack canvas in root window
canvas.focus_set()
time = 0

def rgb(r,g,b): # returns color as mix of red,green,blue [0;255]
  return "#%02x%02x%02x" % (r,g,b)

def time_step():
    global time
    if time%100==0:
        canvas.delete("all") # remove all previous drawings

    # get random color 
    color = rgb(random.randint(0, 255), \
                random.randint(0, 255), \
                random.randint(0, 255))
    
    x1 = random.randint(0, canvas.winfo_width() )
    y1 = random.randint(0, canvas.winfo_height())
    x2 = random.randint(0, canvas.winfo_width() )
    y2 = random.randint(0, canvas.winfo_height())
    canvas.create_line(x1, y1, \
                       x2, y2, fill=color, width=4)

    width  = random.randint(30, 100)
    height = random.randint(30, 100)
    x1 = random.randint(0, canvas.winfo_width() - width )
    y1 = random.randint(0, canvas.winfo_height()- height)
    canvas.create_oval(x1      , y1       , \
                       x1+width, y1+height, fill=color, outline="white")

    width  = random.randint(30, 100)
    height = random.randint(30, 100)
    x1 = random.randint(0, canvas.winfo_width() - width )
    y1 = random.randint(0, canvas.winfo_height()- height)
    canvas.create_rectangle(x1        , y1         , \
                            x1 + width, y1 + height, fill=color, outline="white")

    x1 = random.randint(0, canvas.winfo_width() )
    y1 = random.randint(0, canvas.winfo_height())
    canvas.create_text(x1, y1, fill=color, text="Hello World!")

    time += 1
    root.after(10, time_step) # ask to call time_step()

root.update()
root.after(100, time_step) # ask to call time_step() after waiting 100ms

print("calling mainloop()")
root.mainloop()
print("the end!")
