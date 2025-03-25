# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

##############################
#                            #
# Unit tests for Shape class #
#                            #
##############################

import unittest
import os.path
import time
import numpy as np # To define points for addPolygonBlock
from .context import cst_python_api as cpa
from .context import dataFolder
from .auxiliaryTestFunctions import restoreTestEnvironment

class TestShape(unittest.TestCase):
    def test_addBrick(self):
        """Opens an existing project and tries to add some new bricks. It is
        not possible to check automatically the success of this operation, so it
        must be checked manually.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Shape object and pass to it the COM object to control the
        # example project
        self.myShape = cpa.Shape(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Create a brick inside a new component
        self.myShape.addBrick(
            -2.0, 2.0, -5.0, 5.0, 0.0, 10.0, "Brick1", "Bricks", "PEC")
        
        # Create a brick inside a new subcomponent
        self.myShape.addBrick(
            -5.0, 5.0, -2.0, 2.0, -10.0, 0.0, "Brick2", "Bricks/Sub-bricks", "PEC")
        
        # Create a brick inside an existing component, using parameters to
        # specify its dimensions
        self.myShape.addBrick(
            "iris1", 12.0, "bWG", "aWG", 5.0, "lambda0", "Brick3", "component1", "Vacuum")
        
        # Currently it is not possible to check the result of the former
        # operations manually, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # name not of type str
        with self.assertRaises(TypeError):
            self.myShape.addBrick(
                -2.0, 2.0, -5.0, 5.0, 0.0, 10.0, 42, "Bricks", "PEC")
        # component not of type str
        with self.assertRaises(TypeError):
            self.myShape.addBrick(
                -2.0, 2.0, -5.0, 5.0, 0.0, 10.0, "Brick4", 4, "PEC")
        # material not of type str
        with self.assertRaises(TypeError):
            self.myShape.addBrick(
                -2.0, 2.0, -5.0, 5.0, 0.0, 10.0, "Brick4", "Bricks", 42)
        # Geometric params not float or str
        with self.assertRaises(TypeError):
            self.myShape.addBrick(
                -2, 2, -5.0, 5.0, 0.0, 10.0, "Brick4", "Bricks", "PEC")
        # Any of the geometric params is a str but it does not make reference to a
        # parameter that already exists in the project
        with self.assertRaises(RuntimeError):
            self.myShape.addBrick(
                "nonExisting", 2.0, -5.0, 5.0, 0.0, 10.0, "Brick4", "Bricks",
                "PEC")
        # If the specified name is already in use in the project
        with self.assertRaises(RuntimeError):
            self.myShape.addBrick(
                "iris1", 12.0, "bWG", "aWG", 5.0, "lambda0", "Brick3",
                "component1", "PEC")
        # If the specified material is not defined in the project
        with self.assertRaises(RuntimeError):
            self.myShape.addBrick(
                "iris1", 12.0, "bWG", "aWG", 5.0, "lambda0", "Brick4",
                "component1", "nonExistingMaterial")
 
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_addCylinder(self):
        """Opens an existing project and tries to add some new cylinders. It is
        not possible to check automatically the success of this operation, so it
        must be checked manually.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Shape object and pass to it the COM object to control the
        # example project
        self.myShape = cpa.Shape(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Create a cylinder inside a new component
        self.myShape.addCylinder(
            -5.0, 2.0, 0.0, 1.0, 0.0, "Cylinder1", "Cylinders", "PEC", "x", xMax=10.0)
        
        # Create a cylinder inside a new subcomponent
        self.myShape.addCylinder(
            0.0, 5.0, 0.0, 1.0, 0.0, "Cylinder2", "Cylinders/Sub-cylinders",
            "PEC", "z", zMax=10.0, nSegments=6)
        
        # Create a cylinder inside an existing component, using parameters to
        # specify its dimensions
        self.myShape.addCylinder(
            0.0, -4.0, "iris1", 2.0, 1.0, "Cylinder3", "Cylinders", "Vacuum",
            "y", yMax="res1")
        
        # Currently it is not possible to check the result of the former
        # operations manually, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # name not of type str
        with self.assertRaises(TypeError):
            self.myShape.addCylinder(
                -5.0, 2.0, 0.0, 1.0, 0.0, 42, "Cylinders", "PEC", "x", xMax=10.0)
        # component not of type str
        with self.assertRaises(TypeError):
            self.myShape.addCylinder(
                -5.0, 2.0, 0.0, 1.0, 0.0, "Cylinder1", 42, "PEC", "x", xMax=10.0)
        # material not of type str
        with self.assertRaises(TypeError):
            self.myShape.addCylinder(
                -5.0, 2.0, 0.0, 1.0, 0.0, "Cylinder1", "Cylinders", 42, "x",
                xMax=10.0)
        # Orientation different of "x", "y" or "z"
        with self.assertRaises(ValueError):
            self.myShape.addCylinder(
                -5.0, 2.0, 0.0, 1.0, 0.0, "Cylinder1", "Cylinders", "PEC", "a",
                xMax=10.0)
        # nSegments taking a value smaller than 3 and different of 0
        with self.assertRaises(ValueError):
            self.myShape.addCylinder(
                -5.0, 2.0, 0.0, 1.0, 0.0, "Cylinder1", "Cylinders", "PEC", "x",
                xMax=10.0, nSegments=1)
        # nSegments not of type int
        with self.assertRaises(TypeError):
            self.myShape.addCylinder(
                -5.0, 2.0, 0.0, 1.0, 0.0, "Cylinder1", "Cylinders", "PEC", "x",
                xMax=10.0, nSegments=3.5)
        # Geometric params not float or str
        with self.assertRaises(TypeError):
            self.myShape.addBrick(
                -5, 2.0, 0.0, 1.0, 0.0, "Cylinder1", "Cylinders", "PEC", "x",
                xMax=10.0)
        # Any of the geometric params is a str but it does not make reference to
        # a parameter that already exists in the project
        with self.assertRaises(RuntimeError):
            self.myShape.addCylinder(
                "nonExisting", 2.0, 0.0, 1.0, 0.0, "Cylinder1", "Cylinders",
                "PEC", "x", xMax=10.0)
        # If the specified name is already in use in the project
        with self.assertRaises(RuntimeError):
            self.myShape.addCylinder(
                -4.0, 2.0, 0.0, 2.0, 0.0, "Cylinder1", "Cylinders", "PEC", "x",
                xMax=10.0)
        # If the specified material is not defined in the project
        with self.assertRaises(RuntimeError):
            self.myShape.addCylinder(
                -4.0, 2.0, 0.0, 2.0, 0.0, "Cylinder4", "Cylinders",
                "nonExistingMaterial", "x", xMax=10.0)
 
        
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_addSphere(self):
        """Opens an existing project and tries to add some new spheres. It is
        not possible to check automatically the success of this operation, so it
        must be checked manually.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Shape object and pass to it the COM object to control the
        # example project
        self.myShape = cpa.Shape(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Create a sphere inside a new component
        self.myShape.addSphere(
            0.0, 2.0, 0.0, 3.5, "Sphere1", "Spheres", "PEC", topRad=0.5, botRad=1.0)
        
        # Create a sphere inside a new subcomponent
        self.myShape.addSphere(
            -5.0, 0.0, 3.0, 3.5, "Sphere2", "Spheres/Sub-spheres", "PEC",
            topRad=2.0, botRad=0.20, orientation="y", nSegments=7)
        
        # Create a sphere inside an existing component, using parameters to
        # specify its dimensions
        self.myShape.addSphere(
            "res1", 0.0, "iris1", 2.0, "Sphere3", "Spheres", "Vacuum")
        
        # Currently it is not possible to check the result of the former
        # operations manually, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # name not of type str
        with self.assertRaises(TypeError):
            self.myShape.addSphere(
                0.0, 2.0, 0.0, 3.5, 42, "Spheres", "PEC", topRad=0.5, botRad=1.0)
        # component not of type str
        with self.assertRaises(TypeError):
            self.myShape.addSphere(
            0.0, 2.0, 0.0, 3.5, "Sphere4", 42, "PEC", topRad=0.5, botRad=1.0)
        # material not of type str
        with self.assertRaises(TypeError):
            self.myShape.addSphere(
                0.0, 2.0, 0.0, 3.5, "Sphere4", "Spheres", 42, topRad=0.5, botRad=1.0)
        # Orientation different of "x", "y" or "z"
        with self.assertRaises(ValueError):
            self.myShape.addSphere(
                0.0, 2.0, 0.0, 3.5, "Sphere4", "Spheres", "PEC", topRad=0.5, botRad=1.0, orientation="a")
        # nSegments taking a value smaller than 3 and different of 0
        with self.assertRaises(ValueError):
            self.myShape.addSphere(
                0.0, 2.0, 0.0, 3.5, "Sphere4", "Spheres", "PEC", topRad=0.5, botRad=1.0, nSegments=-1)
        # nSegments not of type int
        with self.assertRaises(TypeError):
            self.myShape.addSphere(
                0.0, 2.0, 0.0, 3.5, "Sphere4", "Spheres", "PEC", topRad=0.5, botRad=1.0, nSegments=3.5)
        # Geometric params not float or str
        with self.assertRaises(TypeError):
            self.myShape.addSphere(
                0, 2.0, 0.0, 3.5, "Sphere4", "Spheres", "PEC", topRad=0.5, botRad=1.0)
        # Any of the geometric params is a str but it does not make reference to
        # a parameter that already exists in the project
        with self.assertRaises(RuntimeError):
            self.myShape.addSphere(
                "nonExisting", 2.0, 0.0, 3.5, "Sphere4", "Spheres", "PEC", topRad=0.5, botRad=1.0)
        # If the specified name is already in use in the project
        with self.assertRaises(RuntimeError):
            self.myShape.addSphere(
                0.0, 2.0, 0.0, 3.5, "Sphere1", "Spheres", "PEC", topRad=0.5, botRad=1.0)
        # If the specified material is not defined in the project
        with self.assertRaises(RuntimeError):
            self.myShape.addSphere(
                0.0, 2.0, 0.0, 3.5, "Sphere1", "Spheres", "nonExistingMaterial", topRad=0.5, botRad=1.0)
            
        # Close the project and restore the files to their original state
        self.finishTest()
        
    def test_addPolygonBlock(self):
        """Opens an existing project and tries to add some new extruded
        polygons. It is not possible to check automatically the success of this
        operation, so it must be checked manually.
        """
        
        self.projectName = "Filter_Example"
        
        # Open the example project
        self.myCST = cpa.CST_MicrowaveStudio(dataFolder, self.projectName + ".cst")
        
        # Create Shape object and pass to it the COM object to control the
        # example project
        self.myShape = cpa.Shape(self.myCST._CST_MicrowaveStudio__MWS)
        
        # Create a cylinder inside a new component
        points = np.array([
            [0.0, 7.0], [5.0, 5.0], [5.0, -5.0], [-5.0, -5.0], [-5.0, 5.0], [0.0, 7.0]
        ])
        self.myShape.addPolygonBlock(
            points, 10.0, "Block1", "Blocks", "PEC")
        
        # Create a block inside a new subcomponent
        self.myShape.addPolygonBlock(
            points+2.0, 3.5, "Block2", "Blocks/Sub-blocks", "PEC", zMin = -5.0)
        
        # Create a block inside an existing component, using parameters to
        # specify its dimensions
        self.myShape.addPolygonBlock(
            points-2.0, "res1", "Block3", "Blocks", "Vacuum", zMin = "iris1")
        
        
        # Currently it is not possible to check the result of the former
        # operations manually, so it has to be checked manually
        time.sleep(15)
        
        # Check that adequate exceptions are raised when received input
        # parameters are not correct
        
        # name not of type str
        with self.assertRaises(TypeError):
            self.myShape.addPolygonBlock(
                points, 10.0, 42, "Blocks", "PEC")
        # component not of type str
        with self.assertRaises(TypeError):
            self.myShape.addPolygonBlock(
                points, 10.0, "Block4", 42, "PEC")
        # material not of type str
        with self.assertRaises(TypeError):
            self.myShape.addPolygonBlock(
                points, 10.0, "Block4", "Blocks", 42)
        # points not of type numpy array
        wrongPoints = [
            [0.0, 7.0], [5.0, 5.0], [5.0, -5.0], [-5.0, -5.0], [-5.0, 5.0], [0.0, 7.0]
        ]
        with self.assertRaises(TypeError):
            self.myShape.addPolygonBlock(
                wrongPoints, 10.0, "Block4", "Blocks", "PEC")
        # Elements of points are not of type float
        wrongPoints = np.array([
            [0, 7], [5, 5], [5, -5], [-5, -5], [-5, 5], [0, 7]
        ])
        with self.assertRaises(TypeError):
            self.myShape.addPolygonBlock(
                wrongPoints, 10.0, "Block4", "Blocks", "PEC")
        # points contains less than three vertices
        wrongPoints = np.array([
            [0.0, 7.0], [5.0, 5.0]
        ])
        with self.assertRaises(ValueError):
            self.myShape.addPolygonBlock(
                wrongPoints, 10.0, "Block4", "Blocks", "PEC")
        # Number of coordinates of each point different of 2
        wrongPoints = np.array([
            [0.0], [5.0], [5.0], [-5.0], [-5.0], [0.0]
        ])
        with self.assertRaises(ValueError):
            self.myShape.addPolygonBlock(
                wrongPoints, 10.0, "Block4", "Blocks", "PEC")
        # If the first and las points are not the same
        wrongPoints = np.array([
            [0.0, 7.0], [5.0, 5.0], [5.0, -5.0], [-5.0, -5.0], [-5.0, 5.0]
        ])
        with self.assertRaises(ValueError):
            self.myShape.addPolygonBlock(
                wrongPoints, 10.0, "Block4", "Blocks", "PEC")    
        # Geometric params not float or str
        with self.assertRaises(TypeError):
            self.myShape.addPolygonBlock(
                points, 42, "Block4", "Blocks", "PEC")
        # Any of the geometric params is a str but it does not make reference to
        # a parameter that already exists in the project
        with self.assertRaises(RuntimeError):
            self.myShape.addPolygonBlock(
                points, 10.0, "Block4", "Blocks", "PEC", zMin="nonExisting")
        # If the specified name is already in use in the project
        with self.assertRaises(RuntimeError):
            self.myShape.addPolygonBlock(
                points, 10.0, "Block1", "Blocks", "PEC")
        # If the specified material is not defined in the project
        with self.assertRaises(RuntimeError):
            self.myShape.addPolygonBlock(
                points, 10.0, "Block4", "Blocks", "nonExistingMaterial")
            
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