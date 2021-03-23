# Geomstats issue 913 basic benchmarks summary

Benches done with branch `feature/test_noautograd` commit 9042ec21 :
* after commit 2197f78c : use Matrices.mul to improve readability (& others)
* plus : use "real" `numpy` instead of `autograd.numpy` + remove all autograd import to prevent unwanted usage

See results file and profiling output for details.

Note : should have run each of these tests 10+ times. observe several %variation between tests.

## geomstat FrechetMean - OMP_NUM_THREADS=1

geomstat FrechetMean with OMP_NUM_THREADS=1, using `numpy` instead of `autograd.numpy`, varying dimension : execution time (seconds), number of iterations for convergence (max iter 1000), final variance, final distance (squared_norm) :

| dim | profiling cpu time | iterations | final variance | final distance | final step |
| --- | ------------------ | ---------- | -------------- | -------------- | ---------- |
| 10  | 0.0199             | 9          | 18.607         | 9.354e-10      | 1.0        |
| 15  | 0.0472             | 12         | 40.934         | 5.230e-9       | 1.0        |
| 20  | 0.110              | 17         | 70.686         | 7.518e-9       | 1.0        | 
| 30  | 0.434              | 35         | 155.98         | 2.850e-8       | 1.0        |
| 40  | 5.723              | 250        | 272.20         | 7.971e-8       | 1.0        |
| 50  | 0.541              | 14         | 422.20         | 4.707e-9       | 0.5        |
| 60  | 0.923              | 19         | 608.61         | 1.303e-7       | 0.25       |
| 70  | 1.144              | 17         | 821.90         | 1.347e-7       | 0.25       |
| 80  | 1.434              | 17         | 1075.8         | 7.167e-8       | 0.25       |
| 90  | 1.058              | 9          | 1360.8         | 1.347e-7       | 0.5        |
| 100 | 1.449              | 10         | 1678.7         | 3.986e-7       | 0.5        |
| 120 | 2.589              | 14         | 2416.8         | 2.462e-7       | 0.5        |
| 140 | 5.283              | 19         | 3285.3         | 7.582e-7       | 0.5        |
| 160 | 10.520             | 29         | 4284.7         | 7.633e-7       | 0.5        |
| 180 | 23.330             | 51         | 5413.0         | 1.350e-6       | 0.5        |
| 200 | error              |            |                |                |            |
| 250 | not tested         |            |                |                |            |
| 300 | not tested         |            |                |                |            |


* convergence comparison with `autograd.numpy` : variance and final distance unchanged (at examined precision), number of steps and final step unchanged

* dimension 200 gives warning (test aborted)) :
```
WARNING: Negative eigenvalue encountered in log
/user/mvesin/home/.conda/envs/geomstats/lib/python3.7/site-packages/autograd/tracer.py:48: RuntimeWarning: invalid value encountered in log
  return f_raw(*args, **kwargs)
```


Time per iteration computed as the profiling cpu time for our problem (ms) until convergence (max iter 1000, not reached), divided by the number of iteration :

| dim | time per iter converge |
| --- | ---------------------- |
| 10  | 2.488                  |
| 15  | 3.933                  |
| 20  | 6.471                  |
| 30  | 12.40                  |
| 40  | 22.89                  |
| 50  | 38.64                  |
| 60  | 48.58                  |
| 70  | 67.29                  |
| 80  | 84.35                  |
| 90  | 117.6                  |
| 100 | 144.9                  |
| 120 | 184.9                  |
| 140 | 278.1                  |
| 160 | 362.8                  |
| 180 | 457.5                  |
| 200 | error                  |
| 250 | not tested             |
| 300 | not tested             |


## geomstats FrechetMean and nilearn _geometric_mean - time per iteration

geomstat FrechetMean, with OMP_NUM_THREADS=1, varying dimension, cpu time per iteration for convergence (max iter 1000)) :
* geomstats FrechetMean using "real" `numpy` and not autograd (current commit 9042ec21)
* geomstats FrechetMean with `autograd.numpy` (previous commit 2197f78c)


| dim | geomstats noautograd | geomstats autograd |
| --- | -------------------- | ------------------ |
| 10  | 2.488                | 2.378              |
| 15  | 3.933                | 4.392              |
| 20  | 6.471                | 6.412              |
| 30  | 12.40                | 12.29              |
| 40  | 22.89                | 22.34              |
| 50  | 38.64                | 38.29              |
| 60  | 48.58                | 50.53              |
| 70  | 67.29                | 67.18              |
| 80  | 84.35                | 82.06              |
| 90  | 117.6                | 114.2              |
| 100 | 144.9                | 142.0              |
| 120 | 184.9                | 196.1              |
| 140 | 278.1                | 275.0              |
| 160 | 362.8                | 372.8              |
| 180 | 457.5                | 485.7              |
| 200 | error                | error              |


* geomstats performance is very similar with `autograd.numpy` and `numpy`


