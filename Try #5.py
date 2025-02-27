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
coloring_mode = [False]  # Whether the user is in drawing mode
selected_region = set()  # Stores the cell IDs that can be colored

# PyVista Picker for selecting cells
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.01)

# UI: Add text for color mode and region selection
plotter.add_text("Color Mode: OFF", position=(10, 50), font_size=12, color="blue", name="color_mode_button")
plotter.add_text("Select a Region", position=(10, 80), font_size=12, color="green", name="region_text")
plotter.add_text("Quit", position=(10, 110), font_size=12, color="red", name="quit_button")

# Function to toggle coloring mode
def toggle_coloring_mode():
    if not selected_region:
        print("Select a region before coloring!")
        return

    coloring_mode[0] = not coloring_mode[0]
    plotter.remove_actor("color_mode_button")  # Remove old text
    plotter.add_text(
        "Color Mode: ON" if coloring_mode[0] else "Color Mode: OFF",
        position=(10, 50), font_size=12, color="blue", name="color_mode_button"
    )
    plotter.render()

# Function to quit the application
def quit_application():
    plotter.close()

# Function to select a region (user clicks on a part of the foot)
def select_region(*args):
    x, y = plotter.iren.get_event_position()
    picker.Pick(x, y, 0, plotter.renderer)
    picked_cell_id = picker.GetCellId()

    if picked_cell_id >= 0:
        selected_region.clear()  # Clear previous selection
        selected_region.add(picked_cell_id)

        # Highlight the selected region by changing its color (yellow)
        colors[picked_cell_id] = [1.0, 1.0, 0.0]  
        mesh.cell_data["face_colors"] = colors
        plotter.update_scalars(colors)

        # Update UI
        plotter.remove_actor("region_text")
        plotter.add_text("Region Selected", position=(10, 80), font_size=12, color="green", name="region_text")
        plotter.render()

# Function to color faces (only in the selected region)
def colorize_on_drag(*args):
    if not coloring_mode[0] or not selected_region:  # Check if coloring is enabled & region selected
        return

    x, y = plotter.iren.get_event_position()
    picker.Pick(x, y, 0, plotter.renderer)
    picked_cell_id = picker.GetCellId()

    if picked_cell_id in selected_region:  # Only color selected region
        colors[picked_cell_id] = [1.0, 0.0, 0.0]  # Set color to red
        mesh.cell_data["face_colors"] = colors
        plotter.update_scalars(colors)

# Function to detect button clicks
def handle_mouse_click(*args):
    x, y = plotter.iren.get_event_position()

    # Check if clicked within the "Color Mode" button bounds
    if 10 <= x <= 140 and 50 <= y <= 80:
        toggle_coloring_mode()

    # Check if clicked within the "Quit" button bounds
    elif 10 <= x <= 60 and 110 <= y <= 140:
        quit_application()

# Register mouse events
plotter.iren.add_observer("LeftButtonPressEvent", select_region)  # Select region when clicking
plotter.iren.add_observer("MouseMoveEvent", colorize_on_drag)  # Allow coloring only in selected region
plotter.iren.add_observer("LeftButtonPressEvent", handle_mouse_click)  # Handle UI button clicks

# Show interactive window
plotter.show()