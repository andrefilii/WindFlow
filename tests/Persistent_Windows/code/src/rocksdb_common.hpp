// includes
#include <cmath>
#include <string>

using namespace std;
using namespace wf;

#include "../includes/util/sampler.hpp"
#include "../includes/util/metric_group.hpp"

// Global variable for the result
atomic<uint64_t> sent_tuples;
unsigned long app_run_time = 600 * 1000000000L; // 10 minutes

/*
// Struct of the input tuple
struct tuple_all_time_t
{
    size_t key;
    size_t value;
    std::vector<size_t> ts;
    // Constructor
    tuple_t() : key(0), value(0) {}
    tuple_t(size_t _key, size_t _value) : key(_key), value(_value) {}
};
*/

struct tuple_t
{
    size_t key;
    size_t value;
    size_t timestamp;
    // Constructor
    tuple_t() : key(0), value(0) {}
    tuple_t(size_t _key, size_t _value) : key(_key), value(_value) {}
};

/*
struct tuple_t
{
    size_t key;
    size_t value;
    // Constructor
    tuple_t() : key(0), value(0) {}
    tuple_t(size_t _key, size_t _value) : key(_key), value(_value) {}
};
*/

// Struct of the window result
typedef tuple_t result_t;
//typedef tuple_time_t result_time_t;
//typedef tuple_all_time_t result_all_time_t;

// Source functor for generating numbers
class Source_Functor
{
private:
    size_t keys;         // number of keys
    uint64_t next_ts{0}; // next timestamp
    long generated_tuples{0};
    unsigned long app_start_time;
    unsigned long current_time;
    size_t batch_size;
    const size_t max_value = (size_t)33;
    const size_t max_timestamp_offest = (size_t)5000;

public:
    // Constructor
    Source_Functor(const unsigned long _app_start_time,
                   const size_t _batch_size,
                   size_t _keys) : keys(_keys),
                                   app_start_time(_app_start_time),
                                   current_time(_app_start_time),
                                   batch_size(_batch_size) {}

    // operator()
    void operator()(Source_Shipper<tuple_t> &shipper)
    {
        current_time = current_time_nsecs(); // get the current time
        static thread_local std::mt19937 generator1;
        static thread_local std::mt19937 generator2;
        static thread_local std::mt19937 generator3;
        std::uniform_int_distribution<size_t> timestamp_distribution(0, max_timestamp_offest);
        std::uniform_int_distribution<size_t> keys_distribution(0, keys);
        std::uniform_int_distribution<size_t> tuple_value_distribution(0, max_value);
        while (current_time - app_start_time <= app_run_time) // generation loop
        {
            if ((batch_size > 0) && (generated_tuples % batch_size == 0))
            {
                current_time = current_time_nsecs(); // get the new current time
            }
            if (batch_size == 0)
            {
                current_time = current_time_nsecs(); // get the new current time
            }
            tuple_t to_sent_tuple;
            to_sent_tuple.key = keys_distribution(generator1);
            to_sent_tuple.value = tuple_value_distribution(generator2);
            to_sent_tuple.timestamp = current_time_nsecs();
            shipper.pushWithTimestamp(std::move(to_sent_tuple), next_ts);
            shipper.setNextWatermark(next_ts);
            auto offset = (timestamp_distribution(generator3) + 1);
            next_ts += offset;
            generated_tuples++;
        }
        sent_tuples.fetch_add(generated_tuples); // save the number of generated tuples
    }

    // Destructor
    ~Source_Functor() {}
};

// Filter functor (stateless)
class Filter_Functor
{
private:
    size_t processed{0};
    size_t outliers{0};
    unsigned long app_start_time;
    unsigned long current_time;
    const size_t mod = (size_t)2;

public:
    // constructor
    Filter_Functor(const unsigned long _app_start_time) : app_start_time(_app_start_time),
                                                          current_time(_app_start_time) {}

    // operator()
    bool operator()(result_t &result)
    {
        if (result.value % mod == 0)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
};

// Window-based functor (incremental version)
class Win_Functor_INC
{
public:
    // operator() incremental version
    void operator()(const tuple_t &tuple, result_t &result)
    {
        result.value += (size_t)tuple.value;
        result.timestamp = tuple.timestamp;
    }
};

// Window-based functor (non-incremental version)
class Win_Functor_NINC
{
public:
    // operator() non-incremental version
    void operator()(const Iterable<tuple_t> &win, result_t &result)
    {
        result.value = 0;
        //result.ts.clear();
        size_t win_size = win.size();
        if (win_size > 0) {
            int sum = 0;
            for (size_t i = 0; i < win_size; i++)
            {
                sum += win[i].value;
                //result.ts.push_back(win[i].timestamp);
                //result.timestamp += win[i].timestamp;
            }
            result.value = sum/win_size;
        }
    }
};

// WinSink functor
class WinSink_Functor
{
private:
    size_t processed{0}; // counter of received results
    unsigned long app_start_time;
    unsigned long current_time;
    size_t sampling;
    util::Sampler latency_sampler;

public:
    // Constructor
    WinSink_Functor(const long _sampling,
                    const unsigned long _app_start_time) : sampling(_sampling),
                                                           app_start_time(_app_start_time),
                                                           current_time(_app_start_time),
                                                           latency_sampler(_sampling) {}

    // operator()
    void operator()(optional<result_t> &out, RuntimeContext &rc)
    {
        if (out)
        {
            //for (auto &x : out->ts)
            //{
                current_time = current_time_nsecs();
                unsigned long tuple_latency = (current_time - out->timestamp) / 1e03;
                processed++;
                latency_sampler.add(tuple_latency, current_time);
            //}
        }
        else
        {
            util::metric_group.add("latency", latency_sampler);
        }
    }
};
