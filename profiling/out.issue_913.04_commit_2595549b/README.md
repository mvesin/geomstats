# Geomstats issue 913 basic benchmarks summary

Benches done with branch `feature/test_profiling` commit 2595549b
* after : use step size & adapt step size in case norm of the tangent mean increases (& others)

See results file and profiling output for details.

Note : should have run each of these tests 10+ times. observe several %variation between tests.

## geomstat FrechetMean - OMP_NUM_THREADS=1

geomstat FrechetMean with OMP_NUM_THREADS=1, varying dimension : execution time (seconds), number of iterations for convergence (max iter 1000), final variance, final distance (squared_norm) :

| dim | profiling cpu time | iterations | final variance | final distance | final step |
| --- | ------------------ | ---------- | -------------- | -------------- | ---------- |
| 10  | 0.0319             | 9          | 18.607         | 9.354e-10      | 1.0        |
| 15  | 0.0866             | 13         | 40.934         | 9.085e-10      | 1.0        |
| 20  | 0.199              | 18         | 70.686         | 2.153e-9       | 1.0        | 
| 30  | 0.982              | 37         | 155.98         | 9.578e-9       | 1.0        |
| 40  | 14.291             | 268        | 272.20         | 2.617e-8       | 1.0        |
| 50  | 1.258              | 14         | 422.20         | 4.707e-9       | 0.5        |
| 60  | 2.738              | 20         | 608.61         | 3.249e-8       | 0.25       |
| 70  | 3.744              | 18         | 821.90         | 3.069e-8       | 0.25       |
| 80  | 4.997              | 17         | 1075.8         | 7.167e-8       | 0.25       |
| 90  | 3.901              | 9          | 1360.8         | 1.347e-7       | 0.5        |
| 100 | 6.281              | 11         | 1678.7         | 6.410e-8       | 0.5        |

* reducing step when norm grows solves divergence problem. 
* fluctuating number of iterations with dimensions for convergence is not identified as a bug, but slow convergence reveals a need for (later) improving algorithm (steps, epsilon, etc.)
  => out of the scope of the current tests

* current performance tests should focus on time per iteration, to cope with varying number of iterations


Time per iteration computed as the profiling cpu time for our problem (ms) until convergence (max iter 1000, not reached), divided by the number of iteration :

| dim | time per iter converge |
| --- | ---------------------- |
| 10  | 3.544                  |
| 15  | 6.662                  |
| 20  | 11.06                  |
| 30  | 26.54                  |
| 40  | 53.32                  |
| 50  | 89.86                  |
| 60  | 136.9                  |
| 70  | 208.0                  |
| 80  | 293.9                  |
| 90  | 433.4                  |
| 100 | 571.0                  |


## nilearn _geometric_mean - OMP_NUM_THREADS=1

nilearn _geometric_mean with OMP_NUM_THREADS=1, varying dimension : execution time (seconds), number of iterations for convergence (max iter 1000), final (norm / gmean.size) , final step (squared_norm) :

| dim | profiling cpu time | iterations | final (norm/gmean.size) | final step |
| --- | ------------------ | ---------- | ----------------------- | ---------- |
| 10  | 0.0645             | 8          | 5.835e-8                | 1.0        |
| 15  | 0.107              | 12         | 5.690e-8                | 1.0        |
| 20  | 0.166              | 15         | 6.928e-8                | 1.0        |
| 30  | 0.487              | 31         | 9.595e-8                | 1.0        |
| 40  | 4.600              | 204        | 9.911e-8                | 1.0        |
| 50  | 0.559              | 16         | 8.805e-8                | 0.25       |
| 60  | 0.614              | 13         | 8.686e-8                | 0.25       |
| 70  | 0.825              | 13         | 8.124e-8                | 0.25       |
| 80  | 1.028              | 13         | 7.954e-8                | 0.25       |
| 90  | 1.339              | 13         | 6.345e-8                | 0.25       |
| 100 | 1.641              | 13         | 4.542e-8                | 0.25       |

* similar profile with current geomstats FrechetMean : iterations increases with dim, until step adaptation


Time per iteration computed as the profiling cpu time for our problem (ms), until convergence (max iter 1000, not reached), divided by the number of iteration :

| dim | time per iter converge |
| --- | ---------------------- |
| 10  | 8.063                  |
| 15  | 8.912                  |
| 20  | 11.07                  |
| 30  | 15.71                  |
| 40  | 22.55                  |
| 50  | 34.94                  |
| 60  | 47.23                  |
| 70  | 63.46                  |
| 80  | 79.08                  |
| 90  | 103.0                  |
| 100 | 126.2                  |


## geomstats FrechetMean and nilearn _geometric_mean - iterations for convergence

geomstat FrechetMean, with OMP_NUM_THREADS=1, varying dimension, number of iterations for convergence (max iter 1000)) :
* geomstats with step reduction (current commit 0b5b5709)
* geomstats without step reduction (older commit eac607b8)
* nilearn _geometric_mean (current commit 2595549b)
* nilearn _geometric_mean (previous commit eac607b8)

| dim | geomstats iter step | geomstats iter nostep | nilearn iter current | nilearn iter previous |
| --- | ------------------- |---------------------- | -------------------- | --------------------- |
| 10  | 9                   | 146                   | 8                    | 153                   |
| 15  | 13                  | 1000                  | 12                   | 16                    |
| 20  | 18                  | 1000                  | 15                   | 16                    |
| 30  | 37                  | 1000                  | 31                   | 14                    |
| 40  | 268                 | 1000                  | 204                  | 12                    |
| 50  | 14                  | error                 | 16                   | 10                    |
| 60  | 20                  | not measured          | 13                   | 9                     |
| 70  | 18                  | not measured          | 13                   | not measured          |
| 80  | 17                  | not measured          | 13                   | not measured          |
| 90  | 9                   | not measured          | 13                   | not measured          |
| 100 | 11                  | not measured          | 13                   | error                 |

* nilearn convergence modified (versus previous commit eac607b8) : due to modified `random_uniform` for `SPDMatrices` in commit 545a329 ?
* current version : more similarity in geomstats and nilearn convergence in terms of iterations for this problem

## geomstats FrechetMean and nilearn _geometric_mean - time per iteratino

geomstat FrechetMean, with OMP_NUM_THREADS=1, varying dimension, cpu time per iteration for convergence (max iter 1000)) :
* geomstats with step reduction (current commit 0b5b5709), until convergence (max iter 1000, not reached)
* nilearn _geometric_mean (current commit 2595549b), until convergence (max iter 1000, not reached)
* geomstats without step reduction and previous `random_uniform` data (older commit eac607b8), until convergence (or max iter 1000 reached)
* nilearn _geometric_mean with previous `random_uniform` data (older commit eac607b8), until convergence (max iter 1000, not reached)

| dim | geomstats converge | nilearn converge | geomstats previous | nilearn previous |
| --- | ------------------ | ---------------- | ------------------ | ---------------- |
| 10  | 3.544              | 8.063            | 3.166              | 6.200            |
| 15  | 6.662              | 8.912            | 6.172              | 8.659            |
| 20  | 11.06              | 11.07            | 10.17              | 10.30            |
| 30  | 26.54              | 15.71            | 25.37              | 16.87            |
| 40  | 53.32              | 22.55            | 49.26              | 24.54            |
| 50  | 89.86              | 34.94            | error              | 34.61            |
| 60  | 136.9              | 47.23            | not measured       | 46.73            |
| 70  | 208.0              | 63.46            | not measured       | error            |
| 80  | 293.9              | 79.08            | not measured       | not measured     |
| 90  | 433.4              | 103.0            | not measured       | not measured     |
| 100 | 571.0              | 126.2            | not measured       | not measured     |

* while geomstats is more time-per-iteration efficient than nilearn for small dim for this problem, geomstats versus nilearn time-per-iteration ratio grows with dim up to ~ x4-5 for dim 100 
* time-per-iteration is very similar with previous version for both geomstats and nilearn, suggests little impact from step reduction (geomstats) and random data distribution (geomstats, nilearn).