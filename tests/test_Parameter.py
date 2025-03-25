# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

#####################################
#                                   #
# Feature tests for Parameter class #
#                                   #
#####################################

import unittest
import os.path
import time
from .context import cst_python_api as cpa
from .context import dataFolder
from .auxiliaryTestFunctions import restoreTestEnvironment

class TestParameter(unittest.TestCase):
    def test_exist(self):
        """Open an example project and check if certain parameter names do
        exist in the project. Some of them do really exist, and others do not.
        """
        self.projectName = "Filter_Example"
        
        # Open the project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Parameter object and pass to it the COM object to control the
        # example project
        self.myParam = cpa.Parameter(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Check if an existing parameter does indeed exist
        result = self.myParam.exist("iris1")
        self.assertTrue(result)
        
        # Now ask about a parameter which does not exist
        result = self.myParam.exist("notExisting")
        self.assertFalse(result)
        
        # Another existing parameter
        result = self.myParam.exist("res2")
        self.assertTrue(result)
        
        # And another non existing parameter
        result = self.myParam.exist("notExisting2")
        self.assertFalse(result)
        
        # Now an existing parameter which does not present number in its name
        # and, in addition, its value is not a double but a string
        result = self.myParam.exist("lPort")
        self.assertTrue(result)
        
        # Test that the method handles adequately input parameters of incorrect
        # type by raising the required exception
        
        # Non str for paramName
        with self.assertRaises(TypeError):
            self.myParam.exist(42)
        
        # Close the project and restore its files to their original state
        self.finishTest()
        
        return
    
    def test_add(self):
        """Open an example project and try to write a new parameter.
        """
        self.projectName = "Filter_Example"
        
        # Open the project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Parameter object and pass to it the COM object to control the
        # example project
        self.myParam = cpa.Parameter(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Try to write a float and a str parameters
        self.myParam.add("newParam1", 1.0)
        self.myParam.add("newParam2", "newParam1")
        
        result = self.myParam.exist("newParam1")
        self.assertTrue(result)
        result = self.myParam.exist("newParam2")
        self.assertTrue(result)
        
        # Test that the method handles adequately input parameters of incorrect
        # type by raising the required exceptions
        
        # Non float or str for paramValue
        with self.assertRaises(TypeError):
            self.myParam.add("newParam", int(1))
        # Non str type for paramName
        with self.assertRaises(TypeError):
            self.myParam.add(42, 1.0)
        # Already existing parameter name
        with self.assertRaises(RuntimeError):
            self.myParam.add("newParam1", 2.0)
        
        # Close the project and restore its files to their original state
        self.finishTest()
        
        return
        
    def test_change(self):
        """Open an example project and try to modify an already existing parameter.
        """
        self.projectName = "Filter_Example"
        
        # Open the project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Parameter object and pass to it the COM object to control the
        # example project
        self.myParam = cpa.Parameter(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Try to write a float and a str parameters
        self.myParam.change("iris1", 42.0)
        self.myParam.change("iris2", "iris1")
        
        # Currently it is not possible to check the result of these operation
        # manually, so they have to be checked manually
        
        time.sleep(15)
        
        # Test that the method handles adequately input parameters of incorrect
        # type by raising the required exceptions
        
        # Non float or str for paramValue
        with self.assertRaises(TypeError):
            self.myParam.change("newParam", int(1))
        # Non str type for paramName
        with self.assertRaises(TypeError):
            self.myParam.change(42, 1.0)
            
        # Close the project and restore its files to their original state
        self.finishTest()
        
        return

            
    def test_delete(self):
        """Open an example project and try to delete an already existing parameter.
        """
        self.projectName = "Filter_Example"
        
        # Open the project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Parameter object and pass to it the COM object to control the
        # example project
        self.myParam = cpa.Parameter(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Before testing the deletion, check if the parameter does indeed exist
        paramName = "iris1"
        result = self.myParam.exist(paramName)
        self.assertTrue(result)
        
        # Try to delete the parameter
        self.myParam.delete(paramName)
        
        # Check if the parameter has been deleted
        result = self.myParam.exist(paramName)
        self.assertFalse(result)
        
        # Test that the method handles adequately input parameters of incorrect
        # type by raising the required exception
        
        # Non str for paramName
        with self.assertRaises(TypeError):
            self.myParam.exist(42)
        
        # Close the project and restore its files to their original state
        self.finishTest()
        
        return
    
    def test_retrieve(self):
        """Open an example project and try to read an already existing
        parameter. Several reads are performed to test the different formats
        (float and expression) that can be used when retrieving a parameter.
        """
        self.projectName = "Filter_Example"
        
        # Open the project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Parameter object and pass to it the COM object to control the
        # example project
        self.myParam = cpa.Parameter(self.myCST._CST_MicrowaveStudio__MWS)
        
        #######################################
        # Perform several retrieval operations
        #######################################
        
        # Retrieve with float format a parameter defined as float
        result = self.myParam.retrieve("iris1", "float")
        self.assertEqual(result, 8.6)
        
        # Retrieve with expr format a parameter defined as float
        result = self.myParam.retrieve("iris1", "expr")
        self.assertEqual(result, "8.6")
        
        # Retrieve with float format a parameter defined as expression
        result = self.myParam.retrieve("res7", "float")
        self.assertEqual(result, 11.7)
        
        # Retrieve with expr format a parameter defined as expression
        result = self.myParam.retrieve("res7", "expr")
        self.assertEqual(result, "res1")
        
        # Retrieve with expr format a parameter defined as mathematical operation
        result = self.myParam.retrieve("lPort", "expr")
        self.assertEqual(result, "lambda0/2")
        
        # Test that the method handles adequately input parameters of incorrect
        # type or value by raising the required exceptions
        
        # Non str for paramName
        with self.assertRaises(TypeError):
            self.myParam.retrieve(42, "float")
        # Non str type for format
        with self.assertRaises(TypeError):
            self.myParam.retrieve("iris1", 42)
        # paramName references a non-existing parameter
        with self.assertRaises(RuntimeError):
            self.myParam.retrieve("nonExisting", "float")
        # format presents a non-valid value
        with self.assertRaises(ValueError):
            self.myParam.retrieve("iris1", "notValidFormat")
            
        # Close the project and restore its files to their original state
        self.finishTest()
        
        return
    
    def test_description(self):
        """Open an example project and try to add a description to an already
        existing parameter. Then, try to retrieve this same description.
        """
        self.projectName = "Filter_Example"
        
        # Open the project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Parameter object and pass to it the COM object to control the
        # example project
        self.myParam = cpa.Parameter(self.myCST._CST_MicrowaveStudio__MWS)
        
        description = "In a hole in the ground there lived a Hobbit."
        
        # Try to write the description
        self.myParam.addDescription("iris1", description)
        # Try to read the description
        readDescription = self.myParam.retrieveDescription("iris1")
        self.assertEqual(readDescription, description)
        
        # Test that the methods handle adequately input parameters of incorrect
        # type or value by raising the required exceptions
        
        # Non str for paramName
        with self.assertRaises(TypeError):
            self.myParam.addDescription(42, description)
        # Non str type for description
        with self.assertRaises(TypeError):
            self.myParam.addDescription("iris1", 42)
        # paramName references a non-existing parameter
        with self.assertRaises(RuntimeError):
            self.myParam.addDescription("nonExisting", description)
        # Description is longer than MAX_LENGTH_PARAMETER_DESCRIPTION
        with self.assertRaises(ValueError):
            self.myParam.addDescription("iris1", "a" * (200 + 1))
            
        # Non str for paramName
        with self.assertRaises(TypeError):
            self.myParam.retrieveDescription(42)
        # paramName references a non-existing parameter
        with self.assertRaises(RuntimeError):
            self.myParam.retrieveDescription("nonExisting")
    
        # Close the project and restore its files to their original state
        self.finishTest()
        
        return
        
    def test_rebuild(self):
        """Open an example project and try to modify an already existing
        parameter. Then try to rebuild the project.
        """
        self.projectName = "Filter_Example"
        
        # Open the project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Parameter object and pass to it the COM object to control the
        # example project
        self.myParam = cpa.Parameter(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Try to write a float and a str parameters
        self.myParam.change("iris1", 42.0)
        self.myParam.change("iris2", "iris1")
        
        # Try to rebuild the project
        self.myParam.rebuild()
        
        # Currently it is not possible to check the result of the rebuild
        # operation manually, so it has to be checked manually
        
        time.sleep(15)
        
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
    
if __name__ == '__main__':
    unittest.main()