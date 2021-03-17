# Geomstats issue 913 basic benchmarks summary

Benches done with branch `feature/test_profiling` commit 0b5b5709
* after : adapt step size in case norm of the tangent mean increases (& others)

See results file and profiling output for details.

Note : should have run each of these tests 10+ times. observe several %variation between tests.

## geomstat FrechetMean - OMP_NUM_THREADS=1

geomstat FrechetMean with OMP_NUM_THREADS=1, varying dimension, execution time (seconds) and number of iterations for convergence (max iter 1000) and final distance :

| dim | profiling cpu time | iterations | final variance | final distance |
| --- | ------------------ | ---------- | -------------- | -------------- |
| 10  | 0.0321             | 9          | 18.607         | 9.085e-10      |
| 15  | 0.0877             | 13         | 40.934         | 9.354e-10      |
| 20  | 0.201              | 18         | 70.686         | 2.153e-9       | 
| 30  | 1.004              | 37         | 155.983        | 9.578e-9       |
| 40  | 13.592             | 268        | 272.204        | 2.617e-8       |
| 50  | 87.407             | 1000       | 485.023        | 121.894        |

* increasingly difficult convergence and then divergence when problem dim grows : convergence algorithm/stepping/tests debug to be continued ?


## geomstats FrechetMean and nilearn _geometric_mean - iterations for convergence

geomstat FrechetMean (previous commit eac607b8, current commit 0b5b5709) and nilearn _geometric_mean, with OMP_NUM_THREADS=1, varying dimension, number of iterations for convergence (max iter 1000)) :

| dim | geomstats iterations previous | geomstats iterations previous | nilearn iterations previous|
| --- | ----------------------------- |------------------------------ | -------------------------- |
| 10  | 9                             | 146                           | 153                        |
| 15  | 13                            | 1000                          | 16                         |
| 20  | 18                            | 1000                          | 16                         |
| 30  | 37                            | 1000                          | 14                         |
| 40  | 268                           | 1000                          | 12                         |
| 50  | 1000                          | error                         | 10                         |
| 60  | not measured                  | not measured                  | 9                          |
| 100 | not measured                  | not measured                  | error                      |

* geomstat convergence improved over previous version with adaptative step
* but still divergence issue when problem dim increases, in contrast with nilearn becomes which more efficient in term of required iterations
