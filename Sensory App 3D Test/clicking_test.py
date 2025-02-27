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


# Callback function to get the coordinates where clicked
def get_click_coordinates(point):
    print(f"Clicked coordinates: {point}")

# Enable point picking and use `get_click_coordinates` as the callback
plotter.enable_point_picking(callback=get_click_coordinates, show_message=False)

# Show interactive window
plotter.show()