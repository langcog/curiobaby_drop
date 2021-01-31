from argparse import ArgumentParser

import model
import generate_stimuli

def get_args():

    parser = ArgumentParser()

    parser.add_argument("--stimulus_dir",
                        type=str,
                        default=None,
                        help="dirname where stimuli are saved")

    parser.add_argument("--stats_dir",
                        type=str,
                        default=None,
                        help="dirname where stats are saved")


    parser.add_argument("--feature_path",
                        type=str,
                        default=None,
                        help="file where stats are collected into a csv")

    parser.add_argument("--feature_std_path",
                        type=str,
                        default=None,
                        help="file where stats stds are collected into a csv") 

    parser.add_argument("--corr_path",
                        type=str,
                        default=None,
                        help="file where split-half reliabilities are saved") 

    parser.add_argument("--fig_path",
                        type=str,
                        default=None,
                        help="file where statistics correlation figure is saved") 

    parser.add_argument("--num_trials",
                        type=int,
                        default=100,
                        help="num trials per condition") 
    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    stimulus_dir = args.stimulus_dir
    stats_dir = args.stats_dir
    feature_path = args.feature_path
    feature_std_path = args.feature_std_path
    corr_path = args.corr_path
    fig_path = args.fig_path
    num_trials = args.num_trials
    generate_stimuli.main(stimulus_dir, num_trials)
    model.get_all_stats(stimulus_dir, stats_dir)
    model.collect_stats(stimulus_dir,
                        feature_path,
                        feat_std_path,
                        corr_path,
                        fig_path)
    
