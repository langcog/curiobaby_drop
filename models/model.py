import os
from multiprocessing import Pool
try:
    import cPickle as pickle
except:
    import pickle
import numpy as np
import h5py
import pandas as pd
import sklearn.svm as svm
from sklearn.model_selection import GridSearchCV
import sklearn.metrics as sk_metrics
import scipy.stats as stats
import matplotlib.pyplot as plt

from experimental import (SCENARIOS, 
                          scenario_pathname,
                          get_drop_target_pairs)


##############
#####TIME#####
##############

def get_time_list(data):
    return [len(d['frames'].keys()) for d in data]


def avg_len(time_list):
    """mean length of time before objects come to rest"""
    return np.mean(time_list)


def len_std(time_list):
    """std in length of time before objects come to rest
    """
    return np.std(time_list)


def sharpe_ratio(x):
    return np.mean(x) / np.std(x)


def len_inverse_sharpe_ratio(time_list):
    """
    length std normalized by mean length
    see https://en.wikipedia.org/wiki/Sharpe_ratio
    """
    return 1./sharpe_ratio(time_list)


###################
#####POSITIONS#####
###################

def get_last_frame_id(d):
    """helper function getting last frame number of trial
    """
    fnames = list(d['frames'].keys())
    fnames.sort()
    return fnames[-2]


def get_last_frame_positions(data):
    """helper function getting positions of objects at last frame
    """
    posvecs = []
    for d in data:
        lf = get_last_frame_id(d)
        posvec = np.asarray(d['frames'][lf]['objects']['positions'][:])
        posvecs.append(posvec)
    #shape is (num_trials, num_objects, 3)
    posvecs = np.array(posvecs)
    return posvecs


def get_positions(data, object_inds=None):
    """
    helper function getting all positions of all frames in all trials
    returns a list rather than an array since the len of the trials will be different
    """
    posfunc = lambda x: get_positions_from_frames(x,
                             object_inds=object_inds)
    return list(map(posfunc, data))


def get_positions_from_frames(d, object_inds=None):
    """helper function getting positions for all frames in a trial
    returns array of shape (num_frames, num_objects_in_selection, 3)
    """
    pos = []
    frame_inds = list(d['frames'].keys())
    frame_inds.sort()
    for f_ind in frame_inds:
        f = d['frames'][f_ind]
        p = f['objects']['positions'][:]
        if object_inds is not None:
            p = p[object_inds]
        pos.append(p)
    return np.array(pos)


def get_velocities(data, object_inds=None):
    """
    helper function getting all positions of all frames in all trials
    returns a list rather than an array since the len of the trials will be different
    """
    posfunc = lambda x: get_velocities_from_frames(x,
                             object_inds=object_inds)
    return list(map(posfunc, data))


def get_velocities_from_frames(d, object_inds=None):
    """helper function getting velocities for all frames in a trial
    returns array of shape (num_frames, num_objects_in_selection, 3)
    """
    vel = []
    frame_inds = list(d['frames'].keys())
    frame_inds.sort()
    for f_ind in frame_inds:
        f = d['frames'][f_ind]
        v = f['objects']['velocities'][:]
        if object_inds is not None:
            v = v[object_inds]
        vel.append(v)
    return np.array(vel)


def get_object_inds(objects):
    #XXX TODO relies on fact that target is placed first...
    #... this seems dangerous. but what else to do?
    if objects == 'target':
        object_inds = [0]
    elif objects == 'drop':
        object_inds = [1]
    else:
        object_inds = None
    return object_inds


def get_posvecs(data, objects=None):
    object_inds = get_object_inds(objects)
    posvecs = get_last_frame_positions(data)
    if object_inds is not None:
        posvecs = posvecs[:, object_inds]
    return posvecs


def obj_final_position_std(posvecs):
    """
    model expressing total std in final positions 
    of objects (can be subselected for specific object)
    """
    posvecs = np.array(posvecs)
    return np.sqrt(posvecs.var(axis=0).sum(axis=0).sum(axis=0))


def obj_final_position_invstd(posvecs):
    """
    model expressing 1 - total std in final positions 
    of objects (can be subselected for specific object)
    """
    return 1 - obj_final_position_std(posvecs, objects=objects)


def get_radii(data, objects=None):
    """helper function"""
    object_inds = get_object_inds(objects)
    positions = get_positions(data, object_inds=object_inds)
    radii = [np.sqrt(((pos**2)[:, :, [0, 2]]).sum(axis=2)) for pos in positions]
    return radii


def avg_final_radius(radii):
    """model expressing avg final radius of objects
       mean is taken over trials and objects of radius of objects at last time point
    """
    return np.mean([rad[-1].mean() for rad in radii])


def avg_max_radius(radii):
    """model expressing avg maximum radius achieved by objects during trial
       max is taken over all objects and all frames with each trial, then
       mean is taken of that over all trials
    """
    max_radii = [r.max() for r in radii]
    return np.mean(max_radii)


def max_radius_std(radii):
    """model expressing avg maximum radius achieved by objects during trial
       max is taken over all objects and all frames with each trial, then
       std is taken of that over all trials
    """
    max_radii = [r.max() for r in radii]
    return np.std(max_radii)


####################
#####COLLISIONS#####
####################

def get_first_collision_frame(d):
    collision_frames = get_collision_frames(d)
    collision_frames.sort()
    if len(collision_frames) > 0:
        return collision_frames[0]
    else:
        return None


def get_collision_frames(d):
    f_inds = list(d['frames'].keys())
    f_inds.sort()
    collision_frames = np.nonzero([d['frames'][fn]['collisions']['contacts'].shape[0] for fn in f_inds])[0]
    return collision_frames


def normed_velocity_after_first_collision(data, objects=None, window=5):
    fcfs = list(map(get_first_collision_frame, data))
    object_inds = get_object_inds(objects)
    vels = get_velocities(data, object_inds=object_inds)
    #V is of shape (num_trials, window, num_objects, 3)
    V = np.array([v[fcf:fcf + window] for v, fcf in zip(vels, fcfs) if fcf is not None])
    return V


def normed_velocity_std_after_first_collision(V):
    Vm = V.mean(axis=1)
    Vn = np.linalg.norm(Vm, axis=2)
    W = Vm / Vn[:, :, np.newaxis]
    return np.sqrt(W.var(axis=0).sum())


def get_collision_types(d, collision_key='collisions'):
    fn = list(d['frames'].keys())
    fn.sort()
    ct = [d['frames'][k][collision_key]['states'][:].flatten().tolist() for k in fn]
    ct1 = np.asarray(list((map(lambda x: x[0].decode('utf-8') if len(x) else '', ct))))
    return ct1


def get_collision_ids(d, collision_key='collisions'):
    """
    helper function returning the ids of objects in collisions at each frame within a trial
    """
    fn = list(d['frames'].keys())
    fn.sort()
    ids = [np.unique(d['frames'][k][collision_key]['object_ids'][:]) for k in fn]
    return ids


def get_support(d):
    """helper function computing a support as at the end of the trial 
    both objects are in a stable collision but only one of the objects is 
    touching the environment (e.g. the floor), and the other object is presumably
    being supported by the first object. This only identifies complete support 
    relationships, but ignores situations when one object is leaning the other but is 
    also supported by the floor.  
    """
    print('... getting supports')
    c_ids = get_collision_ids(d)
    c_ids_env = get_collision_ids(d, collision_key='env_collisions')
    support = ((len(c_ids[-2]) == 2) and (len(c_ids_env[-2]) <= 1))
    return support  


def get_supports_and_radii(data):
    radfunc = lambda x: np.linalg.norm(x['static']['drop_position'][[0, 2]])
    radii = list(map(radfunc, data))
    supports = list(map(get_support, data))
    return [{'radius': r, 'support': s} for r, s in zip(radii, supports)]


def support(supports_and_radii):
    """model expressing empirical likelihood of a support relationship
    arising at the end of a trial
    """    
    supports = [sr['support'] for sr in supports_and_radii]
    radii = [sr['radii'] for sr in supports_and_radii]

    #basic statistics
    m = np.mean(supports)
    s = np.sqrt(m * (1 - m))
    result = {'probability': m, 'std': s}

    #sharpness as measured by categorization accuracy
    print('... getting svc results')
    radii_rs = np.array(radii).reshape((-1, 1)) 
    Cs = [1, 1e-1, 1e1, 1e-2, 1e2, 1e-3, 1e3, 1e-4, 1e4, 1e-5, 1e5]
    for C in Cs:
        if len(np.unique(supports)) == 1:
            score = 0
            acc = 0
        else:
            print('... getting svc results C = %s' % str(C))
            cls = svm.LinearSVC(C=C)
            cls.fit(radii_rs, supports)
            preds = cls.predict(radii_rs)
            score = sk_metrics.f1_score(preds, supports)
            acc = sk_metrics.accuracy_score(preds, supports)
        result['response_sharpness_C=%s' % str(C)] = score
        result['response_sharpness_accuracy_C=%s' % str(C)] = acc
    print('... getting gridsearch svc results')
    if len(np.unique(supports)) == 1:
        score = 0
        acc = 0
    else:
        svc = svm.LinearSVC()
        cls = GridSearchCV(svc, {'C': Cs})
        cls.fit(radii_rs, supports)
        preds = cls.predict(radii_rs)
        score = sk_metrics.f1_score(preds, supports)
        acc = sk_metrics.accuracy_score(preds, supports)
    result['response_sharpness_GridSearchCV'] = score
    result['response_sharpness_accuracy_GridSearchCV'] = acc

    #sharpness as measured by linearity
    print('... getting linearity results')
    if len(np.unique(supports)) == 1:
        absr = pv = 0
    else:
        out = stats.linregress(radii, supports)
        absr = np.abs(out.rvalue)
        pv = 1 - out.pvalue
    result['response_linearity_r'] = absr
    result['response_linearity_pv'] = pv

    return result


########################
#####INFRASTRUCTURE#####
########################

model_funcs = [{'func': (avg_len, get_time_list)}, 
               {'func': (len_std, get_time_list)},
               {'func': (len_inverse_sharpe_ratio, get_time_list)},
               {'func': (obj_final_position_std, get_posvecs),
                'args': {'objects': 'drop'}},
               {'func': (obj_final_position_std, get_posvecs), 
                'args': {'objects': 'target'}},
               {'func': (obj_final_position_invstd, get_posvecs), 
                'args': {'objects': 'drop'}},
               {'func': (obj_final_position_invstd, get_posvecs), 
                'args': {'objects': 'target'}},
               {'func': (avg_final_radius, get_radii), 
                'args': {'objects': 'drop'}},
               {'func': (avg_final_radius, get_radii), 
                'args': {'objects': 'target'}},
               {'func': (avg_max_radius, get_radii),
                'args': {'objects': 'drop'}},
               {'func': (avg_max_radius, get_radii), 
                'args': {'objects': 'target'}},
               {'func': (max_radius_std, get_radii), 
                'args': {'objects': 'drop'}},
               {'func': (max_radius_std, get_radii), 
                'args': {'objects': 'target'}},
               {'func': (normed_velocity_after_first_collision, 
                         normed_velocity_std_after_first_collision),
                'args': {'objects': 'drop'}},
               {'func': (normed_velocity_after_first_collision, 
                         normed_velocity_std_after_first_collision),
                'args': {'objects': 'target'}},
               {'func': (support, get_supports_and_radii)}
              ]


def get_splits(n, k, seed=0):
    rng = np.random.RandomState(seed=seed)
    splits = []
    for i in range(k):
        p = rng.permutation(n)
        lsplit = p[: n // 2]
        rsplit = p[n // 2: ]
        splits.append((lsplit, rsplit))
    return splits


def get_result(mf, df, data, kwargs, name, splits):
    data_out = df(data, **kwargs)
    output = mf(data_out)
    if hasattr(output, 'keys'):
        result = {name + '_' + k: {'all': v, 'splits': []} for k, v in output.items()}
    else:
        result = {name: {'all': output, 'splits': []}}
    for lsplit, rsplit in splits:
        ldata_out = [data_out[i] for i in lsplit]
        rdata_out = [data_out[i] for i in rsplit]
        loutput = mf(ldata_out, **kwargs)
        routput = mf(rdata_out, **kwargs)
        if hasattr(loutput, 'keys'):
            for k in loutput:
                result[name + '_' + k]['splits'].append((loutput[k], routput[k]))
        else:
            result[name]['splits'].append((loutput, routput))
    return result


def get_stats(dirn, num_splits=100):
    L = os.listdir(dirn)
    paths = [os.path.join(dirn, l) for l in L]
    data = [h5py.File(path, mode='r') for path in paths]
    outcomes = {}
    splits = get_splits(len(data), num_splits)
    for m in model_funcs:
        mf, df = m['func']
        if 'args' in m:
            kwargs = m['args']
            argk = list(kwargs.keys())
            argk.sort()
            argstr = '_'.join([str(k) + '=' + str(kwargs[k]) for k in argk])
            name = mf.__name__ + '_' + argstr
        else:
            kwargs = {}
            name = mf.__name__
        print('... getting %s' % name)
        result = get_result(mf, df, data, kwargs, name, splits)
        outcomes.update(result)
    for d in data:
        d.close()
    return outcomes


def get_and_save_stats(sd, st, tp, base_dir, out_dir, num_splits=100):
    drop_obj, target_obj = get_object_names(sd, st)
    sname = scenario_pathname(drop_obj, target_obj, tp)
    path = os.path.join(base_dir, sname)
    print('Getting stats for %s' % sname)
    outcomes = get_stats(path, num_splits=num_splits)
    outpath = os.path.join(out_dir, sname)
    with open(outpath, 'wb') as _f:
        pickle.dump(outcomes, _f)


def get_all_stats(base_dir, out_dir, num_splits=100):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    scenarios = get_drop_target_pairs(SCENARIOS)
    pool = Pool()
    outs = []
    for i in range(len(scenarios)):
        ((sd, st), tp) = scenarios[i]
        out = pool.apply_async(get_and_save_stats, 
                               (sd, st, tp, base_dir, out_dir, num_splits))
        outs.append(out)
    done = [out.get() for out in outs]
    pool.close()
    pool.join()


def get_object_names(sd, st):
    if isinstance(sd, str):
        drop_obj = sd 
    else:
        drop_obj = sd[0]
    if isinstance(st, str):
        target_obj = st
    else:
        target_obj = st[0]
    return drop_obj, target_obj


def collect_stats(dirn, featpath, figpath):
    scenarios = get_drop_target_pairs(SCENARIOS)
    records = []
    for i in range(len(scenarios)):
        ((sd, st), tp) = scenarios[i]
        drop_obj, target_obj = get_object_names(sd, st)
        sname = scenario_pathname(drop_obj, target_obj, tp)
        pth = os.path.join(dirn, sname)
        with open(pth, 'rb') as _f:
            outcomes = pickle.loads(_f.read())
            outcomes['drop_object'] = drop_obj
            outcomes['target_object'] = target_obj
            outcomes['condition'] = tp
            records.append(outcomes)
    features = pd.DataFrame(records)
    features.to_csv(featpath, index=False)
    K = list(filter(lambda x: x not in ['drop_object', 'target_object', 'condition'],
               features.columns))
    C = np.array([[stats.pearsonr(features[k1],
                                  features[k2])[0] for k1 in K] for k2 in K])
    cbar = plt.matshow(C)
    plt.colorbar(cbar)
    plt.xticks(np.arange(C.shape[0]), K, rotation=90)
    plt.yticks(np.arange(C.shape[0]), K, rotation=0)
    plt.savefig(figpath, bbox_inches='tight')



