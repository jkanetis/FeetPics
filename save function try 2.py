import pyvista as pv
import numpy as np
import vtk
import os
from datetime import datetime

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
drawing_mode = [False]  
current_sensation = ["none"] 
# Track screen lock state
#screen_locked = [False] 

# PyVista Picker for selecting cells
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.01)

# Get window dimensions
window_width = plotter.window_size[0]
window_height = plotter.window_size[1]

plotter.iren.interactor_style = None  # Lock camera rotation


# Function to update button states (highlight active button)
def update_buttons(active):
    plotter.remove_actor("tingling_button")
    plotter.remove_actor("numbness_button")
    plotter.remove_actor("stop_button")
    plotter.remove_actor("save_button")
    plotter.remove_actor("quit_button")
    plotter.remove_actor("lock_button")
    plotter.remove_actor("unlock_button")

    # Re-add all buttons, highlighting the active one
    if active == "tingling":
        plotter.add_text("TINGLING", position=(window_width - 150, 10), font_size=16, color="blue", name="tingling_button", shadow=True)
    else:
        plotter.add_text("Tingling", position=(window_width - 150, 10), font_size=16, color="blue", name="tingling_button")

    if active == "numbness":
        plotter.add_text("NUMBNESS", position=(window_width - 150, 50), font_size=16, color="red", name="numbness_button", shadow=True)
    else:
        plotter.add_text("Numbness", position=(window_width - 150, 50), font_size=16, color="red", name="numbness_button")

    if active == "stop":
        plotter.add_text("STOP", position=(window_width - 150, 90), font_size=16, color="black", name="stop_button", shadow=True)
    else:
        plotter.add_text("Stop", position=(window_width - 150, 90), font_size=16, color="black", name="stop_button")

    if active == "save":
        plotter.add_text("SAVE", position=(window_width - 150, 130), font_size=16, color="green", name="save_button", shadow=True)
    else:
        plotter.add_text("Save", position=(window_width - 150, 130), font_size=16, color="green", name="save_button")

    if active == "lock":
        plotter.add_text("LOCKED", position=(window_width - 150, 170), font_size=16, color="black", name="lock_button", shadow=True)
    else:
        plotter.add_text("Lock", position=(window_width - 150, 170), font_size=16, color="black", name="lock_button")

    if active == "unlock":
        plotter.add_text("UNLOCKED", position=(window_width - 150, 210), font_size=16, color="black", name="unlock_button", shadow=True)
    else:
        plotter.add_text("Unlock", position=(window_width - 150, 210), font_size=16, color="black", name="unlock_button")

    if active == "quit":
        plotter.add_text("QUIT", position=(20, window_height - 40), font_size=16, color="red", name="quit_button", shadow=True)
    else:
        plotter.add_text("Quit", position=(20, window_height - 40), font_size=16, color="red", name="quit_button")

# Function to toggle tingling mode
def set_tingling_mode():
    drawing_mode[0] = True
    current_sensation[0] = "tingling"
    update_buttons("tingling")
    plotter.render()

# Function to toggle numbness mode
def set_numbness_mode():
    drawing_mode[0] = True
    current_sensation[0] = "numbness"
    update_buttons("numbness")
    plotter.render()

# Function to stop drawing
def stop_drawing():
    drawing_mode[0] = False
    plotter.disable()
    current_sensation[0] = "none"
    update_buttons("stop")
    plotter.render()

def set_screen_lock_mode():
    #screen_locked[0] = True
    plotter.disable()
    update_buttons("lock")
    plotter.render()

def set_screen_unlock_mode():
    #screen_locked[0] = False
    plotter.enable()
    update_buttons("unlock")
    plotter.render()

# Function to save the foot model image
def save_image():
    now = datetime.now()
    timeText = now.strftime("%Y%m%d-%H%M%S")
    plotter.enable()   
    # Define directories
    base_dir = os.getcwd()
    folder = "Foot Maps"
    save_dir = os.path.join(base_dir, folder)
    
    # Create folder if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Define filename and path
    filename = f"footMap_{timeText}.png"
    save_path = os.path.join(save_dir, filename)
    
    # Save screenshot
    plotter.screenshot(save_path)
    print(f"Image saved at: {save_path}")

    # Highlight "Save" button
    update_buttons("save")
    plotter.render()

# Function to quit the application
def quit_application():
    update_buttons("quit")
    plotter.render()
    plotter.close()

# Function to draw on the foot model
def draw_on_foot(*args):
    #if screen_locked[0] or not drawing_mode[0]:
        #return

    x, y = plotter.iren.get_event_position()
    picker.Pick(x, y, 0, plotter.renderer)
    picked_cell_id = picker.GetCellId()
    
    if picked_cell_id >= 0:
        if current_sensation[0] == "tingling":
            colors[picked_cell_id] = [0.0, 0.0, 1.0]  # Blue
        elif current_sensation[0] == "numbness":
            colors[picked_cell_id] = [1.0, 0.0, 0.0]  # Red
            
        mesh.cell_data["face_colors"] = colors
        plotter.update_scalars(colors)
        plotter.render()

# Function to detect button clicks
def handle_mouse_click(*args):
    #if screen_locked[0]:
        #return

    x, y = plotter.iren.get_event_position()
    
    if window_width - 150 <= x <= window_width - 50:
        if 10 <= y <= 35:
            set_tingling_mode()
        elif 50 <= y <= 75:
            set_numbness_mode()
        elif 90 <= y <= 115:
            stop_drawing()
        elif 130 <= y <= 155:
            save_image()
        elif 170 <= y <= 195:
            set_screen_lock_mode()
        elif 210 <= y <= 235:
            set_screen_unlock_mode()
    elif 20 <= x <= 70 and window_height - 40 <= y <= window_height - 15:
        quit_application()

# Register mouse events
plotter.iren.add_observer("MouseMoveEvent", draw_on_foot)
plotter.iren.add_observer("LeftButtonPressEvent", handle_mouse_click)
plotter.iren.add_observer("LeftButtonPressEvent", draw_on_foot)

# Initialize UI with default button states
update_buttons("none")

# Show interactive window
plotter.show()