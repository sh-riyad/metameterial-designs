# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

##############################
#                            #
# Unit tests for Build class #
#                            #
##############################

import unittest
import os.path
import time
from .context import cst_python_api as cpa
from .context import dataFolder
from .auxiliaryTestFunctions import restoreTestEnvironment

class TestBuild(unittest.TestCase):
    
    def test_deleteObject(self):
        """Open an existing project and try to delete some of its solids and
        components.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Build object and pass to it the COM object to control the
        # example project
        self.myBuild = cpa.Build(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Delete a solid
        result = self.myBuild._Build__MWS.Solid.DoesExist("component1:Iris1")
        self.assertTrue(result)
        self.myBuild.deleteObject("component1:Iris1", "Solid")
        result = self.myBuild._Build__MWS.Solid.DoesExist("component1:Iris1")
        self.assertFalse(result)
        
        # Try to delete a solid that does not exist
        with self.assertRaises(RuntimeError):
            self.myBuild.deleteObject("component1:nonExisting", "Solid")
        # Pass the wrong type of objectType
        with self.assertRaises(RuntimeError):
            self.myBuild.deleteObject("component1:Iris2", "Component")
        
        # Delete a component
        result = self.myBuild._Build__MWS.Component.DoesExist("component1")
        self.assertTrue(result)
        self.myBuild.deleteObject("component1", "Component")
        result = self.myBuild._Build__MWS.Component.DoesExist("component1")
        self.assertFalse(result)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # objectName not of type str
        with self.assertRaises(TypeError):
            self.myBuild.deleteObject(42, "Component")
            
        # objectType not of type str
        with self.assertRaises(TypeError):
            self.myBuild.deleteObject("component1", 42)
            
        # objectType value not valid
        with self.assertRaises(ValueError):
            self.myBuild.deleteObject("component1", "nonValid")
            
        # Close the project and restore its files to their original state    
        self.finishTest()
        
        return
    
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