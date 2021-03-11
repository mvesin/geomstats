import os
import sys
import argparse
from datetime import datetime

import time
import cProfile
import yappi
import pstats

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dimension", type=int,
    help="matrix dimension (default 10)", default=10)
parser.add_argument("-s", "--suffix", type=str,
    help="suffix for result files (default current date and time)",
    default=str(datetime.now()).replace(' ','_'))
parser.add_argument("--omp_num_threads", type=str,
    help="set OMP_NUM_THREADS environment variable (default: dont set)")
parser.add_argument("-c", "--code", type=str, choices = ['geomstats', 'nilearn'],
    help="choose code to run {geomstats, nilearn} (default: geomstats)", default='geomstats')
parser.add_argument("-p", "--profiler", type=str, choices = ['cprofile', 'yappi', 'none'],
    help="choose profiler to use {cprofile, yappi, none} (default: cprofile)", default = 'cprofile')
args = parser.parse_args()

outdir = './profiling/out/'
resfile = outdir + 'stdouterr.' + args.suffix
if args.omp_num_threads is not None:
    os.environ['OMP_NUM_THREADS'] = args.omp_num_threads

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
    dim = args.dimension
    print("matrix dimension {}".format(dim))
    space = SPDMatrices(dim)
    data = space.random_uniform(n_samples=n_points)

    t_cpu_before = time.process_time()
    t_real_before = time.perf_counter()
    if (args.profiler == 'cprofile'):
        profile = cProfile.Profile()
        profile.enable()
    elif (args.profiler == 'yappi'):
        yappi.set_clock_type("cpu")
        yappi.start()

    if (args.code == 'geomstats'):
        metric = SPDMetricAffine(dim)
        mean = FrechetMean(metric=metric, method='default', point_type='matrix',
                           max_iter=1000, verbose=True, epsilon=1e-10)
        mean.fit(data)
        mean_estimate = mean.estimate_
    elif (args.code == 'nilearn'):
        nilearn_mean = _geometric_mean(data, max_iter=1000, tol=1e-7)
    else:
        print('ERROR: bad code {}'.format(args.code))
        sys.exit(1)

    print('\n')
    t_real_after = time.perf_counter()
    t_cpu_after = time.process_time()

    if(args.profiler == 'cprofile'):
        profile.disable()
        profile.dump_stats(outdir + 'cprofile.' + args.suffix)
        profile_stats = pstats.Stats(profile)
        profile_stats.sort_stats('cumulative').print_stats(10)
        profile_stats.sort_stats('tottime').print_stats(10)
    elif (args.profiler == 'yappi'):
        yappi.stop()
        yappi.get_func_stats().sort('tsub').print_all(f)
        yappi.get_thread_stats().print_all(f)
        yappi.clear_stats()

    print('\n')
    print("RESULTS: {} cpu time {}".format(args.code, t_cpu_after - t_cpu_before))
    print("RESULTS: {} real time {}".format(args.code, t_real_after - t_real_before))

