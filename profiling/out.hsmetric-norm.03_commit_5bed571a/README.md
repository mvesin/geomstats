# Geomstats issue 920 metric.norm() basic benchmarks summary

Testing HypersphereMetric().norm() vs gs.linalg.norm() performance issue as described in snippet :
https://github.com/geomstats/geomstats/issues/920#issuecomment-792782040

Benches done with branch `feature/test_profiling` commit 5bed571a
* after : master branch updates from 2021-04-23 which includes rewriting/optimization of norm for various metrics

See results file and profiling output for details.

Note : should have run each of these tests 10+ times. observe several %variation between tests.

Note : all tests (and previous tests) conducted on a Dell Precision 7550 + 1x Intel(R) Core(TM) i7-10875H CPU @ 2.30GHz (8 cores, 16 threads) + 32GB RAM + GPU Quadro T1000 Mobile


## install

```
conda env create -f ./conda-requirements-3_backends/requirements.yaml
conda activate geomstats-conda3backends
# not installed dev requirements for this test
conda env update -f conda-requirements-3_backends/profiling-requirements.yaml
conda env update -f conda-requirements-3_backends/opt-requirements.yaml
# use geomstats
export PYTHONPATH=/path/to/my/gitclonedir
```

## general tests

### perf impact from metrics rewriting

geomstat test script (hypersphere_metric_norm_perfissue.py) vs original snippet, 10k iterations : real execution time (ms) :
- for current code version
- for previous version (commit b21e3e04) before norm metrics rewrite

| test code                        | metric.norm | gs.linalg.norm | metric.norm b21e3e04 | gs.linalg.norm b21e3e04 |
| -------------------------------- | ----------- | -------------- | -------------------- | ----------------------- |
| original snippet                 | 52.45       | 39.62          | 110.7                | 41.35                   |
| test script, no profiling        | 49.03       | 39.70          | 116.2                | 38.94                   |
| test script, cprofile profiling  | 75.11       | 62.03          | 155.8                | 58.52                   |


geomstat test script (hypersphere_metric_norm_perfissue.py) vs original snippet, 100k iterations : real execution time (ms) :
- for current code version
- for previous version (commit b21e3e04) before norm metrics rewrite

| test code                        | metric.norm | gs.linalg.norm | metric.norm b21e3e04 | gs.linalg.norm b21e3e04 |
| -------------------------------- | ----------- | -------------- | -------------------- | ----------------------- |
| test script, no profiling        | 490.8       | 363.3          | 1107                 | 379.5                   |
| test script, cprofile profiling  | 775.7       | 639.9          | 1673                 | 594.4                   |

Rewriting metrics norm gives a 50-60% shorter execution time for our `HypersphereMetric.norm()` test.
Execution time is now only ~1.2-1.35 the execution time of `gs.linalg.norm()`

Further gain can still be expected from adding a pure numpy backend (vs current `autograd.numpy` backend). We did not test pure numpy on current code version.


### perf impact from testing context - 3 backends

geomstat test script (hypersphere_metric_norm_perfissue.py) vs original snippet, 10k iterations : real execution time (ms) :
- numpy backend
- pytorch backend computing in cpu (disabling gpu)
- tensorflow backend computing in cpu (disabling gpu)

| test code                        | backend        | metric.norm | gs.linalg.norm |
| -------------------------------- | -------------- | ----------- | -------------- |
| original snippet                 | numpy          | 52.45       | 39.62          |
| test script, no profiling        | numpy          | 49.03       | 39.70          |
| test script, cprofile profiling  | numpy          | 75.11       | 62.03          |
| original snippet                 | pytorch cpu    | 622.8       | 54.00          |
| test script, no profiling        | pytorch cpu    | 639.8       | 52.26          |
| test script, cprofile profiling  | pytorch cpu    | 777.8       | 55.46          |
| original snippet                 | tensorflow cpu | 1029        | 763.8          |
| test script, no profiling        | tensorflow cpu | 1042        | 837.0          |
| test script, cprofile profiling  | tensorflow cpu | 1625        | 1119           |


This test serves for comparing the impact of the backend and check impact of the testing context (profiling, time counting with perf_counter vs timeit).

* for pytorch backend :
  -`HypersphereMetric.norm()` execution time is ~ x12 that of `gs.linalg.norm()`
  - profiling shows it is mainly due to custom `einsum` in `geomstats/_backend/pytorch/__init__.py` as it represents >88% of the execution time.
* for tensorflow backend :
  - `gs.linalg.norm()` execution time is ~ x15-20 that of other backends which indicates high time cost for the tensorflow implementation for this function
  - as for pytorch backend, `HypersphereMetric.norm()` execution time is dominated ( >92% ) by custom `einsum` in `geomstats/_backend/tensorflow/__init__.py`

