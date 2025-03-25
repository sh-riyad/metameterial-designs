# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

#############################
#                           #
# Unit tests for Port class #
#                           #
#############################

import unittest
import os.path
import time
from .context import cst_python_api as cpa
from .context import dataFolder
from .auxiliaryTestFunctions import restoreTestEnvironment

class TestPort(unittest.TestCase):
    def test_addDiscretePort(self):
        """Open an existing project and try to add some discrete ports
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Port object and pass to it the COM object to control the
        # example project
        self.myPorts = cpa.Port(self.myCST._CST_MicrowaveStudio__MWS)
        
        self.myPorts.addDiscretePort(0.0, 0.0, -2.0, 2.0, -1.0, 0.0)
        
        self.myPorts.addDiscretePort(
            -5.0, 5.0, "bWG", "bWG", "lPort", "lPort", type="Voltage",
            voltage=1.7, radius=3.2)
        
        # Currently it is not possible to check the result of the former
        # operations automatically, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # type not of type str
        with self.assertRaises(TypeError):
            self.myPorts.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, type=42)
        # type different of "SParameter", "Voltage" or "Current"
        with self.assertRaises(ValueError):
            self.myPorts.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, type="nonValid")
        # impedance not of type float
        with self.assertRaises(TypeError):
            self.myPorts.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, impedance=42)
        # impedance is not greater than zero
        with self.assertRaises(ValueError):
            self.myPorts.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, impedance=0.0) 
        # voltage not of type float
        with self.assertRaises(TypeError):
            self.myPorts.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, voltage=42)
        # current not of type float
        with self.assertRaises(TypeError):
            self.myPorts.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, current=42)
        # radius not of type float
        with self.assertRaises(TypeError):
            self.myPorts.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, radius=42)
        # Port position parameter not of type float or str
        with self.assertRaises(TypeError):
            self.myPorts.addDiscretePort(
                42, 0.0, -2.0, 2.0, -1.0, 0.0)
        # Port position parameter of type str does not match a project parameter
        with self.assertRaises(RuntimeError):
            self.myPorts.addDiscretePort(
                "nonExisting", 0.0, -2.0, 2.0, -1.0, 0.0)
            
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_addWaveguidePort(self):
        """Open an existing project and try to add some waveguide ports
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Port object and pass to it the COM object to control the
        # example project
        self.myPorts = cpa.Port(self.myCST._CST_MicrowaveStudio__MWS)
        
        self.myPorts.addWaveguidePort(
            -5.0, 5.0, -2.5, 2.5, 0.0, 5.0, orientation="zmax", nModes=3,
            refPlaneDist=-10.0)
        
        self.myPorts.addWaveguidePort(
            "aWG", 15.0, "res1", 2.5, 0.0, 5.0, orientation="ymin", nModes=2,
            enforcePolar=True, polarAngle="iris1")
        
        # Currently it is not possible to check the result of the former
        # operations automatically, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # orientation not of type str
        with self.assertRaises(TypeError):
            self.myPorts.addWaveguidePort(
                -5.0, 5.0, -2.5, 2.5, 0.0, 5.0, orientation=42, nModes=3,
                refPlaneDist=-10.0)
        # orientation does not present a valid value
        with self.assertRaises(ValueError):
            self.myPorts.addWaveguidePort(
                -5.0, 5.0, -2.5, 2.5, 0.0, 5.0, orientation="nonValid",
                nModes=3, refPlaneDist=-10.0)
        # nModes not of type int
        with self.assertRaises(TypeError):
            self.myPorts.addWaveguidePort(
                -5.0, 5.0, -2.5, 2.5, 0.0, 5.0, orientation="zmax", nModes=3.0,
                refPlaneDist=-10.0)
        # nModes smaller than 1
        with self.assertRaises(ValueError):
            self.myPorts.addWaveguidePort(
                -5.0, 5.0, -2.5, 2.5, 0.0, 5.0, orientation="zmax", nModes=0,
                refPlaneDist=-10.0) 
        # enforcePolar not of type bool
        with self.assertRaises(TypeError):
            self.myPorts.addWaveguidePort(
                -5.0, 5.0, -2.5, 2.5, 0.0, 5.0, orientation="zmax", nModes=3,
                refPlaneDist=-10.0, enforcePolar=42)
        # Port position parameter not of type float or str
        with self.assertRaises(TypeError):
            self.myPorts.addWaveguidePort(
                42, 5.0, -2.5, 2.5, 0.0, 5.0, orientation="zmax", nModes=3,
                refPlaneDist=-10.0)
        # Port position parameter of type str does not match a project parameter
        with self.assertRaises(RuntimeError):
            self.myPorts.addWaveguidePort(
                "nonExisting", 5.0, -2.5, 2.5, 0.0, 5.0, orientation="zmax",
                nModes=3, refPlaneDist=-10.0)
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def finishTest(self):
        """Closes the current project and restores its files to their original
        state.
        """
        
        # Close the project
        self.myCST.closeFile()
        
        # Restore the test data files
        pathCSTFile = os.path.join(dataFolder, self.projectName + ".cst")
        pathProjDataFolder = os.path.join(dataFolder, self.projectName)
        restoreTestEnvironment(pathCSTFile, pathProjDataFolder)
        
        time.sleep(5)
    