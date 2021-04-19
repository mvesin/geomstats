# Geomstats issue 913 basic benchmarks summary

Benches done with branch `feature/test_profiling` commit 9918a42f
* after : use Matrices.mul to improve readability (& others and misc)

See results file and profiling output for details.

Note : should have run each of these tests 10+ times. observe several %variation between tests.

Note : all tests (and previous tests) conducted on a Dell Precision 7550 + 1x Intel(R) Core(TM) i7-10875H CPU @ 2.30GHz (8 cores, 16 threads) + 32GB RAM


## geomstat FrechetMean - openblas autograd.numpy from conda

### install

Using autograd numpy from conda 
* use python 3.7 & others to match geomstats opt-requirements
* need to use `conda-forge` channel for autograd (not available for `defaults`)
* ... but `conda-forge` (autograd and default) numpy use openblas, not mkl

```
conda env create -f ./conda-requirements/requirements.yaml
conda activate geomstats-condanumpy
# not installed dev & opts requirements for this test
conda env update -f conda-requirements/profiling-requirements.yaml
# use geomstats
export PYTHONPATH=/path/to/my/gitclonedir
```

### test - dim=100, various OMP_NUM_THREADS

geomstat FrechetMean with dimension 100, varying OMP_NUM_THREADS : cpu and real execution time (seconds) :

| OMP_NUM_THREADS | profiling real time | profiling cpu time | 
| --------------- | ------------------- | ------------------ |
|               1 | 1.251               | 1.249              |
|               2 | 1.237               | 2.464              |
|               4 | 1.254               | 4.986              |
|               8 | 1.385               | 11.052             |
|              16 | 3.600               | 54.971             |
|     unspecified | 2.755               | 42.660             |

Note : OMP_NUM_THREADS defaults to 16 when unspecified : consistent with the number of hardware threads on the test machine

| OMP_NUM_THREADS | real time per iter (ms) | cpu time per iter (ms) | 
| --------------- | ----------------------- | ---------------------- |
|               1 | 125.1                   | 124.9                  |
|               2 | 123.7                   | 246.4                  |
|               4 | 125.4                   | 498.6                  |
|               8 | 138.5                   | 1105.2                 |
|              16 | 360.0                   | 5497.1                 |
|     unspecified | 275.5                   | 4266.0                 |


### test - dim=140, various OMP_NUM_THREADS

geomstat FrechetMean with dimension 140, varying OMP_NUM_THREADS : cpu and real execution time (seconds) :

| OMP_NUM_THREADS | profiling real time | profiling cpu time | 
| --------------- | ------------------- | ------------------ |
|               1 | 4.684               | 4.675              |
|               2 | 4.421               | 8.802              |
|               4 | 3.959               | 15.776             |
|               8 | 4.281               | 34.127             |
|              16 | 7.349               | 115.50             |
|     unspecified | 7.110               | 111.69             |

Note : OMP_NUM_THREADS defaults to 16 when unspecified : consistent with the number of hardware threads on the test machine

| OMP_NUM_THREADS | real time per iter (ms) | cpu time per iter (ms) | 
| --------------- | ----------------------- | ---------------------- |
|               1 | 246.5                   | 246.1                  |
|               2 | 232.7                   | 463.3                  |
|               4 | 208.4                   | 830.3                  |
|               8 | 225.3                   | 1796.2                 |
|              16 | 386.8                   | 6079.0                 |
|     unspecified | 374.2                   | 5878.4                 |


### test - dim=60, various OMP_NUM_THREADS

See raw output files.


## geomstat FrechetMean - mkl autograd.numpy from conda

### install

Using mkl numpy and autograd from conda 
* use python 3.7 & others to match geomstats opt-requirements
* install numpy from `defaults` channel, autograd from `conda-forge` (not provided in `defaults` channel)

```
conda env create -f ./conda-mkl-requirements/requirements.yaml
conda activate geomstats-condamkl2numpy
# installed for checking it works ...
conda env update -f ./conda-mkl-requirements/dev-requirements.yaml
conda env update -f ./conda-mkl-requirements/opt-requirements.yaml
conda env update -f ./conda-mkl-requirements/ci-requirements.yaml
#
conda env update -f conda-requirements/profiling-requirements.yaml
# use geomstats
export PYTHONPATH=/path/to/my/gitclonedir
```

### test - dim=100, various OMP_NUM_THREADS

geomstat FrechetMean with dimension 100, varying OMP_NUM_THREADS : cpu and real execution time (seconds) :

| OMP_NUM_THREADS | profiling real time | profiling cpu time | 
| --------------- | ------------------- | ------------------ |
|               1 | 0.957               | 0.955              |
|               2 | 0.744               | 1.478              |
|               4 | 0.625               | 2.481              |
|               8 | 0.627               | 4.987              |
|              16 | 0.627               | 4.981              |
|     unspecified | 0.614               | 4.890              |

Note : OMP_NUM_THREADS has no default value when unspecified.

| OMP_NUM_THREADS | real time per iter (ms) | cpu time per iter (ms) | 
| --------------- | ----------------------- | ---------------------- |
|               1 | 95.7                    | 95.5                   |
|               2 | 74.4                    | 147.8                  |
|               4 | 62.5                    | 248.1                  |
|               8 | 62.7                    | 498.7                  |
|              16 | 62.7                    | 498.1                  |
|     unspecified | 61.4                    | 489.0                  |


### test - dim=140, various OMP_NUM_THREADS

geomstat FrechetMean with dimension 140, varying OMP_NUM_THREADS : cpu and real execution time (seconds) :

| OMP_NUM_THREADS | profiling real time | profiling cpu time | 
| --------------- | ------------------- | ------------------ |
|               1 | 3.812               | 3.808              |
|               2 | 2.804               | 5.596              |
|               4 | 2.258               | 9.001              |
|               8 | 2.229               | 17.759             |
|              16 | 2.213               | 17.638             |
|     unspecified | 2.137               | 17.046             |

Note : OMP_NUM_THREADS has no default value when unspecified.

| OMP_NUM_THREADS | real time per iter (ms) | cpu time per iter (ms) | 
| --------------- | ----------------------- | ---------------------- |
|               1 | 200.6                   | 200.4                  |
|               2 | 147.6                   | 294.5                  |
|               4 | 118.8                   | 473.7                  |
|               8 | 117.3                   | 934.7                  |
|              16 | 116.5                   | 928.3                  |
|     unspecified | 112.5                   | 897.2                  |

### test - dim=100, various MKL_NUM_THREADS

geomstat FrechetMean with dimension 100, varying MKL_NUM_THREADS : cpu and real execution time (seconds) :

| MKL_NUM_THREADS | profiling real time | profiling cpu time | 
| --------------- | ------------------- | ------------------ |
|               1 | 0.967               | 0.964              |
|               2 | 0.741               | 1.477              |
|               4 | 0.631               | 2.503              |
|               8 | 0.625               | 4.967              |
|              16 | 0.626               | 4.990              |
|     unspecified | 0.614               | 4.890              |


| MKL_NUM_THREADS | real time per iter (ms) | cpu time per iter (ms) | 
| --------------- | ----------------------- | ---------------------- |
|               1 | 96.7                    | 96.4                   |
|               2 | 74.1                    | 147.7                  |
|               4 | 63.1                    | 250.3                  |
|               8 | 62.5                    | 496.7                  |
|              16 | 62.6                    | 499.0                  |
|     unspecified | 61.4                    | 489.0                  |


### test - dim=140, various MKL_NUM_THREADS

geomstat FrechetMean with dimension 140, varying MKL_NUM_THREADS : cpu and real execution time (seconds) :

| MKL_NUM_THREADS | profiling real time | profiling cpu time | 
| --------------- | ------------------- | ------------------ |
|               1 | 3.809               | 3.802              |
|               2 | 2.765               | 5.514              |
|               4 | 2.269               | 9.039              |
|               8 | 2.294               | 18.271             |
|              16 | 2.295               | 18.269             |
|     unspecified | 2.137               | 17.046             |


| MKL_NUM_THREADS | real time per iter (ms) | cpu time per iter (ms) | 
| --------------- | ----------------------- | ---------------------- |
|               1 | 200.5                   | 200.1                 |
|               2 | 145.5                   | 290.2                 |
|               4 | 119.4                   | 475.7                 |
|               8 | 120.7                   | 961.6                 |
|              16 | 120.8                   | 961.5                 |
|     unspecified | 112.5                   | 897.2                 |


## geomstat FrechetMean - summary packaging & threading

geomstat FrechetMean, varying {OMP,MKL}_NUM_THREADS : real execution time per iteration (ms) :
* openblas autograd.numpy from conda, using OMP_NUM_THREADS
* mkl autograd.numpy from conda, using OMP_NUM_THREADS
* mkl autograd.numpy from conda, using MKL_NUM_THREADS

Dimension 100 :

| num threads | openblas & OMP_NUM_THREADS | mkl blas & OMP_NUM_THREADS | mkl blas & MKL_NUM_THREADS |
| ----------- | -------------------------- | -------------------------- | -------------------------- |
|           1 | 125.1                      | 95.7                       | 96.7                       |
|           2 | 123.7                      | 74.4                       | 74.1                       |
|           4 | 125.4                      | 62.5                       | 63.1                       |
|           8 | 138.5                      | 62.7                       | 62.5                       |
|          16 | 360.0                      | 62.7                       | 62.6                       |
| unspecified | 275.5                      | 61.4                       | 61.4                       |

Dimension 140 :

| num threads | openblas & OMP_NUM_THREADS | mkl blas & OMP_NUM_THREADS | mkl blas & MKL_NUM_THREADS |
| ----------- | -------------------------- | -------------------------- | -------------------------- |
|           1 | 246.5                      | 200.6                      | 200.5                      |
|           2 | 232.7                      | 147.6                      | 145.5                      |
|           4 | 208.4                      | 118.3                      | 119.4                      |
|           8 | 225.3                      | 117.3                      | 120.7                      |
|          16 | 386.8                      | 116.5                      | 120.8                      |
| unspecified | 374.2                      | 112.5                      | 112.5                      |


Main findings for packaging and threading in our test case :
* confirms interest of using mkl autograd.numpy from conda (vs openblas autograd.numpy) : 45-50% real time per iteration gain with best threading parameters
* setting OMP_NUM_THREADS <= number of cores looks necessary for openblas (default number of threads is number of hardware threads & perf degraded if > number of cores)
* auto setting of threading parameters looks ok for mkl blas
* no measured impact for using OMP_NUM_THREADS vs MKL_NUM_THREADS for mkl blas
* compute efficiency of multi threading is far from linear in all cases