import bpy
import os

if not bpy.data.images:
    print("No imgs registered on bpy.data.images")

for img in bpy.data.images:
    path = bpy.path.abspath(img.filepath)
    print("\nImage:", img.name)
    print("  saved filepath:", img.filepath)
    print("  absolut path:", path)
    print("  Does exist:", os.path.exists(path))