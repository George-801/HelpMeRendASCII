"""
HELP!
NumPy doesn't like not being in its proper directory
we have to somehow trick it into thinking that
it is/use stack overflow enough

NumPy is currently the only issue

Daniel: I think i fixed the numpy issue
      
Daniel: What needs to be passed into the instantiateModel function?
for values model and coolourmap. Is it a file directory?

Daniel: Moved all functions into a class which passes its own engine and camera so the user does not have to keep track of it for themselves
--> noice

Daniel: what does the num_workers variable when initialiseREngine do?
--> no clue

I think we might actually be done?
"""


import math
from math import sin
from math import tan
from math import cos
import os
from HelpMeRendASCII.rendascii.interface import Engine as REngine


class RendASCIIHelper():

  def __init__(self, root_dir, asset_dir, colourmap_dir, model_dir, material_dir, num_workers=4):
    # Directories.
    self.root_dir = root_dir
    self.asset_dir = os.path.join(self.root_dir, asset_dir)
    self.colourmap_dir = os.path.join(self.asset_dir, colourmap_dir)
    self.model_dir = os.path.join(self.asset_dir, model_dir)
    self.material_dir = os.path.join(self.asset_dir, material_dir)
    # workers
    self.num_workers = num_workers
    # engine
    self.re = self.initialiseREngine()
    # camera
    self.cam = self.generateDefaultCamera()

  # Creates an instance of the REngine class - has defaults so to not require args
  def initialiseREngine(self):
    r_eng = REngine(
		colormap_dir=self.colourmap_dir,
		model_dir=self.model_dir,
		material_dir=self.material_dir,
		num_workers=self.num_workers
	)
    return r_eng

  # Registers a colourmap within the colourmaps directory
  # Colourmaps determine which character the engine will render
  # depending on the actual colour of a face on the model
  def registerColormap(self, name):
    self.re.load_colormap(
      colormap_name=name,
      colormap_filename=name + ".json"
    )

  # Registers a model within the inputted instance of REngine
  def registerModel(self, name, Lright_handed=True):
    self.re.load_model(
      model_name=name,
      model_filename=name + ".obj",
      right_handed=Lright_handed
    )

  # Passes default values into an re.create_camera() to speed up writing code
  def generateDefaultCamera(self):
    cam = self.re.create_camera(
      resolution=(50, 25),
      near=0.001,
      far=11.0,
      fov=math.radians(80.0),
      ratio=1.5,
      fog_char=' ',
      culling=False
    )
    return cam

  # Creates an instance of a model with transform
  # what needs to be passed here for it to work? file directory?....
  def instantiateModel(self, model, colormap, scale=1, tra_x=0, tra_y=0, tra_z=0, rot_x=0, rot_y=0, rot_z=0):
    # Instantiate model
    mdIns = self.re.create_model_instance(
      model_name=model,
      colormap_name=colormap
    )

    # Extra funky maths to determine a rotational matrix from euler angles (https://en.wikipedia.org/wiki/Rotation_matrix#General_rotations)

    alpha = [[1, 0, 0],
             [0, cos(rot_x), -sin(rot_x)],
             [0, sin(rot_x), cos(rot_x)]
            ]
    
    beta = [[cos(rot_y), 0, sin(rot_y)],
            [0, 1, 0],
            [-sin(rot_y), 0, cos(rot_y)]
           ]
    
    gamma = [[cos(rot_z), -sin(rot_z), 0],
             [sin(rot_z), cos(rot_z), 0],
             [0, 0, 1]
            ]

    """
    Now used, I still hate transformation matrices
    """
    rotationMatrix = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*beta)] for X_row in alpha]
    rotationMatrix = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*gamma)] for X_row in rotationMatrix]

    # Transform model
    mdIns.set_transformation(
      (
        (rotationMatrix[0][0], rotationMatrix[0][1], rotationMatrix[0][2], tra_x),
        (rotationMatrix[1][0], rotationMatrix[1][1], rotationMatrix[1][2], tra_y),
        (rotationMatrix[2][0], rotationMatrix[2][1], rotationMatrix[2][2], tra_z),
        (0.0, 0.0, 0.0, scale)
      )
    )

    # Return result 
    return mdIns


  # Render a frame, clear the previous frame and print the current frame
  def renderFrame(self):
    os.system("cls" if os.name == "nt" else "clear")
    frame = self.re.render_frame(camera=self.cam, as_str=True)
    print("Start\n" + frame + "\nend")