# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

###########################################################################
#                                                                         #
# Integration test for CST_MicrowaveStudio, Project and Parameter classes #
#                                                                         #
###########################################################################

import unittest
import os.path
import time
from .context import cst_python_api as cpa
from .context import dataFolder
from .auxiliaryTestFunctions import deleteTestProject

class TestProject(unittest.TestCase):
    def test_EditParams(self):
        """Create a new, empty project. Add some parameters to it. Save the
        project and close it. Then open again the project and try to read the
        parameters.
        """
        self.projectName = "Empty_Example"
        
        # Create a new project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Try to write a float and a str parameters
        self.myCST.Project.Parameter.add("newParam1", 1.0)
        self.myCST.Project.Parameter.add("newParam2", "newParam1")
        
        # Save the project
        self.myCST.saveFile()
        
        # Close the project
        self.myCST.closeFile()
        del self.myCST # Destroy associated object
        
        # Wait some time for the project to close correctly
        time.sleep(10)
        
        # Open again the project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Retrieve the parameters and verify that they have the expected value
        result = self.myCST.Project.Parameter.retrieve("newParam1", "float")
        self.assertEqual(result, 1.0)
        
        result = self.myCST.Project.Parameter.retrieve("newParam2", "expr")
        self.assertEqual(result, "newParam1")
        
        # Close the project and delete its files
        self.finishTest()
        
        return
    
    def test_setUnits(self):
        """Creates a new, empty project and tries to modify its units
        """
        
        self.projectName = "Empty_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        self.myCST.Project.setUnits(
            leng="m", freq="PHz", time="ms", temp="degC")
        
        # Currently it is not possible to check the result of the former
        # operation manually, so it has to be checked manually
        time.sleep(10)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # leng not of type str
        with self.assertRaises(TypeError):
            self.myCST.Project.setUnits(
                leng=42, freq="kHz", time="ms", temp="degC")
        # leng does not take a valid value
        with self.assertRaises(ValueError):
            self.myCST.Project.setUnits(
                leng="nonValid", freq="kHz", time="ms", temp="degC")
        # freq not of type str
        with self.assertRaises(TypeError):
            self.myCST.Project.setUnits(
                leng="m", freq=42, time="ms", temp="degC")
        # freq does not take a valid value
        with self.assertRaises(ValueError):
            self.myCST.Project.setUnits(
                leng="m", freq="nonValid", time="ms", temp="degC")
        # time not of type str
        with self.assertRaises(TypeError):
            self.myCST.Project.setUnits(
                leng="m", freq="kHz", time=42, temp="degC")
        # time does not take a valid value
        with self.assertRaises(ValueError):
            self.myCST.Project.setUnits(
                leng="m", freq="kHz", time="nonValid", temp="degC")
        # temp not of type str
        with self.assertRaises(TypeError):
            self.myCST.Project.setUnits(
                leng="m", freq="kHz", time="ms", temp=42)
        # temp does not take a valid value
        with self.assertRaises(ValueError):
            self.myCST.Project.setUnits(
                leng="m", freq="kHz", time="ms", temp="nonValid")
            
        # Close the project and delete its files
        self.finishTest()
        
        return
    
    def finishTest(self):
        """Closes the current project and deletes its files"""
        
        # Close the project
        self.myCST.closeFile()
        
        # Delete the project files
        pathCSTFile = os.path.join(dataFolder, self.projectName + ".cst")
        pathProjDataFolder = os.path.join(dataFolder, self.projectName)
        deleteTestProject(pathCSTFile, pathProjDataFolder)
        
        time.sleep(5)
    
if __name__ == '__main__':
    unittest.main()
