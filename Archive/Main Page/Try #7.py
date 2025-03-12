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

# Track modes and states
drawing_mode = [False]  # Whether the user is in drawing mode
current_sensation = ["none"]  # Current selected sensation (tingling or numbness)
description_visible = [False]  # Whether description text is visible

# PyVista Picker for selecting cells
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.01)

# Get window dimensions
window_width = plotter.window_size[0]
window_height = plotter.window_size[1]

# UI: Add buttons and text with larger size and at top right
plotter.add_text("Tingling", position=(window_width - 150, 10), font_size=16, color="blue", name="tingling_button")
plotter.add_text("Numbness", position=(window_width - 150, 50), font_size=16, color="red", name="numbness_button")
plotter.add_text("Stop", position=(window_width - 150, 90), font_size=16, color="black", name="stop_button")
# Position quit button at bottom right
plotter.add_text("Quit", position=(window_width - 100, window_height - 40), font_size=16, color="red", name="quit_button")

# Function to toggle tingling mode
def set_tingling_mode():
    drawing_mode[0] = True
    current_sensation[0] = "tingling"
    
    # Update button highlighting
    plotter.remove_actor("tingling_button")
    plotter.remove_actor("numbness_button")
    plotter.add_text("Tingling", position=(window_width - 150, 10), font_size=16, color="white", 
                     background_color="blue", name="tingling_button")
    plotter.add_text("Numbness", position=(window_width - 150, 50), font_size=16, color="red", name="numbness_button")
    
    # Show description
    if "sensation_desc" in plotter._actors:
        plotter.remove_actor("sensation_desc")
    plotter.add_text("Info to be Added...", position=(window_width - 200, 130), font_size=14, 
                     color="blue", name="sensation_desc")
    description_visible[0] = True
    
    plotter.render()

# Function to toggle numbness mode
def set_numbness_mode():
    drawing_mode[0] = True
    current_sensation[0] = "numbness"
    
    # Update button highlighting
    plotter.remove_actor("tingling_button")
    plotter.remove_actor("numbness_button")
    plotter.add_text("Tingling", position=(window_width - 150, 10), font_size=16, color="blue", name="tingling_button")
    plotter.add_text("Numbness", position=(window_width - 150, 50), font_size=16, color="white", 
                     background_color="red", name="numbness_button")
    
    # Show description
    if "sensation_desc" in plotter._actors:
        plotter.remove_actor("sensation_desc")
    plotter.add_text("Info to be Added...", position=(window_width - 200, 130), font_size=14, 
                     color="red", name="sensation_desc")
    description_visible[0] = True
    
    plotter.render()

# Function to stop drawing
def stop_drawing():
    drawing_mode[0] = False
    current_sensation[0] = "none"
    
    # Reset button highlighting
    plotter.remove_actor("tingling_button")
    plotter.remove_actor("numbness_button")
    plotter.add_text("Tingling", position=(window_width - 150, 10), font_size=16, color="blue", name="tingling_button")
    plotter.add_text("Numbness", position=(window_width - 150, 50), font_size=16, color="red", name="numbness_button")
    
    # Remove description
    if "sensation_desc" in plotter._actors:
        plotter.remove_actor("sensation_desc")
    description_visible[0] = False
    
    plotter.render()

# Function to quit the application
def quit_application():
    plotter.close()

# Function to draw on the foot model
def draw_on_foot(*args):
    if not drawing_mode[0]:
        return
        
    x, y = plotter.iren.get_event_position()
    picker.Pick(x, y, 0, plotter.renderer)
    picked_cell_id = picker.GetCellId()
    
    if picked_cell_id >= 0:
        # Set color based on current mode
        if current_sensation[0] == "tingling":
            colors[picked_cell_id] = [0.0, 0.0, 1.0]  # Blue for tingling
        elif current_sensation[0] == "numbness":
            colors[picked_cell_id] = [1.0, 0.0, 0.0]  # Red for numbness
            
        mesh.cell_data["face_colors"] = colors
        plotter.update_scalars(colors)
        plotter.render()

# Function to detect button clicks
def handle_mouse_click(*args):
    x, y = plotter.iren.get_event_position()
    
    # Check if clicked on the "Tingling" button (top right)
    if window_width - 150 <= x <= window_width - 50 and 10 <= y <= 35:
        set_tingling_mode()
    
    # Check if clicked on the "Numbness" button (top right)
    elif window_width - 150 <= x <= window_width - 50 and 50 <= y <= 75:
        set_numbness_mode()
    
    # Check if clicked on the "Stop" button (top right)
    elif window_width - 150 <= x <= window_width - 50 and 90 <= y <= 115:
        stop_drawing()
    
    # Check if clicked on the "Quit" button (bottom right)
    elif window_width - 100 <= x <= window_width and window_height - 40 <= y <= window_height - 15:
        quit_application()

# Register mouse events
plotter.iren.add_observer("MouseMoveEvent", draw_on_foot)  # Draw while moving mouse
plotter.iren.add_observer("LeftButtonPressEvent", handle_mouse_click)  # Handle UI button clicks
plotter.iren.add_observer("LeftButtonPressEvent", draw_on_foot)  # Start drawing on click

# Show interactive window
plotter.show()