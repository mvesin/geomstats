import os
import sys
import argparse
from datetime import datetime

import time
import cProfile
import pstats

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dimension", type=int,
    help="matrix dimension (default 10)", default=10)
parser.add_argument("-s", "--suffix", type=str,
    help="suffix for result files (default current date and time)",
    default=str(datetime.now()).replace(' ','_'))
parser.add_argument("--omp_num_threads", type=str,
    help="set OMP_NUM_THREADS environment variable (default: dont set)")
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

    pr1 = cProfile.Profile()
    before1 = time.process_time()
    pr1.enable()

    metric = SPDMetricAffine(dim)
    mean = FrechetMean(metric=metric, method='default', point_type='matrix',
                       max_iter=1000, verbose=True, epsilon=1e-10)
    mean.fit(data)
    mean_estimate = mean.estimate_

    print('\n')
    after1 = time.process_time()
    pr1.disable()
    pr1.dump_stats(outdir + 'geomstats.cprofile.' + args.suffix)
    ps1 = pstats.Stats(pr1)
    ps1.sort_stats('cumulative').print_stats(10)
    ps1.sort_stats('tottime').print_stats(10)

    pr2 = cProfile.Profile()
    before2 = time.process_time()
    pr2.enable()

    nilearn_mean = _geometric_mean(data, max_iter=1000, tol=1e-7)

    after2 = time.process_time()
    pr2.disable()
    pr2.dump_stats(outdir + 'nilearn.cprofile.' + args.suffix)

    print('\n\n' + str(metric.dist(nilearn_mean, mean_estimate)))
    print("geomstats time {} nilearn time {}".format(after1 - before1, after2 - before2))


