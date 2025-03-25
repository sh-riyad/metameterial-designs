# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

##################################################################
#                                                                #
# Unit tests for Solver class and integration test of Port class #
#                                                                #
##################################################################

import unittest
import os.path
import time
from .context import cst_python_api as cpa
from .context import dataFolder
from .auxiliaryTestFunctions import restoreTestEnvironment

class TestSolver(unittest.TestCase):
    def test_setFrequencyRange(self):
        """Open an existing project and try to modify its simulation frequency
        range.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Solver object and pass to it the COM object to control the
        # example project
        self.mySolver = cpa.Solver(self.myCST._CST_MicrowaveStudio__MWS)
        
        self.mySolver.setFrequencyRange("iris1", 20.2)
        
        # Currently it is not possible to check the result of this operation
        # manually, so it has to be checked manually
        time.sleep(15)
    
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # Frequency params not float or str
        with self.assertRaises(TypeError):
            self.mySolver.setFrequencyRange(42, 20.2)
        # Any of the frequency params is a str but it does not make reference to
        # a parameter that already exists in the project
        with self.assertRaises(RuntimeError):
            self.mySolver.setFrequencyRange("nonExisting", 20.2)
        # fMax smaller than fMin
        with self.assertRaises(RuntimeError):
            self.mySolver.setFrequencyRange(5.0, 2.0)
            
        # Close the project and restore the files to their original state
        self.finishTest()
            
    def test_getSolverType(self):
        """Open an existing project and try to obtain the type of its solver.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Solver object and pass to it the COM object to control the
        # example project
        self.mySolver = cpa.Solver(self.myCST._CST_MicrowaveStudio__MWS)
        
        result = self.mySolver.getSolverType()
        
        self.assertEqual(result, "HF Frequency Domain")
    
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_changeSolverType(self):
        """Open an existing project and try to change its solver."""
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Solver object and pass to it the COM object to control the
        # example project
        self.mySolver = cpa.Solver(self.myCST._CST_MicrowaveStudio__MWS)
        
        solverTypes = {
            "HF Time Domain", "HF Eigenmode", "HF Frequency Domain",
            "HF IntegralEq", "HF Multilayer", "HF Asymptotic"}
        
        # Currently it is not possible to check the result of these
        # operations manually, so it has to be checked manually
        for solver in solverTypes:
            self.mySolver.changeSolverType(solver)
            time.sleep(5)
    
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # type not str
        with self.assertRaises(TypeError):
            self.mySolver.changeSolverType(42)
        # type does not match a valid solver identifier
        with self.assertRaises(ValueError):
            self.mySolver.changeSolverType("nonValid")
            
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_setBoundaryCondition(self):
        """Opens a new project and tries to set its boundary conditions."""
        
        self.projectName = "Empty_Project"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Solver object and pass to it the COM object to control the
        # example project
        self.mySolver = cpa.Solver(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Currently it is not possible to check the result of these
        # operations manually, so it has to be checked manually
        
        self.mySolver.setBoundaryCondition(
            "open", "expanded open", "periodic", "conducting wall", "electric",
            "magnetic", wallCond=17.2)
        
        time.sleep(5)
        
        self.mySolver.setBoundaryCondition(
            "unit cell", "unit cell", "unit cell", "unit cell", "expanded open",
            "open")
        
        time.sleep(5)
    
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # boundary type not str
        with self.assertRaises(TypeError):
            self.mySolver.setBoundaryCondition(
                42, "expanded open", "periodic", "conducting wall", "electric",
                "magnetic", wallCond=17.2)
        # boundary type does not match a valid type
        with self.assertRaises(ValueError):
            self.mySolver.setBoundaryCondition(
                "open", "nonValid", "periodic", "conducting wall", "electric",
                "magnetic", wallCond=17.2)
        # zMin is "unit cell"
        with self.assertRaises(ValueError):
            self.mySolver.setBoundaryCondition(
                "open", "open", "periodic", "conducting wall", "unit cell",
                "magnetic", wallCond=17.2)
        # "unit cell" is applied to only some of the X and Y boundaries
        with self.assertRaises(ValueError):
            self.mySolver.setBoundaryCondition(
                "unit cell", "unit cell", "periodic", "conducting wall", "electric",
                "magnetic", wallCond=17.2) 
        # wallCond not float or str
        with self.assertRaises(TypeError):
            self.mySolver.setBoundaryCondition(
                "open", "expanded open", "periodic", "conducting wall", "electric",
                "magnetic", wallCond=42)
        # wallCond is a str but it does not make reference to a parameter that
        # already exists in the project
        with self.assertRaises(RuntimeError):
            self.mySolver.setBoundaryCondition(
                "open", "expanded open", "periodic", "conducting wall", "electric",
                "magnetic", wallCond="nonExisting")
            
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_addSymmetryPlane(self):
        """Opens a new project and tries to adjust its symmetry planes."""
        
        self.projectName = "Empty_Project"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Solver object and pass to it the COM object to control the
        # example project
        self.mySolver = cpa.Solver(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Currently it is not possible to check the result of these
        # operations manually, so it has to be checked manually
        
        self.mySolver.addSymmetryPlane("none", "electric", "magnetic")
        
        time.sleep(5)
        
        self.mySolver.addSymmetryPlane("electric", "magnetic", "none")
        
        time.sleep(5)
    
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # input parameter not str
        with self.assertRaises(TypeError):
            self.mySolver.addSymmetryPlane(42, "electric", "magnetic")
        # input parameter does not contain a valid value
        with self.assertRaises(ValueError):
            self.mySolver.addSymmetryPlane("nonValid", "electric", "magnetic")
            
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_addFieldMonitor(self):
        """Opens an existing project and tries to add some field monitors."""
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Solver object and pass to it the COM object to control the
        # example project
        self.mySolver = cpa.Solver(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Currently it is not possible to check the result of these
        # operations manually, so it has to be checked manually
        
        self.mySolver.addFieldMonitor("Efield", 5.0)
        self.mySolver.addFieldMonitor("Hfield", 17.2)
        self.mySolver.addFieldMonitor("Farfield", "f0")
        self.mySolver.addFieldMonitor("Powerloss", "iris1")
        
        time.sleep(5)
    
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # type not str
        with self.assertRaises(TypeError):
            self.mySolver.addFieldMonitor(42, 5.0)
        # type does not contain a valid value
        with self.assertRaises(ValueError):
            self.mySolver.addFieldMonitor("nonValid", 5.0)
        # freq not float or str
        with self.assertRaises(TypeError):
            self.mySolver.addFieldMonitor("Efield", 42)
        # freq is str but it does not make reference to a parameter that already
        # exists in the project
        with self.assertRaises(RuntimeError):
            self.mySolver.addFieldMonitor("Efield", "nonExisting")
            
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_setBackgroundMaterial(self):
        """Opens an existing project and tries to modify its background
        material."""
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Solver object and pass to it the COM object to control the
        # example project
        self.mySolver = cpa.Solver(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Currently it is not possible to check the result of these
        # operations manually, so it has to be checked manually
        
        self.mySolver.setBackgroundMaterial("Vacuum")
        time.sleep(5)
        self.mySolver.setBackgroundMaterial("PEC")
        time.sleep(5)
        self.mySolver.setBackgroundMaterial(
            "Dielectric", epsR=1.7, muR=3.2, sigma="f0", sigmaM=7.9)
        time.sleep(5)
        self.mySolver.setBackgroundMaterial(
            "Dielectric", epsR=1.7, muR=3.2, tanD="iris1", tanDFreq=1.1,
            tanDGiven=True, tanDM=4.5, tanDMFreq="res2", tanDMGiven=True)
        time.sleep(5)
    
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # type not str
        with self.assertRaises(TypeError):
            self.mySolver.setBackgroundMaterial(42)
        # type does not contain a valid value
        with self.assertRaises(ValueError):
            self.mySolver.setBackgroundMaterial("nonValid")
        # tanDGiven not bool
        with self.assertRaises(TypeError):
            self.mySolver.setBackgroundMaterial(
                "Dielectric", epsR=1.7, muR=3.2, tanD="iris1", tanDFreq=1.1,
                tanDGiven=42, tanDM=4.5, tanDMFreq="res2", tanDMGiven=True)
        # bkgrParam not float or str
        with self.assertRaises(TypeError):
            self.mySolver.setBackgroundMaterial("PEC", epsR=42)
        # bkgrParam is str but it does not make reference to a parameter that
        # already exists in the project
        with self.assertRaises(RuntimeError):
            self.mySolver.setBackgroundMaterial("PEC", epsR="nonExisting")
            
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_setBackgroundLimits(self):
        """Opens a new project and tries to modify its background limits."""
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Solver object and pass to it the COM object to control the
        # example project
        self.mySolver = cpa.Solver(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Currently it is not possible to check the result of this
        # operation manually, so it has to be checked manually
        
        self.mySolver.setBackgroundLimits(5.0, 2.2, "iris1", 3.9, 4.1, "res2")
        time.sleep(5)
    
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # bkgrParam not float or str
        with self.assertRaises(TypeError):
            self.mySolver.setBackgroundLimits(
                42, 2.2, "iris1", 3.9, 4.1, "res2")
        # bkgrParam is str but it does not make reference to a parameter that
        # already exists in the project
        with self.assertRaises(RuntimeError):
            self.mySolver.setBackgroundLimits(
                "nonExistent", 2.2, "iris1", 3.9, 4.1, "res2")
        # bkgrParam presents a negative value
        with self.assertRaises(RuntimeError):
            self.mySolver.setBackgroundLimits(
                -1.7, 2.2, "iris1", 3.9, 4.1, "res2")
            
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_defineFloquetModes(self):
        """Opens an existing project and tries to set unit cell boundaries and
        define a Floquet modes excitation."""
        
        self.projectName = "Cube_and_Sphere"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Solver object and pass to it the COM object to control the
        # example project
        self.mySolver = cpa.Solver(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Currently it is not possible to check the result of this
        # operation manually, so it has to be checked manually
        self.mySolver.setBoundaryCondition(
            "unit cell", "unit cell", "unit cell", "unit cell", "expanded open",
            "expanded open")
        self.mySolver.defineFloquetModes(7, theta=17.9, phi=22.3)
        time.sleep(5)
        self.mySolver.defineFloquetModes(
            7, theta="cubeSide", phi="sphereRadius", forcePolar=True, polarAngle=39.7)
        time.sleep(5)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # nModes not int
        with self.assertRaises(TypeError):
            self.mySolver.defineFloquetModes(4.2, theta=17.9, phi=22.3)
        # nModes not greater than zero
        with self.assertRaises(ValueError):
            self.mySolver.defineFloquetModes(0, theta=17.9, phi=22.3)
        # forcePolar not bool
        with self.assertRaises(TypeError):
            self.mySolver.defineFloquetModes(
                4, theta=17.9, phi=22.3, forcePolar=42)
        # bkgrParam not float or str
        with self.assertRaises(TypeError):
            self.mySolver.defineFloquetModes(
                4, theta=42, phi=22.3)
        # portParam is str but it does not make reference to a parameter that
        # already exists in the project
        with self.assertRaises(RuntimeError):
            self.mySolver.defineFloquetModes(
                4, theta="nonExisting", phi=22.3)
            
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_runSimulation(self):
        """Opens an existing project and tries to run the simulation."""
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Solver object and pass to it the COM object to control the
        # example project
        self.mySolver = cpa.Solver(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Currently it is not possible to check the result of this
        # operation manually, so it has to be checked manually
        self.mySolver.runSimulation()
        time.sleep(5)
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_portClassIntegration(self):
        """Open an existing project and tries to add some discrete ports by
        using the Port class through the Solver class."""
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Solver object and pass to it the COM object to control the
        # example project
        self.mySolver = cpa.Solver(self.myCST._CST_MicrowaveStudio__MWS)
        
        self.mySolver.Port.addDiscretePort(0.0, 0.0, -2.0, 2.0, -1.0, 0.0)
        
        self.mySolver.Port.addDiscretePort(
            -5.0, 5.0, "bWG", "bWG", "lPort", "lPort", type="Voltage",
            voltage=1.7, radius=3.2)
        
        # Currently it is not possible to check the result of the former
        # operations automatically, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # type not of type str
        with self.assertRaises(TypeError):
            self.mySolver.Port.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, type=42)
        # type different of "SParameter", "Voltage" or "Current"
        with self.assertRaises(ValueError):
            self.mySolver.Port.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, type="nonValid")
        # impedance not of type float
        with self.assertRaises(TypeError):
            self.mySolver.Port.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, impedance=42)
        # impedance is not greater than zero
        with self.assertRaises(ValueError):
            self.mySolver.Port.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, impedance=0.0) 
        # voltage not of type float
        with self.assertRaises(TypeError):
            self.mySolver.Port.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, voltage=42)
        # current not of type float
        with self.assertRaises(TypeError):
            self.mySolver.Port.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, current=42)
        # radius not of type float
        with self.assertRaises(TypeError):
            self.mySolver.Port.addDiscretePort(
                0.0, 0.0, -2.0, 2.0, -1.0, 0.0, radius=42)
        # Port position parameter not of type float or str
        with self.assertRaises(TypeError):
            self.mySolver.Port.addDiscretePort(
                42, 0.0, -2.0, 2.0, -1.0, 0.0)
        # Port position parameter of type str does not match a project parameter
        with self.assertRaises(RuntimeError):
            self.mySolver.Port.addDiscretePort(
                "nonExisting", 0.0, -2.0, 2.0, -1.0, 0.0)
        
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