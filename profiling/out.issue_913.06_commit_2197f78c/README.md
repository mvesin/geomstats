# Geomstats issue 913 basic benchmarks summary

Benches done with branch `feature/test_profiling` commit 2197f78c
* after : use Matrices.mul to improve readability (& others)
* note : time spent in np.einsum looks too high, so replacing it with Matrices.mul is expected to gain time - we want to test it

See results file and profiling output for details.

Note : should have run each of these tests 10+ times. observe several %variation between tests.

## geomstat FrechetMean - OMP_NUM_THREADS=1

geomstat FrechetMean with OMP_NUM_THREADS=1, varying dimension : execution time (seconds), number of iterations for convergence (max iter 1000), final variance, final distance (squared_norm) :

| dim | profiling cpu time | iterations | final variance | final distance | final step |
| --- | ------------------ | ---------- | -------------- | -------------- | ---------- |
| 10  | 0.0214             | 9          | 18.607         | 9.354e-10      | 1.0        |
| 15  | 0.0527             | 12         | 40.934         | 5.230e-9       | 1.0        |
| 20  | 0.109              | 17         | 70.686         | 7.518e-9       | 1.0        | 
| 30  | 0.430              | 35         | 155.98         | 2.850e-8       | 1.0        |
| 40  | 5.584              | 250        | 272.20         | 7.971e-8       | 1.0        |
| 50  | 0.536              | 14         | 422.20         | 4.707e-9       | 0.5        |
| 60  | 0.960              | 19         | 608.61         | 1.303e-7       | 0.25       |
| 70  | 1.142              | 17         | 821.90         | 1.347e-7       | 0.25       |
| 80  | 1.395              | 17         | 1075.8         | 7.167e-8       | 0.25       |
| 90  | 1.028              | 9          | 1360.8         | 1.347e-7       | 0.5        |
| 100 | 1.420              | 10         | 1678.7         | 3.986e-7       | 0.5        |
| 120 | 2.746              | 14         | 2416.8         | 2.462e-7       | 0.5        |
| 140 | 5.224              | 19         | 3285.3         | 7.582e-7       | 0.5        |
| 160 | 10.812             | 29         | 4284.7         | 7.633e-7       | 0.5        |
| 180 | 24.771             | 51         | 5413.0         | 1.350e-6       | 0.5        |
| 200 | error              |            |                |                |            |
| 250 | not tested         |            |                |                |            |
| 300 | not tested         |            |                |                |            |


* convergence comparison with previous version : variance and final step unchanged, number of steps and final distance moderately changed (minor adaptations in algorithm ?)

* dimension 200 gives warning and cannot compute result :
```
WARNING: Negative eigenvalue encountered in log
/user/mvesin/home/.conda/envs/geomstats/lib/python3.7/site-packages/autograd/tracer.py:48: RuntimeWarning: invalid value encountered in log
  return f_raw(*args, **kwargs)
WARNING: Maximum number of iterations 1000 reached. The mean may be inaccurate
INFO: n_iter: 1000, final variance: nan, final dist: nan
```


Time per iteration computed as the profiling cpu time for our problem (ms) until convergence (max iter 1000, not reached), divided by the number of iteration :

| dim | time per iter converge |
| --- | ---------------------- |
| 10  | 2.378                  |
| 15  | 4.392                  |
| 20  | 6.412                  |
| 30  | 12.29                  |
| 40  | 22.34                  |
| 50  | 38.29                  |
| 60  | 50.53                  |
| 70  | 67.18                  |
| 80  | 82.06                  |
| 90  | 114.2                  |
| 100 | 142.0                  |
| 120 | 196.1                  |
| 140 | 275.0                  |
| 160 | 372.8                  |
| 180 | 485.7                  |
| 200 | error                  |
| 250 | not tested             |
| 300 | not tested             |


## nilearn _geometric_mean - OMP_NUM_THREADS=1

nilearn _geometric_mean with OMP_NUM_THREADS=1, varying dimension : execution time (seconds), number of iterations for convergence (max iter 1000), final (norm / gmean.size) , final step (squared_norm) :

| dim | profiling cpu time | iterations | final (norm/gmean.size) | final step |
| --- | ------------------ | ---------- | ----------------------- | ---------- |
| 10  | 0.0752             | 8          | 5.835e-8                | 1.0        |
| 15  | 0.131              | 12         | 5.690e-8                | 1.0        |
| 20  | 0.183              | 15         | 6.928e-8                | 1.0        |
| 30  | 0.540              | 31         | 9.595e-8                | 1.0        |
| 40  | 4.975              | 204        | 9.911e-8                | 1.0        |
| 50  | 0.585              | 16         | 8.805e-8                | 0.25       |
| 60  | 0.640              | 13         | 8.686e-8                | 0.25       |
| 70  | 0.848              | 13         | 8.124e-8                | 0.25       |
| 80  | 1.064              | 13         | 7.954e-8                | 0.25       |
| 90  | 1.345              | 13         | 6.345e-8                | 0.25       |
| 100 | 1.653              | 13         | 4.542e-8                | 0.25       |
| 120 | 2.257              | 12         | 5.034e-8                | 0.25       |
| 140 | 3.041              | 11         | 5.909e-8                | 0.25       |
| 160 | 3.945              | 10         | 7.068e-8                | 0.25       |
| 180 | 4.955              | 10         | 2.424e-8                | 0.25       |
| 200 | 5.711              | 9          | 3.620e-8                | 0.25       |
| 250 | 9.044              | 8          | 1.971e-8                | 0.25       |
| 300 | error              |            |                         |            |


* note : little overhead versus previous test (~ 1-2 ms per iteration ?), probably due to additional debug output & timing measures. No change in convergence (normal, not modified)

* dimension 300 gives Nan error


Time per iteration computed as the profiling cpu time for our problem (ms), until convergence (max iter 1000, not reached), divided by the number of iteration :

| dim | time per iter converge |
| --- | ---------------------- |
| 10  | 9.400                 |
| 15  | 10.92                 |
| 20  | 12.20                 |
| 30  | 17.42                 |
| 40  | 24.39                 |
| 50  | 36.57                 |
| 60  | 49.23                 |
| 70  | 65.23                 |
| 80  | 81.85                 |
| 90  | 103.5                 |
| 100 | 127.2                 |
| 120 | 188.1                 |
| 140 | 276.5                 |
| 160 | 394.5                 |
| 180 | 495.5                 |
| 200 | 634.6                 |
| 250 | 1130.5                |
| 300 | error                 |


## geomstats FrechetMean and nilearn _geometric_mean - time per iteration

geomstat FrechetMean, with OMP_NUM_THREADS=1, varying dimension, cpu time per iteration for convergence (max iter 1000)) :
* geomstats FrechetMean (current commit 2197f78c)
* nilearn _geometric_mean (current commit 2197f78c) with debugging overhead
* geomstats FrechetMean (previous commit 0b5b5709)
* nilearn _geometric_mean (previous commit 2595549b)


| dim | geomstats current | nilearn current | geomstats previous | nilearn previous |
| --- | ----------------- | --------------- | ------------------ | ---------------- |
| 10  | 2.378             | 9.400           | 3.544              | 8.063            |
| 15  | 4.392             | 10.92           | 6.662              | 8.912            |
| 20  | 6.412             | 12.20           | 11.06              | 11.07            |
| 30  | 12.29             | 17.42           | 26.54              | 15.71            |
| 40  | 22.34             | 24.39           | 53.32              | 22.55            |
| 50  | 38.29             | 36.57           | 89.86              | 34.94            |
| 60  | 50.53             | 49.23           | 136.9              | 47.23            |
| 70  | 67.18             | 65.23           | 208.0              | 63.46            |
| 80  | 82.06             | 81.85           | 293.9              | 79.08            |
| 90  | 114.2             | 103.5           | 433.4              | 103.0            |
| 100 | 142.0             | 127.2           | 571.0              | 126.2            |
| 120 | 196.1             | 188.1           | not tested         | not tested       |
| 140 | 275.0             | 276.5           | not tested         | not tested       |
| 160 | 372.8             | 394.5           | not tested         | not tested       |
| 180 | 485.7             | 495.5           | not tested         | not tested       |
| 200 | error             | 634.6           | not tested         | not tested       |
| 250 | not tested        | 1130.5          | not tested         | not tested       |
| 300 | not tested        | error           | not tested         | not tested       |


* geomstats and nilearn performance is now very similar for high dimensions for this problem, and geomstats is more efficient for small dimensions. Detailed profiling & tracing confirms time in `spd_matrices'py` function `_aux_log` is now mainly for computing `logm` (as expected, and same as nilearn)

* note: nilearn debug output for tests adds significant overhead for low dimensions, becomes < 1% around dim 100

## geomstats FrechetMean and nilearn _geometric_mean - total time for convergence

geomstat FrechetMean, with OMP_NUM_THREADS=1, varying dimension, cpu total time for convergence (max iter 1000)) :
* geomstats FrechetMean (current commit 2197f78c)
* nilearn _geometric_mean (current commit 2197f78c) with debugging overhead


| dim | geomstats conv time | nilearn conv time |
| --- | ------------------- | ----------------- |
| 10  | 0.0214              | 0.0752            |
| 15  | 0.0527              | 0.131             |
| 20  | 0.109               | 0.183             |
| 30  | 0.430               | 0.540             |
| 40  | 5.584               | 4.975             |
| 50  | 0.536               | 0.585             |
| 60  | 0.960               | 0.640             |
| 70  | 1.142               | 0.848             |
| 80  | 1.395               | 1.064             |
| 90  | 1.028               | 1.345             |
| 100 | 1.420               | 1.653             |
| 120 | 2.746               | 2.257             |
| 140 | 5.224               | 3.041             |
| 160 | 10.812              | 3.945             |
| 180 | 24.771              | 4.955             |
| 200 | error               | 5.711             |
| 250 | not tested          | 9.044             |
| 300 | not tested          | error             |

* differences now measure algorithmic efficiency of geomstats FrechetMean vs nilearn _geometric_mean
