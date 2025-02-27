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

# State to determine whether the screen rotation is active or not
coloring_mode = [False]

# Add a text indicator for coloring mode
text_actor = plotter.add_text("Coloring Mode: OFF", position="upper_left", font_size=14)

# Save the default interactor style
interactor = plotter.iren  # Get interactor
default_interactor_style = interactor.get_interactor_style()  # Save default style

# Function to toggle coloring mode
def toggle_coloring_mode():
    coloring_mode[0] = not coloring_mode[0]
    if coloring_mode[0]:
        # Set interaction mode to picking only (disabling camera rotation)
        new_style = vtk.vtkInteractorStyleTrackballActor()  # Only allows picking objects
        interactor.SetInteractorStyle(new_style)
        text_actor.SetText(0, "Coloring Mode: ON")
    else:
        # Restore default interaction (camera movement enabled)
        interactor.SetInteractorStyle(default_interactor_style)
        text_actor.SetText(0, "Coloring Mode: OFF")
    plotter.render()

# Function to colorize a face on mouse click
def colorize_on_click(picked_info):
    if not coloring_mode[0]:  # Only allow coloring if in coloring mode
        return
    picked_cell_id = picked_info.cell_id
    if picked_cell_id is not None and picked_cell_id >= 0:
        # Change the color of the selected cell (e.g., red for highlighting)
        colors[picked_cell_id] = [1.0, 0.0, 0.0]  # Red for marking
        mesh.cell_data["face_colors"] = colors
        plotter.update_scalars(colors)  # Update the plotter to reflect changes

# Simulate a button with a text label and a mouse click event
button_actor = plotter.add_text("Toggle Coloring", position=(10, 10), font_size=12, color="blue")
button_click_area = [10, 110, 10, 40]  # [x_min, x_max, y_min, y_max]

# Function to check if a mouse click is within the button area
def handle_mouse_click(*args):
    click_position = plotter.iren.get_event_position()
    x, y = click_position
    if button_click_area[0] <= x <= button_click_area[1] and button_click_area[2] <= y <= button_click_area[3]:
        toggle_coloring_mode()

# Enable cell picking and use `colorize_on_click` as the callback
plotter.enable_cell_picking(callback=colorize_on_click, show_message=False, through=False)

# Register mouse click event to detect button clicks
plotter.iren.add_observer("LeftButtonPressEvent", handle_mouse_click)

# Show interactive window
plotter.show()