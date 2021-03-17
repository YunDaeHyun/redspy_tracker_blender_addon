bl_info = {
   "name": "Import redspy tracking data",
   "author": "DaeHyeon Yun",
   "description": "Imports redspy tracking data in blender",
   "version": (1, 0, 3),
   "blender": (2, 80, 0),
   "location": "File > Import-Export",
   "url": "Not yet",
   "wiki_url": "Not yet",
   "tracker_url": "Not yet",
   "category": "Import-Export"
}

try:
    if "bpy" in locals():
        import importlib
        importlib.reload(redspy_tracker)
        importlib.reload(addon)
    else:
        from . import redspy_tracker
        from . import addon

    import bpy

    def menu_func_import(self, context): 
        self.layout.operator(addon.ImportRedspyTrackingdata.bl_idname, text="redspy_trackingdata (.xml)")

    def register():
        bpy.utils.register_class(addon.ImportRedspyTrackingdata)
        # Add import menu item
        if hasattr(bpy.types, 'TOPBAR_MT_file_import'):
            #2.8+
            bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
        else:
            bpy.types.INFO_MT_file_import.append(menu_func_import)
        

    def unregister(): #
        bpy.utils.unregister_class(addon.ImportRedspyTrackingdata)
        # Remove import menu item
        if hasattr(bpy.types, 'TOPBAR_MT_file_import'):
            #2.8+
            bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
        else:
            bpy.types.INFO_MT_file_import.remove(menu_func_import)

    if __name__ == "__main__":
        register()

except ImportError: #예외처리
    # assume no bpy module. fail silently
    pass