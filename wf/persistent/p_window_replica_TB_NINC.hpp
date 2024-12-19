/**************************************************************************************
 *  Copyright (c) 2019- Gabriele Mencagli and Simone Frassinelli
 *  
 *  This file is part of WindFlow.
 *  
 *  WindFlow is free software dual licensed under the GNU LGPL or MIT License.
 *  You can redistribute it and/or modify it under the terms of the
 *    * GNU Lesser General Public License as published by
 *      the Free Software Foundation, either version 3 of the License, or
 *      (at your option) any later version
 *    OR
 *    * MIT License: https://github.com/ParaGroup/WindFlow/blob/master/LICENSE.MIT
 *  
 *  WindFlow is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Lesser General Public License for more details.
 *  You should have received a copy of the GNU Lesser General Public License and
 *  the MIT License along with WindFlow. If not, see <http://www.gnu.org/licenses/>
 *  and <http://opensource.org/licenses/MIT/>.
 **************************************************************************************
 */

/** 
 *  @file    p_window_replica.hpp
 *  @author  Gabriele Mencagli and Simone Frassinelli
 *  
 *  @brief P_Window_Replica is the replica of the P_Keyed_Windows operator
 *  
 *  @section P_Window_Replica (Description)
 *  
 *  This file implements the P_Window_Replica representing the replica of the
 *  P_Keyed_Windows operators, which processes windows with key-based parallelism
 *  keeping information on RocksDB.
 */ 

#ifndef P_WIN_REPLICA_TB_NINC_H
#define P_WIN_REPLICA_TB_NINC_H

// includes
#include<map>
#include<list>
#include<cmath>
#include<deque>
#include<regex>
#include<vector>
#include<string>
#include<cstddef>
#include<functional>
#include<unordered_map>
#include<string.h>
#include<context.hpp>
#include<batch_t.hpp>
#include<single_t.hpp>
#if defined(WF_TRACING_ENABLED)
    #include<stats_record.hpp>
#endif
#include<basic_emitter.hpp>
#include<basic_operator.hpp>
#include<persistent/db_handle.hpp>
#include<persistent/p_window_structure_TB_NINC.hpp>

namespace wf {

// class P_Window_Replica
template<typename win_func_t, typename keyextr_func_t>
class P_Window_Replica_TB_NINC: public Basic_Replica
{
private:
    template<typename T1, typename T2> friend class P_Keyed_Windows;
    win_func_t func; // functional logic used by the P_Window_Replica
    keyextr_func_t key_extr; // logic to extract the key attribute from the tuple_t
    using tuple_t = decltype(get_tuple_t_Win(func)); // extracting the tuple_t type and checking the admissible signatures
    using result_t = decltype(get_result_t_Win(func)); // extracting the result_t type and checking the admissible signatures
    using key_t = decltype(get_key_t_KeyExtr(key_extr)); // extracting the key_t type and checking the admissible singatures
    // static predicates to check the type of the functional logic to be invoked
    static constexpr bool isNonIncNonRiched = std::is_invocable<decltype(func), const Iterable<tuple_t> &, result_t &>::value;
    static constexpr bool isNonIncRiched = std::is_invocable<decltype(func), const Iterable<tuple_t> &, result_t &, RuntimeContext &>::value;
    static constexpr bool isIncNonRiched = std::is_invocable<decltype(func), const tuple_t &, result_t &>::value;
    static constexpr bool isIncRiched = std::is_invocable<decltype(func), const tuple_t &, result_t &, RuntimeContext &>::value;
    // check the presence of a valid functional logic
    static_assert(isNonIncNonRiched || isNonIncRiched || isIncNonRiched || isIncRiched,
                  "WindFlow Compilation Error - P_Window_Replica_TB_NINC does not have a valid functional logic:\n");
    // this version of the replica is only for time-base non incremental version

    using wrapper_t = wrapper_tuple_t<tuple_t>; // alias for the wrapped tuple type
    using input_iterator_t = typename std::deque<wrapper_t>::iterator; // iterator type for accessing wrapped tuples in the archive
    using win_t = P_Window_TB_NINC<tuple_t, result_t>; // window type used by the P_Window_Replica
    using compare_func_t = std::function<bool(const wrapper_t &, const wrapper_t &)>; // function type to compare two wrapped tuples
    using index_t = decltype(wrapper_t::index); // type of the index field
    using compare_func_index_t = std::function<bool(const index_t &, const index_t &)>; // function type to compare two indexes
    using meta_frag_t = std::tuple<index_t, index_t, size_t>; // tuple type for fragment metadata (min, max, id)
    size_t n_max_elements; // max capacity of volatile buffers representing fragments
    DBHandle<tuple_t> *mydb_wrappers; // pointer to the DBHandle object used to interact with RocksDB
    DBHandle<result_t> *mydb_results; // pointer to the DBHandle object used to interact with RocksDB

    std::map<uint64_t, win_t> wins; // open windows
    std::map<uint64_t, std::deque<wrapper_t>> buffer_map; // open window buffers
    uint64_t next_lwid = 0; // next window to be opened of this key (lwid)
    int64_t last_lwid = -1; // last window closed of this key (lwid)

    bool sort_enabled;
    std::set<key_t> seen_keys;

    compare_func_t compare_func = [](const wrapper_t &w1, const wrapper_t &w2) { return w1.index < w2.index; }; // function to compare two wrapped tuples
    compare_func_index_t geqt = [](const index_t &w1, const index_t &w2) { return w1 >= w2; }; // geq function between indexes
    compare_func_index_t leqt = [](const index_t &w1, const index_t &w2) { return w1 <= w2; }; // leq function between indexes
    compare_func_index_t compare_func_index = [](const index_t &w1, const index_t &w2) { return w1 < w2; }; // compare function between indexes
    uint64_t win_len; // window length (in no. of tuples or in time units)
    uint64_t slide_len; // slide length (in no. of tuples or in time units)
    uint64_t lateness; // triggering delay in time units (meaningful for TB windows in DEFAULT mode)
    Win_Type_t winType; // window type (CB or TB)
    size_t ignored_tuples; // number of ignored tuples
    uint64_t last_time; // last received timestamp or watermark

public:
    //method to get the windows of the tuple based on the timestamp
    std::vector<uint64_t> get_tuple_windows(wrapper_t wt)
    {
        std::vector<uint64_t> result;

        uint64_t ts = wt.index;

        // the start of the last window that contains the tuple
        uint64_t start = (ts / slide_len) * slide_len;

        // add all windows of the tuple
        while (true)
        {
            uint64_t end = start + (win_len-1);
            if (ts <= end)
            {
                uint64_t lwid = (start / slide_len);
                result.push_back(lwid);
            } 
            else break;

            if (start == 0) break;

            start -= slide_len;
        }

        return result;
    }

    // method to insert a new tuple in the in-memory buffer
    void insert(wrapper_t &&_wt)
    {
        auto windows = get_tuple_windows(_wt);
        for (const auto &lwid : windows)
        {
            auto &buffer = buffer_map[lwid];
            if (buffer.size() + 1 > n_max_elements)
            {
                mydb_wrappers->merge(buffer, lwid);
                buffer.clear();
            }
            buffer.push_back(std::move(_wt));
        }
    }

    // method to insert a new tuple in the in-memory buffer
    void insert(const wrapper_t &_wt)
    {
        auto windows = get_tuple_windows(_wt);
        for (const auto &lwid : windows)
        {
            auto &buffer = buffer_map[lwid];
            if (buffer.size() + 1 > n_max_elements)
            {
                mydb_wrappers->merge(buffer, lwid);
                buffer.clear();
            }
            buffer.push_back(_wt);
        }
    }

    // method to purge all tuples of a window
    void purge(const uint64_t &_lwid)
    {
        buffer_map.erase(_lwid);
        mydb_wrappers->delete_window(_lwid);
    }

    // method to get tuples of a window
    std::deque<wrapper_t> get_window(const uint64_t &_lwid)
    {
        std::deque<wrapper_t> final_range;
        auto it = buffer_map.find(_lwid);
        if (it != buffer_map.end() && !it->second.empty())
        {
            final_range.insert(final_range.end(), it->second.begin(), it->second.end());
        }

        auto to_push = mydb_wrappers->get_window(_lwid);
        final_range.insert(final_range.end(), std::make_move_iterator(to_push.begin()), std::make_move_iterator(to_push.end()));
        
        std::sort(final_range.begin(), final_range.end(), [this](const wrapper_t &w1, const wrapper_t &w2){
            key_t k1 = this->key_extr(w1.tuple);
            key_t k2 = this->key_extr(w2.tuple);
            if (k1 == k2)
            {
                // TODO if(sort_enabled){compare}else{return false}
                return compare_func(w1, w2);
            }
            return k1 < k2;
        }); // sorting the archive before passing to the user function (NIC)

        return final_range;
    }

    // getEnd method
    input_iterator_t getEnd(const uint64_t &_lwid)
    {
        auto it = buffer_map.find(_lwid);
        if (it != buffer_map.end())
        {
            // buffer exists, return the end
            return it->second.end();
        }
        std::deque<wrapper_t> temp;
        return temp.end();
    }

    // Constructor
    P_Window_Replica_TB_NINC(win_func_t _func,
                     keyextr_func_t _key_extr,
                     std::string _opName,
                     std::string _dbpath,
                     RuntimeContext _context,
                     std::function<void(RuntimeContext &)> _closing_func,
                     std::function<std::string(tuple_t &)> _tuple_serialize,
                     std::function<tuple_t(std::string &)> _tuple_deserialize,
                     std::function<std::string(result_t &)> _result_serialize,
                     std::function<result_t(std::string &)> _result_deserialize,
                     bool _deleteDb,
                     bool _sharedDb,
                     size_t _whoami,
                     size_t _buffer_size,
                     uint64_t _win_len,
                     uint64_t _slide_len,
                     uint64_t _lateness,
                     Win_Type_t _winType,
                     bool _sort_enabled):
                     Basic_Replica(_opName, _context, _closing_func, true),
                     func(_func),
                     key_extr(_key_extr),
                     n_max_elements(_buffer_size),
                     win_len(_win_len),
                     slide_len(_slide_len),
                     lateness(_lateness),
                     winType(_winType),
                     ignored_tuples(0),
                     last_time(0),
                     sort_enabled(_sort_enabled)
    {
        if ( !((isNonIncRiched || isNonIncNonRiched) && winType == Win_Type_t::TB) )
        {
            std::cerr << RED << "WindFlow Error: P_Window_Replica_TB_NINC works only with a non-incremental time-based logic" << DEFAULT_COLOR << std::endl;
            exit(EXIT_FAILURE);
        }

        _dbpath = _sharedDb ? _dbpath + "_shared" : _dbpath;
        mydb_wrappers = new DBHandle<tuple_t>(_tuple_serialize,
                                                _tuple_deserialize,
                                                _deleteDb,
                                                _dbpath + "_windows",
                                                tuple_t{},
                                                _whoami);
        mydb_results = nullptr;
    }

    // Copy Constructor
    P_Window_Replica_TB_NINC(const P_Window_Replica_TB_NINC &_other):
                     Basic_Replica(_other),
                     func(_other.func),
                     key_extr(_other.key_extr),
                     n_max_elements(_other.n_max_elements),     
                     compare_func(_other.compare_func),
                     geqt(_other.geqt),
                     leqt(_other.leqt),
                     compare_func_index(_other.compare_func_index),
                     win_len(_other.win_len),
                     slide_len(_other.slide_len),
                     lateness(_other.lateness),
                     winType(_other.winType),                     
                     ignored_tuples(_other.ignored_tuples),
                     last_time(_other.last_time)
    {
        if (_other.mydb_wrappers != nullptr) {
            mydb_wrappers = (_other.mydb_wrappers)->getCopy();
        }
        else {
            mydb_wrappers = nullptr;
        }
        if (_other.mydb_results != nullptr) {
            mydb_results = (_other.mydb_results)->getCopy();
        }
        else {
            mydb_results = nullptr;
        }
    }

    // Destructor
    ~P_Window_Replica_TB_NINC()
    {
        if (mydb_wrappers != nullptr) {
            delete mydb_wrappers;
        }
        if (mydb_results != nullptr) {
            delete mydb_results;
        }
    }

    // svc (utilized by the FastFlow runtime)
    void *svc(void *_in) override
    {
        this->startStatsRecording();
        if (this->input_batching) { // receiving a batch
            Batch_t<tuple_t> *batch_input = reinterpret_cast<Batch_t<tuple_t> *>(_in);
            if (batch_input->isPunct()) { // if it is a punctuaton
                (this->emitter)->propagate_punctuation(batch_input->getWatermark((this->context).getReplicaIndex()), this); // propagate the received punctuation
                assert(last_time <= batch_input->getWatermark((this->context).getReplicaIndex())); // sanity check
                last_time = batch_input->getWatermark((this->context).getReplicaIndex());
                deleteBatch_t(batch_input); // delete the punctuation
                return this->GO_ON;
            }
#if defined(WF_TRACING_ENABLED)
            (this->stats_record).inputs_received += batch_input->getSize();
            (this->stats_record).bytes_received += batch_input->getSize() * sizeof(tuple_t);
#endif
            for (size_t i = 0; i < batch_input->getSize(); i++) { // process all the inputs within the received batch
                process_input(batch_input->getTupleAtPos(i), 0, batch_input->getTimestampAtPos(i), batch_input->getWatermark((this->context).getReplicaIndex()));
            }
            deleteBatch_t(batch_input); // delete the input batch
        }
        else { // receiving a single input
            Single_t<tuple_t> *input = reinterpret_cast<Single_t<tuple_t> *>(_in);
            if (input->isPunct()) { // if it is a punctuaton
                (this->emitter)->propagate_punctuation(input->getWatermark((this->context).getReplicaIndex()), this); // propagate the received punctuation
                assert(last_time <= input->getWatermark((this->context).getReplicaIndex())); // sanity check
                last_time = input->getWatermark((this->context).getReplicaIndex());
                deleteSingle_t(input); // delete the punctuation
                return this->GO_ON;
            }
#if defined(WF_TRACING_ENABLED)
            (this->stats_record).inputs_received++;
            (this->stats_record).bytes_received += sizeof(tuple_t);
#endif
            process_input(input->tuple, 0, input->getTimestamp(), input->getWatermark((this->context).getReplicaIndex()));
            deleteSingle_t(input); // delete the input Single_t
        }
        this->endStatsRecording();
        return this->GO_ON;
    }

    // Process a single input
    void process_input(tuple_t &_tuple,
                       uint64_t _identifier,
                       uint64_t _timestamp,
                       uint64_t _watermark)
    {
#ifdef DEBUG_MODE
        std::cout << "PW::process_input CALLED idx:" << _timestamp << " wm:" << _watermark << std::endl;
#endif
        if (this->execution_mode == Execution_Mode_t::DEFAULT) {
            assert(last_time <= _watermark); // sanity check
            last_time = _watermark;
        }
        else { // timestamps are monotonically increasing in DETERMINISTIC and PROBABILISTIC modes
            assert(last_time <= _timestamp); // sanity check
            last_time = _timestamp;
        }
        auto key = key_extr(_tuple); // get the key attribute of the input tuple
        seen_keys.insert(key);

        uint64_t index = _timestamp;
        // gwid of the first window of the key assigned to the replica
        uint64_t first_gwid_key = 0;
        // initial identifer (CB) or timestamp (TB) of the keyed sub-stream arriving at the replica
        uint64_t initial_index = 0;
        uint64_t min_boundary = (last_lwid >= 0) ? win_len + (last_lwid * slide_len) : 0; // if the tuple is related to a closed window -> IGNORED
        if (index < initial_index + min_boundary) {
            if (last_lwid >= 0) {
#if defined(WF_TRACING_ENABLED)
                stats_record.inputs_ignored++;
#endif
                ignored_tuples++;
            }
            return;
        }
        long last_w = -1; // determine the lwid of the last window containing t
        if (win_len >= slide_len) { // sliding or tumbling windows
            last_w = ceil(((double)index + 1 - initial_index) / ((double)slide_len)) - 1;
        }
        else { // hopping windows
            uint64_t n = floor((double)(index - initial_index) / slide_len);
            last_w = n;
        }

        for (long lwid = next_lwid; lwid <= last_w; lwid++) { // create all the new opened windows
            uint64_t gwid = first_gwid_key + lwid; // translate lwid -> gwid
            wins.insert({lwid, win_t(lwid, gwid, Triggerer_TB(win_len, slide_len, lwid, initial_index), win_len, slide_len)});
            next_lwid++;
        }
        size_t cnt_fired = 0;
        insert(wrapper_t(_tuple, index)); // insert the wrapped tuple in the archive of the key (non-incremental processing only)

        std::vector<uint64_t> wins_to_delete;
        for (auto &pair: wins) { // evaluate all the open windows
            auto &win = pair.second;

            uint64_t lwid = win.getLWID(); // local id of window to calculate boundaries
            win_event_t event = win.onTuple(_tuple, index, _timestamp); // get the event
            if (event == win_event_t::FIRED) { // window is fired
#ifdef DEBUG_MODE
        std::cout << "PW::process_input IS FIRED lwid:" << lwid << " res_ts:" << win.getResultTimestamp() << " lateness:" << lateness << " wm:" << _watermark << std::endl;
#endif
                if ((this->execution_mode != Execution_Mode_t::DEFAULT) || (win.getResultTimestamp() + lateness < _watermark)) {
                    // per l'invio dei risultati
                    uint64_t used_ts = (this->execution_mode != Execution_Mode_t::DEFAULT) ? _timestamp : _watermark;
                    uint64_t used_wm = (this->execution_mode != Execution_Mode_t::DEFAULT) ? 0 : _watermark;

                    bool isEmpty = win.getSize() <= 0; // if win is empty i just return an empty iterator
#ifdef DEBUG_MODE
                    std::cout << "PW::process_input FIRED lwid:" << lwid << " isEmpty:"<< isEmpty << std::endl;
#endif
                    if (!isEmpty) { // non empty window
                        std::set<key_t> window_keys;
                        auto window = get_window(lwid);
#ifdef DEBUG_MODE
                    std::cout << "PW::process_input WINDOW LOADED:" << std::endl;
                    for (auto &t : window)
                    {
                        std::cout << "\t{key: " << key_extr(t.tuple) << ", val: " << t.tuple.value << "}" << std::endl;
                    }
#endif
                        auto group_start = window.begin();
                        while (group_start != window.end())
                        {
                            key_t group_key = key_extr(group_start->tuple);

                            // fine del gruppo con chiave group_key
                            auto group_end = std::find_if(group_start, window.end(), [this, &group_key](const wrapper_t &w) { 
                                key_t key = this->key_extr(w.tuple);
                                return key != group_key; 
                            });

                            if (group_start != group_end)
                            {
                                window_keys.insert(group_key);

                                Iterable<tuple_t> iter(group_start, group_end);
                                result_t res = create_win_result_t<result_t, key_t>(group_key, win.getGWID());
                                if constexpr (isNonIncNonRiched) { // non-riched
                                    func(iter, res);
                                }
                                if constexpr (isNonIncRiched) { // riched
                                    func(iter, res, this->context);
                                }
                                this->doEmit(this->emitter, &(res), 0, used_ts, used_wm, this);
                            }

                            group_start = group_end;
                        }

                        // differenza tra chiavi della replica e chiavi con dati, per inviare iteratori vuoti
                        std::set<key_t> difference;
                        std::set_difference(seen_keys.begin(), seen_keys.end(),
                                            window_keys.begin(), window_keys.end(),
                                            std::inserter(difference, difference.begin()));
                        for (const auto &key : difference)
                        {
                            Iterable<tuple_t> empty_it(getEnd(lwid), getEnd(lwid));
                            result_t res = create_win_result_t<result_t, key_t>(key, win.getGWID());
                            if constexpr (isNonIncNonRiched) { // non-riched
                                func(empty_it, res);
                            }
                            if constexpr (isNonIncRiched) { // riched
                                func(empty_it, res, this->context);
                            }

                            this->doEmit(this->emitter, &(res), 0, used_ts, used_wm, this);
                        }

                        purge(lwid);
                    } else {
                        // finestra vuota, invio iteratori vuoti a tutte le chiavi della replica
                        for (const auto &key : seen_keys)
                        {
                            Iterable<tuple_t> empty_it(getEnd(lwid), getEnd(lwid));
                            result_t res = create_win_result_t<result_t, key_t>(key, win.getGWID());
                            if constexpr (isNonIncNonRiched) { // non-riched
                                func(empty_it, res);
                            }
                            if constexpr (isNonIncRiched) { // riched
                                func(empty_it, res, this->context);
                            }

                            this->doEmit(this->emitter, &(res), 0, used_ts, used_wm, this);
                        }
                    }
                    
                    cnt_fired++;
                    last_lwid++;
#if defined(WF_TRACING_ENABLED)
                    (this->stats_record).outputs_sent++;
                    (this->stats_record).bytes_sent += sizeof(result_t);
#endif
                    wins_to_delete.push_back(pair.first);
                }
            }
        }

        // elimino le finestre scattate
        for (auto &key : wins_to_delete)
        {
            wins.erase(key);
        }
    }

    // method to manage the EOS (utilized by the FastFlow runtime)
    void eosnotify(ssize_t id) override
    {
        for (auto &pair: wins) { // evaluate all the open windows
            auto &win = pair.second;

            uint64_t used_wm = (this->execution_mode != Execution_Mode_t::DEFAULT) ? 0 : last_time;

            uint64_t lwid = win.getLWID(); // local id of window to calculate boundaries
            bool isEmpty = win.getSize() <= 0; // if win is empty i just return an empty iterator
#ifdef DEBUG_MODE
                    std::cout << "PW::process_input FIRED lwid:" << lwid << " isEmpty:"<< isEmpty << std::endl;
#endif
            if (!isEmpty) { // non empty window
                std::set<key_t> window_keys;
                auto window = get_window(lwid);
                auto group_start = window.begin();
                while (group_start != window.end())
                {
                    key_t group_key = key_extr(group_start->tuple);

                    // fine del gruppo con chiave group_key
                    auto group_end = std::find_if(group_start, window.end(), [this, &group_key](const wrapper_t &w) { 
                        key_t key = this->key_extr(w.tuple);
                        return key != group_key; 
                    });

                    if (group_start != group_end)
                    {
                        window_keys.insert(group_key);

                        Iterable<tuple_t> iter(group_start, group_end);
                        result_t res = create_win_result_t<result_t, key_t>(group_key, win.getGWID());
                        if constexpr (isNonIncNonRiched) { // non-riched
                            func(iter, res);
                        }
                        if constexpr (isNonIncRiched) { // riched
                            func(iter, res, this->context);
                        }
                        this->doEmit(this->emitter, &(res), 0, last_time, used_wm, this);
                    }

                    group_start = group_end;
                }

                // differenza tra chiavi della replica e chiavi con dati, per inviare iteratori vuoti
                std::set<key_t> difference;
                std::set_difference(seen_keys.begin(), seen_keys.end(),
                                    window_keys.begin(), window_keys.end(),
                                    std::inserter(difference, difference.begin()));
                for (const auto &key : difference)
                {
                    Iterable<tuple_t> empty_it(getEnd(lwid), getEnd(lwid));
                    result_t res = create_win_result_t<result_t, key_t>(key, win.getGWID());
                    if constexpr (isNonIncNonRiched) { // non-riched
                        func(empty_it, res);
                    }
                    if constexpr (isNonIncRiched) { // riched
                        func(empty_it, res, this->context);
                    }

                    this->doEmit(this->emitter, &(res), 0, last_time, used_wm, this);
                }

                purge(lwid);
            } else {
                // finestra vuota, invio iteratori vuoti a tutte le chiavi della replica
                for (const auto &key : seen_keys)
                {
                    Iterable<tuple_t> empty_it(getEnd(lwid), getEnd(lwid));
                    result_t res = create_win_result_t<result_t, key_t>(key, win.getGWID());
                    if constexpr (isNonIncNonRiched) { // non-riched
                        func(empty_it, res);
                    }
                    if constexpr (isNonIncRiched) { // riched
                        func(empty_it, res, this->context);
                    }

                    this->doEmit(this->emitter, &(res), 0, last_time, used_wm, this);
                }
            }
        }

        Basic_Replica::eosnotify(id);
    }

    // Get the number of ignored tuples
    size_t getNumIgnoredTuples() const
    {
        return ignored_tuples;
    }

    P_Window_Replica_TB_NINC(P_Window_Replica_TB_NINC &&) = delete; ///< Move constructor is deleted
    P_Window_Replica_TB_NINC &operator=(const P_Window_Replica_TB_NINC &) = delete; ///< Copy assignment operator is deleted
    P_Window_Replica_TB_NINC &operator=(P_Window_Replica_TB_NINC &&) = delete; ///< Move assignment operator is deleted
};

} // namespace wf

#endif
