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

# State to track coloring mode
coloring_mode = [False]

# Add a single text actor for coloring mode
text_actor = plotter.add_text("Coloring Mode: OFF", position=(10, 550), font_size=14, name="coloring_text")

# Function to toggle coloring mode
def toggle_coloring_mode():
    coloring_mode[0] = not coloring_mode[0]
    plotter.remove_actor("coloring_text")  # Remove old text
    plotter.add_text(
        "Coloring Mode: ON" if coloring_mode[0] else "Coloring Mode: OFF",
        position=(10, 550), font_size=14, name="coloring_text"
    )
    plotter.render()

# Function to color a face when Shift + Click is used
def colorize_on_click(picked_info):
    if not coloring_mode[0]:  # Only allow coloring if mode is ON
        return

    picked_cell_id = picked_info.cell_id
    if picked_cell_id is not None and picked_cell_id >= 0:
        # Set color to red
        colors[picked_cell_id] = [1.0, 0.0, 0.0]  
        mesh.cell_data["face_colors"] = colors
        plotter.update_scalars(colors)  # Update the plotter

# Function to detect Shift key press
def on_key_press(obj, event):
    key = obj.GetKeySym()  # Get key name
    if key.lower() == "shift":  # If Shift key is pressed
        plotter.enable_cell_picking(callback=colorize_on_click, show_message=False, through=False)

# Function to detect Shift key release
def on_key_release(obj, event):
    key = obj.GetKeySym()  # Get key name
    if key.lower() == "shift":  # If Shift key is released
        plotter.enable_cell_picking(callback=None, show_message=False, through=False)

# Add a text button to toggle coloring mode
plotter.add_text("Toggle Coloring", position=(10, 10), font_size=12, color="blue", name="toggle_button")

# Function to detect button clicks
def handle_mouse_click(*args):
    click_position = plotter.iren.get_event_position()
    x, y = click_position
    if 10 <= x <= 110 and 10 <= y <= 40:  # If clicked within button bounds
        toggle_coloring_mode()

# Register Shift key press and release events
plotter.iren.add_observer("KeyPressEvent", on_key_press)
plotter.iren.add_observer("KeyReleaseEvent", on_key_release)

# Register mouse click event for toggling coloring mode
plotter.iren.add_observer("LeftButtonPressEvent", handle_mouse_click)

# Show interactive window
plotter.show()