#include <string>
#include <random>
#include <iostream>
#include <math.h>
#include <windflow.hpp>
#include <persistent/windflow_rocksdb.hpp>
#include "rocksdb_common.hpp"

using namespace std;
using namespace chrono;
using namespace wf;

// global variable for the result
// extern atomic<uint64_t> sent_tuples;

// main
int main(int argc, char *argv[])
{
    int option = 0;
    size_t runs = 1;           // 0 -> CB_INC_NORMAL , 1 -> CB_P_INC, 2 -> CB_NON_INC_NORMAL, 3 -> CB_P_NON_INC, 4 -> TB_INC_NORMAL , 5 -> TB_P_INC, 6 -> TB_NONINC_NORMAL, 7 -> TB_P_NONINC ;;
    size_t n_memtables = 0;    // N MemTable ;;
    size_t size_memtables = 0; // MemTable Size ;;
    size_t parallelism = 0;    // Parallelism of each operator replica ;;
    size_t n_keys = 1;         // N_KEYS ;;
    size_t win_slide = 300;
    size_t win_len = 1500;
    size_t key_buff; // Buffer size of fragment
    size_t shared = 0;
    // arguments from command line
    if (argc != 19)
    {
        cout << argv[0] << " -y SharedDb(0 false 1 true) -x Size Buffer Key -r [0 -> CB_INC_NORMAL , 1-> CB_P_INC, 2->CB_NON_INC_NORMAL, 3->CB_P_NON_INC, 4 -> TB_INC_NORMAL , 5-> TB_P_INC, 6->TB_NONINC_NORMAL, 7->TB_P_NONINC] -l [N MemTable] -k [n_keys] -w [MemTable Size] -s [Parallelism of each operator replica]" << endl;
        exit(EXIT_SUCCESS);
    }
    while ((option = getopt(argc, argv, "y:x:r:l:k:m:p:w:s:")) != -1)
    {
        switch (option)
        {
        case 'y':
            shared = atoi(optarg);
            break;
        case 'x':
            key_buff = atoi(optarg);
            break;
        case 'r':
            runs = atoi(optarg);
            break;
        case 'l':
            n_memtables = atoi(optarg);
            break;
        case 'k':
            n_keys = atoi(optarg);
            break;
        case 'm':
            size_memtables = atoi(optarg);
            break;
        case 'p':
            parallelism = atoi(optarg);
            break;
        case 'w':
            win_len = atoi(optarg);
            break;
        case 's':
            win_slide = atoi(optarg);
            break;
        default:
        {
            cout << argv[0] << " -y SharedDb(0 false 1 true) -x Size Buffer Key -r [0 -> CB_INC_NORMAL , 1-> CB_P_INC, 2->CB_NON_INC_NORMAL, 3->CB_P_NON_INC, 4 -> TB_INC_NORMAL , 5-> TB_P_INC, 6->TB_NONINC_NORMAL, 7->TB_P_NONINC] -l [N MemTable] -k [n_keys] -m [MemTable Size] -p [Parallelism of each operator replica] -w [Window length in number of tuples or microseconds if TB] -s [Window slide]" << endl;
            exit(EXIT_SUCCESS);
        }
        }
    }
    auto tuple_serializer = [](tuple_t &t) -> std::string
    {
        std::string x = std::to_string(t.key) + "," + std::to_string(t.value);
        return x;
    };
    auto tuple_deserializer = [](std::string &s) -> tuple_t
    {
        tuple_t t;
        t.key = atoll(s.substr(0, s.find(",")).c_str());
        t.value = atoll(s.substr(s.find(",") + 1, s.length() - 1).c_str());
        return t;
    };
    /*
    auto tuple_serializer = [](tuple_t &t) -> std::string
    {
        std::string x = std::to_string(t.key) + "," + std::to_string(t.value) + "&" + std::to_string(t.timestamp) + "%";
        for (auto &v : t.ts)
        {
            x = x + std::to_string(v) + "(";
        }
        return x;
    };
    auto tuple_deserializer = [](std::string &s) -> tuple_t
    {
        tuple_t t;
        t.key = atoll(s.substr(0, s.find(",")).c_str());
        t.value = atoll(s.substr(s.find(",") + 1, s.find("&")).c_str());
        t.timestamp = atoll(s.substr(s.find("&") + 1, s.find("%")).c_str());
        std::string ts = s.substr(s.find("%") + 1, s.length() - 1);
        size_t pos = 0;
        std::string token;
        size_t wrap_len = std::string("(").length();
        while ((pos = ts.find("(")) != std::string::npos)
        {
            token = ts.substr(0, pos);
            size_t new_wrap = std::stoul(token);
            t.ts.push_back(new_wrap);
            ts.erase(0, pos + wrap_len);
        }
        return t;
    };
    */
    unsigned long app_start_time = current_time_nsecs();
    std::string RR = "X" + std::to_string(parallelism) + std::to_string(runs) + std::to_string(n_keys);
    PipeGraph graph("WindowTest", Execution_Mode_t::DEFAULT, Time_Policy_t::EVENT_TIME);

    Source_Functor source_functor(app_start_time, 16, n_keys);
    Source source = Source_Builder(source_functor)
                        .withName("source")
                        .withParallelism(parallelism)
                        .build();
    MultiPipe &mp = graph.add_source(source);

    Win_Functor_NINC ninc_win_functor;
    Win_Functor_INC inc_win_functor;
    bool real_shared = shared == 0 ? false : true;
    size_t total_memt = real_shared ? n_memtables * parallelism : n_memtables;
    rocksdb::Options _myopt;
    DBOptions::set_default_db_options(_myopt);
    _myopt.write_buffer_size = size_memtables * 1024 * 1024;
    _myopt.max_write_buffer_number = total_memt + 1;
    if (runs == 0)
    {
        Keyed_Windows kwins = Keyed_Windows_Builder(inc_win_functor)
                                  .withName("CB_INC_NORMAL")
                                  .withParallelism(parallelism)
                                  .withKeyBy([](const tuple_t &t) -> size_t
                                             { return t.key; })
                                  .withCBWindows(win_len, win_slide)
                                  .build();
        mp.add(kwins);
    }
    if (runs == 1)
    {
        auto kwins = P_Keyed_Windows_Builder(inc_win_functor)
                                    .withName("CB_P_INC" + RR)
                                    .withParallelism(parallelism)
                                    .withSharedDb(real_shared)
                                    .withKeyBy([](const tuple_t &t) -> size_t
                                               { return t.key; })
                                    .withCBWindows(win_len, win_slide)
                                    .withResultSerializerAndDeserializer(tuple_serializer, tuple_deserializer)
                                    .withOptions(_myopt)
                                    .setFragmentSize(key_buff)
                                    .build();
        mp.add(kwins);
    }
    if (runs == 2)
    {
        Keyed_Windows kwins = Keyed_Windows_Builder(ninc_win_functor)
                                  .withName("CB_NON_INC_NORMAL")
                                  .withParallelism(parallelism)
                                  .withKeyBy([](const tuple_t &t) -> size_t
                                             { return t.key; })
                                  .withCBWindows(win_len, win_slide)
                                  .build();
        mp.add(kwins);
    }
    if (runs == 3)
    {
        P_Keyed_Windows kwins = P_Keyed_Windows_Builder(ninc_win_functor)
                                    .withName("CB_P_NON_INC" + RR)
                                    .withParallelism(parallelism)
                                    .withSharedDb(real_shared)
                                    .withKeyBy([](const tuple_t &t) -> size_t
                                               { return t.key; })
                                    .withCBWindows(win_len, win_slide)
                                    .withOptions(_myopt)
                                    .setFragmentSize(key_buff * sizeof(tuple_t))
                                    .withTupleSerializerAndDeserializer(tuple_serializer, tuple_deserializer)
                                    .build();
        mp.add(kwins);
    }
    if (runs == 4)
    {
        Keyed_Windows kwins = Keyed_Windows_Builder(inc_win_functor)
                                  .withName("TB_INC_NORMAL2MEM")
                                  .withParallelism(parallelism)
                                  .withKeyBy([](const tuple_t &t) -> size_t
                                             { return t.key; })
                                  .withTBWindows(microseconds(win_len), microseconds(win_slide))
                                  .build();
        mp.add(kwins);
    }
    if (runs == 5)
    {
        P_Keyed_Windows kwins = P_Keyed_Windows_Builder(inc_win_functor)
                                    .withName("TB_P_INC" + RR)
                                    .withParallelism(parallelism)
                                    .withSharedDb(real_shared)
                                    .withKeyBy([](const tuple_t &t) -> size_t
                                               { return t.key; })
                                    .withTBWindows(microseconds(win_len), microseconds(win_slide))
                                    .withOptions(_myopt)
                                    .setFragmentSize(key_buff)
                                    .withResultSerializerAndDeserializer(tuple_serializer, tuple_deserializer)
                                    .build();
        mp.add(kwins);
    }
    if (runs == 6)
    {
        Keyed_Windows kwins = Keyed_Windows_Builder(ninc_win_functor)
                                  .withName("TB_NON_INC_NORMAL2MEM")
                                  .withParallelism(parallelism)
                                  .withKeyBy([](const tuple_t &t) -> size_t
                                             { return t.key; })
                                  .withTBWindows(microseconds(win_len), microseconds(win_slide))
                                  .build();
        mp.add(kwins);
    }
    if (runs == 7)
    {
        P_Keyed_Windows kwins = P_Keyed_Windows_Builder(ninc_win_functor)
                                    .withName("TB_P_NONINC" + RR)
                                    .withParallelism(parallelism)
                                    .withSharedDb(real_shared)
                                    .withKeyBy([](const tuple_t &t) -> size_t
                                               { return t.key; })
                                    .withTBWindows(microseconds(win_len), microseconds(win_slide))
                                    .withOptions(_myopt)
                                    .setFragmentSize(key_buff)
                                    .withTupleSerializerAndDeserializer(tuple_serializer, tuple_deserializer)
                                    .build();
        mp.add(kwins);
    }

    Filter_Functor filter_functor(app_start_time);
    Filter filter = Filter_Builder(filter_functor)
                        .withName("filter")
                        .withParallelism(parallelism)
                        .build();
    mp.add(filter);

    WinSink_Functor sink_functor(100, app_start_time);
    Sink sink = Sink_Builder(sink_functor)
                    .withName("sink")
                    .withParallelism(parallelism)
                    .build();
    mp.add_sink(sink);

    cout << "Executing topology" << endl;
    volatile unsigned long start_time_main_usecs = current_time_usecs();
    graph.run();
    volatile unsigned long end_time_main_usecs = current_time_usecs();
    cout << "Exiting" << endl;
    double elapsed_time_seconds = (end_time_main_usecs - start_time_main_usecs) / (1000000.0);
    double throughput = sent_tuples / elapsed_time_seconds;
    cout << "Measured throughput: " << (size_t)throughput << " tuples/second" << endl;
    cout << "Dumping metrics" << endl;
    util::metric_group.dump_all();
    return 0;
}