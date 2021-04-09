#
# Wrapper around HypersphereMetric norm performance issue from 
# https://github.com/geomstats/geomstats/issues/920#issuecomment-792782040
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


parser = argparse.ArgumentParser()
parser.add_argument("-m","--metric", type=str, choices = ['hsmetric', 'gs.linalg'],
    help="norm to test (default: hsmetric)", default='hsmetric')
parser.add_argument("-i","--iterations", type=int,
    help="number of repetitions of the test (default 10000)", default=10000)
parser.add_argument("-s", "--suffix", type=str,
    help="suffix for result files (default current date and time)",
    default=str(datetime.now()).replace(' ','_'))
parser.add_argument("--omp_num_threads", type=str,
    help="set OMP_NUM_THREADS environment variable (default: dont set)")
parser.add_argument("-p", "--profiler", type=str, choices = ['cprofile', 'yappi', 'none'],
    help="choose profiler to use (default: cprofile)", default = 'cprofile')
args = parser.parse_args()

outdir = './profiling/out/'
resfile = outdir + 'stdouterr.' + args.suffix
if args.omp_num_threads is not None:
    os.environ['OMP_NUM_THREADS'] = args.omp_num_threads

# OMP_NUM_THREADS needs to be set before imports
import geomstats.backend as gs
from geomstats.geometry.hypersphere import HypersphereMetric

with open(resfile, 'w') as f:
    sys.stderr = sys.stdout
    sys.stdout = f
    print("INFO: command line {}".format(sys.argv))
    print("INFO: user profiler {}".format(args.profiler))
    print("INFO: result file suffix {}\n".format(args.suffix))
    if 'OMP_NUM_THREADS' in os.environ:
        print("INFO: OMP_NUM_THREADS is {}".format(os.environ['OMP_NUM_THREADS']))
    else:
        print("INFO: OMP_NUM_THREADS is not set")

    # useful or not ?
    #gs.random.seed()

    x = gs.array([1., 0., 0., 0.])
    v = gs.array([0., 2., 1.5, .4])
    metric = HypersphereMetric(3)

    # start profiling
    if (args.profiler == 'cprofile'):
        profile = cProfile.Profile()
        profile.enable()
    elif (args.profiler == 'yappi'):
        yappi.set_clock_type("cpu")
        yappi.start()
    t_cpu_before = time.process_time()
    t_real_before = time.perf_counter()

    # run payload
    if (args.metric == 'hsmetric'):
        for _ in range(args.iterations):
            metric.norm(v, x)
    elif (args.metric == 'gs.linalg'):
        for _ in range(args.iterations):
            gs.linalg.norm(v)
    else:
        print('bad metric param {}'.format(args.metric))

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

