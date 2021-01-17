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
                     ('triangular prism', ['bowl', 'dumbbell'])]

SUPPORT_SCENARIOS = [('bowl', ['torus', 'triangular prism']),
                     ('cone', ['triangular prism', 'sphere']),
                     ('dumbbell', ['pentagon', 'octahedron']),
                     ('octahedron', ['pentagon', 'pyramid']),
                     ('pentagon', ['pipe', 'pyramid']),
                     ('pipe', ['torus', 'dumbbell']),
                     ('pyramid', ['triangular prism', 'sphere']),
                     ('sphere', ['pipe', 'cone']),
                     ('torus', ['bowl', 'octahedron']),
                     ('triangular prism', ['pentagon', 'cone'])]

SCENARIO_TYPES = 10 * ['contain'] + 10 * ['support']

SCENARIOS = CONTAIN_SCENARIOS + SUPPORT_SCENARIOS

def get_drop_target_pairs(scenarios):
    pairs = []
    for sd, st in scenarios:
        pairs.append((sd, st[0]))
        pairs.append((sd, st[1]))
    pairs = list(set(pairs))
    return pairs


def main(output_dir, num):
    scenarios = get_drop_target_pairs(SCENARIOS)
    print(scenarios)
    scenes = list(zip(scenarios, SCENARIO_TYPES))
    scenes = scenes[:1]
    for (sd, st), tp in scenes:
        if isinstance(sd, str):
            drop_obj = sd 
            drop_rotation = [0, 0, 0]
            drop_scale = 1
        else:
            drop_obj, drop_rotation, drop_scale = sd
        if isinstance(st, str):
            target_obj = st
            target_rotation = [0, 0, 0]
            target_scale = 1
        else:
            target_obj, target_rotation, target_scale = st

        dc = drop.Drop(randomize=0,
                       seed=0,
                       height_range=[0.75, 1.25],
                       drop_scale_range=[drop_scale, drop_scale],
                       drop_jitter=0.2,
                       drop_rotation=drop_rotation,
                       drop_objects = [drop_obj],
                       target_objects = [target_obj],
                       target_scale_range=[target_scale, target_scale],
                       target_rotation=target_rotation,
                       camera_min_angle=0,
                       camera_max_angle=0
        )

        suffix = '%s_on_%s_%s' % (drop, target, tp)
        output_path = os.path.join(output_dir, suffix)
        dc.run(num=num,
               output_dir=output_path,
               width=256,
               height=256)
               
                       
