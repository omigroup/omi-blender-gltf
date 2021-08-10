from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
import bpy

import os
OMI_DEBUG = os.environ.get("OMI_DEBUG", False)

class OMIExtension:
    Extension = Extension

    @staticmethod
    def autoregister(all):
        # autodetect registerable bpy.types 
        for k, v in all.items():
            name = v.__class__.__name__
            if name == "RNAMeta" or name == "RNAMetaPropGroup":
                if OMI_DEBUG: print("register_class", k, name)
                bpy.utils.register_class(v)

# dynamically scan for OMIExtension subclasses in the current directory
def queryExtensions():
    extensions = []
    package_dir = Path(__file__).resolve().parent
    for (_, module_name, _) in iter_modules([package_dir]):
        module = import_module(f"{__name__}.{module_name}")

        if OMI_DEBUG: print("scanning", module_name, f"{__name__}.{module_name}", module is OMIExtension, OMIExtension.__name__)

        for attribute_name in dir(module):
            if attribute_name == "OMIExtension":
                continue
            attribute = getattr(module, attribute_name)
            if isclass(attribute) and issubclass(attribute, OMIExtension):
                print("found omi extension", attribute_name, attribute)
                extensions.append(attribute)
    return extensions
