# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

###############################################
#                                             #
# Feature tests for CST_MicrowaveStudio class #
#                                             #
###############################################

import unittest
import os.path
import shutil # To delete a non-empty folder
import time
from .context import cst_python_api as cpa
from .context import dataFolder

class TestCSTMicrowaveStudio(unittest.TestCase):
    def test_connect_to_open_project(self):
        """Try to connect to the current active project. If successful, verify
        that the folder and file names of this project have been correctly
        retrieved and print them.
        
        ---------------
        Tested Methods
        ---------------
        - __init__()
        
        IMPORTANT: This test requires that CST is already running and a project
        has been opened.
        """
        myCST = cpa.CST_MicrowaveStudio()
        folder = myCST._CST_MicrowaveStudio__folder
        filename = myCST._CST_MicrowaveStudio__filename
        self.assertIsNotNone(folder, msg="Error while reading folder name of already open project.")
        self.assertIsNotNone(filename, msg="Error while reading file name of already open project.")
        print("Folder: " + folder)
        print("Filename: " + filename)
        
    def test_open_project(self):
        """Try to open the project Filter_Example.cst. If successful, verify
        that the folder and file names of this project have been correctly
        retrieved and print them.
        
        ---------------
        Tested Methods
        ---------------
        - __init__()
        - __openFile(): Opening an already existent project.
        - quit()
        
        """
        
        myCST = cpa.CST_MicrowaveStudio(dataFolder, "Filter_Example.cst")
        
        # Verify that the folder and filename registered at the object are the
        # correct ones.
        folder = myCST._CST_MicrowaveStudio__folder
        filename = myCST._CST_MicrowaveStudio__filename
        self.assertEqual(folder, dataFolder)
        self.assertEqual(filename + ".cst", "Filter_Example.cst")
        print("Folder: " + folder)
        print("Filename: " + filename)
        
        # Close the CST application
        myCST.quit()
        
        # Wait some time after closing CST before finishing the test. Otherwise
        # the test is not marked as successful.
        time.sleep(5)
        
        return
    
    def test_create_project(self):
        """Try to create a new project called Empty_Example.cst and save it.
        
        ---------------
        Tested Methods
        ---------------
        - __init__()
        - __openFile(): Opening a new project.
        - saveFile()
        - closeFile()
        
        """

        myCST = cpa.CST_MicrowaveStudio(dataFolder, "Empty_Example.cst")
        
        # Verify that the folder and filename registered at the object are the
        # correct ones.
        folder = myCST._CST_MicrowaveStudio__folder
        filename = myCST._CST_MicrowaveStudio__filename
        self.assertEqual(folder, dataFolder)
        self.assertEqual(filename + ".cst", "Empty_Example.cst")
        print("Folder: " + folder)
        print("Filename: " + filename)
        
        # Save the project
        myCST.saveFile()
        
        # Verify that the project has been saved. A CST file along with a folder
        # for the data of the project must have been created
        pathCSTFile = os.path.join(dataFolder, "Empty_Example.cst")
        pathProjDataFolder = os.path.join(dataFolder, "Empty_Example")
        projectExists = os.path.isfile(pathCSTFile)
        projDataExists = os.path.isdir(pathProjDataFolder)
        
        self.assertTrue(projectExists)
        self.assertTrue(projDataExists)
        
        # Close the project and delete the created files
        myCST.closeFile()
        
        # Wait some time to guarantee that CST has liberated the project files
        # and then remove them
        time.sleep(5)
        os.remove(pathCSTFile)
        shutil.rmtree(os.path.join(pathProjDataFolder))
        
        # Wait some time for the deletion of the files to be completed.
        # Otherwise the test is not marked as successful.
        time.sleep(10)
        
        return
        
if __name__ == '__main__':
    unittest.main()