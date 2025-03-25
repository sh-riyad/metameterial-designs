# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

#%%
import numpy as np
import matplotlib.pyplot as plt
import context
import cst_python_api as cpa
import os

projectName = "Temp_file"

# Create the CST project
myCST = cpa.CST_MicrowaveStudio(context.dataFolder, projectName + ".cst")

# Set the default units for the project
myCST.Project.setUnits()


# Define geometric parameters for the metamaterial unit cell
g  = 3.0     # Gap width
h  = 2.5   # Substrate height
l1 = 22.0    # Outer ring length
l2 = 15.0    # Inner ring length
ls = 25.0    # Substrate length
lw = 1.4  # Wire width
s  = 1.5   # Spacing between outer and inner rings
t  = 0.17  # Thickness of copper layers
w  = 2.0     # Width of the rings

# --------------------------------------------------------------------------------------------
# Add FR4 material to the project
myCST.Build.Material.addNormalMaterial(
    "FR4 (Lossy)", 4.3, 1.0, colour=[0.94, 0.82, 0.76], tanD=0.025)

# Add Copper (pure) material to the project
myCST.Build.Material.addNormalMaterial(
    "Copper (pure)",    # Material name
    1.0,                # Epsilon (relative permittivity)
    1.0,                # Mu (relative permeability)
    colour=[0.85, 0.55, 0.2],  # RGB color (values between 0 and 1)
    tanD=0.0,           # Electric loss tangent
    sigma=5.96e7,       # Electric conductivity in S/m
    tanDM=0.0,          # Magnetic loss tangent (not used for metals)
    sigmaM=0.0          # Magnetic conductivity
)


# Create the substrate (using FR-4 (lossy) material)
myCST.Build.Shape.addBrick(
    xMin=-ls/2, xMax=ls/2,
    yMin=-ls/2, yMax=ls/2,
    zMin=-h,    zMax=0.0,
    name="Substrate", component="component1", material="FR4 (Lossy)"
)

# --------------------------------------------------------------------------------------------
# Create the outer box (copper material) for the outer ring
myCST.Build.Shape.addBrick(
    xMin=-l1/2, xMax=l1/2,
    yMin=-l1/2, yMax=l1/2,
    zMin=0.0,     zMax=t,
    name="Outer Box", component="component1", material="Copper (pure)"
)

# Create a brick to hollow out the outer ring ("Cut1")
myCST.Build.Shape.addBrick(
    xMin=-(l1/2)+w, xMax=(l1/2)-w,
    yMin=-(l1/2)+w, yMax=(l1/2)-w,
    zMin=0.0,         zMax=t,
    name="Cut1", component="component1", material="Copper (pure)"
)

# Subtract Cut1 from Outer Box to create the ring shape
myCST.Build.Boolean.subtract("component1:Outer Box", "component1:Cut1")

# Create another brick ("Cut2") for an additional subtraction on the outer ring
myCST.Build.Shape.addBrick(
    xMin=-2.0, xMax=2.0,
    yMin=-l1/2, yMax=-(l1/2)+w,
    zMin=0.0,     zMax=t,
    name="Cut2", component="component1", material="Copper (pure)"
)

# Subtract Cut2 from Outer Box
myCST.Build.Boolean.subtract("component1:Outer Box", "component1:Cut2")

# --------------------------------------------------------------------------------------------
# Create the inner box (copper material) for the inner ring
myCST.Build.Shape.addBrick(
    xMin=-l2/2, xMax=l2/2,
    yMin=-l2/2, yMax=l2/2,
    zMin=0.0,     zMax=t,
    name="Inner Box", component="component1", material="Copper (pure)"
)

# Create a brick ("Cut3") to hollow out the inner ring
myCST.Build.Shape.addBrick(
    xMin=-(l2/2)+w, xMax=(l2/2)-w,
    yMin=-(l2/2)+w, yMax=(l2/2)-w,
    zMin=0.0,         zMax=t,
    name="Cut3", component="component1", material="Copper (pure)"
)

# Subtract Cut3 from Inner Box
myCST.Build.Boolean.subtract("component1:Inner Box", "component1:Cut3")

# Create another brick ("Cut4") for an additional subtraction on the inner ring
myCST.Build.Shape.addBrick(
    xMin=-2.0, xMax=2.0,
    yMin=(l2/2)-w, yMax=l2/2,
    zMin=0.0,       zMax=t,
    name="Cut4", component="component1", material="Copper (pure)"
)

# Subtract Cut4 from Inner Box
myCST.Build.Boolean.subtract("component1:Inner Box", "component1:Cut4")


#%%
###########################
#
# CONFIGURE THE SIMULATION
#
###########################

myCST.Solver.setFrequencyRange(5.0, 15.0)


# Set the boundary conditions
myCST.Solver.setBoundaryCondition(
    xMin = "unit cell", xMax = "unit cell",
    yMin = "unit cell", yMax = "unit cell",
    zMin = "expanded open", zMax = "expanded open",
)

# Set floquet ports
myCST.Solver.defineFloquetModes(1)


# Set the solver type
myCST.Solver.changeSolverType("HF Frequency Domain")

myCST.Solver.stimulation("Zmin", "TE(0,0)")


##############################################
#
# RUN THE SIMULATION AND RETRIEVE THE RESULTS
#
##############################################
#%%
# Launch the simulation
myCST.Solver.runSimulation()

# Save the file with results
current_dir = os.getcwd()
output_dir = os.path.join(current_dir, "output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
myCST.saveFile(folder=output_dir, filename=f"{projectName}.cst", includeResults=True)


#
# #%%
# # Retrieve the S-Parameters results
freq, SMin1Min1 = myCST.Results.getSParameters(-1, -1, 1, 1)
_,    SMax1Min1 = myCST.Results.getSParameters(0, -1, 1, 1)


# Combine the results into a 2D array:
# Columns: Frequency, Re(SMin1Min1), Im(SMin1Min1), Re(SMax1Min1), Im(SMax1Min1)
data = np.column_stack((
    freq,
    np.real(SMin1Min1), np.imag(SMin1Min1),
    np.real(SMax1Min1), np.imag(SMax1Min1)
))

# Define a header for the CSV file
header = "Frequency, Re(SMin1Min1), Im(SMin1Min1), Re(SMax1Min1), Im(SMax1Min1)"

# Save the data to a CSV file in your output directory
csv_filename = os.path.join(output_dir, f"{projectName}.csv")
np.savetxt(csv_filename, data, delimiter=",", header=header, comments="")


#%%
# PLOT THE S-PARAMETERS RESULTS
# Create a new figure
plt.figure(0)
# Plot the retrieved results
plt.plot(freq, 20*np.log10(np.abs(SMin1Min1)), color="C0", label="Zmin(1),Zmin(1)")
plt.plot(freq, 20*np.log10(np.abs(SMax1Min1)), color="C2", label="Zmax(1),Zmin(1)")
# Decorate the figure
plt.xlabel("Frequency (GHz)")
plt.ylabel("$|S_{ij}|$ (dB)")
plt.legend()
plt.grid()
plt.show()