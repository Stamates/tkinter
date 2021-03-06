# Simple GUI for creating and modifying basic shapes
## To Run
Use standard install of Python 2.7 (change to tkinter for import statement if using Python 3)
```
$ python shapes.py
```

## Functions
* Menubar features
    * Quit - Exits the program (can also use the std close window button at top right)
    * Draw - Sets the shape that will be created when left clicking on the canvas area
    * Set Fill - Opens a color palette to select the default fill color for new shapes
    * Set Outline - Opens a color palette to select the default outline color for new shapes
* Canvas area mouse controls / contextual menus
    * Left click creates a new shape at that location
        * Circles are created at the center point
        * Squares are created at the top left corner
        * Triangles are created at the top point
    * Middle click and drag to move shapes (drops shape in new location upon release)
    * Right click on canvas
        * On open area - menu for selecting shapes to draw and a delete all shapes option
        * On shape - menu for editing the current shapes fill, outline, or dimensions and option to delete selected shape

__Note:__ All shapes are created based on default dimensions and can be edited to change size.
