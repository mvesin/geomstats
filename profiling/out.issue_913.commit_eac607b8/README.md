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


## geomstats FrechetMean comparison with previous version

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

| dim | current profiling ncalls c_einsum/eigh | previous profiling ncalls c_einsum/eigh |
| --- | -------------------------------------- | --------------------------------------- |
| 10  | 3080/879                               | 4116/1323                               |
| 15  | 21000/6000                             | 28000/9000                              |
| 20  | 21000/6000                             | 28000/9000                              |
| 30  | 21000/6000                             | 28000/9000                              |
| 40  | 21000/6000                             | 28000/9000                              |

* ... with a 25% ncalls reduction for `c_einsum` and 33.3% ncalls reduction for `eigh`

