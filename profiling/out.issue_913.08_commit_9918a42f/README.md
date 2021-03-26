# Geomstats issue 913 basic benchmarks summary

Benches done with branch `feature/test_profiling` commit 9918a42f
* after : use Matrices.mul to improve readability (& others and misc)

See results file and profiling output for details.

Note : should have run each of these tests 10+ times. observe several %variation between tests.

## geomstat FrechetMean - OMP_NUM_THREADS=1 - autograd numpy from pip

### install

Using autograd numpy from pip (same as geomstats packaging, and previous tests).
* choice : pip inside a conda environment
* use python 3.7 to match geomstats opt-requirements

```
conda create -n geomstats python=3.7
conda activate geomstats
# useless when using a specific python version, already installed with python
# conda install pip
pip install -r requirements.txt
pip install -r dev-requirements.txt -r opt-requirements.txt
# use geomstats
export PYTHONPATH=/path/to/my/gitclonedir
```

Note : `autograd.numpy` (same for `numpy`) uses openblas
```
>>> import autograd.numpy
>>> autograd.numpy.show_config()
blas_mkl_info:
  NOT AVAILABLE
blis_info:
  NOT AVAILABLE
openblas_info:
    libraries = ['openblas', 'openblas']
    library_dirs = ['/usr/local/lib']
    language = c
    define_macros = [('HAVE_CBLAS', None)]
blas_opt_info:
    libraries = ['openblas', 'openblas']
    library_dirs = ['/usr/local/lib']
    language = c
    define_macros = [('HAVE_CBLAS', None)]
lapack_mkl_info:
  NOT AVAILABLE
openblas_lapack_info:
    libraries = ['openblas', 'openblas']
    library_dirs = ['/usr/local/lib']
    language = c
    define_macros = [('HAVE_CBLAS', None)]
lapack_opt_info:
    libraries = ['openblas', 'openblas']
    library_dirs = ['/usr/local/lib']
    language = c
    define_macros = [('HAVE_CBLAS', None)]
```

### test

geomstat FrechetMean with OMP_NUM_THREADS=1, varying dimension : execution time (seconds), number of iterations for convergence (max iter 1000), final variance, final distance (squared_norm) :

| dim | profiling cpu time | iterations | final variance | final distance | final step |
| --- | ------------------ | ---------- | -------------- | -------------- | ---------- |
| 10  | 0.0217             | 9          | 18.607         | 9.354e-10      | 1.0        |
| 15  | 0.0495             | 12         | 40.934         | 5.230e-9       | 1.0        |
| 20  | 0.111              | 17         | 70.686         | 7.518e-9       | 1.0        | 
| 30  | 0.441              | 35         | 155.98         | 2.850e-8       | 1.0        |
| 40  | 5.467              | 250        | 272.20         | 7.971e-8       | 1.0        |
| 50  | 0.519              | 14         | 422.20         | 4.707e-9       | 0.5        |
| 60  | 0.898              | 19         | 608.61         | 1.303e-7       | 0.25       |
| 70  | 1.113              | 17         | 821.90         | 1.347e-7       | 0.25       |
| 80  | 1.463              | 17         | 1075.8         | 7.167e-8       | 0.25       |
| 90  | 1.194              | 9          | 1360.8         | 1.347e-7       | 0.5        |
| 100 | 1.488              | 10         | 1678.7         | 3.986e-7       | 0.5        |
| 120 | 3.032              | 14         | 2416.8         | 3.462e-7       | 0.5        |
| 140 | 5.957              | 19         | 3285.3         | 7.582e-7       | 0.5        |
| 160 | 11.974             | 29         | 4284.7         | 7.633e-7       | 0.5        |
| 180 | 23.613             | 51         | 5413.0         | 1.350e-6       | 0.5        |
| 200 | not tested         |            |                |                |            |
| 250 | not tested         |            |                |                |            |
| 300 | not tested         |            |                |                |            |


* convergence comparison with previous version : variance and final step unchanged, number of steps and final distance unchanged at observed precision (4 digits)


Time per iteration computed as the profiling cpu time for our problem (ms) until convergence (max iter 1000, not reached), divided by the number of iteration :

| dim | time per iter converge |
| --- | ---------------------- |
| 10  | 2.411                  |
| 15  | 4.125                  |
| 20  | 6.529                  |
| 30  | 12.60                  |
| 40  | 21.87                  |
| 50  | 37.07                  |
| 60  | 47.26                  |
| 70  | 65.47                  |
| 80  | 86.06                  |
| 90  | 132.7                  |
| 100 | 148.8                  |
| 120 | 216.6                  |
| 140 | 313.5                  |
| 160 | 412.9                  |
| 180 | 463.0                  |
| 200 | not tested             |
| 250 | not tested             |
| 300 | not tested             |

* goal : check performance is consistent with previous version 2197f78c. Observe ~ -+ 10% fluctuation but no general tendency (would need 10+ tests for averaging ...)


## geomstat FrechetMean - OMP_NUM_THREADS=1 - autograd numpy from conda

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

Note : conda-forge numpy uses openblas
```
>>> import autograd.numpy
>>> autograd.numpy.show_config()
blas_info:
    libraries = ['cblas', 'blas', 'cblas', 'blas']
    library_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condanumpy/lib']
    include_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condanumpy/include']
    language = c
    define_macros = [('HAVE_CBLAS', None)]
blas_opt_info:
    define_macros = [('NO_ATLAS_INFO', 1), ('HAVE_CBLAS', None)]
    libraries = ['cblas', 'blas', 'cblas', 'blas']
    library_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condanumpy/lib']
    include_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condanumpy/include']
    language = c
lapack_info:
    libraries = ['lapack', 'blas', 'lapack', 'blas']
    library_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condanumpy/lib']
    language = f77
lapack_opt_info:
    libraries = ['lapack', 'blas', 'lapack', 'blas', 'cblas', 'blas', 'cblas', 'blas']
    library_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condanumpy/lib']
    language = c
    define_macros = [('NO_ATLAS_INFO', 1), ('HAVE_CBLAS', None)]
    include_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condanumpy/include']
```

### test

geomstat FrechetMean with OMP_NUM_THREADS=1, varying dimension : execution time (seconds), number of iterations for convergence (max iter 1000), final variance, final distance (squared_norm) :

| dim | profiling cpu time | iterations | final variance | final distance | final step |
| --- | ------------------ | ---------- | -------------- | -------------- | ---------- |
| 10  | 0.0212             | 9          | 18.607         | 9.354e-10      | 1.0        |
| 15  | 0.0508             | 12         | 40.934         | 5.230e-9       | 1.0        |
| 20  | 0.105              | 17         | 70.686         | 7.518e-9       | 1.0        | 
| 30  | 0.418              | 35         | 155.98         | 2.850e-8       | 1.0        |
| 40  | 5.146              | 250        | 272.20         | 7.971e-8       | 1.0        |
| 50  | 0.491              | 14         | 422.20         | 4.707e-9       | 0.5        |
| 60  | 0.856              | 19         | 608.61         | 1.303e-7       | 0.25       |
| 70  | 1.106              | 17         | 821.90         | 1.347e-7       | 0.25       |
| 80  | 1.345              | 17         | 1075.8         | 7.167e-8       | 0.25       |
| 90  | 1.015              | 9          | 1360.8         | 1.347e-7       | 0.5        |
| 100 | 1.516              | 10         | 1678.7         | 3.986e-7       | 0.5        |
| 120 | 2.852              | 14         | 2416.8         | 3.462e-7       | 0.5        |
| 140 | 5.467              | 19         | 3285.3         | 7.582e-7       | 0.5        |
| 160 | 11.586             | 29         | 4284.7         | 7.633e-7       | 0.5        |
| 180 | 23.641             | 51         | 5413.0         | 1.350e-6       | 0.5        |
| 200 | not tested         |            |                |                |            |
| 250 | not tested         |            |                |                |            |
| 300 | not tested         |            |                |                |            |


* convergence comparison with autograd numpy from pip version : variance and final step unchanged, number of steps and final distance unchanged at observed precision (4 digits)


Time per iteration computed as the profiling cpu time for our problem (ms) until convergence (max iter 1000, not reached), divided by the number of iteration :

| dim | time per iter converge |
| --- | ---------------------- |
| 10  | 2.356                  |
| 15  | 4.233                  |
| 20  | 6.176                  |
| 30  | 11.94                  |
| 40  | 20.58                  |
| 50  | 35.07                  |
| 60  | 45.05                  |
| 70  | 65.06                  |
| 80  | 79.12                  |
| 90  | 112.8                  |
| 100 | 151.6                  |
| 120 | 203.7                  |
| 140 | 287.7                  |
| 160 | 399.5                  |
| 180 | 463.5                  |
| 200 | not tested             |
| 250 | not tested             |
| 300 | not tested             |

* observe ~ -+ 10% fluctuation versus autograd numpy from pip, but no general tendency (would need 10+ tests for averaging ...)





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

