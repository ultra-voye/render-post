import bpy

def update_stamp(scene):
    cam = bpy.data.objects.get("fspy-contemporary-copenhague.fspy.001")
    if not cam:
        return

    x, y, z = cam.location

    scene.render.use_stamp = True
    scene.render.use_stamp_note = True
    scene.render.stamp_font_size = 20

    # Text and background colors
    scene.render.stamp_foreground = (0.0, 0.0, 0.0, 1.0)
    scene.render.stamp_background = (0.0, 0.0, 0.0, 0.0)

    scene.render.stamp_note_text = (
        f"Camera pos:\nX={x:.2f}, Y={y:.2f}, Z={z:.2f}"
    )

bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(update_stamp)
