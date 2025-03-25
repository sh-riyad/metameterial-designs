# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

##################################
#                                #
# Unit tests for Transform class #
#                                #
##################################

import unittest
import os.path
import time
import numpy as np # To define points for addPolygonBlock
from .context import cst_python_api as cpa
from .context import dataFolder
from .auxiliaryTestFunctions import restoreTestEnvironment

class TestTransform(unittest.TestCase):
    def test_translate(self):
        """Opens an existing project and tries to translate some of its objects. 
        It is not possible to check automatically the success of this operation,
        so it must be checked manually.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Transform object and pass to it the COM object to control the
        # example project
        self.myTransform = cpa.Transform(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Perform translate operations
        self.myTransform.translate(
            "component1:Iris1", 5.0, 7.0, 0.0
        )
        
        self.myTransform.translate(
            "component1:Iris2", "iris1", -7.0, "res2", copy=True, 
            destination="copyComp", material="PEC"
        )
        
        self.myTransform.translate(
            "component1:Iris3", -4.5, -5.0, 0.0, copy=True, group=True
        )
        
        # Currently it is not possible to check the result of the former
        # operations automatically, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # object not of type str
        with self.assertRaises(TypeError):
            self.myTransform.translate(
            42, 5.0, 7.0, 0.0)
        # copy not of type bool
        with self.assertRaises(TypeError):
            self.myTransform.translate(
                "component1:Iris1", 5.0, 7.0, 0.0, copy=42)
        # repetitions not of type int
        with self.assertRaises(TypeError):
            self.myTransform.translate(
                "component1:Iris1", 5.0, 7.0, 0.0, repetitions=4.2)
        # repetitions smaller than 1
        with self.assertRaises(ValueError):
            self.myTransform.translate(
                "component1:Iris1", 5.0, 7.0, 0.0, repetitions=0)
        # group not of type bool
        with self.assertRaises(TypeError):
            self.myTransform.translate(
                "component1:Iris1", 5.0, 7.0, 0.0, group=42)
        # destination not of type str
        with self.assertRaises(TypeError):
            self.myTransform.translate(
                "component1:Iris1", 5.0, 7.0, 0.0, destination=42)
        # material not of type str
        with self.assertRaises(TypeError):
            self.myTransform.translate(
                "component1:Iris1", 5.0, 7.0, 0.0, material=42)
        # group is true but copy is false
        with self.assertRaises(ValueError):
            self.myTransform.translate(
                "component1:Iris1", 5.0, 7.0, 0.0, group=True, copy=False)
        # A destination is specified but copy is false
        with self.assertRaises(ValueError):
            self.myTransform.translate(
                "component1:Iris1", 5.0, 7.0, 0.0, destination="newComponent",
                copy=False)
        # A material is specified but copy is false
        with self.assertRaises(ValueError):
            self.myTransform.translate(
                "component1:Iris1", 5.0, 7.0, 0.0, material="PEC", copy=False)
        # Transformation parameters not of type float or str
        with self.assertRaises(TypeError):
            self.myTransform.translate(
                "component1:Iris1", 42, 7.0, 0.0)
        # Transformation parameter of type str does not match a project
        # parameter
        with self.assertRaises(RuntimeError):
            self.myTransform.translate(
                "component1:Iris1", "nonExisting", 7.0, 0.0)
        # destination contains a non-valid character
        with self.assertRaises(RuntimeError):
            self.myTransform.translate(
                "component1:Iris1", 5.0, 7.0, 0.0, copy=True,
                destination="newComponent?")
        # A non existing material is specified
        with self.assertRaises(RuntimeError):
            self.myTransform.translate(
                "component1:Iris1", 5.0, 7.0, 0.0, copy=True,
                material="nonExisting")
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_scale(self):
        """Opens an existing project and tries to scale some of its objects. 
        It is not possible to check automatically the success of this operation,
        so it must be checked manually.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Transform object and pass to it the COM object to control the
        # example project
        self.myTransform = cpa.Transform(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Perform scale operations
        self.myTransform.scale(
            "component1:Iris1", 5.0, 7.0, 2.0
        )
        
        self.myTransform.scale(
            "component1:Iris2", "iris1", 7.0, 1.0, copy=True, 
            destination="copyComp", material="PEC"
        )
        
        self.myTransform.scale(
            "component1:Iris3", 3.0, 3.0, 1.0, x0=10.0, y0="res2", z0=0.0, 
            origin="free", repetitions=2
        )
        
        self.myTransform.scale(
            "component1:Iris4", 3.0, 3.0, 1.0, x0=10.0, y0="res2", z0=0.0, 
            origin="free", repetitions=2, copy=True, group=True
        )
        
        # Currently it is not possible to check the result of the former
        # operations automatically, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # object not of type str
        with self.assertRaises(TypeError):
            self.myTransform.scale(
                42, 5.0, 7.0, 2.0)
        # origin not of type str
        with self.assertRaises(TypeError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 2.0, origin=42)
        # origin other than "object" and "free"
        with self.assertRaises(ValueError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 2.0, origin="nonValid")
        # copy not of type bool
        with self.assertRaises(TypeError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 2.0, copy=42)
        # repetitions not of type int
        with self.assertRaises(TypeError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 0.0, repetitions=4.2)
        # repetitions smaller than 1
        with self.assertRaises(ValueError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 0.0, repetitions=0)
        # group not of type bool
        with self.assertRaises(TypeError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 0.0, group=42)
        # destination not of type str
        with self.assertRaises(TypeError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 0.0, destination=42)
        # material not of type str
        with self.assertRaises(TypeError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 0.0, material=42)
        # group is true but copy is false
        with self.assertRaises(ValueError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 0.0, group=True, copy=False)
        # A destination is specified but copy is false
        with self.assertRaises(ValueError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 0.0, destination="newComponent",
                copy=False)
        # A material is specified but copy is false
        with self.assertRaises(ValueError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 0.0, material="PEC", copy=False)
        # Transformation parameters not of type float or str
        with self.assertRaises(TypeError):
            self.myTransform.scale(
                "component1:Iris1", 42, 7.0, 0.0)
        # Transformation parameter of type str does not match a project
        # parameter
        with self.assertRaises(RuntimeError):
            self.myTransform.scale(
                "component1:Iris1", "nonExisting", 7.0, 0.0)
        # destination contains a non-valid character
        with self.assertRaises(RuntimeError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 0.0, copy=True, destination="newComponent?")
        # A non existing material is specified
        with self.assertRaises(RuntimeError):
            self.myTransform.scale(
                "component1:Iris1", 5.0, 7.0, 0.0, copy=True, material="nonExisting")
        # A negative scaling factor is specified
        with self.assertRaises(RuntimeError):
            self.myTransform.scale(
                "component1:Iris1", -2.0, -2.0, -2.0)
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_rotate(self):
        """Opens an existing project and tries to rotate some of its objects. 
        It is not possible to check automatically the success of this operation,
        so it must be checked manually.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Transform object and pass to it the COM object to control the
        # example project
        self.myTransform = cpa.Transform(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Perform rotate operations
        self.myTransform.rotate(
            "component1:Iris1", 20.0, 0.0, 45.0
        )
        
        self.myTransform.rotate(
            "component1:Iris2", "iris1", 7.0, "iris2", copy=True, 
            destination="copyComp", material="PEC"
        )
        
        self.myTransform.rotate(
            "component1:Iris3", 90.0, 90.0, 0.0, x0=0.0, y0=0.0, z0=0.0, 
            origin="free", repetitions=2
        )
        
        self.myTransform.rotate(
            "component1:Iris4", "iris1", 7.0, "iris2", copy=True, group=True
        )
        
        # Currently it is not possible to check the result of the former
        # operations automatically, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # object not of type str
        with self.assertRaises(TypeError):
            self.myTransform.rotate(
                42,  20.0, 0.0, 45.0)
        # origin not of type str
        with self.assertRaises(TypeError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, origin=42)
        # origin other than "object" and "free"
        with self.assertRaises(ValueError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, origin="nonValid")
        # copy not of type bool
        with self.assertRaises(TypeError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, copy=42)
        # repetitions not of type int
        with self.assertRaises(TypeError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, repetitions=4.2)
        # repetitions smaller than 1
        with self.assertRaises(ValueError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, repetitions=0)
        # group not of type bool
        with self.assertRaises(TypeError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, group=42)
        # destination not of type str
        with self.assertRaises(TypeError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, destination=42)
        # material not of type str
        with self.assertRaises(TypeError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, material=42)
        # group is true but copy is false
        with self.assertRaises(ValueError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, group=True, copy=False)
        # A destination is specified but copy is false
        with self.assertRaises(ValueError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, destination="newComponent",
                copy=False)
        # A material is specified but copy is false
        with self.assertRaises(ValueError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, material="PEC", copy=False)
        # Transformation parameters not of type float or str
        with self.assertRaises(TypeError):
            self.myTransform.rotate(
                "component1:Iris1", 42, 7.0, 0.0)
        # Transformation parameter of type str does not match a project
        # parameter
        with self.assertRaises(RuntimeError):
            self.myTransform.rotate(
                "component1:Iris1", "nonExisting", 7.0, 0.0)
        # destination contains a non-valid character
        with self.assertRaises(RuntimeError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, copy=True, destination="newComponent?")
        # A non existing material is specified
        with self.assertRaises(RuntimeError):
            self.myTransform.rotate(
                "component1:Iris1", 20.0, 0.0, 45.0, copy=True, material="nonExisting")
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_mirror(self):
        """Opens an existing project and tries to mirror some of its objects. 
        It is not possible to check automatically the success of this operation,
        so it must be checked manually.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Transform object and pass to it the COM object to control the
        # example project
        self.myTransform = cpa.Transform(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Perform mirror operations
        self.myTransform.mirror(
            "component1:Iris1", 0.0, 0.0, 1.0, x0=0.0, y0=0.0, z0=0.0, 
            origin="free"
        )
        
        self.myTransform.mirror(
            "component1:Iris2", "iris1", "res2", 0.0, x0=5.0, y0=2.0, z0=0.0, 
            origin="free", copy=True, destination="copyComp", material="PEC"
        )
        
        self.myTransform.mirror(
            "component1:Iris3", 1.0, 1.0, 0.0
        )
        
        self.myTransform.mirror(
            "component1:Iris4", "iris1", "res2", 0.0, x0=5.0, y0=2.0, z0=0.0, 
            origin="free", copy=True, group=True
        )
        
        # Currently it is not possible to check the result of the former
        # operations automatically, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # object not of type str
        with self.assertRaises(TypeError):
            self.myTransform.mirror(
                42, 1.0, 1.0, 0.0)
        # origin not of type str
        with self.assertRaises(TypeError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, origin=42)
        # origin other than "object" and "free"
        with self.assertRaises(ValueError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, origin="nonValid")
        # copy not of type bool
        with self.assertRaises(TypeError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, copy=42)
        # repetitions not of type int
        with self.assertRaises(TypeError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, repetitions=4.2)
        # repetitions smaller than 1
        with self.assertRaises(ValueError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, repetitions=0)
        # group not of type bool
        with self.assertRaises(TypeError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, group=42)
        # destination not of type str
        with self.assertRaises(TypeError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, destination=42)
        # material not of type str
        with self.assertRaises(TypeError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, material=42)
        # group is true but copy is false
        with self.assertRaises(ValueError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, group=True, copy=False)
        # A destination is specified but copy is false
        with self.assertRaises(ValueError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, destination="newComponent",
                copy=False)
        # A material is specified but copy is false
        with self.assertRaises(ValueError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, material="PEC", copy=False)
        # Transformation parameters not of type float or str
        with self.assertRaises(TypeError):
            self.myTransform.mirror(
                "component1:Iris1", 42, 1.0, 0.0)
        # Transformation parameter of type str does not match a project
        # parameter
        with self.assertRaises(RuntimeError):
            self.myTransform.mirror(
                "component1:Iris1", "nonExisting", 1.0, 0.0)
        # destination contains a non-valid character
        with self.assertRaises(RuntimeError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, copy=True, destination="newComponent?")
        # A non existing material is specified
        with self.assertRaises(RuntimeError):
            self.myTransform.mirror(
                "component1:Iris1", 1.0, 1.0, 0.0, copy=True, material="nonExisting")
        
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