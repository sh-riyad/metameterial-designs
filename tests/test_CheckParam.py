# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

#################################
#                               #
# Unit tests for Material class #
#                               #
#################################

import unittest
import os.path
import time
from .context import cst_python_api as cpa
from .context import dataFolder
from .auxiliaryTestFunctions import restoreTestEnvironment

class TestCheckParam(unittest.TestCase):
    
    def test_doCheck(self):
        """Checks that the doCheck() method behaves correctly when it receives
        parameters of different type.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create CheckParam object and pass to it the COM object to control the
        # example project
        self.myCheck = cpa.CheckParam(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Check that a float is processed correctly.
        result = self.myCheck.doCheck(1.0)
        self.assertEqual(result, "1.0")
        
        # Check that a string indicating a parameter existing in the project is
        # processed correctly.
        result = self.myCheck.doCheck("iris1")
        self.assertEqual(result, "iris1")
        
        # Check that parameters other than float or str raise produce an exception.
        with self.assertRaises(TypeError):
            self.myCheck.doCheck(42)
        
        # Check that strings which do not make reference to a parameter already
        # existing in the project do produce an exception.   
        with self.assertRaises(RuntimeError):
            self.myCheck.doCheck("nonExistingParam")
            
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