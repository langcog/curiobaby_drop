import time
import os
import drop #how are we dealing with the fact that we might want to reuse controller code like this? drop controller is not in any package!

OBJECT_INFO = {}

CONTAIN_SCENARIOS = [('bowl', ['pyramid', 'trianular_prism']),
                     ('cone', ['torus', 'octahedron']),
                     ('dumbbell', ['pipe', 'pyramid']),
                     ('octahedron', ['pipe', 'sphere']),
                     ('pentagon', ['bowl', 'sphere']),
                     ('pipe', ['cone', 'octahedron']),
                     ('pyramid', ['torus', 'dumbbell']),
                     ('sphere', ['bowl', 'pentagon']),
                     ('torus', ['cone', 'dumbbell']),
                     ('triangular_prism', ['bowl', 'dumbbell'])]

SUPPORT_SCENARIOS = [('bowl', ['torus', 'triangular_prism']),
                     ('cone', ['triangular_prism', 'sphere']),
                     ('dumbbell', ['pentagon', 'octahedron']),
                     ('octahedron', ['pentagon', 'pyramid']),
                     ('pentagon', ['pipe', 'pyramid']),
                     ('pipe', ['torus', 'dumbbell']),
                     ('pyramid', ['triangular_prism', 'sphere']),
                     ('sphere', ['pipe', 'cone']),
                     ('torus', ['bowl', 'octahedron']),
                     ('triangular_prism', ['pentagon', 'cone'])]

SCENARIO_TYPES = 10 * ['contain'] + 10 * ['support']

SCENARIOS = CONTAIN_SCENARIOS + SUPPORT_SCENARIOS

def get_drop_target_pairs(scenarios):
    pairs = []
    for sd, st in scenarios:
        if (sd, st[0]) not in scenarios:
            pairs.append((sd, st[0]))
        if (sd, st[1]) not in scenarios:
            pairs.append((sd, st[1]))
    return pairs


def main(output_dir, num, launch_build=True, port=1071):
    scenarios = get_drop_target_pairs(SCENARIOS)
    scenes = list(zip(scenarios, SCENARIO_TYPES))
    #scenes = scenes[:1]
    for i, ((sd, st), tp) in enumerate(scenes):
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

        if i == 0:
            dc = drop.Drop(launch_build=launch_build,
                       port=port,
                       randomize=0,
                       seed=0,
                       height_range=[1.2, 1.2],
                       drop_scale_range=[drop_scale, drop_scale],
                       drop_jitter=0.2,
                       drop_rotation_range=drop_rotation,
                       drop_objects = [drop_obj],
                       target_objects = [target_obj],
                       target_scale_range=[target_scale, target_scale],
                       target_rotation_range=target_rotation,
                       camera_radius=1.5,
                       camera_min_angle=0,
                       camera_max_angle=0)

            initialization_commands = dc.get_initialization_commands(width=256,
                                                                     height=256)
            dc.communicate(initialization_commands)
        else:
            dc.drop_scale_range = [drop_scale, drop_scale]
            dc.target_scale_range = [target_scale, target_scale]
            dc.drop_rotation_range = drop_rotation
            dc.target_rotation_range = target_rotation
            dc.drop_objects = [drop_obj]
            dc.target_objects = [dc]

        dc.trial_loop(num,
                      output_dir = output_path,
                      temp_path = temp_path)
                       
    dc.communicate({"$type": "terminate"})

