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

# Function to change the color of a known cell
def change_cell_color(cell_id, color):
    colors[cell_id] = color
    mesh.cell_data["face_colors"] = colors
    plotter.update_scalars(colors)  # Update plotter to reflect changes

# Example: Change the color of cell 0 to red
change_cell_color(0, [1.0, 0.0, 0.0])  # Set to red

# Callback function to colorize face on mouse click and get centroid
def colorize_on_click(picked_info):
    print(f"Picked cell: {picked_info.cell}")
    print(f"Picked points: {picked_info.points}")

    # Get the picked cell
    picked_cell = picked_info.cell
    if picked_cell is not None:
        # Find the cell ID by comparing the picked cell with the mesh cells
        for cell_id in range(mesh.n_cells):
            if np.array_equal(mesh.extract_cells(cell_id).points, picked_cell.points):
                # Change color of the selected cell to blue
                change_cell_color(cell_id, [0.0, 0.0, 1.0])  # Set to blue
                # Get the coordinates of the vertices for the picked cell
                cell_coordinates = get_cell_coordinates(mesh, cell_id)
                # Calculate the centroid of the picked cell
                centroid = np.mean(cell_coordinates, axis=0)
                print(f"Centroid of the cell {cell_id}: {centroid}")
                break

# Enable cell picking and use `colorize_on_click` as the callback
plotter.enable_cell_picking(callback=colorize_on_click, show_message=False, through=False)

# Show interactive window
plotter.show()