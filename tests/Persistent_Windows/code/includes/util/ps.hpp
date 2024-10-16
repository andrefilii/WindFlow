#ifndef SPIKEDETECTION_PTUPLE_HPP
#define SPIKEDETECTION_PTUPLE_HPP

#include <windflow.hpp>
#include <deque>

using namespace std;

struct persistent_state_t
{
    unsigned one{};
    double result{};
    std::deque<double> vals{};
};

#endif
