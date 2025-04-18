import pyvista as pv
import numpy as np
import vtk
import os
from datetime import datetime

# Load the 3D model
mesh = pv.read("mesh_test1.obj")

# Start PyVista plotter
plotter = pv.Plotter()

# Initialize colors array for each face (cell)
colors = np.ones((mesh.n_cells, 3)) * 0.8  # Set initial gray color for each face
mesh.cell_data["face_colors"] = colors

# Add the mesh to the plotter, specifying cell scalars for face coloring
plotter.add_mesh(mesh, scalars="face_colors", rgb=True)

# Track drawing mode and current sensation
drawing_mode = [False]
current_sensation = ["none"]
mouse_down = {"left": False}  # Track left mouse button state

# Define color mapping for each sensation
sensation_colors = {
    "paresthesia": [1.0, 0.0, 0.0],  # Red
    "pressure":    [1.0, 0.5, 0.0],  # Orange
    "movement":    [0.0, 0.0, 1.0],  # Blue
    "vibration":   [0.0, 1.0, 0.0],  # Green
}

# PyVista Picker for selecting cells
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.01)

# Get window dimensions
window_width = plotter.window_size[0]
window_height = plotter.window_size[1]

plotter.iren.interactor_style = None  # Lock camera rotation

# Function to update button display
def update_buttons(active):
    for name in list(plotter.actors.keys()):
        if name.endswith("_button"):
            plotter.remove_actor(name)

    y_offset = 10
    spacing = 40
    for i, (sensation, color) in enumerate(sensation_colors.items()):
        label = sensation.upper() if active == sensation else sensation.capitalize()
        shadow = True if active == sensation else False
        plotter.add_text(
            label,
            position=(window_width - 150, y_offset + i * spacing),
            font_size=16,
            color=color,
            name=f"{sensation}_button",
            shadow=shadow
        )

    extra_buttons = [
        ("Stop", "black", "stop_button"),
        ("Save", "green", "save_button"),
        ("Lock", "black", "lock_button"),
        ("Unlock", "black", "unlock_button"),
        ("Quit", "red", "quit_button"),
    ]
    for j, (label, color, name) in enumerate(extra_buttons):
        pos_y = y_offset + (len(sensation_colors) + j) * spacing
        highlight = (active.lower() == label.lower())
        plotter.add_text(
            label.upper() if highlight else label,
            position=(window_width - 150, pos_y),
            font_size=16,
            color=color,
            name=name,
            shadow=highlight
        )

# Sensation mode setter
def set_sensation_mode(sensation):
    drawing_mode[0] = True
    current_sensation[0] = sensation
    update_buttons(sensation)
    plotter.render()

# Stop drawing
def stop_drawing():
    drawing_mode[0] = False
    current_sensation[0] = "none"
    update_buttons("stop")
    plotter.render()

# Lock / Unlock screen (camera movement)
def set_screen_lock_mode():
    plotter.disable()
    update_buttons("lock")
    plotter.render()

def set_screen_unlock_mode():
    plotter.enable()
    update_buttons("unlock")
    plotter.render()

# Save screenshot of current model
def save_image():
    now = datetime.now()
    timeText = now.strftime("%Y%m%d-%H%M%S")
    plotter.enable()
    save_dir = os.path.join(os.getcwd(), "Foot Maps")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"footMap_{timeText}.png")
    plotter.screenshot(save_path)
    print(f"Image saved at: {save_path}")
    update_buttons("save")
    plotter.render()

# Quit the application
def quit_application():
    update_buttons("quit")
    plotter.render()
    plotter.close()

# Drawing on the foot model
def draw_on_foot(*args):
    if not drawing_mode[0]:
        return

    x, y = plotter.iren.get_event_position()
    picker.Pick(x, y, 0, plotter.renderer)
    picked_cell_id = picker.GetCellId()

    if picked_cell_id >= 0 and current_sensation[0] in sensation_colors:
        new_color = np.array(sensation_colors[current_sensation[0]])
        current_color = colors[picked_cell_id]

        if not np.allclose(current_color, [0.8, 0.8, 0.8]):
            blended_color = (current_color + new_color) / 2
            colors[picked_cell_id] = blended_color
            print(f"Blended color {current_color} and {new_color} -> {blended_color}")

            if np.allclose(current_color, [1.0, 0.0, 0.0]) and np.allclose(new_color, [0.0, 0.0, 1.0]):
                print("The color produced by averaging red and blue in digital systems is typically magenta or a purplish-red hue.")
        else:
            colors[picked_cell_id] = new_color

        mesh.cell_data["face_colors"] = colors.copy()
        plotter.update_scalars(colors.copy(), render=True)

# Handle button clicks
def handle_mouse_click(*args):
    x, y = plotter.iren.get_event_position()
    
    y_offset = 10
    spacing = 40

    for i, sensation in enumerate(sensation_colors):
        if window_width - 150 <= x <= window_width - 50 and y_offset + i * spacing <= y <= y_offset + i * spacing + 25:
            set_sensation_mode(sensation)
            return

    extra_actions = [
        ("stop", stop_drawing),
        ("save", save_image),
        ("lock", set_screen_lock_mode),
        ("unlock", set_screen_unlock_mode),
        ("quit", quit_application),
    ]

    for j, (label, action) in enumerate(extra_actions):
        btn_y = y_offset + (len(sensation_colors) + j) * spacing
        if window_width - 150 <= x <= window_width - 50 and btn_y <= y <= btn_y + 25:
            action()
            return

# Mouse event handlers
def on_left_press(obj, event):
    mouse_down["left"] = not mouse_down["left"]
    print("set mouse down to true")
    handle_mouse_click()
    draw_on_foot()

def on_mouse_move(obj, event):
    if mouse_down["left"]:
        print("mouse is held down")
        draw_on_foot()

def on_left_release(obj, event):
    
    print("mouse is up")

# Register mouse event observers
plotter.iren.add_observer("LeftButtonPressEvent", on_left_press)
plotter.iren.add_observer("MouseMoveEvent", on_mouse_move)
plotter.iren.add_observer("LeftButtonReleaseEvent", on_left_release)

# Initialize UI
update_buttons("none")

# Show plotter window
plotter.show()