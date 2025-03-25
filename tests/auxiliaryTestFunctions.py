# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os.path
import shutil # To delete a non-empty folder
import time
import git # Used to restore the CST test project to its original state

def restoreTestEnvironment(pathCSTFile, pathProjDataFolder):
    """Restores a CST project to its original state.
    
    Deletes the data folder of the project if this was created by CST, as well
    as an eventual back-up folder in case that the project is opened with a
    different version of that used for creating it.

    Parameters
    ----------
    pathCSTFile : str
        Absolute path to CST file.
    pathProjDataFolder : str
        Absolute path to project data folder.
    """
    
    # Wait for for some time to guarantee that CST has liberated the project
    # files and then remove them
    time.sleep(5)
    
    # Delete the folder with the project data.
    try:
        shutil.rmtree(pathProjDataFolder)
    except Exception as errMsg:
        print("WARNING: Failed to delete folder with project data. " +
              "Please, delete it manually before launching a new test: "+ 
              "{}".format(errMsg))
    
    # In case that a newer/older CST version is used to open the example
    # project, CST will create a back-up folder to store the original
    # project. Delete this folder too.
    backUpDataExists = os.path.isdir(pathProjDataFolder + ".bak1")
    if backUpDataExists:
        try:
            shutil.rmtree(pathProjDataFolder + ".bak1")
        except Exception as errMsg:
            print("WARNING: Failed to delete folder with back-up project " +
              "data. Please, delete it manually before launching a new "+ 
              "test: {}".format(errMsg))
    
    # Restore the project file to its original state.
    try:
        repo = git.Repo(".")
        repo.git.checkout('--', pathCSTFile)
        print(f"Restored {pathCSTFile} to its original state.")
    except Exception as errMsg:
        print(f"Failed to restore {pathCSTFile}: {errMsg}")
        
    return

def deleteTestProject(pathCSTFile, pathProjDataFolder):
    """Deletes a CST project generated during a test.
    
    Deletes the data folder of the project if this was created by CST, as well
    as the project file.

    Parameters
    ----------
    pathCSTFile : str
        Absolute path to CST file.
    pathProjDataFolder : str
        Absolute path to project data folder.
    """
    
    # Wait for for some time to guarantee that CST has liberated the project
    # files and then remove them
    time.sleep(5)
    
    # Delete the folder with the project data.
    try:
        shutil.rmtree(pathProjDataFolder)
    except Exception as errMsg:
        print("WARNING: Failed to delete folder with project data. " +
              "Please, delete it manually before launching a new test: "+ 
              "{}".format(errMsg))
    
    # Delete the folder with the project data.
    try:
        os.remove(pathCSTFile)
    except Exception as errMsg:
        print("WARNING: Failed to delete the project file. " +
              "Please, delete it manually before launching a new test: "+ 
              "{}".format(errMsg))
        
    return
        