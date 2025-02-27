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

# Track coloring mode & camera state
coloring_mode = [False]
camera_locked = [False]

# PyVista Picker for selecting cells
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.01)

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
 
# Function to start coloring (locks camera)
def start_coloring(*args):
    if coloring_mode[0]:  # Only allow coloring if mode is ON
        global camera_locked
        camera_locked = True  # Disable camera movement
        plotter.iren.interactor_style = None  # Lock camera rotation

# Function to stop coloring (restores camera)
def stop_coloring(*args):
    global camera_locked
    camera_locked = False  # Enable camera movement
    plotter.enable_trackball_actor_style()  # Restore normal interaction

# Function to color faces while dragging
def colorize_on_drag(*args):
    if not coloring_mode[0]:  # Only allow coloring if mode is ON
        return

    x, y = plotter.iren.get_event_position()  # Get mouse position
    picker.Pick(x, y, 0, plotter.renderer)  # Perform picking

    picked_cell_id = picker.GetCellId()  # Get the picked cell ID
    if picked_cell_id >= 0:
        # Set color to red
        colors[picked_cell_id] = [1.0, 0.0, 0.0]  
        mesh.cell_data["face_colors"] = colors
        plotter.update_scalars(colors)  # Update the plotter

# Add a text button to toggle coloring mode
plotter.add_text("Toggle Coloring", position=(10, 10), font_size=12, color="blue", name="toggle_button")

# Function to detect button clicks
def handle_mouse_click(*args):
    click_position = plotter.iren.get_event_position()
    x, y = click_position
    if 10 <= x <= 110 and 10 <= y <= 40:  # If clicked within button bounds
        toggle_coloring_mode()

# Register mouse events
plotter.iren.add_observer("LeftButtonPressEvent", start_coloring)  # Disable rotation on click
plotter.iren.add_observer("MouseMoveEvent", colorize_on_drag)  # Enable coloring on drag
plotter.iren.add_observer("LeftButtonReleaseEvent", stop_coloring)  # Re-enable rotation on release

# Register mouse click event for toggling coloring mode
plotter.iren.add_observer("LeftButtonPressEvent", handle_mouse_click)

# Show interactive window
plotter.show()