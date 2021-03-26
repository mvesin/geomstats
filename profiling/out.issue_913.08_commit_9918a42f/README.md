# Geomstats issue 913 basic benchmarks summary

Benches done with branch `feature/test_profiling` commit 9918a42f
* after : use Matrices.mul to improve readability (& others and misc)

See results file and profiling output for details.

Note : should have run each of these tests 10+ times. observe several %variation between tests.

Note : all tests (and previous tests) conducted on a Dell Precision 7550 + 1x Intel(R) Core(TM) i7-10875H CPU @ 2.30GHz (8 cores, 16 threads) + 32GB RAM

## geomstat FrechetMean - openblas autograd.numpy from pip

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

### test - OMP_NUM_THREADS=1

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


* convergence comparison with previous version : iterations variance and final step unchanged, number of steps and final distance unchanged at observed precision (4 digits)


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

### test - default thread options

geomstat FrechetMean, varying dimension : execution time (seconds), number of iterations for convergence (max iter 1000), final variance, final distance (squared_norm).

* real time (per iteration) is ~ 20-30% higher (worse) than OMP_NUM_THREADS=1 ...
* ... while using several cores (16 hardware threads on the test machine), thus cpu time (per iteration) is ~ x15-16 higher (worse)

See output and profiling files for details.


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

### test - OMP_NUM_THREADS=1

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


* convergence comparison with autograd numpy from pip version : iterations, variance and final step unchanged, number of steps and final distance unchanged at observed precision (4 digits)

* note : profiling real time is very close to profiling cpu time (~ <1% diff)

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

### test - default thread options

geomstat FrechetMean, varying dimension : execution time (seconds), number of iterations for convergence (max iter 1000), final variance, final distance (squared_norm).

* real time (per iteration) is ~ 20-30% higher (worse) than OMP_NUM_THREADS=1 ...
* ... while using several cores (16 hardware threads on the test machine), this cpu time (per iteration) is ~ x15-16 higher (worse)

See output and profiling files for details.


## geomstat FrechetMean - mkl numpy from conda, no autograd

### install

Using mkl numpy from conda 
* use python 3.7 & others to match geomstats opt-requirements
* install numpy from `defaults` channel, don't use autograd (not provided in `defaults` channel)

**WARNING : tests done in `feature/test_noautograd`, results added here for commodity**

```
# git checkout feature/test_noautograd
conda env create -f ./conda-requirements/requirements.yaml
conda activate geomstats-condamklnumpy
# not installed dev & opts requirements for this test
conda env update -f conda-requirements/profiling-requirements.yaml
# use geomstats
export PYTHONPATH=/path/to/my/gitclonedir
```

Note : ok using mkl numpy, no autograd installed
```
>>> import autograd.numpy
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'autograd'
>>> import numpy
>>> numpy.show_config()
blas_mkl_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamklnumpy/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamklnumpy/include']
blas_opt_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamklnumpy/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamklnumpy/include']
lapack_mkl_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamklnumpy/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamklnumpy/include']
lapack_opt_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamklnumpy/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamklnumpy/include']
```

### test - OMP_NUM_THREADS=1

geomstat FrechetMean with OMP_NUM_THREADS=1, varying dimension : cpu and real execution time (seconds) :

| dim | profiling cpu time | profiling real time | iterations |
| --- | ------------------ | ------------------- | ---------- |
| 10  | 0.0160             | 0.0175              | 9          |
| 15  | 0.0332             | 0.0332              | 12         |
| 20  | 0.0626             | 0.0627              | 17         |
| 30  | 0.283              | 0.284               | 35         |
| 40  | 3.337              | 3.347               | 250        |
| 50  | 0.307              | 0.308               | 14         |
| 60  | 0.611              | 0.613               | 19         |
| 70  | 0.762              | 0.764               | 17         |
| 80  | 0.969              | 0.971               | 17         |
| 90  | 0.733              | 0.738               | 9          |
| 100 | 0.972              | 0.974               | 10         |
| 120 | 2.014              | 2.018               | 14         |
| 140 | 3.886              | 3.893               | 19         |
| 160 | 8.647              | 8.704               | 29         |
| 180 | 20.416             | 20.604              | 51         |
| 200 | not tested         | not tested          |            |
| 250 | not tested         | not tested          |            |
| 300 | not tested         | not tested          |            |


* note : convergence comparison with autograd numpy from pip version : iterations, variance and final step unchanged, number of steps and final distance unchanged at observed precision (4 digits)


Time per iteration computed as the profiling cpu time for our problem (ms) until convergence (max iter 1000, not reached), divided by the number of iteration :

| dim | cpu time per iter  | real time per iter |
| --- | ------------------ | ------------------ |
| 10  | 1.778              | 1.944              |
| 15  | 2.767              | 2.767              |
| 20  | 3.682              | 3.688              |
| 30  | 8.086              | 8.000              |
| 40  | 13.35              | 13.88              |
| 50  | 21.93              | 22.00              |
| 60  | 32.16              | 32.26              |
| 70  | 44.82              | 44.94              |
| 80  | 57.00              | 57.12              |
| 90  | 81.44              | 82.00              |
| 100 | 97.20              | 97.40              |
| 120 | 143.9              | 144.1              |
| 140 | 204.5              | 204.9              |
| 160 | 298.2              | 300.1              |
| 180 | 400.3              | 404.0              |
| 200 | not tested         | not tested         | 
| 250 | not tested         | not tested         | 
| 300 | not tested         | not tested         | 

* observing gains (~ 15-30% in high dimensions) versus openblas numpy


### test - default thread options

geomstat FrechetMean, varying dimension : cpu and real execution time (seconds) :

| dim | profiling cpu time | profiling real time | iterations |
| --- | ------------------ | ------------------- | ---------- |
| 10  | 0.0888             | 0.0179              | 9          |
| 15  | 0.265              | 0.0343              | 12         |
| 20  | 0.531              | 0.0668              | 17         |
| 30  | 2.594              | 0.326               | 35         |
| 40  | 29.326             | 3.680               | 250        |
| 50  | 2.199              | 0.276               | 14         |
| 60  | 4.120              | 0.516               | 19         |
| 70  | 4.705              | 0.591               | 17         |
| 80  | 5.104              | 0.641               | 17         |
| 90  | 3.786              | 0.476               | 9          |
| 100 | 5.200              | 0.653               | 10         |
| 120 | 9.780              | 1.254               | 14         |
| 140 | 18.267             | 2.293               | 19         |
| 160 | 34.555             | 4.340               | 29         |
| 180 | 81.243             | 10.206              | 51         |
| 200 | not tested         | not tested          |            |
| 250 | not tested         | not tested          |            |
| 300 | not tested         | not tested          |            |


* note : convergence comparison with autograd numpy from pip version : iterations, variance and final step unchanged, number of steps and final distance unchanged at observed precision (4 digits)


Time per iteration computed as the profiling cpu time for our problem (ms) until convergence (max iter 1000, not reached), divided by the number of iteration :

| dim | cpu time per iter  | real time per iter |
| --- | ----    ---------- | ------------------ |
| 10  | 9.867              | 1.989              |
| 15  | 22.08              | 2.858              |
| 20  | 31.24              | 3.929              |
| 30  | 74.11              | 9.314              |
| 40  | 117.3              | 14.72              |
| 50  | 157.1              | 19.71              |
| 60  | 216.8              | 27.16              |
| 70  | 276.8              | 34.76              |
| 80  | 300.2              | 37.71              |
| 90  | 420.7              | 52.89              |
| 100 | 520.0              | 65.30              |
| 120 | 698.6              | 89.57              |
| 140 | 961.4              | 120.7              |
| 160 | 1191.6             | 149.7              |
| 180 | 1593.0             | 200.1              |
| 200 | not tested         | not tested         | 
| 250 | not tested         | not tested         | 
| 300 | not tested         | not tested         | 

* in high dimensions ~ x4 cpu time for ~ 50% lower real time per iteration, versus mkl with OMP_NUM_THREADS=1

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

Note : ok using mkl numpy, with autograd
```
>>> import autograd.numpy
>>> autograd.numpy.show_config()
blas_mkl_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamkl2numpy/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamkl2numpy/include']
blas_opt_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamkl2numpy/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamkl2numpy/include']
lapack_mkl_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamkl2numpy/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamkl2numpy/include']
lapack_opt_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamkl2numpy/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/user/mvesin/home/.conda/envs/geomstats-condamkl2numpy/include']
```
### test - OMP_NUM_THREADS=1

geomstat FrechetMean with OMP_NUM_THREADS=1, varying dimension : cpu and real execution time (seconds) :

| dim | profiling cpu time | profiling real time | iterations |
| --- | ------------------ | ------------------- | ---------- |
| 10  | 0.0163             | 0.0164              | 9          |
| 15  | 0.0337             | 0.0338              | 12         |
| 20  | 0.0643             | 0.0644              | 17         |
| 30  | 0.291              | 0.292               | 35         |
| 40  | 3.378              | 3.387               | 250        |
| 50  | 0.311              | 0.312               | 14         |
| 60  | 0.627              | 0.627               | 19         |
| 70  | 0.766              | 0.768               | 17         |
| 80  | 0.987              | 0.989               | 17         |
| 90  | 0.749              | 0.751               | 9          |
| 100 | 1.017              | 1.020               | 10         |
| 120 | 2.050              | 2.055               | 14         |
| 140 | 4.150              | 4.180               | 19         |
| 160 | 9.371              | 9.496               | 29         |
| 180 | 21.407             | 21.706              | 51         |
| 200 | not tested         | not tested          |            |
| 250 | not tested         | not tested          |            |
| 300 | not tested         | not tested          |            |


Time per iteration computed as the profiling cpu time for our problem (ms) until convergence (max iter 1000, not reached), divided by the number of iteration :

| dim | cpu time per iter  | real time per iter |
| --- | ----    ---------- | ------------------ |
| 10  | 1.811              | 1.822              |
| 15  | 2.808              | 2.817              |
| 20  | 3.782              | 3.788              |
| 30  | 8.314              | 8.343              |
| 40  | 13.51              | 13.55              |
| 50  | 22.21              | 22.29              |
| 60  | 33.00              | 33.00              |
| 70  | 45.06              | 45.18              |
| 80  | 58.06              | 58.18              |
| 90  | 83.22              | 83.44              |
| 100 | 101.7              | 102.0              |
| 120 | 146.4              | 146.8              |
| 140 | 218.4              | 220.0              |
| 160 | 323.1              | 327.4              |
| 180 | 419.7              | 425.6              |
| 200 | not tested         | not tested         | 
| 250 | not tested         | not tested         | 
| 300 | not tested         | not tested         | 

* observing gains (~ 10-25% in high dimensions) versus openblas numpy, but slight overhead versus the non-autograd mkl numpy (< ~10%)


### test - default thread options

geomstat FrechetMean, varying dimension : cpu and real execution time (seconds) :

| dim | profiling cpu time | profiling real time | iterations |
| --- | ------------------ | ------------------- | ---------- |
| 10  | 0.0940             | 0.0190              | 9          |
| 15  | 0.394              | 0.0497              | 12         |
| 20  | 0.554              | 0.0695              | 17         |
| 30  | 2.551              | 0.321               | 35         |
| 40  | 30.764             | 3.851               | 250        |
| 50  | 2.014              | 0.252               | 14         |
| 60  | 3.508              | 0.439               | 19         |
| 70  | 4.090              | 0.513               | 17         |
| 80  | 5.012              | 0.630               | 17         |
| 90  | 3.620              | 0.454               | 9          |
| 100 | 5.010              | 0.629               | 10         |
| 120 | 9.774              | 1.229               | 14         |
| 140 | 17.999             | 2.260               | 19         |
| 160 | 37.197             | 4.681               | 29         |
| 180 | 77.749             | 9.771               | 51         |
| 200 | not tested         | not tested          |            |
| 250 | not tested         | not tested          |            |
| 300 | not tested         | not tested          |            |


* note : convergence comparison with autograd numpy from pip version : iterations, variance and final step unchanged, number of steps and final distance unchanged at observed precision (4 digits)


Time per iteration computed as the profiling cpu time for our problem (ms) until convergence (max iter 1000, not reached), divided by the number of iteration :

| dim | cpu time per iter  | real time per iter |
| --- | ------------------ | ------------------ |
| 10  | 10.44              | 2.111              |
| 15  | 32.83              | 4.142              |
| 20  | 32.59              | 4.088              |
| 30  | 72.89              | 9.171              |
| 40  | 123.1              | 15.40              |
| 50  | 143.9              | 18.00              |
| 60  | 184.6              | 23.11              |
| 70  | 240.6              | 30.41              |
| 80  | 294.8              | 37.06              |
| 90  | 402.2              | 50.44              |
| 100 | 501.0              | 62.90              |
| 120 | 698.1              | 87.79              |
| 140 | 947.3              | 118.9              |
| 160 | 1282.7             | 161.4              |
| 180 | 1524.5             | 191.6              |
| 200 | not tested         | not tested         | 
| 250 | not tested         | not tested         | 
| 300 | not tested         | not tested         | 

* versus mkl with OMP_NUM_THREADS=1 : in high dimensions ~ x4 cpu time for ~ 50% lower real time per iteration





## geomstats FrechetMean - time per iteration depending on numpy

geomstat FrechetMean, varying dimension, real time per iteration and cpu time per iteration for convergence (max iter 1000)) :
* openblas autograd.numpy from pip, with OMP_NUM_THREADS=1
* openblas autograd.numpy from conda , with OMP_NUM_THREADS=1
* mkl numpy from conda, no autograd, with OMP_NUM_THREADS=1
* mkl numpy from conda, no autograd, default thread options
* mkl autograd.numpy from conda, with OMP_NUM_THREADS=1
* mkl autograd.numpy from conda, default thread options

See above for numbers, summary for testing FrechetMean problem on our 8 core / 16 thread test machine:

* no observed impact on numerical results from the numpy package (same number of iterations, final variance, distance and step)

* openblas autograd.numpy is ~ 20-30% faster (real time) with OMP_NUM_THREADS=1 (vs default thread options), while using only 1 core (cpu time consumed is x15-16 higher with default thread options)
* openblas autograd.numpy performance is equivalent with pip vs conda package
* mkl numpy from conda, no autograd, with OMP_NUM_THREADS=1 is ~ 15-30% faster in high dimensions vs openblas numpy (real time or cpu time)
* mkl numpy from conda, no autograd, default thread options is ~ 50% faster (real time) in high dimensions versus OMP_NUM_THREADS=1, but with a x4 cpu time cost
* mkl autograd.numpy from conda performance is close to mkl numpy from conda without autograd (both with OMP_NUM_THREADS=1 and default thread options)

Conclusion at this point :
* would be useful to propose conda requirements file for mkl autograd.numpy with geomstats, in addition to the pip requirements file. It permits easy performance gains for users in many scenario
* need to investigate a bit more numpy packaging (begining of next sprint)