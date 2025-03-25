# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

##################################
#                                #
# Unit tests for Component class #
#                                #
##################################

import unittest
import os.path
import time
import numpy as np # To define points for addPolygonBlock
from .context import cst_python_api as cpa
from .context import dataFolder
from .auxiliaryTestFunctions import restoreTestEnvironment

class TestComponent(unittest.TestCase):
    
    def test_new(self):
        """Create a new empty project. Try to create some components in this
        project and check that they are successfully created.
        
        Makes use of the exist() method.
        """
        
        self.projectName = "Empty_Project"
        
        # Open a new empty project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Component object and pass to it the COM object to control the
        # example project
        self.myComponent = cpa.Component(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Check that a component does not exist, then create it and check its
        # existance
        result = self.myComponent.exist("newComponent1")
        self.assertFalse(result)
        self.myComponent.new("newComponent1")
        result = self.myComponent.exist("newComponent1")
        self.assertTrue(result)
        
        # Do the same thing for a subcomponent inside of the formerly created
        # component Check that a component does not exist, then create it and
        # check its existance
        result = self.myComponent.exist("newComponent1/subcomponent1")
        self.assertFalse(result)
        self.myComponent.new("newComponent1/subcomponent1")
        result = self.myComponent.exist("newComponent1/subcomponent1")
        self.assertTrue(result)
        
        # The same test but creating a subcomponent directly on a component
        # which does not exist yet
        result = self.myComponent.exist("newComponent2/subcomponent1")
        self.assertFalse(result)
        self.myComponent.new("newComponent2/subcomponent1")
        result = self.myComponent.exist("newComponent2/subcomponent1")
        self.assertTrue(result)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # name not of type str
        with self.assertRaises(TypeError):
            self.myComponent.new(42)
            
        # name contains an invalid character
        with self.assertRaises(RuntimeError):
            self.myComponent.new("newComponent1?")
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_delete(self):
        """Create a new empty project. Create some components in this project,
        try to delete them and check that they have been successfully deleted.
        
        Makes use of the new() and exist() methods.
        """
        
        self.projectName = "Empty_Example"
        
        # Open a new empty project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Component object and pass to it the COM object to control the
        # example project
        self.myComponent = cpa.Component(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Create a component containing a subcomponent and verify the existance
        # of both of them
        self.myComponent.new("newComponent1")
        result = self.myComponent.exist("newComponent1")
        self.assertTrue(result)
        self.myComponent.new("newComponent1/subcomponent1")
        result = self.myComponent.exist("newComponent1/subcomponent1")
        self.assertTrue(result)
        
        # Delete the subcomponent and check that it has effectively been deleted
        self.myComponent.delete("newComponent1/subcomponent1")
        result = self.myComponent.exist("newComponent1/subcomponent1")
        self.assertFalse(result)
        
        # Do the same thing for the component
        self.myComponent.delete("newComponent1")
        result = self.myComponent.exist("newComponent1")
        self.assertFalse(result)
        
        # Create a component containing a subcomponent and verify the existance
        # of both of them
        self.myComponent.new("newComponent2")
        result = self.myComponent.exist("newComponent2")
        self.assertTrue(result)
        self.myComponent.new("newComponent2/subcomponent1")
        result = self.myComponent.exist("newComponent2/subcomponent1")
        self.assertTrue(result)
        
        # Delete the component (before deleting the subcomponent) and check that
        # neither the component, nor the subcomponent exist anymore
        self.myComponent.delete("newComponent2")
        result = self.myComponent.exist("newComponent2")
        self.assertFalse(result)
        result = self.myComponent.exist("newComponent2/subcomponent1")
        self.assertFalse(result)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # name not of type str
        with self.assertRaises(TypeError):
            self.myComponent.delete(42)
            
        # name does not indicate a component existing in the project
        with self.assertRaises(ValueError):
            self.myComponent.delete("nonExisting")
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_rename(self):
        """Create a new empty project. Create some components in this project
        and try to rename them. Check that the renaming process was successful.
        
        Makes use of the new() and exist() methods.
        """
        
        self.projectName = "Empty_Example"
        
        # Open a new empty project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Component object and pass to it the COM object to control the
        # example project
        self.myComponent = cpa.Component(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Create a component containing a subcomponent and verify the existance
        # of both of them
        self.myComponent.new("newComponent1")
        result = self.myComponent.exist("newComponent1")
        self.assertTrue(result)
        self.myComponent.new("newComponent1/subcomponent1")
        result = self.myComponent.exist("newComponent1/subcomponent1")
        self.assertTrue(result)
        
        # Rename the compenent and check that this operation was sucessful
        self.myComponent.rename("newComponent1", "newComponent2")
        result = self.myComponent.exist("newComponent1")
        self.assertFalse(result)
        result = self.myComponent.exist("newComponent2")
        self.assertTrue(result)
        
        # Do the same thing for the subcomponent
        self.myComponent.rename("newComponent2/subcomponent1", "newComponent2/subcomponent2")
        result = self.myComponent.exist("newComponent2/subcomponent1")
        self.assertFalse(result)
        result = self.myComponent.exist("newComponent2/subcomponent2")
        self.assertTrue(result)
        
        # Make use of the rename operation to move the subcomponent out of the
        # component
        self.myComponent.rename("newComponent2/subcomponent2", "subcomponent2")
        result = self.myComponent.exist("newComponent2/subcomponent2")
        self.assertFalse(result)
        result = self.myComponent.exist("subcomponent2")
        self.assertTrue(result)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # name not of type str
        with self.assertRaises(TypeError):
            self.myComponent.rename(42, "subcomponent2")
        # name not of type str
        with self.assertRaises(TypeError):
            self.myComponent.rename("subcomponent2", 42)
            
        # name does not indicate a component existing in the project
        with self.assertRaises(ValueError):
            self.myComponent.rename("nonExisting", "subcomponent2")
            
        # newName contains an invalid character
        with self.assertRaises(RuntimeError):
            self.myComponent.rename("subcomponent2", "subcomponent2:")
        
        # Close the project and restore the files to their original state
        self.finishTest()
    
    def test_exist(self):
        """Open an existing project and check if certain components do exist in
        the project. Some of them do really exist, and others do not.
        """
        
        self.projectName = "Filter_Example"
        
        # Open an already existing project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Component object and pass to it the COM object to control the
        # example project
        self.myComponent = cpa.Component(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Check if an existing component does indeed exist
        result = self.myComponent.exist("component1")
        self.assertTrue(result)
        
        # Now ask about a component which does not exist
        result = self.myComponent.exist("nonExisting")
        self.assertFalse(result)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # name not of type str
        with self.assertRaises(TypeError):
            self.myComponent.exist(42)
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_ensureExistence(self):
        """Create a new empty project. Create some new components via the
        ensureExistence() method
        
        Makes use of the exist() method.
        """
        
        self.projectName = "Empty_Example"
        
        # Open a new empty project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Component object and pass to it the COM object to control the
        # example project
        self.myComponent = cpa.Component(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Check that a component does not exist, then use the ensureExistence()
        # method and check that the project was successfully created
        result = self.myComponent.exist("newComponent1")
        self.assertFalse(result)
        self.myComponent.ensureExistence("newComponent1")
        result = self.myComponent.exist("newComponent1")
        self.assertTrue(result)
        
        # Do the same thing for a subcomponent
        result = self.myComponent.exist("newComponent1/subcomponent1")
        self.assertFalse(result)
        self.myComponent.ensureExistence("newComponent1/subcomponent1")
        result = self.myComponent.exist("newComponent1/subcomponent1")
        self.assertTrue(result)
        
        # Try to ensure the existance of a component that already exists.
        # Nothing should happen.
        self.myComponent.ensureExistence("newComponent1")
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # name not of type str
        with self.assertRaises(TypeError):
            self.myComponent.ensureExistence(42)
            
        # newName contains an invalid character
        with self.assertRaises(RuntimeError):
            self.myComponent.ensureExistence("newComponent2?")
        
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