/******************************************************************************
 *  This program is free software; you can redistribute it and/or modify it
 *  under the terms of the GNU Lesser General Public License version 3 as
 *  published by the Free Software Foundation.
 *  
 *  This program is distributed in the hope that it will be useful, but WITHOUT
 *  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 *  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
 *  License for more details.
 *  
 *  You should have received a copy of the GNU Lesser General Public License
 *  along with this program; if not, write to the Free Software Foundation,
 *  Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 ******************************************************************************
 */

/*  
 *  Test 5 of merge between MultiPipes with both CPU and GPU operators. Version
 *  with keyby distributions.
 *  
 *  +---------------------------------+
 *  |  +-----+    +-----+    +-----+  |
 *  |  |  S  |    |  M  |    |  M  |  |
 *  |  | CPU +--->+ CPU +--->+ GPU |  +---+
 *  |  | (*) |    | (*) |    | (*) |  |   |      +----------------------+
 *  |  +-----+    +-----+    +-----+  |   |      |  +-----+    +-----+  |
 *  +---------------------------------+   |      |  |  M  |    |  S  |  |
 *                                        +----->+  | CPU +--->+ CPU |  |
 *  +---------------------------------+   |      |  | (*) |    | (*) |  |
 *  |  +-----+    +-----+    +-----+  |   |      |  +-----+    +-----+  |
 *  |  |  S  |    |  M  |    |  M  |  |   |      +----------------------+
 *  |  | CPU +--->+ CPU +--->+ CPU |  +---+
 *  |  | (*) |    | (*) |    | (*) |  |
 *  |  +-----+    +-----+    +-----+  |
 *  +---------------------------------+
 */ 

// include
#include<random>
#include<iostream>
#include<ff/ff.hpp>
#include<windflow.hpp>
#include<windflow_gpu.hpp>
#include"merge_common_gpu_kb.hpp"

using namespace std;
using namespace wf;

// global variable for the result
extern atomic<long> global_sum;

// main
int main(int argc, char *argv[])
{
    int option = 0;
    size_t runs = 1;
    size_t stream_len = 0;
    // initalize global variable
    global_sum = 0;
    // arguments from command line
    if (argc != 5) {
        cout << argv[0] << " -r [runs] -l [stream_length]" << endl;
        exit(EXIT_SUCCESS);
    }
    while ((option = getopt(argc, argv, "r:l:")) != -1) {
        switch (option) {
            case 'r': runs = atoi(optarg);
                     break;
            case 'l': stream_len = atoi(optarg);
                     break;
            default: {
                cout << argv[0] << " -r [runs] -l [stream_length]" << endl;
                exit(EXIT_SUCCESS);
            }
        }
    }
    // set random seed
    mt19937 rng;
    rng.seed(std::random_device()());
    size_t min = 1;
    size_t max = 4;
    std::uniform_int_distribution<std::mt19937::result_type> dist_p(min, max);
    std::uniform_int_distribution<std::mt19937::result_type> dist_b(100, 200);
    int map1_degree, map2_degree, map3_degree, map4_degree, map5_degree, sink_degree;
    size_t source1_degree = dist_p(rng);
    size_t source2_degree = dist_p(rng);
    long last_result = 0;
    // executes the runs in DEFAULT mode
    for (size_t i=0; i<runs; i++) {
        map1_degree = dist_p(rng);
        map2_degree = dist_p(rng);
        map3_degree = dist_p(rng);
        map4_degree = dist_p(rng);
        map5_degree = dist_p(rng);
        sink_degree = dist_p(rng);
        cout << "Run " << i << endl;
        cout << "+---------------------------------+" << endl;
        cout << "|  +-----+    +-----+    +-----+  |" << endl;
        cout << "|  |  S  |    |  M  |    |  M  |  |" << endl;
        cout << "|  | CPU +--->+ CPU +--->+ GPU |  +---+" << endl;
        cout << "|  | (" << source1_degree << ") |    | (" << map1_degree << ") |    | (" << map2_degree << ") |  |   |      +----------------------+" << endl;
        cout << "|  +-----+    +-----+    +-----+  |   |      |  +-----+    +-----+  |" << endl;
        cout << "+---------------------------------+   |      |  |  M  |    |  S  |  |" << endl;
        cout << "                                      +----->+  | CPU +--->+ CPU |  |" << endl;
        cout << "+---------------------------------+   |      |  | (" << map3_degree << ") |    | (" << sink_degree << ") |  |" << endl;
        cout << "|  +-----+    +-----+    +-----+  |   |      |  +-----+    +-----+  |" << endl;
        cout << "|  |  S  |    |  M  |    |  M  |  |   |      +----------------------+" << endl;
        cout << "|  | CPU +--->+ CPU +--->+ CPU |  +---+" << endl;
        cout << "|  | (" << source2_degree << ") |    | (" << map4_degree << ") |    | (" << map5_degree << ") |  |" << endl;
        cout << "|  +-----+    +-----+    +-----+  |" << endl;
        cout << "+---------------------------------+" << endl;
        // compute the total parallelism degree of the PipeGraph
        size_t check_degree = source1_degree;
        if (source1_degree != map1_degree) {
            check_degree += map1_degree;
        }
        check_degree += map2_degree;
        check_degree += source2_degree;
        if (source2_degree != map4_degree) {
            check_degree += map4_degree;
        }
        if (map4_degree != map5_degree) {
            check_degree += map5_degree;
        }        
        check_degree += map3_degree;
        if (map3_degree != sink_degree) {
            check_degree += sink_degree;
        }
        // prepare the test
        PipeGraph graph("test_merge_gpu_kb_5", Execution_Mode_t::DEFAULT, Time_Policy_t::EVENT_TIME);
        // prepare the first MultiPipe
        Source_Functor source_functor1(stream_len, true);
        Source source1 = Source_Builder(source_functor1)
                            .withName("source1")
                            .withParallelism(source1_degree)
                            .withOutputBatchSize(dist_b(rng))
                            .build();
        MultiPipe &pipe1 = graph.add_source(source1);
        Map_Functor map_functor1;
        Map map1 = Map_Builder(map_functor1)
                        .withName("map1")
                        .withParallelism(map1_degree)
                        .withOutputBatchSize(dist_b(rng))
                        .build();
        pipe1.chain(map1);
        Map_Functor_GPU_KB map_functor_gpu2;
        Map_GPU mapgpu2 = MapGPU_Builder(map_functor_gpu2)
                                .withName("mapgpu2")
                                .withParallelism(map2_degree)
                                .withKeyBy([] __host__ __device__ (const tuple_t &t) -> char { return t.key; })
                                .build();
        pipe1.chain(mapgpu2);
        // prepare the second MultiPipe
        Source_Functor source_functor2(stream_len, true);
        Source source2 = Source_Builder(source_functor2)
                            .withName("source2")
                            .withParallelism(source2_degree)
                            .withOutputBatchSize(dist_b(rng))
                            .build();
        MultiPipe &pipe2 = graph.add_source(source2);
        Map_Functor map_functor4;
        Map map4 = Map_Builder(map_functor4)
                        .withName("map4")
                        .withParallelism(map4_degree)
                        .withOutputBatchSize(dist_b(rng))
                        .build();
        pipe2.chain(map4);
        Map_Functor map_functor5;
        Map map5 = Map_Builder(map_functor5)
                        .withName("map5")
                        .withParallelism(map5_degree)
                        .withOutputBatchSize(dist_b(rng))
                        .build();
        pipe2.chain(map5);
        // prepare the third MultiPipe
        MultiPipe &pipe3 = pipe1.merge(pipe2);
        Map_Functor map_functor3;
        Map map3 = Map_Builder(map_functor3)
                        .withName("map3")
                        .withParallelism(map3_degree)
                        .withOutputBatchSize(dist_b(rng))
                        .build();
        pipe3.chain(map3);
        Sink_Functor sink_functor;
        Sink sink = Sink_Builder(sink_functor)
                        .withName("sink")
                        .withParallelism(sink_degree)
                        .build();
        pipe3.chain_sink(sink);
        assert(graph.getNumThreads() == check_degree);
        // run the application
        graph.run();
        if (i == 0) {
            last_result = global_sum;
            cout << "Result is --> " << GREEN << "OK" << DEFAULT_COLOR << " value " << global_sum.load() << endl;
        }
        else {
            if (last_result == global_sum) {
                cout << "Result is --> " << GREEN << "OK" << DEFAULT_COLOR << " value " << global_sum.load() << endl;
            }
            else {
                cout << "Result is --> " << RED << "FAILED" << DEFAULT_COLOR << " value " << global_sum.load() << endl;
                abort();
            }
        }
        global_sum = 0;
    }
    return 0;
}