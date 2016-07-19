from Tkinter import *
import sys

# Object settings and selection
def setObject(value):
    global shape
    shape = value

def getObject(event):
    obj_list = event.widget.find_overlapping(event.x, event.y, event.x, event.y)
    if obj_list:
        return obj_list[len(obj_list)-1]
    return False

def setFill(value):
    global fill
    fill = value


def setEdge(value):
    global edge
    edge = value


# Contextual menu functions
def changeColor(obj, chars):
    if obj:
        app.canvas.itemconfig(obj, **chars)
    else:
        if "fill" in chars:
            setFill(chars["fill"])
            app.fill.config(background=fill)
        else:
            setEdge(chars["edge"])
            app.outline.config(background=edge)

def delObject(obj):
    if obj:
        app.canvas.delete(obj)
    else:
        app.canvas.delete("all")

class colorMenu(Menu):
    def __init__(self, menu, obj, target):
        Menu.__init__(self, master)
        self.add_command(background="white", command=lambda *args: changeColor(obj, {target: "white"}))
        self.add_command(background="red", command=lambda *args: changeColor(obj, {target: "red"}))
        self.add_command(background="orange", command=lambda *args: changeColor(obj, {target: "orange"}))
        self.add_command(background="yellow", command=lambda *args: changeColor(obj, {target: "yellow"}))
        self.add_command(background="green", command=lambda *args: changeColor(obj, {target: "green"}))
        self.add_command(background="blue", command=lambda *args: changeColor(obj, {target: "blue"}))
        self.add_command(background="purple", command=lambda *args: changeColor(obj, {target: "purple"}))
        self.add_command(background="black", command=lambda *args: changeColor(obj, {target: "black"}))

def popupMenu(event):
    menu = Menu(master, tearoff=0)
    obj = getObject(event)

    if obj:
        menu.add_cascade(label="Edit Fill", menu=colorMenu(menu, obj, "fill"))
        menu.add_cascade(label="Edit Border", menu=colorMenu(menu, obj, "outline"))
        menu.add_command(label="Edit Size", command=lambda *args: editObject(obj))
        menu.add_separator()
        menu.add_command(label="Delete", foreground="red", command=lambda *args: delObject(obj))
    else:
        menu.add_command(label="Circle", command=lambda *args: setObject("circle"))
        menu.add_command(label="Square", command=lambda *args: setObject("square"))
        menu.add_command(label="Triangle", command=lambda *args: setObject("triangle"))
        menu.add_separator()
        menu.add_command(label="Delete All", foreground="red", command=lambda *args: delObject(obj))
    menu.post(event.x_root, event.y_root)

def fileMenu(frame):
    # create a toplevel menu
    menubar = Menu(master)
    menubar.add_command(label="Quit", foreground="red", command=frame.quit)
    
    # create draw pulldown menus
    drawmenu = Menu(menubar, tearoff=0)
    drawmenu.add_command(label="Circle", command=lambda *args: setObject("circle"))
    drawmenu.add_command(label="Square", command=lambda *args: setObject("square"))
    drawmenu.add_command(label="Triangle", command=lambda *args: setObject("triangle"))
    menubar.add_cascade(label="Draw", menu=drawmenu)
    
    menubar.add_cascade(label="Set Fill", menu=colorMenu(menubar, False, "fill"))
    menubar.add_cascade(label="Set Outline", menu=colorMenu(menubar, False, "edge"))
    master.config(menu=menubar)


# Shape creation and editing
def createObject(event):
    if shape == "circle":
        # box = (event.x - 20, event.y - 20, event.x + 20, event.y + 20)
        obj = app.canvas.create_oval(event.x - 20, event.y - 20, event.x + 20, event.y + 20, \
                            fill=fill, outline=edge, activefill="red", tags="circle")
    elif shape == "square":
        obj = app.canvas.create_rectangle(event.x, event.y, event.x + 30, event.y + 30, \
                            fill=fill, outline=edge, activefill="red", tags="square")
    elif shape == "triangle":
        obj = app.canvas.create_polygon(event.x, event.y, event.x + 10, event.y + 20, \
                            event.x - 10, event.y + 20, fill=fill, outline=edge, activefill="red", tags="triangle")


def selectObject(event):
    global move
    move = False
    obj = getObject(event)
    if obj:
        move = obj

def dropObject(event):
    if move:
        #import pdb; pdb.set_trace()
        coords = app.canvas.coords(move)
        box = app.canvas.bbox(move)
        x_offset = event.x - (box[0]+(box[2]-box[0])/2)
        y_offset = event.y - (box[1]+(box[3]-box[1])/2)
        new_coords = []
        for i, c in enumerate(coords):
            if i % 2 == 0: # even are x-coords
                new_coords.append(c+x_offset)
            else:
                new_coords.append(c+y_offset)
        app.canvas.coords(move, tuple(new_coords))

class editDims:
    def __init__(self, parent, obj, obj_type):

        top = self.top = Toplevel(parent)
        if obj_type == "circle":
            Label(top, text="Enter new radius").pack()
            self.width = self.height = Entry(top)
            self.width.pack(padx=5)
            self.width.focus_set()
        else:
            Label(top, text="Enter new width").pack()
            self.width = Entry(top)
            self.width.pack(padx=5)
            self.width.focus_set()
            Label(top, text="Enter new height").pack()
            self.height = Entry(top)
            self.height.pack(padx=5)  


        b = Button(top, text="Enter", command=lambda *args: self.update(obj, obj_type))
        b.pack(pady=5)

    def update(self, obj, obj_type):
        coords = app.canvas.coords(obj)
        if obj_type == "circle":
            new_rad = float(self.width.get())
            offset =  (coords[2]-coords[0])/2 - new_rad
            new_coords = (coords[0]+offset, coords[1]+offset, coords[2]-offset, coords[3]-offset)
        elif obj_type == "square":
            new_coords = (coords[0], coords[1], coords[0]+float(self.width.get()), coords[1]+float(self.height.get()))
        else:
            new_coords = (coords[0], coords[1], coords[0]+float(self.width.get())/2, coords[1]+float(self.height.get()), \
                          coords[0]-float(self.width.get())/2, coords[1]+float(self.height.get()))
        app.canvas.coords(obj, new_coords)
        self.top.destroy()


def editObject(obj):
    obj_type = app.canvas.itemcget(obj, "tags")
    d = editDims(master, obj, obj_type)
    master.wait_window(d.top)
  

class App:
    def __init__(self, master):
        frame = self.frame = Frame(master, width=300)
        frame.pack()
        setObject("select")
        setFill("blue")
        setEdge("black")

        fileMenu(frame)
        
        # Default color labels
        Label(frame, text="Fill Color = ").grid(row=0, column=0, sticky=E)
        self.fill = Label(frame, width=4, background=fill)
        self.fill.grid(row=0, column=1)
        Label(frame, text="Outline Color = ").grid(row=0, column=2, sticky=E)
        self.outline = Label(frame, width=4, background=edge)
        self.outline.grid(row=0, column=3)

        # Canvas setup and bindings
        self.canvas = Canvas(frame, width=300, height=300)
        self.canvas.bind("<Button-1>", createObject) # Binds left mouse to object creation
        self.canvas.bind("<Button-2>", selectObject) # Binds center mouse to select object to move
        self.canvas.bind("<ButtonRelease-2>", dropObject) # Ends an object move
        self.canvas.bind("<Button-3>", popupMenu) # Binds right mouse to object edit
        self.canvas.grid(row=1, column=0, rowspan=20, columnspan=5, sticky=W+E+N+S)


master = Tk()
app = App(master)


master.mainloop()
