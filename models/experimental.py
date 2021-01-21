#OCT_ROT = 90
OCT_ROT = 0

CONTAIN_SCENARIOS = [(('torus', {"x": 0, "y": 0, "z": 0}, 0.8), 
                      [('cone', {"x": 0, "y": 0, "z": 0}, 0.9), 
                       ('dumbbell', {"x": 0, "y": 0, "z": 0}, 0.5)]),
                     (('bowl', {"x": 0, "y": 0, "z": 180}, 1.15), 
                      ['pyramid', 
                       ('triangular_prism', {"x": 0, "y": 90., "z": 0}, 1)]),
                     (('cone', {"x": 0, "y": 0, "z": 180}, 0.9),
                      [('torus', {"x": 0, "y": 0, "z": 0}, 0.8), 
                      ('octahedron', {"x": 0, "y": 0, "z": OCT_ROT}, 1)]),
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
                      ('octahedron', {"x": 0, "y": 0, "z": OCT_ROT}, 1)]),
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
                     (('octahedron', {"x": 0, "y": 0, "z": OCT_ROT}, 1), 
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


def scenario_pathname(drop_obj, target_obj, tp):
    return '%s_on_%s_%s' % (drop_obj, target_obj, tp)


def get_drop_target_pairs(scenarios):
    pairs = []
    for (sd, st), stype in scenarios:
        if ((sd, st[0]), stype) not in scenarios:
            pairs.append(((sd, st[0]), stype))
        if ((sd, st[1]), stype) not in scenarios:
            pairs.append(((sd, st[1]), stype))
    return pairs