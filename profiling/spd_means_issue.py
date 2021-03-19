#
# Wrapper around nguigs' SPD means computation with geomstats and nilearn
# https://github.com/geomstats/geomstats/issues/913
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
parser.add_argument("-d", "--dimension", type=int,
    help="matrix dimension (default 10)", default=10)
parser.add_argument("-i","--iterations", type=int,
    help="maximum number of iterations (default 1000)", default=1000)
parser.add_argument("-f", "--factor", type=float,
    help="multiply factor for convergence epsilon/tol (default 1)", default=1.)
parser.add_argument("-s", "--suffix", type=str,
    help="suffix for result files (default current date and time)",
    default=str(datetime.now()).replace(' ','_'))
parser.add_argument("--omp_num_threads", type=str,
    help="set OMP_NUM_THREADS environment variable (default: dont set)")
parser.add_argument("-c", "--code", type=str, choices = ['geomstats', 'nilearn', 'dummy', 'dummy-pythreads'],
    help="choose code to run {geomstats, nilearn, dummy, dummy-pythreads} (default: geomstats)", default='geomstats')
parser.add_argument("-p", "--profiler", type=str, choices = ['cprofile', 'yappi', 'none'],
    help="choose profiler to use {cprofile, yappi, none} (default: cprofile)", default = 'cprofile')
args = parser.parse_args()

outdir = './profiling/out/'
resfile = outdir + 'stdouterr.' + args.suffix
if args.omp_num_threads is not None:
    os.environ['OMP_NUM_THREADS'] = args.omp_num_threads

def cpuburn(number):
    print("cpuburn: in instance {} starting".format(number))
    t_init = time.thread_time()
    while (time.thread_time() < (t_init + 5)):
        # dummy payload
        a = 1
    print("cpuburn: in instance {} finishing".format(number))

# OMP_NUM_THREADS needs to be set before imports
from nilearn.connectome.connectivity_matrices import _geometric_mean
from geomstats.geometry.spd_matrices import SPDMatrices, SPDMetricAffine
from geomstats.learning.frechet_mean import FrechetMean
import geomstats.backend as gs

with open(resfile, 'w') as f:
    sys.stderr = sys.stdout
    sys.stdout = f
    print("INFO: command line {}".format(sys.argv))
    print("INFO: running code {}".format(args.code))
    print("INFO: user profiler {}".format(args.profiler))
    print("INFO: result file suffix {}\n".format(args.suffix))
    if 'OMP_NUM_THREADS' in os.environ:
        print("INFO: OMP_NUM_THREADS is {}".format(os.environ['OMP_NUM_THREADS']))
    else:
        print("INFO: OMP_NUM_THREADS is not set")

    gs.random.seed(0)
    n_points = 100
    max_iter = args.iterations
    print("maximum number of iterations {}".format(max_iter))
    dim = args.dimension
    print("matrix dimension {}".format(dim))
    space = SPDMatrices(dim)
    data = space.random_uniform(n_samples=n_points)

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
    if (args.code == 'geomstats'):
        metric = SPDMetricAffine(dim)
        mean = FrechetMean(metric=metric, method='default', point_type='matrix',
                           max_iter=max_iter, verbose=True, epsilon=1e-10*args.factor)
        mean.fit(data)
        mean_estimate = mean.estimate_
    elif (args.code == 'nilearn'):
        nilearn_mean = _geometric_mean(data, max_iter=max_iter, tol=1e-7*args.factor)
    elif (args.code == 'dummy'):
        # dummy payload for testing profiling with system processes
        # (cannot use system threads in python)
        print('\n')
        with ProcessPoolExecutor(max_workers=5) as executor:
            for i in range(5):
                executor.submit(cpuburn, i)
                print("multiprocessing: started process {}".format(i))
        print("multiprocessing: finished all processes")
        print('\n')
    elif (args.code == 'dummy-pythreads'):
        # dummy payload for testing profiling with python threading
        print('\n')
        threads = []
        for i in range(5):
            th = threading.Thread(target=cpuburn, args=(i,), daemon=True)
            threads.append(th)
            th.start()
            print("pythreading: started thread {}".format(i))
        for i, th in enumerate(threads):
            th.join()
            print("pythreading: joined thread {}".format(i))
        print('\n')
    else:
        print('ERROR: bad code {}'.format(args.code))
        sys.exit(1)

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
    print("RESULTS: {} cpu time {}".format(args.code, t_cpu_after - t_cpu_before))
    print("RESULTS: {} real time {}".format(args.code, t_real_after - t_real_before))

