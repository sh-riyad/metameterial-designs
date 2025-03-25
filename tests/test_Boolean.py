# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

################################
#                              #
# Unit tests for Boolean class #
#                              #
################################

import unittest
import os.path
import time
from .context import cst_python_api as cpa
from .context import dataFolder
from .auxiliaryTestFunctions import restoreTestEnvironment

class TestBoolean(unittest.TestCase):
    def test_add(self):
        """Opens an existing project and tries to perform a boolean addition
        between two of its objects. It is not possible to check automatically
        the success of this operation, so it must be checked manually.
        """
        
        self.projectName = "Cube_and_Sphere"
        
        # Open a project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Boolean object and pass to it the COM object to control the
        # example project
        self.myBoolean = cpa.Boolean(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Add the Cube and the Sphere
        self.myBoolean.add("component1:Cube", "component1:Sphere")
        
        # Currently it is not possible to check the result of the former
        # operations automatically, so it has to be checked manually
        time.sleep(5)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # object1 is not of type str
        with self.assertRaises(TypeError):
            self.myBoolean.add(42, "component1:Sphere")
            
        # object2 is not of type str
        with self.assertRaises(TypeError):
            self.myBoolean.add("component1:Cube", 42)
            
        # A non existing object is specified
        with self.assertRaises(RuntimeError):
            self.myBoolean.add("nonExisting", "component1:Sphere")
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_subtract(self):
        """Opens an existing project and tries to perform a boolean subtraction
        between two of its objects. It is not possible to check automatically
        the success of this operation, so it must be checked manually.
        """
        
        self.projectName = "Cube_and_Sphere"
        
        # Open a project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Boolean object and pass to it the COM object to control the
        # example project
        self.myBoolean = cpa.Boolean(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Subtract the Sphere from the Cube
        self.myBoolean.subtract("component1:Cube", "component1:Sphere")
        
        # Currently it is not possible to check the result of the former
        # operations automatically, so it has to be checked manually
        time.sleep(5)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # object1 is not of type str
        with self.assertRaises(TypeError):
            self.myBoolean.subtract(42, "component1:Sphere")
            
        # object2 is not of type str
        with self.assertRaises(TypeError):
            self.myBoolean.subtract("component1:Cube", 42)
            
        # A non existing object is specified
        with self.assertRaises(RuntimeError):
            self.myBoolean.subtract("nonExisting", "component1:Sphere")
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    
    def test_intersect(self):
        """Opens an existing project and tries to perform a boolean intersection
        between two of its objects. It is not possible to check automatically
        the success of this operation, so it must be checked manually.
        """
        
        self.projectName = "Cube_and_Sphere"
        
        # Open a project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Boolean object and pass to it the COM object to control the
        # example project
        self.myBoolean = cpa.Boolean(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Intersect the Cube and the Sphere
        self.myBoolean.intersect("component1:Cube", "component1:Sphere")
        
        # Currently it is not possible to check the result of the former
        # operations automatically, so it has to be checked manually
        time.sleep(5)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # object1 is not of type str
        with self.assertRaises(TypeError):
            self.myBoolean.intersect(42, "component1:Sphere")
            
        # object2 is not of type str
        with self.assertRaises(TypeError):
            self.myBoolean.intersect("component1:Cube", 42)
            
        # A non existing object is specified
        with self.assertRaises(RuntimeError):
            self.myBoolean.intersect("nonExisting", "component1:Sphere")
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
        
    def test_insert(self):
        """Opens an existing project and tries to perform a boolean insertion
        of one of its objects into another. It is not possible to check
        automatically the success of this operation, so it must be checked
        manually.
        """
        
        self.projectName = "Cube_and_Sphere"
        
        # Open a project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Boolean object and pass to it the COM object to control the
        # example project
        self.myBoolean = cpa.Boolean(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Insert the Sphere into the Cube
        self.myBoolean.insert("component1:Cube", "component1:Sphere")
        
        # Currently it is not possible to check the result of the former
        # operations automatically, so it has to be checked manually
        time.sleep(5)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # object1 is not of type str
        with self.assertRaises(TypeError):
            self.myBoolean.insert(42, "component1:Sphere")
            
        # object2 is not of type str
        with self.assertRaises(TypeError):
            self.myBoolean.insert("component1:Cube", 42)
            
        # A non existing object is specified
        with self.assertRaises(RuntimeError):
            self.myBoolean.insert("nonExisting", "component1:Sphere")
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_mergeCommonMaterials(self):
        """Opens an existing project and tries to perform a boolean addition
        of all the objects of a certain object that are made of the same
        material. It is not possible to check automatically the success of this
        operation, so it must be checked manually.
        """
        
        self.projectName = "Cube_and_Sphere"
        
        # Open a project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Boolean object and pass to it the COM object to control the
        # example project
        self.myBoolean = cpa.Boolean(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Perform the addition
        self.myBoolean.mergeCommonMaterials("component1")
        
        # Currently it is not possible to check the result of the former
        # operations automatically, so it has to be checked manually
        time.sleep(5)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # component is not of type str
        with self.assertRaises(TypeError):
            self.myBoolean.mergeCommonMaterials(42)
            
        # The RuntimeError is not tested since a case where it is raised has not
        # been found.
        
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