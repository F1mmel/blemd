import bpy
import sys
import os.path
import logging.config
import io, os
import math
# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty
from bpy.types import Operator

if "bpy" in locals():  # trick to reload module on f8-press in blender
    LOADED = True
else:
    LOADED = False
    log_out = None
import bpy

if LOADED:
    from importlib import reload
    reload(BModel)
    reload(common)
    #log_out = log.handlers[1].stream  # kinda hacky, but it works (?)
else:
    if not logging.root.handlers:
        # if this list is not empty, logging is configured.
        # here, it isn't
        config_logging()
    from . import common, BModel
del LOADED

path=' '.join(sys.argv[4:])  # path to the bmd file

bpy.data.objects.remove(bpy.data.objects['Cube'])
bpy.data.meshes.remove(bpy.data.meshes['Cube'])

bpy.data.objects.remove(bpy.data.objects['Light'])
bpy.data.lights.remove(bpy.data.lights['Light'])

bpy.data.objects.remove(bpy.data.objects['Camera'])
bpy.data.cameras.remove(bpy.data.cameras['Camera'])

retcode = 'FINISHED'
temp = BModel.BModel()
path = os.path.abspath(os.path.split(__file__)[0])  # automatically find where we are
print(__file__)

bpy.data.objects.remove(bpy.data.objects['Cube'])
bpy.data.meshes.remove(bpy.data.meshes['Cube'])

bpy.data.objects.remove(bpy.data.objects['Light'])
py.data.lights.remove(bpy.data.lights['Light'])

bpy.data.objects.remove(bpy.data.objects['Camera'])
bpy.data.cameras.remove(bpy.data.cameras['Camera'])

        
temp.SetBmdViewExePath(path + os.sep)  # add 'backslash' for good measure
temp.Import(filename=self.filepath, **{x: getattr(self, x) for x in self.ALL_PARAMS})
            
for ob in bpy.data.objects:
    print (ob.name)
    try:
        ob.rotation_euler[0] = math.radians(90)
        print ("removed material from " + ob.name)
    except:
        print (ob.name + " does not have materials.")

try:
    bpy.ops.blemd.importer(filepath=path)
except AttributeError:  # module not loaded: do it manually
    import blemd
    temp = blemd.BModel.BModel()
    # current_dir = OSPath.abspath(OSPath.split(__file__)[0])  # automatically find where we are
    temp.SetBmdViewExePath(os.path.split(blemd.__file__)[0]+os.path.sep)  # add backslash for good measure
    temp.Import(path,
        boneThickness=5,
        frc_cr_bn=False,
        sv_anim='CHAINED',
        tx_pck='DO',
        ic_sc=True,
        imtype='TGA'
    )
    # actual model importing


# this line (below) is the export command. feel free to change it to whatever you want
bpy.ops.export_scene.fbx(filepath=path[:-3]+'fbx', axis_forward='Y', axis_up='Z', path_mode='COPY', embed_textures=True)

os.system("pause")