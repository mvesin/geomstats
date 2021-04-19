# Geomstats issue 920 metric.norm() basic benchmarks summary

Testing HypersphereMetric().norm() vs gs.linalg.norm() performance issue as described in snippet :
https://github.com/geomstats/geomstats/issues/920#issuecomment-792782040

Benches done with branch `feature/test_profiling` commit 8d611afb
* after : master branch updates from 2021-03-31

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

| test code                        | metric.norm | gs.linalg.norm |
| -------------------------------- | ----------- | -------------- |
| original snippet                 | 619.2       | 40.90          |
| test script, no profiling        | 598.0       | 40.25          |
| test script, cprofile profiling  | 1078        | 58.56          |
| test script, yappi profiling     | 2075        | 121.8          |

This test serves for comparing the impact of the testing context (profiling, time counting with perf_counter vs timeit, iteration with for loop vs map).

For this test :
* test script has very similar performance without profiling : test conditions are close to original reported issue
* profile has heavy impact on performance, but in comparable proportions for metric.norm and gs.linalg.norm

Impact from profile on performance : execution time dominated by function calls ?


### perf impact of numpy openblas threading + scaling on iterations

geomstat test script (hypersphere_metric_norm_perfissue.py), varying threading, profiling and number of iterations : real execution time (ms) :

| OMP_NUM_THREADS |profiling | iterations | metric.norm | gs.linalg.norm |
| --------------- | -------- |----------- | ----------- | -------------- |
| default         | none     | 10000      | 619.2       | 40.90          |
| default         | none     | 100000     | 6036        | 392.8          |
| default         | cprofile | 10000      | 1078        | 58.56          |
| default         | cprofile | 100000     | 10569       | 588.1          |
| 1               | none     | 10000      | 603.8       | 41.46          |
| 1               | none     | 100000     | 6387        | 383.1          |
| 1               | cprofile | 10000      | 1072        | 62.07          |
| 1               | cprofile | 100000     | 10733       | 575.2          |

Execution time is ~ x10 when scaling x10 iterations : no unexpected effects, using 10k iterations is fine.

OMP_NUM_THREADS also has minimal impact on performance


## investigating impact from vectorization decorators

Profiling from previous tests suggest 40-50% time impact from vectorization.py/decorator when calling inner_product from riemannian_metric.py/squared_norm

### test - remove decorator for inner_product

Simple test : comment out `riemannian_metric.py:178` before calling inner_product (name this test: nodec_inner_product )
```
@geomstats.vectorization.decorator(['else', 'vector', 'vector', 'vector'])
```

geomstat test script (hypersphere_metric_norm_perfissue.py), OMP_NUM_THREADS default, 10k iteration, varying profiling, normal vs nodec_inner_product : real execution time (ms) :

| test case           | profiling | metric.norm | gs.linalg.norm |
| ------------------- | --------- | ----------- | -------------- |
| normal              | none      | 619.2       | 40.90          |
| normal              | cprofile  | 1078        | 58.56          |
| nodec_inner_product | none      | 315.6       | 40.72          |
| nodec_inner_product | cprofile  | 533.2       | 60.33          |

| profiling | metric.norm %gain vs normal test case | gs.linalg.norm %gain vs normal test case |
| --------- | ------------------------------------- | ---------------------------------------- |
| none      | 49.0%                                 | 0.4%                                     |
| cprofile  | 50.5%                                 | -3.0%                                    |

Decorator on `riemannian_metric.py` inner_product accounts for ~50% of `metric.norm` execution time. This is ~independant from profiling overhead.

### test - rewrite decorator

*TODO* : test with rewriting `vectorize.py` decorator (all decorators affected, call the decorator but null payload)

## investigating inner_product code

`riemaniann_metric.py/inner_product` code includes `einsum` (that may be replaced by other numpy operation eg inner ?) and `to_ndarray` (are all necessary ?). We'd like to assess their impact in our test case.

geomstat test script (hypersphere_metric_norm_perfissue.py), OMP_NUM_THREADS default, 10k iteration, varying profiling : real execution time (ms) :
* for nodec_inner_product : see above
* test_inner_prod2 : modify nodec_inner_product by replacing :
```
        #inner_prod = gs.einsum('...k,...k->...', aux, tangent_vec_b)
        inner_prod = autograd.numpy.inner(aux, tangent_vec_b)
```
(notice : this is not a viable replacement as it is less general than current code, but is more optimized in our case - for testing)
* test_inner_prod :  modify nodec_inner_product by commenting out :
```
        #inner_prod = gs.to_ndarray(inner_prod, to_ndim=1)
        #inner_prod = gs.to_ndarray(inner_prod, to_ndim=2, axis=1)
```
(notice : this is not a viable replacement as it is less general than current code, but is more optimized in our case - for testing)

| test case           | profiling | metric.norm | gs.linalg.norm |
| ------------------- | --------- | ----------- | -------------- |
| nodec_inner_product | none      | 315.6       | 40.72          |
| nodec_inner_product | cprofile  | 533.2       | 60.33          |
| test_inner_product2 | none      | 280.6       | 38.99          |
| test_inner_product2 | cprofile  | 483.1       | 60.74          |
| test_inner_product  | none      | 229.7       | 38.90          |
| test_inner_product  | cprofile  | 339.0       | 62.30          |

* removing two final `to_ndarray` permits 25-35% gain on total test execution time
* replacing `einsum` by `numpy.inner` permits ~10% gain on total test execution time


## investigating autograd.numpy vs pure numpy

Current test case execution profile is dominated by function calls and wrapping : autograd numpy wrapping impact may be significative.

### test - pure numpy for inner_product only

geomstat test script (hypersphere_metric_norm_perfissue.py), OMP_NUM_THREADS default, 10k iteration, varying profiling : real execution time (ms) :
* for nodec_inner_product : see above
* test_inner_prod3 : modify nodec_inner_product by replacing :
  * calls to `gs.einsum` by `numpy.einsum` in inner_product
  * function `import autograd.numpy` by `import numpy` in to_ndarray
(notice : this is not a viable replacement as it is less general than current code, but is more optimized in our case - for testing)
* test_inner_prod4 :  modify nodec_inner_product3 by commenting out :
```
        #inner_prod = gs.to_ndarray(inner_prod, to_ndim=1)
        #inner_prod = gs.to_ndarray(inner_prod, to_ndim=2, axis=1)
```
(same as test_inner_prod but in pure numpy)

| test case           | profiling | metric.norm | gs.linalg.norm |
| ------------------- | --------- | ----------- | -------------- |
| nodec_inner_product | none      | 315.6       | 40.72          |
| nodec_inner_product | cprofile  | 533.2       | 60.33          |
| test_inner_product3 | none      | 201.4       | 39.87          |
| test_inner_product3 | cprofile  | 319.9       | 62.27          |
| test_inner_product4 | none      | 151.1       | 41.28          |
| test_inner_product4 | cprofile  | 250.5       | 63.76          |

* using pure numpy in function `inner_product` (test_inner_prod3) permits a 35-40% gain on total test execution time
* ... and removing two final `to_ndarray` in function `inner_product` permits another 20-25% gain on total test execution time


### test - pure numpy for all geomstats

*TODO* test pure numpy replaces autograd.numpy for all geomstats