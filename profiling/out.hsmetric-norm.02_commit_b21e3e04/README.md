# Geomstats issue 920 metric.norm() basic benchmarks summary

Testing HypersphereMetric().norm() vs gs.linalg.norm() performance issue as described in snippet :
https://github.com/geomstats/geomstats/issues/920#issuecomment-792782040

Benches done with branch `feature/test_profiling` commit b21e3e04
* after : master branch updates from 2021-04-18 which includes
  - removing vectorization decorator when calling `RiemannianMetric.inner_product()` in riemannian_metric.py
  - removing `gs.to_ndarray()` calls in `RiemannianMetric.inner_product()`

See results file and profiling output for details.

Note : should have run each of these tests 10+ times. observe several %variation between tests.

Note : all tests (and previous tests) conducted on a Dell Precision 7550 + 1x Intel(R) Core(TM) i7-10875H CPU @ 2.30GHz (8 cores, 16 threads) + 32GB RAM


## install

Using `autograd.numpy` from conda channel `conda-forge`
* use python 3.7 & others to match geomstats opt-requirements
* using `conda-forge` channel for both autograd (not available for `defaults`) and numpy
* ... but `conda-forge` numpy use openblas, not mkl

```
conda env create -f ./conda-requirements/requirements.yaml
conda activate geomstats-condanumpy
# not installed dev & opts requirements for this test
conda env update -f conda-requirements/profiling-requirements.yaml
# use geomstats
export PYTHONPATH=/path/to/my/gitclonedir
```

## general tests

### perf impact from testing context

geomstat test script (hypersphere_metric_norm_perfissue.py) vs original snippet, 10k iterations : real execution time (ms) :

| test code                        | metric.norm | gs.linalg.norm | metric.norm 8d611afb | gs.linalg.norm 8d611afb|
| -------------------------------- | ----------- | -------------- | -------------------- | ---------------------- |
| original snippet                 | 110.7       | 41.35          | 619.2                | 40.90                  |
| test script, no profiling        | 116.2       | 38.94          | 598.0                | 40.25                  |
| test script, cprofile profiling  | 155.8       | 58.52          | 1078                 | 58.56                  |
| test script, yappi profiling     | 349.1       | 128.4          | 2075                 | 121.8                  |

This test serves for comparing the impact of the testing context (profiling, time counting with perf_counter vs timeit, iteration with for loop vs map) + comparing with previous code version (commit 8d611afb)

For this test :
* test script and gs.linalg.norm have ~same performance as previous version : as expected
* original snippet and test script without profiling have ~same performance : test conditions are close to original reported issue
* profile has heavy impact on performance, but in comparable proportions for metric.norm and gs.linalg.norm

Compared with previous version (commit 8d611afb):
* metric.norm benefits from a > x5 speedup
* ... but metric.norm is still ~ 2.5-3 times slower than gs.linalg.norm

Impact from profile on performance : execution time still somewhat dominated by function calls ?


### perf impact of numpy openblas threading + scaling on iterations

geomstat test script (hypersphere_metric_norm_perfissue.py), varying threading, profiling and number of iterations : real execution time (ms) :

| OMP_NUM_THREADS |profiling | iterations | metric.norm | gs.linalg.norm | metric.norm 8d611afb | gs.linalg.norm 8d611afb |
| --------------- | -------- |----------- | ----------- | -------------- | -------------------- | ----------------------- |
| default         | none     | 10000      | 116.2       | 38.94          | 619.2                | 40.90                   |
| default         | none     | 100000     | 1107        | 379.5          | 6036                 | 392.8                   |
| default         | cprofile | 10000      | 155.8       | 58.52          | 1078                 | 58.56                   |
| default         | cprofile | 100000     | 1673        | 594.4          | 10569                | 588.1                   |
| 1               | none     | 10000      | 108.3       | 41.48          | 603.8                | 41.46                   |
| 1               | none     | 100000     | 1112        | 395.6          | 6387                 | 383.1                   |
| 1               | cprofile | 10000      | 165.1       | 58.95          | 1072                 | 62.07                   |
| 1               | cprofile | 100000     | 1700        | 605.4          | 10733                | 575.2                   |

* execution time is still ~ x10 when scaling x10 iterations : no unexpected effects, using 10k iterations is fine.
* OMP_NUM_THREADS still has minimal impact on performance

* gs.linalg results ~same as 8d611afb : same as expected
* metric.norm > x5 speedup versus 8d611afb (but remains 2.5-3 slower) : for all tested conditions


## investigating autograd.numpy vs pure numpy

Current test case execution profile suggest autograd numpy wrapping impact may now be a major/dominant factor for performance.

### test - pure numpy for inner_product only & all geomstats

geomstat test script (hypersphere_metric_norm_perfissue.py), OMP_NUM_THREADS default, 10k iteration, varying profiling : real execution time (ms) :
* nodec_inner_product : remove decorator (in previous version, already removed in current version)
* test_inner_prod3 : modify nodec_inner_product by replacing :
  * 2 calls to `gs.einsum` by `numpy.einsum` in inner_product
  * function `import autograd.numpy` by `import numpy` in to_ndarray
(notice : this is not meant to be a viable replacement as it is less general than current code, but is more optimized in our case - for testing)
* test_no_autograd : fully replacing `autograd.numpy` by pure numpy


| test case           | profiling | metric.norm | gsinalg.norm | metric.norm 8d611afb | gs.linalg.norm 8d611afb |
| ------------------- | --------- | ----------- | ------------ | -------------------- | ----------------------- |
| default             | none      | 116.2       | 38.94        | 619.2                | 40.90                   |
| default             | cprofile  |  155.8       | 58.52       | 1078                 | 58.56                   |
| nodec_inner_product | none      | N/A         | N/A          | 315.6                | 40.72                   |
| nodec_inner_product | cprofile  | N/A         | N/A          | 533.2                | 60.33                   |
| test_inner_product3 | none      | 98.54       | 39.23        | 201.4                | 39.87                   |
| test_inner_product3 | cprofile  | 136.7       | 61.19        | 319.9                | 62.27                   |
| test_no_autograd    | none      | 78.25       | 33.12        | N/A                  | N/A                    |
| test_no_autograd    | cprofile  | 109.5       | 50.44        | N/A                  | N/A                    |


geomstat test script (hypersphere_metric_norm_perfissue.py), OMP_NUM_THREADS default, 100k iteration, varying profiling : real execution time (ms) 

| test case           | profiling | metric.norm | gsinalg.norm |
| ------------------- | --------- | ----------- | ------------ |
| default             | none      | 1107        | 379.5        |
| default             | cprofile  | 1673        | 594.4        |          
| test_no_autograd    | none      | 825.4       | 337.5        |
| test_no_autograd    | cprofile  | 1139        | 494.5        |


* using pure numpy (test_no_autograd) with `HypersphereMetric.norm()` reduces execution time by ~25-30% versus current master branch (default)
* using pure numpy (test_no_autograd) with `gs.linalg.norm()` also reduces execution time by ~11-16% versus current master branch (default) ...
* ... so `HypersphereMetric.norm()` execution time is still x ~2.2-2.5 `gs.linalg.norm()` execution time for this test
* note : `to_ndarray` is not called anymore in current version of `inner_product`


