/* how to compile: 
    g++ -std=c++17 -g test_1.cpp -o test_1 -I${WINDFLOW_INCLUDE_PATH} -I${FASTFLOW_INCLUDE_PATH} -lrocksdb -O3 
*/

#include <windflow.hpp>
#include <persistent/windflow_rocksdb.hpp>
#include "../rocksdb_common.hpp"

// global variable for the result
extern atomic<long> global_sum;

int main(void)
{
    /* parameters (static for now) */
    size_t stream_len = 100;
    size_t win_len = 10;
    size_t win_slide = 1;
    size_t n_keys = 2;
    size_t source_degree = 1;
    size_t kw_degree = 1;
    size_t sink_degree = 1;
    size_t output_batch = 0;

    // initialize global variable
    global_sum = 0;

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
    PipeGraph graph("test_rocksdb", Execution_Mode_t::DEFAULT, Time_Policy_t::EVENT_TIME);
    Source_Functor_Overlapped source_functor(stream_len, n_keys, true);
    Source source = Source_Builder(source_functor)
                        .withName("source")
                        .withParallelism(source_degree)
                        .withOutputBatchSize(output_batch)
                        .build();
    MultiPipe &mp = graph.add_source(source);

#if true
    Win_Functor_NINC win_functor;
    P_Keyed_Windows kwins = P_Keyed_Windows_Builder(win_functor)
                                    .withName("p_keyed_wins")
                                    .withWindowSorting(true)
                                    .withParallelism(kw_degree)
                                    .withKeyBy([](const tuple_t &t) -> size_t { return t.key; })
                                    .withTBWindows(std::chrono::microseconds(win_len), std::chrono::microseconds(win_slide))
                                    // .withCBWindows(win_len, win_slide)
                                    .withTupleSerializerAndDeserializer(tuple_serializer, tuple_deserializer)
                                    .withResultSerializerAndDeserializer(result_serializer, result_deserializer)
                                    .setFragSizeBytes(100)
                                    .build();
#else
    Win_Functor_INC win_functor;
    P_Keyed_Windows kwins = P_Keyed_Windows_Builder(win_functor)
                                .withName("p_keyed_wins")
                                .withWindowSorting(true)
                                .withParallelism(kw_degree)
                                .withKeyBy([](const tuple_t &t) -> size_t { return t.key; })
                                // .withTBWindows(std::chrono::microseconds(win_len), std::chrono::microseconds(win_slide))
                                .withCBWindows(win_len, win_slide)
                                .withResultSerializerAndDeserializer(result_serializer, result_deserializer)
                                .build();
#endif
    mp.add(kwins);
    WinSink_Functor sink_functor;
    Sink sink = Sink_Builder(sink_functor)
                    .withName("sink")
                    .withParallelism(sink_degree)
                    .build();
    mp.chain_sink(sink);

    // run the application
    graph.run();
    cout << "Result is --> " << GREEN << "OK" << DEFAULT_COLOR << " value " << global_sum.load() << endl;

    return EXIT_SUCCESS;
}