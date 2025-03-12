import pyvista as pv
import numpy as np

# Load the 3D model
mesh = pv.read("duck.obj")

# Start PyVista plotter
plotter = pv.Plotter()

# Initialize colors array for each face (cell)
colors = np.ones((mesh.n_cells, 3)) * 0.5  # Set initial gray color for each face
mesh.cell_data["face_colors"] = colors

# Add the mesh to the plotter, specifying cell scalars for face coloring
plotter.add_mesh(mesh, scalars="face_colors", rgb=True)

# Load the 3D model
mesh = pv.read("duck.obj")

# Function to get the coordinates of the vertices for a specific cell
def get_cell_coordinates(mesh, cell_id):
    # Extract the cell
    cell = mesh.extract_cells(cell_id)
    # Get the coordinates of the points (vertices) that make up the cell
    cell_points = cell.points
    return cell_points

# Example: Get the coordinates of the vertices for the first cell
cell_id = 0
cell_coordinates = get_cell_coordinates(mesh, cell_id)
print(f"Coordinates of the vertices for cell {cell_id}:")
print(cell_coordinates)



# Callback function to colorize face on mouse click
def colorize_on_click(picked_info):
    # Get the ID of the picked cell
    picked_cell_id = picked_info.cell_id
    if picked_cell_id is not None and picked_cell_id >= 0:  # Check if a cell was actually picked
        # Change color of the selected cell to blue
        colors[picked_cell_id] = [0.0, 0.0, 1.0]  # Set to blue
        # Update mesh face colors
        mesh.cell_data["face_colors"] = colors
        plotter.update_scalars(colors)  # Update plotter to reflect changes

# Enable cell picking and use `colorize_on_click` as the callback
plotter.enable_cell_picking(callback=colorize_on_click, show_message=False, through=False)

# Show interactive window
plotter.show()