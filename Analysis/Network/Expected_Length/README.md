These scripts can be used to compute the expected maximum topological length of a binary branching network with a given number of inlet segments, following Shreve (1974, Eq. 13 & 14). This calculation involves a time consuming iteratation so is implemented in `C++` here for efficiency. To compile the code type:

```
$ g++ -o shreve_probabilities shreve_probabilities.cpp -DN=<max_N1>
```

where `<max_N1>` is the desired maximum number of inlet segments. Then, to execute the code, type:

```
$ ./shreve_probabilities
```

This should produce the file `expected_lengths.dat`, containing the results.