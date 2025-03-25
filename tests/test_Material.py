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

class TestMaterial(unittest.TestCase):
    def test_addNormalMaterial(self):
        """Opens an existing project and tries to add some new materials. It is
        not possible to check automatically the success of this operation, so it
        must be checked manually.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Material object and pass to it the COM object to control the
        # example project
        self.myMaterial = cpa.Material(self.myCST._CST_MicrowaveStudio__MWS)
        
        self.myMaterial.addNormalMaterial(
            "Material1", 1.7, 4.2, [0.2, 0.4, 0.6])
        
        self.myMaterial.addNormalMaterial(
            "Material2", 0.07, 2.2, [0.5, 0.3, 0.1], tanD=0.01, tanDM=0.02)
        
        self.myMaterial.addNormalMaterial(
            "Material3", 0.07, 2.2, [0.5, 0.3, 0.1], sigma=1e7, sigmaM=5e6)
        
        self.myMaterial.addNormalMaterial(
            "Material4", "iris1", "res1", [0.4, 0.4, 0.4])
        
        # Currently it is not possible to check the result of the rebuild
        # operation manually, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # name not of type str
        with self.assertRaises(TypeError):
            self.myMaterial.addNormalMaterial(42, 1.7, 4.2, [0.2, 0.4, 0.6])
        # EM params not float or str
        with self.assertRaises(TypeError):
            self.myMaterial.addNormalMaterial("Material5", 1, 4.2, [0.2, 0.4, 0.6])
        # Any of the EM params is a str but it does not make reference to a
        # parameter that already exists in the project
        with self.assertRaises(RuntimeError):
            self.myMaterial.addNormalMaterial("Material5", "nonExisting", 4.2, [0.2, 0.4, 0.6])
        # colour is not a list
        with self.assertRaises(TypeError):
            self.myMaterial.addNormalMaterial("Material5", 1.7, 4.2, 0.0)
        # Any element of colour is not float
        with self.assertRaises(TypeError):
            self.myMaterial.addNormalMaterial("Material5", 1.7, 4.2, [0, 0.4, 0.6])
        # Length of colour is not 3
        with self.assertRaises(ValueError):
            self.myMaterial.addNormalMaterial("Material5", 1.7, 4.2, [0.4, 0.6])   
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_addAnisotropicMaterial(self):
        """Opens an existing project and tries to add some new materials. It is
        not possible to check automatically the success of this operation, so it
        must be checked manually.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Material object and pass to it the COM object to control the
        # example project
        self.myMaterial = cpa.Material(self.myCST._CST_MicrowaveStudio__MWS)
        
        self.myMaterial.addAnisotropicMaterial(
            "Material1", [1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [0.2, 0.4, 0.6])
        
        self.myMaterial.addAnisotropicMaterial(
            "Material2", ["iris1", "iris2", "iris3"], ["res1", "res2", "res3"],
            [0.4, 0.4, 0.4])
        
        # Currently it is not possible to check the result of the rebuild
        # operation manually, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct.
        
        # name not of type str
        with self.assertRaises(TypeError):
            self.myMaterial.addAnisotropicMaterial(
            42, [1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [0.2, 0.4, 0.6])
        # eps is not a list
        with self.assertRaises(TypeError):
            self.myMaterial.addAnisotropicMaterial(
            "Material3", 1.0, [4.0, 5.0, 6.0], [0.2, 0.4, 0.6])
        # Length of eps is not 3
        with self.assertRaises(ValueError):
            self.myMaterial.addAnisotropicMaterial(
                "Material3", [1.0, 2.0], [4.0, 5.0, 6.0], [0.2, 0.4, 0.6])
        # mu is not a list
        with self.assertRaises(TypeError):
            self.myMaterial.addAnisotropicMaterial(
            "Material3", [1.0, 2.0, 3.0], 4.0, [0.2, 0.4, 0.6])
        # Length of mu is not 3
        with self.assertRaises(ValueError):
            self.myMaterial.addAnisotropicMaterial(
                "Material3", [1.0, 2.0, 3.0], [4.0, 5.0], [0.2, 0.4, 0.6])
        # Any of the elements in eps or mu is not float or str
        with self.assertRaises(TypeError):
            self.myMaterial.addAnisotropicMaterial(
            "Material3", [0, 2.0, 3.0], [4.0, 5.0, 6.0], [0.2, 0.4, 0.6])
        # Any of the elements in eps or mu is a str but it does not make
        # reference to a parameter that already exists in the project
        with self.assertRaises(RuntimeError):
            self.myMaterial.addAnisotropicMaterial(
            "Material3", [1.0, 2.0, 3.0], ["nonExisting", 5.0, 6.0], [0.2, 0.4, 0.6])
        # colour is not a list
        with self.assertRaises(TypeError):
            self.myMaterial.addAnisotropicMaterial(
                "Material3", [1.0, 2.0, 3.0], [4.0, 5.0, 6.0], 0.2)
        # Length of colour is not 3
        with self.assertRaises(ValueError):
            self.myMaterial.addAnisotropicMaterial(
                "Material3", [1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [0.4, 0.6]) 
        # Any element of colour is not float
        with self.assertRaises(TypeError):
            self.myMaterial.addAnisotropicMaterial(
                "Material3", [1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [0, 0.4, 0.6])
          
        
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