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



