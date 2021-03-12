# Geomstats issue 913 basic benchmarks summary

See results file and profiling output for details.

Note : should have run each of these tests 10+ times. observe several %variation between tests.

## geomstat FrechetMean - base test

geomstat FrechetMean with varying dimension, execution time (seconds) :

| dim | profiling real time | time(1) real time | profiling cpu time | time(1) user + sys time |
| --- | ------------------- | ----------------- | ------------------ | ----------------------- |
| 10  | 1.366               | 2.133             | 14.300             | 5.429 + 14.181          |
| 15  | 20.373              | 21.171            | 303.61             | 71.562 + 238.163        |
| 20  | 37.441              | 38.284            | 588.116            | 128.620 + 465.864       |
| 30  | 87.751              | 88.568            | 1379.287           | 306.025 + 1079.799      |
| 40  | 163.285             | 164.189           | 2554.397           | 565.717 + 1995.365      |

* time when code is profiled is a bit under full execution time (normal) but quite near (significant estimate of execution time)
* OMP multithreading seems to be misbehaving (most time spent in kernel)
* looking to profiling detailed info : reported time is close to real time (normal, rest of cpu time is non-python system level threads)

* try OMP_NUM_THREADS=1


## geomstat FrechetMean - OMP_NUM_THREADS=1

geomstat FrechetMean with OMP_NUM_THREADS=1, varying dimension, execution time (seconds) :

| dim | profiling real time | time(1) real time | profiling cpu time | time(1) user + sys time |
| --- | ------------------- | ----------------- | ------------------ | ----------------------- |
| 10  | 0.748               | 1.393             | 0.747              | 1.329 + 0.061           |
| 15  | 9.633               | 10.271            | 9.612              | 10.192 + 0.057          |
| 20  | 17.264              | 17.917            | 17.213             | 17.795 + 0.064          |
| 30  | 41.646              | 42.341            | 41.493             | 41.483 + 0.702          |
| 40  | 76.798              | 77.454            | 76.678             | 75.573 + 1.759          |

* raw performance increase (real time) ~ x2
* compute performance increase (cpu time) ~ x30 : OMP threading really misbehaving
* time spent in kernel is now very low (fine)
* looking to profiling detailed info : reported time is close to cpu time (gives us confidence in profiling info)

* rule of the thumb : execution (real) time seems ~ x4 for a ~ x2 dimension : advice ?

* OMP_NUM_THREADS=1 is a good base for further tests, need to investigate underlying problem


## misc profiling tests

geomstat FrechetMean with OMP_NUM_THREADS=1 and dimension 15, different profilers, execution time (seconds) :

| profiler | profiling real time | time(1) real time | profiling cpu time | time(1) user + sys time |
| -------- | ------------------- | ----------------- | ------------------ | ----------------------- |
| cProfile | 9.633               | 10.271            | 9.612              | 10.192 + 0.057          |
| yappi    | 10.613              | 11.271            | 10.613             | 10.843 + 0.402          |
| none     | 9.595               | 10.258            | 9.595              | 10.169 + 0.065          |

* cProfile profiler impact on execution time seems moderate (error margin for measurements, a few %) : confidence in profiling measures with cProfile

Other tests :
* use python threads and cProfile : as expected, profiling reports execution time but not profiling details for python threads, processes do not use multicore (python limit)
* use python multiprocess and cProfile : as expected, profiling does not report execution time or profiling info for other processes, processes use multicore

* better confidence and understanding of profiler measurements


## misc geomstats backend test

* this test crashes when using `GEOMSTATS_BACKEND=pytorch` or `GEOMSTATS_BACKEND=tensorflow` : advice ?


## nilearn _geometric_mean - base test

nilearn _geometric_mean with varying dimension, execution time (seconds) :

| dim | profiling real time | time(1) real time | profiling cpu time | time(1) user + sys time |
| --- | ------------------- | ----------------- | ------------------ | ----------------------- |
| 15  | 0.217               | 0.989             | 2.385              | 2.266 + 4.998           |
| 20  | 0.274               | 1.070             | 2.766              | 2.486 + 5.446           |
| 30  | 0.475               | 1.281             | 4.877              | 3.074 + 7.247           |
| 40  | 0.673               | 1.548             | 7.332              | 4.160 + 9.432           |
| 50  | 0.748               | 1.623             | 8.735              | 4.495 + 10.816          |
| 60  | 0.818               | 1.712             | 10.658             | 5.278 + 12.953          |

* note : test crashing with dim 100

* problem with OMP threading also applies to nilearn, not geomstats specific (kernel time)
* can't explain : divergence between cpu profiling time and user+sys time

## nilearn _geometric_mean - OMP_NUM_THREADS=1

nilearn _geometric_mean with OMP_NUM_THREADS=1, varying dimension, execution time (seconds) :

| dim | profiling real time | time(1) real time | profiling cpu time | time(1) user + sys time |
| --- | ------------------- | ----------------- | ------------------ | ----------------------- |
| 15  | 0.136               | 0.796             | 0.136              | 0.728 + 0.065           |
| 20  | 0.174               | 0.821             | 0.173              | 0.751 + 0.061           |
| 30  | 0.229               | 0.906             | 0.227              | 0.811 + 0.080           |
| 40  | 0.300               | 0.955             | 0.299              | 0.888 + 0.065           |
| 50  | 0.353               | 1.022             | 0.353              | 0.946 + 0.074           |
| 60  | 0.426               | 1.107             | 0.425              | 1.032 + 0.073           |

* impact of OMP_NUM_THREADS=1 comparable to geomstats (raw performance ~ x2, compute performance ~ x15-30, low time spent in kernel)

* rule of the thumb : execution (real) time seems sublinear to dimension (< x2 for a ~ x2 dimension) : advice ?

## geomstats and nilearn comparison

geomstats and nilearn comparison varying dimension, execution time (seconds) :

| dim | geomstats profiling real time | nilearn profiling real time |
| --- | ----------------------------- | --------------------------- |
| 10  | 1.366                         | not measured                |
| 15  | 20.373                        | 0.217                       |
| 20  | 37.441                        | 0.274                       | 
| 30  | 87.751                        | 0.475                       |
| 40  | 163.285                       | 0.673                       |
| 50  | not measured                  | 0.748                       | 
| 60  | not measured                  | 0.818                       |


geomstats and nilearn comparison OMP_NUM_THREADS=1, varying dimension, execution time (seconds) :

| dim | geomstats profiling real time | nilearn profiling real time |
| --- | ----------------------------- | --------------------------- |
| 10  | 0.748                         | not measured                |
| 15  | 9.633                         | 0.136                       |
| 20  | 17.264                        | 0.174                       |
| 30  | 41.646                        | 0.229                       |
| 40  | 76.798                        | 0.300                       |
| 50  | not measured                  | 0.353                       |
| 60  | not measured                  | 0.426                       |

* ~ x100-200 performance ratio for this problem between nilearn and geomstats
* rule of the thumb : better scaling for nilearn for this problem (~sublinear vs ~quadratic execution time ?)

* OMP_NUM_THREADS=1 looks a good practice for geomstats and nilearn when using numpy backend, at least with the PyPi package : investigate other numpy packaging options ?
* ... but this wont fill the performance gap between geomstats and nilearn for this example : investigate implementation and algorithmic aspects of geomstats ?
