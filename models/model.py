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
import sklearn.metrics as sk_metrics
import scipy.stats as stats

from experimental import (SCENARIOS, 
                          scenario_pathname,
                          get_drop_target_pairs)

################
#####BASICS#####
################

def softmax(x, beta=1):
    numerator = np.exp(beta * x)
    denominator = numerator.sum()
    return numerator / denominator


class CuriosityBinaryChoice(object):
    def __init__(self,
                 curiosity_function,
                 linking_function=softmax,
                 curiosity_kwargs=None,
                 linking_kwargs=None):
        if curiosity_kwargs is None:
            curiosity_kwargs = {}
        if linking_kwargs is None:
            linking_kwargs = {}
        self.curiosity_function = curiosity_function
        self.linking_function = linking_function
        self.curiosity_kwargs = curiosity_kwargs
        self.linking_kwargs = linking_kwargs

    def judgement(self, data):
        data_left, data_right = data
        m0 = self.curiosity_function(data_left, **self.curiosity_kwargs)
        m1 = self.curiosity_function(data_right, **self.curiosity_kwargs)
        judgement = self.linking_function([m0, m1], **self.linking_kwargs)
        return {'curiosity_left': m0,
                'curiosity_right': m1,
                'judgement': judgement}


##############
#####TIME#####
##############

def avg_len(data):
    """mean length of time before objects come to rest
    """
    time_list = [len(d['frames'].keys()) for d in data]
    return np.mean(time_list)


def len_std(data):
    """std in length of time before objects come to rest
    """
    time_list = [len(d['frames'].keys()) for d in data]
    return np.std(time_list)


def sharpe_ratio(x):
    return np.mean(x) / np.std(x)


def len_inverse_sharpe_ratio(data):
    """
    length std normalized by mean length
    see https://en.wikipedia.org/wiki/Sharpe_ratio
    """
    time_list = [len(d['frames'].keys()) for d in data]
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


def obj_final_position_std(data, objects=None):
    """
    model expressing total std in final positions 
    of objects (can be subselected for specific object)
    """
    object_inds = get_object_inds(objects)
    posvecs = get_last_frame_positions(data)
    if object_inds is not None:
        posvecs = posvecs[:, object_inds]
    total_std = np.sqrt(posvecs.var(axis=0).sum(axis=0).sum(axis=0))
    return total_std


def obj_final_position_invstd(data, objects=None):
    """
    model expressing 1 - total std in final positions 
    of objects (can be subselected for specific object)
    """
    return 1 - obj_final_position_std(data, objects=objects)


def get_radii(data, objects=None):
    """helper function"""
    object_inds = get_object_inds(objects)
    positions = get_positions(data, object_inds=object_inds)
    radii = [np.sqrt(((pos**2)[:, :, [0, 2]]).sum(axis=2)) for pos in positions]
    return radii


def avg_final_radius(data, objects=None):
    """model expressing avg final radius of objects
       mean is taken over trials and objects of radius of objects at last time point
    """
    radii = get_radii(data, objects=objects)
    return np.mean([rad[-1].mean() for rad in radii])


def avg_max_radius(data, objects=None):
    """model expressing avg maximum radius achieved by objects during trial
       max is taken over all objects and all frames with each trial, then
       mean is taken of that over all trials
    """
    radii = get_radii(data, objects=objects)
    max_radii = [r.max() for r in radii]
    return np.mean(max_radii)


def max_radius_std(data, objects=None):
    """model expressing avg maximum radius achieved by objects during trial
       max is taken over all objects and all frames with each trial, then
       std is taken of that over all trials
    """
    radii = get_radii(data, objects=objects)
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


def normed_velocity_std_after_first_collision(data, objects=None, window=5):
    fcfs = list(map(get_first_collision_frame, data))
    object_inds = get_object_inds(objects)
    vels = get_velocities(data, object_inds=object_inds)
    #V is of shape (num_trials, window, num_objects, 3)
    V = np.array([v[fcf:fcf + window] for v, fcf in zip(vels, fcfs) if fcf is not None])
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
    c_ids = get_collision_ids(d)
    c_ids_env = get_collision_ids(d, collision_key='env_collisions')
    support = ((len(c_ids[-2]) == 2) and (len(c_ids_env[-2]) <= 1))
    return support  


def support(data):
    """model expressing empirical likelihood of a support relationship
    arising at the end of a trial
    """
    supports = list(map(get_support, data))

    #basic statistics
    m = np.mean(supports)
    s = np.sqrt(m * (1 - m))
    result = {'probability': m, 'std': s}

    #sharpness as measured by categorization accuracy
    radfunc = lambda x: np.linalg.norm(x['static']['drop_position'][[0, 2]])
    radii = list(map(radfunc, data))
    radii_rs = np.array(radii).reshape((-1, 1)) 
    Cs = [1, 1e-5, 1e5]
    for C in Cs:
        if len(np.unique(supports)) == 1:
            score = 0
        else:
            cls = svm.LinearSVC(C=C)
            cls.fit(radii_rs, supports)
            preds = cls.predict(radii_rs)
            score = sk_metrics.f1_score(preds, supports)
        result['response_sharpness_C=%s' % str(C)] = score

    #sharpness as measured by linearity
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

model_funcs = [avg_len, 
               len_std,
               len_inverse_sharpe_ratio,
               (obj_final_position_std, {'objects': 'drop'}),
               (obj_final_position_std, {'objects': 'target'}),
               (obj_final_position_invstd, {'objects': 'drop'}),
               (obj_final_position_invstd, {'objects': 'target'}),
               (avg_final_radius, {'objects': 'drop'}),
               (avg_final_radius, {'objects': 'target'}),
               (avg_max_radius, {'objects': 'drop'}),
               (avg_max_radius, {'objects': 'target'}),
               (max_radius_std, {'objects': 'drop'}),
               (max_radius_std, {'objects': 'target'}),
               (normed_velocity_std_after_first_collision, {'objects': 'drop'}),
               (normed_velocity_std_after_first_collision, {'objects': 'target'}),
               support
              ]


def get_stats(dirn):
    L = os.listdir(dirn)
    paths = [os.path.join(dirn, l) for l in L]
    data = [h5py.File(path, mode='r') for path in paths]
    outcomes = {}
    for m in model_funcs:
        if hasattr(m, '__len__'):
            mf, kwargs = m
            argk = list(kwargs.keys())
            argk.sort()
            argstr = '_'.join([str(k) + '=' + str(kwargs[k]) for k in argk])
            name = mf.__name__ + '_' + argstr
        else:
            mf = m
            kwargs = {}
            name = mf.__name__
        print('... getting %s' % name)
        result = mf(data, **kwargs)
        if hasattr(result, 'keys'):
            new_d = {name + '_' + k: v for k, v in result.items()}
            outcomes.update(new_d)
        else:
            outcomes[name] = result
    for d in data:
        d.close()
    return outcomes


def get_and_save_stats(sd, st, tp, base_dir, out_dir):
    drop_obj, target_obj = get_object_names(sd, st)
    sname = scenario_pathname(drop_obj, target_obj, tp)
    path = os.path.join(base_dir, sname)
    print('Getting stats for %s' % sname)
    outcomes = get_stats(path)
    outpath = os.path.join(out_dir, sname)
    with open(outpath, 'wb') as _f:
        pickle.dump(outcomes, _f)


def get_all_stats(base_dir, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    scenarios = get_drop_target_pairs(SCENARIOS)
    pool = Pool()
    outs = []
    for i in range(len(scenarios)):
        ((sd, st), tp) = scenarios[i]
        out = pool.apply_async(get_and_save_stats, 
                               (sd, st, tp, base_dir, out_dir))
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


def collect_stats(dirn, outpath):
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
    features.to_csv(outpath, index=False)




