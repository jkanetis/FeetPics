import pyvista as pv
import numpy as np

# Load the mesh
mesh = pv.read("new.ply")  # Substitute with your actual file name

# Generate random RGB colors for each point
colors = np.random.randint(0, 256, size=(mesh.n_points, 3), dtype=np.uint8)

# Add RGB as separate channels
mesh.point_data['red'] = colors[:, 0]
mesh.point_data['green'] = colors[:, 1]
mesh.point_data['blue'] = colors[:, 2]

# Visualize the changes
mesh.plot(scalars=colors, rgb=True)

# Save the modified mesh
modified_file = "modified_mesh.vtk"
mesh.save(modified_file)

# # Load the new mesh with the modified changes
# modified_mesh = pv.read(modified_file)

# # Visualize the new mesh to confirm changes
# modified_mesh.plot(scalars=colors, rgb=True)

