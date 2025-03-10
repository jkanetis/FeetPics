import pyvista as pv
import numpy as np
import vtk

# Load the 3D model
mesh = pv.read("human_foot.obj")

# Start PyVista plotter
plotter = pv.Plotter()

# Initialize colors array for each face (cell)
colors = np.ones((mesh.n_cells, 3)) * 0.8  # Set initial gray color for each face
mesh.cell_data["face_colors"] = colors

# Add the mesh to the plotter, specifying cell scalars for face coloring
plotter.add_mesh(mesh, scalars="face_colors", rgb=True)

# Reset camera to properly see the model
plotter.reset_camera()

# Store the original camera interaction style
original_style = plotter.iren.get_interactor_style()

# Create a custom style that disables camera movements
class ColoringStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.on_left_button_press)
        self.AddObserver("LeftButtonReleaseEvent", self.on_left_button_release)
        self.AddObserver("MouseMoveEvent", self.on_mouse_move)

        
    def on_left_button_press(self, obj, event):
        # Disable the default rotation behavior by not calling the parent method
        pass
        
    def on_left_button_release(self, obj, event):
        # Disable the default behavior by not calling the parent method
        pass
        
    def on_mouse_move(self, obj, event):
        # Disable the default behavior by not calling the parent method
        pass

# Create an instance of the custom style
coloring_style = ColoringStyle()

# PyVista Picker for selecting cells
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.01)

# Track states
coloring_mode = [False]
mouse_pressed = [False]  # Track if mouse button is currently pressed

# Button dimensions
button_x, button_y = 20, 20
button_width, button_height = 200, 40

# Add a colored background for the button using a proper plane
def create_button_background(color='lightblue'):
    # Create a plane for the button
    plane = pv.Plane(
        center=(button_x + button_width/2, button_y + button_height/2, 0),
        direction=(0, 0, 1),
        i_size=button_width,
        j_size=button_height
    )
    return plotter.add_mesh(plane, color=color, name="button_bg")

# Create the initial button background
create_button_background('lightblue')

# Add a text for coloring mode status - larger and more visible
plotter.add_text("COLORING MODE: OFF", position=(20, 550), font_size=18, color='black', name="mode_text")

# Add button text - larger and centered on the button
plotter.add_text("TOGGLE COLORING MODE (or press 'C')", 
                position=(button_x + 10, button_y + button_height//2), 
                font_size=14, color='black', name="button_text")

# Function to toggle coloring mode
def toggle_coloring_mode():
    coloring_mode[0] = not coloring_mode[0]
    
    # Update text and button colors
    plotter.remove_actor("mode_text")
    plotter.remove_actor("button_bg")
    
    if coloring_mode[0]:
        status = "ON"
        text_color = 'red'
        create_button_background('salmon')
        # Switch to coloring style (no camera movement)
        plotter.iren.SetInteractorStyle(coloring_style)
    else:
        status = "OFF"
        text_color = 'black'
        create_button_background('lightblue')
        # Switch back to original style (with camera movement)
        plotter.iren.SetInteractorStyle(original_style)
    
    plotter.add_text(f"COLORING MODE: {status}", position=(20, 550), 
                    font_size=18, color=text_color, name="mode_text")
    
    plotter.render()

# Function to check if coordinates are within button area
def is_in_button_area(x, y):
    return button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height

# Function to handle mouse click
def on_left_button_press(obj, event):
    x, y = plotter.iren.GetEventPosition()
    
    # Check if click is on the button
    if is_in_button_area(x, y):
        toggle_coloring_mode()
        return
    
    # Toggle the mouse_pressed state if in coloring mode
    if coloring_mode[0]:
        mouse_pressed[0] = not mouse_pressed[0]
        if mouse_pressed[0]:
            # Start coloring
            color_at_position(x, y)

# Function to handle mouse movement
def on_mouse_move(obj, event):
    # Only color if in coloring mode AND mouse button is pressed
    if coloring_mode[0] and mouse_pressed[0]:
        x, y = plotter.iren.GetEventPosition()
        color_at_position(x, y)

# Function to color at a specific position
def color_at_position(x, y):
    picker.Pick(x, y, 0, plotter.renderer)
    cell_id = picker.GetCellId()
    if cell_id >= 0:
        colors[cell_id] = [1.0, 0.0, 0.0]  # Set to red
        mesh.cell_data["face_colors"] = colors
        plotter.render()

# Add keyboard shortcut to toggle coloring mode
def keypress_callback(obj, event):
    key = plotter.iren.GetKeySym().lower()
    if key == 'c':  # Press 'c' to toggle coloring mode
        toggle_coloring_mode()

# Register callbacks
plotter.iren.add_observer(vtk.vtkCommand.LeftButtonPressEvent, on_left_button_press)
plotter.iren.add_observer(vtk.vtkCommand.MouseMoveEvent, on_mouse_move)
plotter.iren.add_observer(vtk.vtkCommand.KeyPressEvent, keypress_callback)

# Add instructions text at the bottom
instructions = (
    "Instructions:\n"
    "- Press 'C' or click the blue button to toggle coloring mode\n"
    "- In coloring mode: Click to start coloring, click again to stop\n"
    "- In normal mode: Click and drag to rotate the model"
)
plotter.add_text(instructions, position=(20, 100), font_size=12, name="instructions")

# Show the plotter
plotter.show()