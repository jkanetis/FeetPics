import pyvista as pv
import numpy as np
import pandas as pd

# Load the modified mesh
mesh = pv.read("modified_mesh.vtk")

# Check if 'face_colors' data exists in mesh.cell_data
if 'face_colors' in mesh.cell_data:
    # Assign the 'face_colors' to be used in visualization
    colors = mesh.cell_data['face_colors']
    
    # Visualize the mesh with the cell colors, and hide the orientation axes
    mesh.plot(scalars=colors, rgb=True, show_axes=False)
else:
    print("No 'face_colors' found in cell_data.")



# Ensure 'face_colors' data exists in mesh.cell_data
if 'face_colors' in mesh.cell_data:
    # Retrieve the cell data to export
    cell_data = mesh.cell_data['face_colors']

    # Access the faces and points array
    faces = mesh.faces
    n_faces = mesh.n_faces
    points = mesh.points
    offset = 0

    # Prepare a list to store data
    face_vertex_data = []

    # Iterate through each face
    for i in range(n_faces):
        n_vertices = faces[offset]  # Number of vertices in this face
        vertex_indices = faces[offset + 1 : offset + 1 + n_vertices]
        
        # Retrieve the coordinates for each vertex in the current face
        vertex_coords = points[vertex_indices]

        # Format the coordinates for CSV output as a string
        vertex_coords_str = ["({}, {}, {})".format(x, y, z) for x, y, z in vertex_coords]
        
        color = cell_data[i]  # Get the color for this face

        # Append the vertex coordinates and color data to the list
        face_vertex_data.append({
            'Face_Index': i,
            'Vertex_Coordinates': "; ".join(vertex_coords_str),
            'Red': color[0],
            'Green': color[1],
            'Blue': color[2]
        })

        # Move to the next face's starting index in the array
        offset += 1 + n_vertices

    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(face_vertex_data)

    # Save the DataFrame to a CSV file
    csv_file = "face_data_with_vertex_coords.csv"
    df.to_csv(csv_file, index=False)
    
    print(f"Face data with vertex coordinates and colors has been saved to {csv_file}")
else:
    print("No 'face_colors' found in cell_data.")