import time
import os
import numpy as np

import drop #how are we dealing with the fact that we might want to reuse controller code like this? drop controller is not in any package!
from experimental import (SCENARIOS, 
                          scenario_pathname,
                          get_drop_target_pairs)


class Rotator(object):
    def __init__(self, range_dict, seed=0, initial=None):
        if initial is None:
            initial = {}
        self.initial = initial
        self.xmin, self.xmax = range_dict['x']
        self.ymin, self.ymax = range_dict['y']
        self.zmin, self.zmax = range_dict['z']
        self.rng = np.random.RandomState(seed=seed)

    def __call__(self):
        xinit = self.initial.get('x', 0)
        yinit = self.initial.get('y', 0)
        zinit = self.initial.get('z', 0)
        xrot = self.rng.uniform(xinit + self.xmin, xinit + self.xmax)
        yrot = self.rng.uniform(yinit + self.ymin, yinit + self.ymax)
        zrot = self.rng.uniform(zinit + self.zmin, zinit + self.zmax)
        return {'x': xrot, 'y': yrot, 'z': zrot}


def main(output_dir, num, launch_build=True, port=1071):
    scenarios = get_drop_target_pairs(SCENARIOS)
    for i, ((sd, st), tp) in enumerate(scenarios):
        if isinstance(sd, str):
            drop_obj = sd 
            drop_rotation = {"x": 0, "y": 0, "z": 0}
            drop_scale = 1
        else:
            drop_obj, drop_rotation, drop_scale = sd
        if isinstance(st, str):
            target_obj = st
            target_rotation = {"x": 0, "y": 0, "z": 0}
            target_scale = 1
        else:
            target_obj, target_rotation, target_scale = st

        suffix = scenario_pathname(drop_obj, target_obj, tp)
        output_path = os.path.join(output_dir, suffix)
        temp_path = 'tmp' 

        drop_rotation_range = Rotator({"x": [-20, 20],
                                       "y": [-20, 20],
                                       "z": [-20, 20]},
                                       seed=i,
                                       initial=drop_rotation)

        if i == 0:
            dc = drop.Drop(launch_build=launch_build,
                       port=port,
                       randomize=0,
                       seed=0,
                       height_range=[2.1, 2.1],
                       drop_scale_range=drop_scale,
                       drop_jitter=0.35,
                       drop_rotation_range=drop_rotation_range,
                       drop_objects = [drop_obj],
                       target_objects = [target_obj],
                       target_scale_range=target_scale,
                       target_rotation_range=target_rotation,
                       camera_radius=2.5,
                       camera_min_angle=0,
                       camera_max_angle=0)

            initialization_commands = dc.get_initialization_commands(width=256,
                                                                     height=256)
            dc.communicate(initialization_commands)
        else:
            dc.clear_static_data()
            dc.drop_scale_range = drop_scale
            dc.target_scale_range = target_scale
            dc.drop_rotation_range = drop_rotation_range
            dc.target_rotation_range = target_rotation
            dc.set_drop_types([drop_obj])
            dc.set_target_types([target_obj])

        dc.trial_loop(num,
                      output_dir = output_path,
                      temp_path = temp_path)
                       
    dc.communicate({"$type": "terminate"})

