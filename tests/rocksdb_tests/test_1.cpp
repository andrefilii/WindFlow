/* how to compile: 
    g++ -std=c++17 -g test_1.cpp -o test_1 -I${WINDFLOW_INCLUDE_PATH} -I${FASTFLOW_INCLUDE_PATH} -lrocksdb -O3 
*/

#include <windflow.hpp>
#include <persistent/windflow_rocksdb.hpp>
#include "rocksdb_common.hpp"

#include <getopt.h>

// global variable for the result
extern atomic<long> global_sum;

int main(int argc, char *argv[])
{
    int option = 0;
    struct option long_options[] = {
        {"cb", no_argument, 0, 0},  // Flag per --cb
        {"tb", no_argument, 0, 0},  // Flag per --tb
        {0, 0, 0, 0}  // Terminatore della lista
    };
    int option_index = 0;
    /* parameters */
    bool tb_win = true;
    size_t stream_len = 10000;
    size_t win_len = 1000;
    size_t win_slide = 1000;
    size_t n_keys = 1;
    size_t op_degree = 1;
    size_t output_batch = 0;

    // initialize global variable
    global_sum = 0;

    while ((option = getopt_long(argc, argv, "l:k:w:s:n:", long_options, &option_index)) != -1) {
        switch (option) {
            case 'l': stream_len = atoi(optarg);
            break;
            case 'k': n_keys = atoi(optarg);
            break;
            case 'w': win_len = atoi(optarg);
            break;
            case 's': win_slide = atoi(optarg);
            break;
            case 'n': op_degree = atoi(optarg);
            break;
            case 0:
                if (std::string(long_options[option_index].name) == "cb") {
                    tb_win = false;
                } else if (std::string(long_options[option_index].name) == "tb") {
                    tb_win = true;
                }
            break;
            default: {
                cout << argv[0] << " -l [stream_length] -k [n_keys] -w [win length] -s [win slide]" << endl;
                exit(EXIT_SUCCESS);
            }
        }
    }

    /* serializers and deserializers*/
    auto tuple_serializer = [](tuple_t &t) -> std::string {
        return std::to_string(t.key) + "," + std::to_string(t.value);
    };
    auto tuple_deserializer = [](std::string &s) -> tuple_t {
        tuple_t t;
        t.key = atoi(s.substr(0, s.find(",")).c_str());
        t.value = atoi(s.substr(s.find(",")+1, s.length()-1).c_str());
        return t;
    };
    auto result_serializer = [](result_t &r) -> std::string {
        return std::to_string(r.key) + "," + std::to_string(r.value) + ";" + std::to_string(r.wid);
    };
    auto result_deserializer = [](std::string &s) -> result_t {
        result_t r;
        r.key = atoi(s.substr(0, s.find(",")).c_str());
        r.value = atoi(s.substr(s.find(",")+1, s.find(";")).c_str());
        r.wid = atoi(s.substr(s.find(";")+1, s.length()-1).c_str());
        return r;
    };

    // preparation of graph
    PipeGraph graph("test_rocksdb", Execution_Mode_t::DEFAULT, (tb_win ? Time_Policy_t::EVENT_TIME : Time_Policy_t::INGRESS_TIME));
    Source_Functor_2 source_functor(stream_len, n_keys, tb_win);
    Source source = Source_Builder(source_functor)
                        .withName("source")
                        .withParallelism(op_degree)
                        .withOutputBatchSize(output_batch)
                        .build();
    MultiPipe &mp = graph.add_source(source);

    Win_Functor_NINC win_functor;
    auto builder = P_Keyed_Windows_Builder(win_functor)
                                    .withName("p_keyed_wins")
                                    .withWindowSorting(true)
                                    .withParallelism(op_degree)
                                    .withKeyBy([](const tuple_t &t) -> size_t { return t.key; })
                                    .withTupleSerializerAndDeserializer(tuple_serializer, tuple_deserializer)
                                    .withResultSerializerAndDeserializer(result_serializer, result_deserializer)
                                    .setFragSizeBytes(100);

    if (tb_win) builder = builder.withTBWindows(std::chrono::microseconds(win_len), std::chrono::microseconds(win_slide));
    else builder = builder.withCBWindows(win_len, win_slide);

    auto kwin = builder.build();
    mp.add(kwin);
    WinSink_Functor sink_functor;
    Sink sink = Sink_Builder(sink_functor)
                    .withName("sink")
                    .withParallelism(op_degree)
                    .build();
    mp.chain_sink(sink);

    // run the application
    graph.run();
    cout << "Result is --> " << GREEN << "OK" << DEFAULT_COLOR << " value " << global_sum.load() << endl;

    return EXIT_SUCCESS;
}