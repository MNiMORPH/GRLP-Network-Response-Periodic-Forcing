import numpy as np
import subprocess as subp
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def calculate_probabilities(max_magnitude):

    # Compile and execute c++ routine
    compiler = [
        "g++",
        "-o",
        "shreve_probabilities",
        "shreve_probabilities.cpp",
        "-DN="+str(max_magnitude)
        ]
    subp.call(compiler)
    execute = ["./shreve_probabilities"]
    subp.call(execute)

    # load output
    arr = np.loadtxt("expected_lengths.dat")
    magnitudes = arr[:,0]
    lengths = arr[:,1]

    # return
    return magnitudes, lengths

magnitudes, lengths = calculate_probabilities(200)

find_magnitude = interp1d(lengths, magnitudes)

# plt.plot(magnitudes, lengths)
# plt.show()