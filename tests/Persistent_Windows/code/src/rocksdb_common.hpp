// includes
#include <cmath>
#include <string>
#include <stdint.h>

using namespace std;
using namespace wf;

#include "../includes/util/sampler.hpp"
#include "../includes/util/metric_group.hpp"

// Global variable for the result
atomic<uint64_t> sent_tuples;
atomic<uint64_t> size_win_tot;
atomic<uint64_t> tot_wins;
atomic<uint64_t> max_win_size;
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
    uint64_t next_ts = 0;
    long generated_tuples{0};
    unsigned long app_start_time;
    unsigned long current_time;
    size_t batch_size;
    const size_t max_value = (size_t)33;
    const size_t max_timestamp_offest = (size_t)5000;
    uint64_t max_next_ts = 0;

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
        std::uniform_int_distribution<size_t> keys_set_distribution(keys/2, keys);

        std::vector<size_t> all_keys(keys);
        std::iota(all_keys.begin(), all_keys.end(), 0);

        int iter=0;
        int n;
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

            std::set<size_t> keys_to_send;
            iter++;
            if (iter%2 == 0) {
                // seconda iterazione
                keys_to_send.insert(all_keys.begin() + n, all_keys.end());
            } else {
                // prima iterazione
                std::shuffle(all_keys.begin(), all_keys.end(), generator3);
                n = keys_set_distribution(generator3);
                keys_to_send.insert(all_keys.begin(), all_keys.begin() + n);
            }

            auto value = tuple_value_distribution(generator2);
            auto timestamp = current_time_nsecs();
            for (auto key : keys_to_send)
            {
                tuple_t to_sent_tuple;
                to_sent_tuple.key = key;
                to_sent_tuple.value = value;
                to_sent_tuple.timestamp = timestamp;
                shipper.pushWithTimestamp(std::move(to_sent_tuple), next_ts);
                shipper.setNextWatermark(next_ts);
                
                generated_tuples++;
            }
            auto offset = (timestamp_distribution(generator3) + 1);
            next_ts += offset;
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
            size_win_tot.fetch_add(win_size);
            tot_wins.fetch_add(1);
            auto cur = max_win_size.load();
            if (cur < win_size) max_win_size.compare_exchange_weak(cur, win_size);

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
                // current_time = current_time_nsecs();
                // unsigned long tuple_latency = (current_time - out->timestamp) / 1e03;
                processed++;
                // latency_sampler.add(tuple_latency, current_time);
            //}
        }
        else
        {
            // util::metric_group.add("latency", latency_sampler);
        }
    }
};
