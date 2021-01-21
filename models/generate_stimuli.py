import time
import os
import numpy as np

import drop #how are we dealing with the fact that we might want to reuse controller code like this? drop controller is not in any package!

OBJECT_INFO = {}

CONTAIN_SCENARIOS = [(('torus', {"x": 0, "y": 0, "z": 0}, 0.8), 
                      [('cone', {"x": 0, "y": 0, "z": 0}, 0.9), 
                       ('dumbbell', {"x": 0, "y": 0, "z": 0}, 0.5)]),
                     (('bowl', {"x": 0, "y": 0, "z": 180}, 1.15), 
                      ['pyramid', 
                       ('triangular_prism', {"x": 0, "y": 90., "z": 0}, 1)]),
                     (('cone', {"x": 0, "y": 0, "z": 180}, 0.9),
                      [('torus', {"x": 0, "y": 0, "z": 0}, 0.8), 
                      ('octahedron', {"x": 0, "y": 0, "z": 90}, 1)]),
                     (('dumbbell', {"x": 90, "y": 0, "z": 0}, .5), 
                      [('pipe', 
                        {"x": 0, "y": 0, "z": 0}, 
                        {"x": 1, "y": 0.35, "z": 1}),
                       ('pyramid', 
                        {"x": 0, "y": 0, "z": 0}, 
                        0.8)]),
                     ('octahedron', 
                      [('pipe', 
                        {"x": 0, "y": 0, "z": 0}, 
                        {"x": 1, "y": 0.35, "z": 1}),
                      'sphere']),
                     (('pentagon',
                       {"x": 0, "y": 0, "z": 0}, 
                       {"x": 0.7, "y": 0.49, "z": 0.7}), 
                      [('bowl', {"x": 0, "y": 0, "z": 0}, 1.15), 
                       ('sphere',{"x": 0, "y": 0, "z": 0}, 0.7)]),
                     (('pipe', 
                        {"x": 0, "y": 0, "z": 0}, 
                        {"x": 1, "y": 0.35, "z": 1}),
                      [('cone', {"x": 0, "y": 0, "z": 0}, 0.9), 
                      ('octahedron', {"x": 0, "y": 0, "z": 90.}, 1)]),
                     (('pyramid', {"x": 0, "y": 0, "z": 180}, 1), 
                      [('torus', {"x": 0, "y": 0, "z": 0}, 0.8),
                       ('dumbbell', {"x": 0, "y": 0, "z": 0}, 0.5)]),
                     (('sphere', {"x": 0, "y": 0, "z": 0}, 0.8), 
                      [('bowl', {"x": 0, "y": 0, "z": 0}, 1.15), 
                       ('pentagon',
                        {"x": 0, "y": 0, "z": 0}, 
                        {"x": 0.8, "y": 0.56, "z": 0.8})
                       ]),
                     (('triangular_prism',
                       {"x": 0, "y": 0, "z": 90},
                       {"x": 1, "y": 0.6, "z": 0.6}),
                      [('bowl', {"x": 0, "y": 0, "z": 0}, 1.15), 
                       ('dumbbell', {"x": 0, "y": 0, "z": 0}, 0.5)])
                      ]

SUPPORT_SCENARIOS = [
                     (('bowl', {"x": 0, "y": 0, "z": 180}, 1.15), 
                      [('torus', {"x": 0, "y": 0, "z": 0}, 0.8), 
                       ('triangular_prism', 
                        {"x": 0, "y": 0, "z": 0},
                        {"x": 1, "y": 0.6, "z": 0.6})]),
                     (('cone', {"x": 0, "y": 0, "z": 0}, 0.9), 
                      [('triangular_prism',
                        {"x": 0, "y": 0., "z": 90}, 
                        {"x": 1, "y": 0.8, "z": 0.8}),
                       'sphere']),
                     (('dumbbell', {"x": 0, "y": 0, "z": 0}, 0.5), 
                      [('pentagon', 
                        {"x": 0, "y": 0, "z": 0}, 
                        {"x": 1, "y": 0.7, "z": 1}),
                      'octahedron']),
                     (('octahedron', {"x": 0, "y": 0, "z": 90.}, 1), 
                     [('pentagon', 
                        {"x": 0, "y": 0, "z": 0}, 
                        {"x": 1, "y": 0.7, "z": 1}), 
                      'pyramid']),
                     (('pentagon', 
                      {"x": 0, "y": 0, "z": 0},
                      {"x": 1, "y": 0.7, "z": 1}), 
                     [('pipe', 
                       {"x": 0, "y": 0, "z": 0}, 
                       {"x": 1, "y": 0.35, "z": 1}),
                      'pyramid']),
                     (('pipe',
                      {"x": 0, "y": 0, "z": 0},
                      {"x": 1, "y": 0.35, "z": 1}), 
                     [('torus', {"x": 0, "y": 0, "z": 0}, 0.8), 
                     ('dumbbell', {"x": 0, "y": 0, "z": 0}, 0.5)]),
                     (('pyramid', {"x": 0, "y": 0., "z": 0}, .8), 
                      [('triangular_prism', 
                       {"x": 0, "y": 0., "z": 90}, 
                       {"x": 1.2, "y": 0.96, "z": 0.96}),
                       'sphere']),
                     ('sphere', 
                      [('pipe',
                        {"x": 0, "y": 0, "z": 0},
                        {"x": 1, "y": 0.35, "z": 1}),
                      ('cone', {"x": 0, "y": 0, "z": 0}, 0.9)]),
                     (('torus', {"x": 0, "y": 0, "z": 0}, 0.8), 
                      [('bowl', {"x": 0, "y": 0, "z": 0}, 1.15), 
                       ('octahedron', {"x": 0, "y": 0, "z": 0}, 0.6)]),
                     ('triangular_prism', 
                      [('pentagon',
                        {"x": 0, "y": 0, "z": 0},
                        {"x": 1, "y": 0.7, "z": 1}),
                      ('cone', {"x": 0, "y": 0, "z": 0}, 0.9)])
                     ]

CONTAIN_SCENARIOS = [(x, 'contain') for x in CONTAIN_SCENARIOS]
SUPPORT_SCENARIOS = [(x, 'support') for x in SUPPORT_SCENARIOS]

SCENARIOS = CONTAIN_SCENARIOS + SUPPORT_SCENARIOS

def get_drop_target_pairs(scenarios):
    pairs = []
    for (sd, st), stype in scenarios:
        if ((sd, st[0]), stype) not in scenarios:
            pairs.append(((sd, st[0]), stype))
        if ((sd, st[1]), stype) not in scenarios:
            pairs.append(((sd, st[1]), stype))
    return pairs


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

        suffix = '%s_on_%s_%s' % (drop_obj, target_obj, tp)
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
                       height_range=[1.9, 1.9],
                       drop_scale_range=drop_scale,
                       drop_jitter=0.2,
                       drop_rotation_range=drop_rotation_range,
                       drop_objects = [drop_obj],
                       target_objects = [target_obj],
                       target_scale_range=target_scale,
                       target_rotation_range=target_rotation,
                       camera_radius=1.5,
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

