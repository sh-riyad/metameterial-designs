import os
import context
import cst_python_api as cpa
import numpy as np
import matplotlib.pyplot as plt
from Database import save_simulation_parameters


projectName = "217"

# Create the substrate (using FR-4 (lossy) material)
ls = 10.0   # Substrate length change 8 to 10
hs = 1.6  # Substrate height change 1.6 to 2.0

t = 0.045 # Thickness of copper layers change to 0.035 to 0.045
gc = 0.8 # Global Cut  Change 0.3 to 0.5 then 0.8

l1 = 9.16 # outer_box length
w1 = 1.5 # wide change 1 to 1.2 then 1.5

ed1 = 6.0 # outer circle
id1 = 5.0 # outer circle


l2 = 3.0 # inner_box

ed2 = 2.5  # Inner circle
id2 = 2.0 # Inner Circle


# Create the CST project
myCST = cpa.CST_MicrowaveStudio(context.dataFolder, projectName + ".cst")

# Set the default units for the project
myCST.Project.setUnits()

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

myCST.Build.Shape.addBrick(
    xMin=-ls, xMax=ls,
    yMin=-ls, yMax=ls,
    zMin=-hs,    zMax=0.0,
    name="Substrate", component="component1", material="FR4 (Lossy)"
)

# --------------------------------------------------------------------------------------------

# Create the outer box (copper material) for the outer ring
myCST.Build.Shape.addBrick(
    xMin=-l1, xMax=l1,
    yMin=-l1, yMax=l1,
    zMin=0.0,     zMax=t,
    name="Outer Box", component="component1", material="Copper (pure)"
)

# Create a brick to hollow out the outer ring ("Cut1")
myCST.Build.Shape.addBrick(
    xMin=-l1 + w1, xMax=l1 - w1,
    yMin=-l1 + w1, yMax=l1 - w1,
    zMin=0.0,         zMax=t,
    name="Cut1", component="component1", material="Copper (pure)"
)

myCST.Build.Boolean.subtract("component1:Outer Box", "component1:Cut1")


myCST.Build.Shape.addBrick(
    xMin=-gc, xMax=gc,
    yMin=-l1 - gc, yMax=l1+ gc ,
    zMin=0.0,      zMax=t,
    name="Cut2", component="component1", material="Copper (pure)"
)
myCST.Build.Boolean.subtract("component1:Outer Box", "component1:Cut2")

myCST.Build.Shape.addBrick(
    xMin=-l1- gc, xMax=l1+ gc,
    yMin=-gc, yMax=gc,
    zMin=0.0,      zMax=t,
    name="Cut3", component="component1", material="Copper (pure)"
)
myCST.Build.Boolean.subtract("component1:Outer Box", "component1:Cut3")

# ----------------------------------------------------------------------------------------------------------

myCST.Build.Shape.addCylinder(
    xMin=0.0,
    yMin=0.0,
    zMin=0.0,
    extRad=ed1,
    intRad=id1,
    name="Outer Circle",
    component="component1",
    material="Copper (pure)",
    orientation='z',
    zMax=t
)

myCST.Build.Shape.addBrick(
    xMin= -gc, xMax = gc,
    yMin=-ed1, yMax=ed1,
    zMin=0.0,      zMax=t,
    name="Cut4", component="component1", material="Copper (pure)"
)
myCST.Build.Boolean.subtract("component1:Outer Circle", "component1:Cut4")

myCST.Build.Shape.addBrick(
    xMin=-ed1, xMax=ed1,
    yMin=-gc, yMax=gc ,
    zMin=0.0,      zMax=t,
    name="Cut5", component="component1", material="Copper (pure)"
)
myCST.Build.Boolean.subtract("component1:Outer Circle", "component1:Cut5")



#----------------------------------------------------------------------------------------------------------------------
myCST.Build.Shape.addBrick(
    xMin=-l2, xMax=l2,
    yMin=-l2, yMax=l2,
    zMin=0.0,         zMax=t,
    name="Inner Box", component="component1", material="Copper (pure)"
)

myCST.Build.Shape.addBrick(
    xMin = -gc, xMax = gc,
    yMin=-l2, yMax=l2,
    zMin=0.0,      zMax=t,
    name="Cut6", component="component1", material="Copper (pure)"
)
myCST.Build.Boolean.subtract("component1:Inner Box", "component1:Cut6")

# -------------------------------------------------------------------------------------------
myCST.Build.Shape.addCylinder(
    xMin=0.0,
    yMin=0.0,
    zMin=0.0,
    extRad=ed2,
    intRad=id2,
    name="Cut7",
    component="component1",
    material="Copper (pure)",
    orientation='z',
    zMax=t
)

myCST.Build.Boolean.subtract("component1:Inner Box", "component1:Cut7")

#----------------------------------------------------------------------------------------------------

myCST.Solver.setFrequencyRange(20.0, 32.0)


# Set the boundary conditions
myCST.Solver.setBoundaryCondition(
    xMin = "unit cell", xMax = "unit cell",
    yMin = "unit cell", yMax = "unit cell",
    zMin = "expanded open", zMax = "expanded open",
)

# Set floquet ports
myCST.Solver.defineFloquetModes(1)

myCST.Solver.changeSolverType("HF Frequency Domain")

myCST.Solver.stimulation("Zmin", "TE(0,0)")

myCST.Solver.runSimulation()

current_dir = os.getcwd()
output_dir = os.path.join(current_dir, "output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
myCST.saveFile(folder=output_dir, filename=f"{projectName}.cst", includeResults=True)

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

# Get min S11 and S21 and their frequencies (in GHz)
s11_db = 20 * np.log10(np.abs(SMin1Min1))
s21_db = 20 * np.log10(np.abs(SMax1Min1))


min_s11_index = np.argmin(s11_db)
min_s21_index = np.argmin(s21_db)

params = {
    "project_name": projectName,
    "ls": ls,
    "hs": hs,
    "t": t,
    "gc": gc,
    "l1": l1,
    "ed1": ed1,
    "id1": id1,
    "l2": l2,
    "ed2": ed2,
    "id2": id2,
    "s11_freq": freq[min_s11_index],  # Frequency at min S11
    "s11_db": s11_db[min_s11_index],  # Min S11 in dB
    "s21_freq": freq[min_s21_index],  # Frequency at min S21
    "s21_db": s21_db[min_s21_index],  # Min S21 in dB
}

save_simulation_parameters(params)

#%%
# PLOT THE S-PARAMETERS RESULTS
plt.figure(0)
# Plot the retrieved results
plt.plot(freq, 20*np.log10(np.abs(SMin1Min1)), color="C0", label="Zmin(1),Zmin(1)")
plt.plot(freq, 20*np.log10(np.abs(SMax1Min1)), color="C2", label="Zmax(1),Zmin(1)")
plt.xlabel("Frequency (GHz)")
plt.ylabel("$|S_{ij}|$ (dB)")
plt.legend()
plt.grid()
plt.show()