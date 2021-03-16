# Geomstats issue 913 basic benchmarks summary

Benches done with branch `feature/test_profiling` commit eac607b8
* after : remove redundant call to variance function for FrechetMean

See results file and profiling output for details.

Note : should have run each of these tests 10+ times. observe several %variation between tests.

## geomstat FrechetMean - OMP_NUM_THREADS=1

geomstat FrechetMean with OMP_NUM_THREADS=1, varying dimension, execution time (seconds) :

| dim | profiling real time | time(1) real time | profiling cpu time | time(1) user + sys time |
| --- | ------------------- | ----------------- | ------------------ | ----------------------- |
| 10  | 0.470               | 1.116             | 0.469              | 1.054 + 0.059           |
| 15  | 6.125               | 6.847             | 6.111              | 6.765 + 0.062           |
| 20  | 10.255              | 10.920            | 10.200             | 10.784 + 0.078          |
| 30  | 25.231              | 25.885            | 25.181             | 25.468 + 0.365          |
| 40  | 49.910              | 50.621            | 49.811             | 49.326 + 1.195          |
| 50  | error               | error             | error              | error                   |


* looking to profiling detailed info : execution time still dominated by `c_einsum` (15.510/25.231 sec for dim 30) and `eigh` (7.961/25.231 sec for dim 30) functions

* dimension 50 : test manually aborted after `WARNING: Negative eigenvalue encountered in log` error on console), if completing `INFO: n_iter: 1000, final variance: nan, final dist: nan`
* looking to profiling detailed info : reported time is close to cpu time (gives us confidence in profiling info)

* rule of the thumb : execution (real) time seems >= x4 for a ~ x2 dimension : advice ?


## geomstats FrechetMean - comparison with previous version

geomstats comparison between current version (commit eac607b8) and previous version (commit e1a1c5f1) OMP_NUM_THREADS=1, varying dimension, execution time (seconds) :

| dim | current profiling cpu time | previous profiling cpu time |
| --- | -------------------------- | --------------------------- |
| 10  | 0.469                      | 0.747                       |
| 15  | 6.111                      | 9.612                       |
| 20  | 10.200                     | 17.213                      |
| 30  | 25.181                     | 41.493                      |
| 40  | 49.811                     | 76.678                      |
| 50  | error                      | not measured                |

* ~ 30-40% faster with newer code version versus previous version

geomstats comparison between current version (commit eac607b8) and previous version (commit e1a1c5f1) OMP_NUM_THREADS=1, varying dimension, number of calls to c_einsum/eigh functions :

| dim | current profiling ncalls c_einsum/eigh | previous profiling ncalls c_einsum/eigh |
| --- | -------------------------------------- | --------------------------------------- |
| 10  | 3080/879                               | 4116/1323                               |
| 15  | 21000/6000                             | 28000/9000                              |
| 20  | 21000/6000                             | 28000/9000                              |
| 30  | 21000/6000                             | 28000/9000                              |
| 40  | 21000/6000                             | 28000/9000                              |

* ... with a 25% ncalls reduction for `c_einsum` and 33.3% ncalls reduction for `eigh`

## geomstats FrechetMean and nilearn _geometric_mean - iterations for convergence

geomstat FrechetMean and nilearn _geometric_mean, with OMP_NUM_THREADS=1, varying dimension, number of iterations for convergence (max iter 1000)) :

| dim | geomstats iterations | nilearn iterations |
| --- | -------------------- | ------------------ |
| 10  | 146                  | 153                |
| 15  | 1000                 | 16                 |
| 20  | 1000                 | 16                 |
| 30  | 1000                 | 14                 |
| 40  | 1000                 | 12                 |
| 50  | error                | 10                 |
| 60  | not measured         | 9                  |
| 100 | not measured         | error              |

* convergence issue for geomstats FrechetMean (to be patched soon) : divergence or very slow convergence
* convergence issue for geomstats FrechetMean is probably the biggest factor yet for the ~ x100-200 execution time between geomstats and nilearn for issue 913


geomstat FrechetMean and nilearn _geometric_mean, with OMP_NUM_THREADS=1, varying dimension, profiling cpu time divided by iteration number (ms) :

| dim | geomstats cpu time per iter | nilearn cpu time per iter |
| --- | --------------------------- | ------------------------- |
| 10  | 3.166                       | 6.1998                    |
| 15  | 6.172                       | 8.6594                    |
| 20  | 10.172                      | 10.3032                   |
| 30  | 25.372                      | 16.8727                   |
| 40  | 49.256                      | 24.5363                   |
| 50  | error                       | 34.6073                   |
| 60  | not measured                | 46.7325                   |
| 100 | not measured                | error                     |

* execution time per iteration now equivalent or quicker with geomstats for small problems
* ... still better scaling for nilearn for this problem (~ x2 duration for geomstats for dim 40)

geomstat FrechetMean versus nilearn _geometric_mean execution time ratio, with OMP_NUM_THREADS=1, varying dimension, profiling cpu time raw or divided by iteration number :

| dim | geomstats/nilearn cpu time | geomstats/nilearn cpu time per iter |
| --- | -------------------------- | ----------------------------------- |
| 10  | 0.487                      | 0.511                               |
| 15  | 44.549                     | 0.713                               |
| 20  | 61.706                     | 0.988                               |
| 30  | 107.409                    | 1.504                               |
| 40  | 167.290                    | 2.007                               |

* test suggests that solving convergence problems for geomstats FrechetMean will reduce execution time overhead for this tests (dim 30-40) from ~ x100-200 to ~1.5-2 ratio
* need to confirm after patching the code

* maybe useful to test this code with :
  * higher dimension : requires solving errors for geomstats (dim 50) and nilearn (dim 100)
  * higher number of points (not tested yet)
  * more iterations (not tested yet, would require a problem with a slower convergence)
* maybe useful to continue investigating for remaining performance difference between geomstats and nilearn (or switch to other test case ?)