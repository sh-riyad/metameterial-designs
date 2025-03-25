# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

################################
#                              #
# Unit tests for Results class #
#                              #
################################

import unittest
import os.path
import time
import numpy as np
import matplotlib.pyplot as plt
from .context import cst_python_api as cpa
from .context import dataFolder
from .auxiliaryTestFunctions import restoreTestEnvironment

class TestResults(unittest.TestCase):
    
    def test_getSParameters(self):
        """Open an existing project, try to retrieve its S-Parameter results and
        plot them. NOTE: The project must have been simulated before running the
        test.
        """
        
        self.projectName = "Waveguide_Array"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Results object and pass to it the COM object to control the
        # example project
        self.myResults = cpa.Results(self.myCST._CST_MicrowaveStudio__MWS)
        
        freq, S11 = self.myResults.getSParameters(1, 1, modeA=1, modeB=1)
        freq, SMax11 = self.myResults.getSParameters(0, 1, modeA=1, modeB=1)
        _, SMax21 = self.myResults.getSParameters(0, 1, modeA=2, modeB=1)
        
        plt.plot(freq, 20*np.log10(np.abs(S11)), color="C0", label="$S_{1(1),1(1)}$")
        plt.plot(freq, 20*np.log10(np.abs(SMax11)), color="C1", label="$S_{ZMax(1),1(1)}$")
        plt.plot(freq, 20*np.log10(np.abs(SMax21)), color="C2", label="$S_{ZMax(2),1(1)}$")
        plt.xlabel("Frequency (GHz)")
        plt.ylabel("$|S_{i,j}|$ (dB)")
        plt.legend()
        plt.grid()
        plt.show()
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # portA or portB not of type int
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getSParameters(42.0, 1)
        # portA or portB smaller that -1
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getSParameters(1, -2)
        # modeA or modeB not of type int
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getSParameters(1, 1, modeA=42.0, modeB=1)
        # modeA or modeB smaller than 0
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getSParameters(1, 1, modeA=1, modeB=-1)
        # Only one of the two mode numbers is equal to 0
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getSParameters(1, 1, modeA=0, modeB=2)
        # runID not of type int
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getSParameters(1, 1, runID=42.0)
        # runID smaller than 0
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getSParameters(1, 1, runID=-1)
        # runID not present in the project
        with self.assertRaises(RuntimeError):
            _, _ = self.myResults.getSParameters(1, 1, runID=417)
        
        return
    
    def test_getFarField(self):
        """Open an existing project, try to retrieve its farfield results and
        plot them. NOTE: The project must have been simulated before running the
        test.
        """
        
        self.projectName = "Radiating_Waveguide"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Results object and pass to it the COM object to control the
        # example project
        self.myResults = cpa.Results(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Define the theta and phi points over which the radiation pattern will
        # be calculated
        theta = np.arange(-180, 181, 1)
        phi = np.array([0, 45, 90])
        
        # Retrieve the directivity pattern in dB scale for one of the farfield
        # monitors
        farField = self.myResults.getFarField(
            11.7, theta, phi, 1, 1, coordSys="ludwig3",
            component=["vertical", "horizontal"])
        
        # Create a new figure
        plt.figure(0)
        # Plot the retrieved results
        plt.plot(theta, farField[0][:,0], color="green", label="$\phi=0^\circ$ (Cop)")
        plt.plot(theta, farField[1][:,0], color="green", label="$\phi=0^\circ$ (Cxp)", linestyle="dashed")
        plt.plot(theta, farField[0][:,2], color="blue", label="$\phi=90^\circ$ (Cop)")
        plt.plot(theta, farField[1][:,2], color="blue", label="$\phi=90^\circ$ (Cxp)", linestyle="dashed")
        plt.plot(theta, farField[0][:,1], color="red", label="$\phi=45^\circ$ (Cop)")
        plt.plot(theta, farField[1][:,1], color="red", label="$\phi=45^\circ$ (Cxp)", linestyle="dashed")
        # Decorate the figure
        plt.xlabel("$\\theta (^\circ)$")
        plt.ylabel("Directivity (dBi)")
        plt.title("farfield (f=11.7) [1(1)]")
        plt.ylim((-51,11))
        plt.legend()
        plt.grid()
        
        # Retrieve the electric field pattern in linear scale for a different
        # farfield monitor
        farField = self.myResults.getFarField(
            "f0", theta, phi, 1, 2, plotMode="efield", coordSys="spherical",
            component=["theta", "phi"], linearScale=True)
        
        # Create a new figure
        plt.figure(1)
        # Plot the retrieved results
        plt.plot(theta, farField[0][:,0], color="green", label="$\phi=0^\circ (\hat{\\theta})$")
        plt.plot(theta, farField[1][:,0], color="green", label="$\phi=0^\circ (\hat{\phi})$", linestyle="dashed")
        plt.plot(theta, farField[0][:,2], color="blue", label="$\phi=90^\circ (\hat{\\theta})$")
        plt.plot(theta, farField[1][:,2], color="blue", label="$\phi=90^\circ (\hat{\phi})$", linestyle="dashed")
        plt.plot(theta, farField[0][:,1], color="red", label="$\phi=45^\circ (\hat{\\theta})$")
        plt.plot(theta, farField[1][:,1], color="red", label="$\phi=45^\circ (\hat{\phi})$", linestyle="dashed")
        # Decorate the figure
        plt.xlabel("$\\theta (^\circ)$")
        plt.ylabel("Radiated E-field (V/m)")
        plt.title("farfield (f=f0) [1(2)]")
        plt.legend()
        plt.grid()
        
        # Show all the created figures and wait for the user to close them
        plt.show()
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # freq not of type float or str
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(42, theta, phi, 1)
            
        # freq of type str but does not make reference to a project parameter
        with self.assertRaises(RuntimeError):
            _, _ = self.myResults.getFarField("nonExistent", theta, phi, 1)
        
        # theta not of type NDArray
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(11.7, 42, phi, 1)
        
        # theta not a one-dimensional array
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getFarField(
                11.7, np.array([[1,2],[3,4]]), phi, 1)
        
        # phi not of type NDArray
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(11.7, theta, 42, 1)
        
        # phi not a one-dimensional array
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getFarField(
                11.7, theta, np.array([[1,2],[3,4]]), 1)
        
        # port not of type int
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 42.0)
        
        # port smaller than 1
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 0)
        
        # mode not of type int
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, mode=42.0)
        
        # mode smaller than 0
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, mode=-1)
        
        # plotMode not of type str
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, plotMode=42)
        
        # plotMode does not take a valid value
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, plotMode="nonValid")
        
        # coordSys not of type str
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, coordSys=42)
        
        # coordSys does not take a valid value
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, coordSys="nonValid")
        
        # polarization not of type str
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, polarization=42)
        
        # polarization does not take a valid value
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, polarization="nonValid")
        
        # component not of type list
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, component=42)
        
        # complexComp not of type list
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, complexComp=42)
        
        # Lengths of component and complexComp are not the same
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, component=["theta", "phi"],
                complexComp=["abs"])
        
        # An element of component is not of type str
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, component=["theta", 42],
                complexComp=["abs", "abs"])
        
        # An element of complexComp is not of type str
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, component=["theta", "phi"],
                complexComp=["abs", 42])
        
        # An element of component takes a non-valid value
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, component=["nonValid", "phi"],
                complexComp=["abs", "abs"])
        
        # An element of complexComp takes a non-valid value
        with self.assertRaises(ValueError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, component=["theta", "phi"],
                complexComp=["nonValid", "abs"])
        
        # linearScale not of type bool
        with self.assertRaises(TypeError):
            _, _ = self.myResults.getFarField(
                11.7, theta, phi, 1, linearScale=42)
        
        # The specified farfield result is not present in the project
        with self.assertRaises(RuntimeError):
            _, _ = self.myResults.getFarField(
                42.0, theta, phi, 17)
        
        return
        