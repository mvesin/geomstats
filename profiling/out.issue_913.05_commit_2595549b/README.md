# Geomstats issue 913 basic benchmarks summary

Benches done with branch `feature/test_profiling` commit 2595549b
* after : use step size & adapt step size in case norm of the tangent mean increases (& others)

See results file and profiling output for details.

Note : should have run each of these tests 10+ times. observe several %variation between tests.

Note : all tests (and previous tests conducted on a Dell Precision 7550 + 1x Intel(R) Core(TM) i7-10875H CPU @ 2.30GHz + 32GB RAM)


## geomstat FrechetMean - OMP_NUM_THREADS=1

geomstat FrechetMean with OMP_NUM_THREADS=1, varying number of points : execution time (ms), number of iterations for convergence (max iter 1000), time per iteration (ms)

For dimension 30 :

| n_points | profiling cpu time | iterations | time per iter | time per iter / dim |
| -------- | ------------------ | ---------- | ------------- | ------------------- |
| 100      | 960.2              | 37         | 25.95         | 0.260               |
| 200      | 1643               | 31         | 53.00         | 0.265               | 
| 300      | 2352               | 29         | 81.10         | 0.270               |
| 400      | 3033               | 28         | 108.3         | 0.271               |
| 500      | 3847               | 28         | 137.4         | 0.275               |
| 600      | 4212               | 27         | 156.0         | 0.260               |
| 700      | 4884               | 27         | 180.9         | 0.258               |
| 800      | 5542               | 26         | 213.2         | 0.267               |
| 900      | 5996               | 26         | 230.6         | 0.256               |
| 1000     | 6889               | 26         | 265.0         | 0.265               |

For dimension 60 :

| n_points | profiling cpu time | iterations | time per iter | time per iter / dim |
| -------- | ------------------ | ---------- | ------------- | ------------------- |
| 100      | 2812.9             | 20         | 140.6         | 1.406               |
| 200      | 3640.8             | 13         | 280.1         | 1.401               | 
| 300      | 5917.8             | 14         | 422.7         | 1.409               |
| 400      | 7442.4             | 14         | 531.6         | 1.329               |
| 500      | 9190.9             | 14         | 656.5         | 1.313               |
| 600      | 11545              | 14         | 824.6         | 1.374               |
| 700      | 14679              | 16         | 917.4         | 1.311               |
| 800      | 16820              | 16         | 1051          | 1.314               |
| 900      | 19022              | 16         | 1189          | 1.321               |
| 1000     | 21275              | 16         | 1329          | 1.329               |

For dimension 100 :

| n_points | profiling cpu time | iterations | time per iter | time per iter / dim |
| -------- | ------------------ | ---------- | ------------- | ------------------- |
| 100      | 5695.1             | 11         | 517.7         | 5.177               |
| 200      | 10669              | 10         | 1067          | 5.335               | 
| 300      | 23691              | 16         | 1481          | 4.938               |
| 400      | 30096              | 15         | 2006          | 5.015               |
| 500      | 42389              | 17         | 2493          | 4.986               |
| 600      | 51112              | 17         | 3007          | 5.012               |
| 700      | 60086              | 17         | 3534          | 5.049               |
| 800      | 78279              | 19         | 4120          | 5.150               |
| 900      | 95618              | 21         | 4553          | 5.059               |
| 1000     | 109323             | 21         | 5206          | 5.206               |

* for dimensions tested (30 60 100), time per iteration seems to be growing linearly with number of points


## nilearn _geometric_mean - OMP_NUM_THREADS=1

nilearn _geometric_mean with OMP_NUM_THREADS=1, varying number of points : execution time (ms), number of iterations for convergence (max iter 1000), time per iteration (ms)

For dimension 30 :

| n_points | profiling cpu time | iterations | time per iter |
| -------- | ------------------ | ---------- | ------------- |
| 100      | 480.4              | 31         | 15.50         |
| 200      | 816.9              | 26         | 31.42         | 
| 300      | 1074               | 23         | 46.70         |
| 400      | 1396               | 22         | 63.45         |
| 500      | 1661               | 21         | 79.10         |
| 600      | 1939               | 20         | 96.95         |
| 700      | 2222               | 20         | 111.1         |
| 800      | 2583               | 20         | 129.2         |
| 900      | 2894               | 20         | 144.7         |
| 1000     | 3148               | 20         | 157.4         |

For dimension 60 :

| n_points | profiling cpu time | iterations | time per iter |
| -------- | ------------------ | ---------- | ------------- |
| 100      | 621.1              | 13         | 47.78         |
| 200      | 1211               | 13         | 93.15         | 
| 300      | 1690               | 12         | 140.8         |
| 400      | 2237               | 12         | 186.4         |
| 500      | 2881               | 12         | 240.1         |
| 600      | 3374               | 12         | 281.2         |
| 700      | 3984               | 12         | 332.0         |
| 800      | 4396               | 12         | 366.3         |
| 900      | 4637               | 11         | 421.5         |
| 1000     | 5130               | 11         | 466.4         |

For dimension 100 :

| n_points | profiling cpu time | iterations | time per iter |
| -------- | ------------------ | ---------- | ------------- |
| 100      | 1618.0               | 13       | 124.5         |
| 200      | 3195.1               | 13       | 245.8         | 
| 300      | 4791.1               | 13       | 368.5         |
| 400      | 5914.7               | 12       | 492.9         |
| 500      | 7435.1               | 12       | 619.6         |
| 600      | 9053.8               | 12       | 754.5         |
| 700      | 10506                | 12       | 875.5         |
| 800      | 11868                | 12       | 989.0         |
| 900      | 13298                | 12       | 1108          |
| 1000     | 14688                | 12       | 1224          |

* for dimensions tested (30 60 100), time per iteration seems to be growing linearly with number of points

