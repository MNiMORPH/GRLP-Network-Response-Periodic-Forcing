#include <iostream>
#include <cmath>
#include <fstream>
using namespace std;

// Global array to fill with F values
// Avoids computing multiple times which becomes VERY expensive
double F_array[N+1][N+1];

double F(int magnitude, int length)
{
    if (not std::isnan(F_array[magnitude][length]))
        return F_array[magnitude][length];
    if (magnitude == 1)
        return 0.5;
    else if (length == 1)
        return 0.;
    else
    {
        double sum{0.};
        for (int i{1}; i<magnitude; ++i)
        {
            F_array[i][length-1] = F(i, length-1);
            F_array[magnitude-i][length-1] = F(magnitude-i, length-1);
            sum += F_array[i][length-1]*F_array[magnitude-i][length-1];
        }
        return 0.5*sum;
    }
}

double compute_expected_length(int magnitude)
{
    double sum{0.};
    F_array[magnitude][magnitude] = F(magnitude, magnitude);
    for (int i{1}; i<magnitude; ++i)
    {
        F_array[magnitude][i] = F(magnitude, i);
        sum += F_array[magnitude][i] / F_array[magnitude][magnitude];
    }
    return magnitude - sum;
}


int main()
{

    for (int i{0}; i < N+1; ++i)
        for (int j{0}; j < N+1; ++j)
            F_array[i][j] = std::nan("");
   
    ofstream file;
    file.open("expected_lengths.dat");

    for (int magnitude{1}; magnitude < N+1; ++magnitude)
    {
        double expected_length{ compute_expected_length(magnitude) };
        file << magnitude << " " << expected_length << "\n";
        std::cout << "Magnitude: " << magnitude << ", expected_length: " << expected_length << ".\n";

    }

    file.close();

    return 0;
}