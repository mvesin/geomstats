#
# Wrapper around empirical_frechet_mean_uncertainty_sn.py example's empirical_frechet_var_bubble()
# https://github.com/geomstats/geomstats/blob/8d611afb83107f5a4e1a2e3522a6dac2a46c6e5f/examples/empirical_frechet_mean_uncertainty_sn.py#L20
# to test params & measure/profile
# 

import os
import sys
import argparse
from datetime import datetime
import time
import threading
from concurrent.futures import ProcessPoolExecutor

import cProfile
import yappi
import pstats

from examples.empirical_frechet_mean_uncertainty_sn import empirical_frechet_var_bubble
import geomstats.backend as gs


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dimension", type=int,
    help="matrix dimension (default 2)", default=2)
parser.add_argument("-n","--n_sample", type=int,
    help="number of samples (default 2)", default=2)
parser.add_argument("-e","--n_expectation", type=int,
    help="number of computations for approaching the expectation (default 10)", default=10)
parser.add_argument("-t","--theta-delta", type=float,
    help="negative delta of theta from pi/2 aka theta == (pi/2 - t) (default 1e-6)", default=1e-6)
parser.add_argument("-s", "--suffix", type=str,
    help="suffix for result files (default current date and time)",
    default=str(datetime.now()).replace(' ','_'))
parser.add_argument("-p", "--profiler", type=str, choices = ['cprofile', 'yappi', 'none'],
    help="choose profiler to use {cprofile, yappi, none} (default: cprofile)", default = 'cprofile')
args = parser.parse_args()

outdir = './profiling/out/'
resfile = outdir + 'stdouterr.' + args.suffix

with open(resfile, 'w') as f:
    sys.stderr = sys.stdout
    sys.stdout = f
    print("INFO: command line {}".format(sys.argv))
    print("INFO: user profiler {}".format(args.profiler))
    print("INFO: result file suffix {}\n".format(args.suffix))

    # useful or not ?
    gs.random.seed(0)

    print("number of samples {}".format(args.n_sample))
    print("hypersphere dimension {}".format(args.dimension))
    print("theta delta {}".format(args.theta_delta))
    theta = gs.pi / 2.0 - args.theta_delta
    print("theta {}".format(theta))

    # start profiling
    t_cpu_before = time.process_time()
    t_real_before = time.perf_counter()
    if (args.profiler == 'cprofile'):
        profile = cProfile.Profile()
        profile.enable()
    elif (args.profiler == 'yappi'):
        yappi.set_clock_type("cpu")
        yappi.start()

    # run payload
    empirical_frechet_var_bubble(args.n_sample, theta, args.dimension, args.n_expectation)

    print('\n')
    t_real_after = time.perf_counter()
    t_cpu_after = time.process_time()

    # stop profiling
    if(args.profiler == 'cprofile'):
        profile.disable()
        profile.dump_stats(outdir + 'cprofile.' + args.suffix)
        profile_stats = pstats.Stats(profile)
        profile_stats.sort_stats('cumulative').print_stats(10)
        profile_stats.sort_stats('tottime').print_stats(10)
        profile_stats.sort_stats('ncalls').print_stats(10)
        profile_stats.sort_stats('tottime').print_callers(5)
        profile_stats.sort_stats('cumulative').print_callees(5)
    elif (args.profiler == 'yappi'):
        yappi.stop()
        yappi.get_func_stats().sort('tsub').print_all(f)
        yappi.get_thread_stats().print_all(f)
        yappi.clear_stats()

    print('\n')
    print("RESULTS: cpu time {}".format(t_cpu_after - t_cpu_before))
    print("RESULTS: real time {}".format(t_real_after - t_real_before))

