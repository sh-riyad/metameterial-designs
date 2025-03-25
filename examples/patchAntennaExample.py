# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

#%%
import numpy as np
import matplotlib.pyplot as plt
import context
import cst_python_api as cpa


projectName = "Patch_Antenna_Example"

# Create the CST project
myCST = cpa.CST_MicrowaveStudio(context.dataFolder, projectName + ".cst")

# Set the default units for the project
myCST.Project.setUnits()

######################
#
# CREATE THE 3D MODEL
#
######################
#%%
# Definition of the geometry parameters for the antenna
patchWidth = 28.45
patchLength = 28.45
feedPoint = 9
feedLineWidth = 1.137
feedingGap = 1
substrateWidth = 2 * patchWidth
substrateLength = 2 * patchLength
condThickness = 0.035
substrateThickness = 1.6

# Add FR4 material to the project
myCST.Build.Material.addNormalMaterial(
    "FR4 (Lossy)", 4.3, 1.0, colour=[0.94, 0.82, 0.76], tanD = 0.025)

# Create ground plane
myCST.Build.Shape.addBrick(
    xMin = -0.5*substrateWidth, xMax = 0.5*substrateWidth,
    yMin = -0.5*substrateLength, yMax = 0.5*substrateLength,
    zMin = 0.0, zMax = condThickness,
    name = "Groundplane", component = "component1", material="PEC"
)

# Create substrate
myCST.Build.Shape.addBrick(
    xMin = -0.5*substrateWidth, xMax = 0.5*substrateWidth,
    yMin = -0.5*substrateLength, yMax = 0.5*substrateLength,
    zMin = condThickness, zMax = condThickness+substrateThickness, 
    name = "Substrate", component = "component1", material="FR4 (Lossy)"
)

# Create patch
myCST.Build.Shape.addBrick(
    xMin = -0.5*patchWidth, xMax = 0.5*patchWidth,
    yMin = -0.5*patchLength, yMax = 0.5*patchLength,
    zMin = condThickness+substrateThickness,
    zMax = 2*condThickness+substrateThickness,
    name = "Patch", component = "component1", material="PEC"
)

# Create feeding gap
myCST.Build.Shape.addBrick(
    xMin = -(0.5*feedLineWidth + feedingGap),
    xMax = (0.5*feedLineWidth + feedingGap),
    yMin = -0.5*patchLength, yMax = -0.5*patchLength + feedPoint,
    zMin = condThickness+substrateThickness,
    zMax = 2*condThickness+substrateThickness,
    name = "Feeding_gap", component = "component1", material="Vacuum"
)

# Subtract the feeding gap from the patch
myCST.Build.Boolean.subtract("component1:Patch", "component1:Feeding_gap")

# Create feed line
myCST.Build.Shape.addBrick(
    xMin = -0.5*feedLineWidth, xMax = 0.5*feedLineWidth,
    yMin = -0.5*substrateLength, yMax = -0.5*patchLength + feedPoint,
    zMin = condThickness+substrateThickness,
    zMax = 2*condThickness+substrateThickness,
    name = "Feed_line", component = "component1", material="PEC"
)

# Join the feed line and the patch
myCST.Build.Boolean.add("component1:Patch", "component1:Feed_line")

###########################
#
# CONFIGURE THE SIMULATION
#
###########################

myCST.Solver.setFrequencyRange(1.5, 3.5)

# Set the bounding box limits
myCST.Solver.setBackgroundLimits(
    xMin = 0.0, xMax = 0.0,
    yMin = 0.0, yMax = 0.0,
    zMin = 0.0, zMax = 0.0,
)

# Set the boundary conditions
myCST.Solver.setBoundaryCondition(
    xMin = "expanded open", xMax = "expanded open",
    yMin = "expanded open", yMax = "expanded open",
    zMin = "expanded open", zMax = "expanded open",
)

# Define excitation port
myCST.Solver.Port.addWaveguidePort(
    xMin =-substrateWidth/2, xMax = substrateWidth/2,
    yMin = -substrateLength/2, yMax = -substrateLength/2,
    zMin = -1.6, zMax = 8.035,
    orientation = "ymin", nModes = 1
)

# Set the field monitors
myCST.Solver.addFieldMonitor("Efield", 2.48)
myCST.Solver.addFieldMonitor("Hfield", 2.48)
myCST.Solver.addFieldMonitor("Farfield", 2.48)

# Set the solver type
myCST.Solver.changeSolverType("HF Time Domain")

##############################################
#
# RUN THE SIMULATION AND RETRIEVE THE RESULTS
#
##############################################
#%%
# Launch the simulation
myCST.Solver.runSimulation()

#%%
# Retrieve S-Parameters results
freq, S11 = myCST.Results.getSParameters(1, 1)

# Retrieve farfield results
vTheta = np.arange(-180, 181, 1)
vPhi = np.array([0, 45, 90])
farField = myCST.Results.getFarField(
    2.48, vTheta, vPhi, port = 1, coordSys="ludwig3",
    component=["vertical", "horizontal"])

#%%
# PLOT THE S-PARAMETERS RESULTS
# Create a new figure
plt.figure(0)
# Plot the retrieved results
plt.plot(freq, 20*np.log10(np.abs(S11)), color="C0")
# Decorate the figure
plt.xlabel("Frequency (GHz)")
plt.ylabel("$|S_{11}|$ (dB)")
plt.legend()
plt.grid()
plt.show()

# PLOT THE FARFIELD RESULTS
# Create a new figure
plt.figure(1)
# Plot the retrieved results
plt.plot(vTheta, farField[0][:,0], color="green", label="$\phi=0^\circ$ (Cop)")
plt.plot(vTheta, farField[1][:,0], color="green", label="$\phi=0^\circ$ (Cxp)", linestyle="dashed")
plt.plot(vTheta, farField[0][:,2], color="blue", label="$\phi=90^\circ$ (Cop)")
plt.plot(vTheta, farField[1][:,2], color="blue", label="$\phi=90^\circ$ (Cxp)", linestyle="dashed")
plt.plot(vTheta, farField[0][:,1], color="red", label="$\phi=45^\circ$ (Cop)")
plt.plot(vTheta, farField[1][:,1], color="red", label="$\phi=45^\circ$ (Cxp)", linestyle="dashed")
# Decorate the figure
plt.xlabel("$\\theta (^\circ)$")
plt.ylabel("Directivity (dBi)")
plt.title("farfield (f=2.48) [1]")
plt.ylim((-51,11))
plt.legend()
plt.grid()
plt.show()