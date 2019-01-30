import vispy.scene


def get_axis(orientation, **kwargs):
    key_vals = [
        ('axis_color', 'white'),
        ('tick_color', 'white'),
        ('text_color', 'white'),
        ('tick_width', 1),
    ]
    for key, default_val in key_vals:
        if key not in kwargs:
            kwargs[key] = default_val
    return vispy.scene.AxisWidget(orientation=orientation, **kwargs)
