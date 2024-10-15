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

#ifndef P_WIN_REPLICA_H
#define P_WIN_REPLICA_H

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
#include<persistent/p_window_structure.hpp>


namespace wf {

// class P_Window_Replica
template<typename win_func_t, typename keyextr_func_t>
class P_Window_Replica: public Basic_Replica
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
                  "WindFlow Compilation Error - P_Window_Replica does not have a valid functional logic:\n");
    using wrapper_t = wrapper_tuple_t<tuple_t>; // alias for the wrapped tuple type
    using input_iterator_t = typename std::deque<wrapper_t>::iterator; // iterator type for accessing wrapped tuples in the archive
    using win_t = P_Window<tuple_t, result_t, key_t>; // window type used by the P_Window_Replica
    using compare_func_t = std::function<bool(const wrapper_t &, const wrapper_t &)>; // function type to compare two wrapped tuples
    using index_t = decltype(wrapper_t::index); // type of the index field
    using compare_func_index_t = std::function<bool(const index_t &, const index_t &)>; // function type to compare two indexes
    using meta_frag_t = std::tuple<index_t, index_t, size_t>; // tuple type for fragment metadata (min, max, id)
    size_t n_max_elements; // max capacity of volatile buffers representing fragments
    DBHandle<tuple_t> *mydb_wrappers; // pointer to the DBHandle object used to interact with RocksDB
    DBHandle<result_t> *mydb_results; // pointer to the DBHandle object used to interact with RocksDB

    struct Key_Descriptor // struct of a key descriptor
    {
        std::unordered_map<std::string, std::deque<wrapper_t>> buffer_map; /* FOR WINDOWS SOLUTION */
        std::vector<win_t> wins; // open windows of this key
        std::deque<result_t> res_wins; // results of open windows of this key
        uint64_t next_lwid = 0; // next window to be opened of this key (lwid)
        int64_t last_lwid = -1; // last window closed of this key (lwid)
        uint64_t next_input_id = 0; // identifier of the next tuple of this key
    };

    std::unordered_map<key_t, Key_Descriptor> keyMap; // hashtable mapping keys to Key_Descriptor structures
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
    
    bool sort_enabled = false; // true if the user wants the tuple of a window to be sorted

public:

/* WINDOWS SOLUTION */
    std::string key_db_extr(const uint64_t &lwid, key_t &_my_key)
    {
        return std::to_string(_my_key) + "_" + std::to_string(lwid);
    }


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


    // method to insert a new tuple in the correct window buffer
    // if the tuple is present in different windows, it's duplicated
    void insert(wrapper_t &&_wt,
                Key_Descriptor &_kd,
                key_t &_my_key)
    {
        auto windows = get_tuple_windows(_wt);
#ifdef DEBUG_MODE
        std::cout << "PW::insert CALLED tuple with idx " << _wt.index << " is in " << windows.size() << " windows for key " << _my_key << std::endl;
#endif
        for(auto window : windows)
        {
            std::string key = key_db_extr(window, _my_key);
            
            std::deque<wrapper_t> &buffer = _kd.buffer_map[key];
#ifdef DEBUG_MODE
            std::cout << "PW::insert key->" << key << " buffer_size_BEFORE->" << buffer.size() << std::endl;
#endif
            if (buffer.size() + 1 > n_max_elements) {
#ifdef DEBUG_MODE
                std::cout << "PW::insert FLUSH for key " << key << std::endl;
#endif
                mydb_wrappers->merge(buffer, key);
                buffer.clear();
            }
            buffer.push_back(std::move(_wt));
#ifdef DEBUG_MODE
            std::cout << "PW::insert key->" << key << " buffer_size_AFTER->" << buffer.size() << std::endl;
#endif
        }
    }


    // method to insert a new tuple in the correct window buffer
    void insert(const wrapper_t &_wt,
                Key_Descriptor &_kd,
                key_t &_my_key)
    {
#ifdef DEBUG_MODE
        std::cout << "PW::insert CONST CALLED" << std::endl;
#endif
        auto windows = get_tuple_windows(_wt);

        for(auto window : windows)
        {
            std::string key = key_db_extr(window, _my_key);
            
            std::deque<wrapper_t> &buffer = _kd.buffer_map[key];

            if (buffer.size() + 1 > n_max_elements) {
                mydb_wrappers->merge(buffer, key);
                buffer.clear();
            }
            buffer.push_back(_wt);
        }
    }


    void purge(const uint64_t &_lwid,
               Key_Descriptor &_kd,
               key_t &_my_key)
    {
        // create the key to use to identify the window
        std::string key = key_db_extr(_lwid, _my_key);
        // get the buffer associated with the window
        bool erased = _kd.buffer_map.erase(key) != 0;
        if (erased)
        {
#ifdef DEBUG_MODE
            std::cout << "PW::purge buffer succefully erased for key " << key << std::endl;
#endif
        }

        mydb_wrappers->delete_key(key);
    }


    std::deque<wrapper_t> get_window(const uint64_t &_lwid, Key_Descriptor &_kd, key_t &_my_key)
    {
        // deque for the response
        std::deque<wrapper_t> final_range;

        // create the key to use to identify the window
        std::string key = key_db_extr(_lwid, _my_key);
        // get the buffer associated with the window
        auto it = _kd.buffer_map.find(key);
        if (it != _kd.buffer_map.end() && !it->second.empty())
        {
            // if the buffer exists and contains something add the elements in the response
#ifdef DEBUG_MODE
            std::cout << "PW::get_window BUFFER FOUND for key " << key << std::endl << " with no. tuple " << it->second.size() << std::endl;
#endif
            final_range.insert(final_range.end(), it->second.begin(), it->second.end());
        } else {
#ifdef DEBUG_MODE
            std::cout << "PW::get_window BUFFER NOT FOUND for key " << key << std::endl;
#endif
        }
        // get the window saved on the db and insert the tuples in the response
        std::deque<wrapper_t> to_push = mydb_wrappers->get_window(key);
        final_range.insert(final_range.end(), std::make_move_iterator(to_push.begin()), std::make_move_iterator(to_push.end()));
        if (sort_enabled)
        {
            // if the user wants, the tuple can be sorted
            std::sort(final_range.begin(), final_range.end(), compare_func);
        }
#ifdef DEBUG_MODE
        std::cout << "PW::get_window WINDOW COMPLETED:" << std::endl;
        for (auto x : final_range)
        {
            std::cout << "\t<" << x.index << "," << x.tuple.value << ">" << std::endl;
        }
#endif
        return final_range;
    }

    // getEnd method
    input_iterator_t getEnd(const uint64_t &_lwid,
                            Key_Descriptor &_kd, 
                            key_t &_my_key)
    {
        std::string key = key_db_extr(_lwid, _my_key);

        auto it = _kd.buffer_map.find(key);
        if (it != _kd.buffer_map.end())
        {
            // buffer exists, return the end
            return it->second.end();
        }
        std::deque<wrapper_t> temp;
        return temp.end();
    }

    // Constructor
    P_Window_Replica(win_func_t _func,
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
                     bool _results_in_memory,
                     size_t _buffer_bytes,
                     uint64_t _win_len,
                     uint64_t _slide_len,
                     uint64_t _lateness,
                     Win_Type_t _winType,
                     bool _sort_enabled):
                     Basic_Replica(_opName, _context, _closing_func, true),
                     func(_func),
                     key_extr(_key_extr),
                     results_in_memory(_results_in_memory),
                     n_max_elements(size_t(_buffer_bytes / sizeof(tuple_t))), // <-- Occhio!
                     win_len(_win_len),
                     slide_len(_slide_len),
                     lateness(_lateness),
                     winType(_winType),
                     ignored_tuples(0),
                     last_time(0),
                     sort_enabled(_sort_enabled)
    {
        _dbpath = _sharedDb ? _dbpath + "_shared" : _dbpath;
        if constexpr (isNonIncNonRiched || isNonIncRiched) {
            mydb_wrappers = new DBHandle<tuple_t>(_tuple_serialize,
                                                  _tuple_deserialize,
                                                  _deleteDb,
                                                  _dbpath + "_frag",
                                                  tuple_t{},
                                                  _whoami);
            mydb_results = nullptr;
        }
        else {
            mydb_wrappers = nullptr;
            mydb_results = new DBHandle<result_t>(_result_serialize,
                                                  _result_deserialize,
                                                  _deleteDb,
                                                  _dbpath + "_result",
                                                  result_t{},
                                                  _whoami);
        }
    }

    // Copy Constructor
    P_Window_Replica(const P_Window_Replica &_other):
                     Basic_Replica(_other),
                     func(_other.func),
                     key_extr(_other.key_extr),
                     n_max_elements(_other.n_max_elements),
                     keyMap(_other.keyMap),          
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
    ~P_Window_Replica()
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
        std::cout << "PW::process_input CALLED idx:" << _timestamp << " wm:" << _watermark << " t:" << _tuple.value << std::endl;
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
        size_t hashcode = std::hash<key_t>()(key); // compute the hashcode of the key
        auto it = keyMap.find(key); // find the corresponding key_descriptor (or allocate it if does not exist)
        if (it == keyMap.end()) {
            auto p = keyMap.insert(std::make_pair(key, Key_Descriptor())); // create the state of the key
            it = p.first;
        }
        Key_Descriptor &key_d = (*it).second;
        _identifier = key_d.next_input_id++; // set the progressive identifier of the tuple (per key basis)
        uint64_t index = (winType == Win_Type_t::CB) ? _identifier : _timestamp; // index value is the identifier (CB) of the timestamp (TB) of the tuple
        // gwid of the first window of the key assigned to the replica
        uint64_t first_gwid_key = 0;
        // initial identifer (CB) or timestamp (TB) of the keyed sub-stream arriving at the replica
        uint64_t initial_index = 0;
        uint64_t min_boundary = (key_d.last_lwid >= 0) ? win_len + (key_d.last_lwid * slide_len) : 0; // if the tuple is related to a closed window -> IGNORED
        if (index < initial_index + min_boundary) {
            if (key_d.last_lwid >= 0) {
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
        std::deque<result_t> _win_results; // used only by incremental processing
        bool res_opened = false; // used only by incremental processing
        auto &wins = key_d.wins;
        if constexpr (isIncNonRiched || isIncRiched) {
            if ((long) key_d.next_lwid <= last_w) { // if there are new windows, and results are kept on RocksDB
                _win_results = mydb_results->get_list_result(key); // deserialize windows results associated with key
                res_opened = true;
            }
        }
        for (long lwid = key_d.next_lwid; lwid <= last_w; lwid++) { // create all the new opened windows
            uint64_t gwid = first_gwid_key + lwid; // translate lwid -> gwid
            if constexpr (isIncNonRiched || isIncRiched) {
                result_t new_res = create_win_result_t<result_t, key_t>(key, gwid);
                _win_results.push_back(new_res);
            }
            if (winType == Win_Type_t::CB) {
                wins.push_back(win_t(key, lwid, gwid, Triggerer_CB(win_len, slide_len, lwid, initial_index), Win_Type_t::CB, win_len, slide_len));
            }
            else {
                wins.push_back(win_t(key, lwid, gwid, Triggerer_TB(win_len, slide_len, lwid, initial_index), Win_Type_t::TB, win_len, slide_len));
            }
            key_d.next_lwid++;
        }
        size_t cnt_fired = 0;
        if constexpr (isNonIncRiched || isNonIncNonRiched) {
            insert(wrapper_t(_tuple, index), key_d, key); // insert the wrapped tuple in the archive of the key (non-incremental processing only)
        }
        if constexpr (isIncNonRiched || isIncRiched) {
            if (!wins.empty() && !res_opened) {
                _win_results = mydb_results->get_list_result(key); // deserialize windows results associated with key
                res_opened = true;
            }
        }
        typename std::deque<result_t>::iterator result_it_list = _win_results.begin();
        for (auto &win: wins) { // evaluate all the open windows of the key
            win_event_t event = win.onTuple(_tuple, index, _timestamp); // get the event
            if (event == win_event_t::IN) { // window is not fired
                if constexpr (isIncNonRiched) { // incremental and non-riched
                    result_t &res = *result_it_list;
                    func(_tuple, res);
                }
                if constexpr (isIncRiched) { // incremental and riched
                    result_t &res = *result_it_list;
                    (this->context).setContextParameters(_timestamp, _watermark); // set the parameter of the RuntimeContext
                    func(_tuple, res, this->context);
                }
            }
            else if (event == win_event_t::FIRED) { // window is fired
                if ((winType == Win_Type_t::CB) || (this->execution_mode != Execution_Mode_t::DEFAULT) || (win.getResultTimestamp() + lateness < _watermark)) {
                    uint64_t lwid = win.getLWID(); // local id of window to calculate boundaries
                    bool isEmpty = win.getSize() <= 0; // if win is empty i just return an empty iterator
#ifdef DEBUG_MODE
                    std::cout << "PW::process_input FIRED lwid:" << lwid << " isEmpty:"<< isEmpty << std::endl;
#endif
                    if constexpr (isNonIncNonRiched || isNonIncRiched) { // non-incremental
                        std::pair<input_iterator_t, input_iterator_t> its;
                        std::deque<wrapper_t> window;
                        if (isEmpty) { // empty window
                            its.first = getEnd(lwid, key_d, key);
                            its.second = its.first;
                        }
                        else { // non-empty window
                            window = get_window(lwid, key_d, key);
                            its.first = window.begin();
                            its.second = window.end();
                        }
                        Iterable<tuple_t> iter(its.first, its.second);
                        result_t res = create_win_result_t<result_t, key_t>(key, win.getGWID());
                        if constexpr (isNonIncNonRiched) { // non-riched
                            func(iter, res);
                        }
                        if constexpr (isNonIncRiched) { // riched
                            (this->context).setContextParameters(_timestamp, _watermark); // set the parameter of the RuntimeContext
                            func(iter, res, this->context);
                        }
                        if (!isEmpty) { // purge tuples from the archive
                            purge(lwid, key_d, key);
                        }
                        cnt_fired++;
                        key_d.last_lwid++;
                        uint64_t used_ts = (this->execution_mode != Execution_Mode_t::DEFAULT) ? _timestamp : _watermark;
                        uint64_t used_wm = (this->execution_mode != Execution_Mode_t::DEFAULT) ? 0 : _watermark;
                        this->doEmit(this->emitter, &(res), 0, used_ts, used_wm, this);
                    }
                    else {
                        result_t &res = *result_it_list;
                        cnt_fired++;
                        key_d.last_lwid++;
                        uint64_t used_ts = (this->execution_mode != Execution_Mode_t::DEFAULT) ? _timestamp : _watermark;
                        uint64_t used_wm = (this->execution_mode != Execution_Mode_t::DEFAULT) ? 0 : _watermark;
                        this->doEmit(this->emitter, &(res), 0, used_ts, used_wm, this);
                    }
#if defined(WF_TRACING_ENABLED)
                    (this->stats_record).outputs_sent++;
                    (this->stats_record).bytes_sent += sizeof(result_t);
#endif
                }
            }
            if constexpr (isIncNonRiched || isIncRiched) {
                result_it_list++;
            }
        }
        if constexpr (isIncNonRiched || isIncRiched) {
            _win_results.erase(_win_results.begin(), _win_results.begin() + cnt_fired);
            mydb_results->put(_win_results, key);
        }
        wins.erase(wins.begin(), wins.begin() + cnt_fired); // purge the fired windows
    }

    // method to manage the EOS (utilized by the FastFlow runtime)
    void eosnotify(ssize_t id) override
    {
        for (auto &k: keyMap) { // iterate over all the keys
            key_t key = (k.first);
            Key_Descriptor &key_d = (k.second);
            std::deque<result_t> _win_results; // used only by incremental processing
            typename std::deque<result_t>::iterator result_it_list;
            if constexpr (isIncNonRiched || isIncRiched) {
                _win_results = mydb_results->get_list_result(key);
                result_it_list = _win_results.begin();
            }
            auto &wins = key_d.wins;
            for (auto &win: wins) { // iterate over all the windows of the key
                if constexpr (isNonIncNonRiched || isNonIncRiched) { // non-incremental
                    uint64_t lwid = win.getLWID(); // local id of window to calculate boundaries
                    bool isEmpty = win.getSize() <= 0; // if win is empty i just return an empty iterator
#ifdef DEBUG_MODE
                    std::cout << "PW::eosnotify FIRED lwid:" << lwid << std::endl;
#endif
                    std::pair<input_iterator_t, input_iterator_t> its;
                    std::deque<wrapper_t> window;
                    if (isEmpty) { // empty window
                        its.first = getEnd(lwid, key_d, key);
                        its.second = its.first;
                    }
                    else { // non-empty window
                        window = get_window(lwid, key_d, key);
                        its.first = window.begin();
                        its.second = window.end();
                    }
                    Iterable<tuple_t> iter(its.first, its.second);
                    result_t res = create_win_result_t<result_t, key_t>(key, win.getGWID());
                    if constexpr (isNonIncNonRiched) { // non-riched
                        func(iter, res);
                    }
                    if constexpr (isNonIncRiched) { // riched
                        func(iter, res, this->context);
                    }
                    uint64_t used_wm = (this->execution_mode != Execution_Mode_t::DEFAULT) ? 0 : last_time;
                    this->doEmit(this->emitter, &(res), 0, last_time, used_wm, this);
                }
                else {
                    result_t &res = *result_it_list;
                    uint64_t used_wm = (this->execution_mode != Execution_Mode_t::DEFAULT) ? 0 : last_time;
                    this->doEmit(this->emitter, &(res), 0, last_time, used_wm, this);
                    result_it_list++;
                }
#if defined(WF_TRACING_ENABLED)
                (this->stats_record).outputs_sent++;
                (this->stats_record).bytes_sent += sizeof(result_t);
#endif
            }
            if constexpr (isIncNonRiched || isIncRiched) { // I don't think this part is really necessary
                mydb_results->put(_win_results, key);
            }
        }
        Basic_Replica::eosnotify(id);
    }

    // Get the number of ignored tuples
    size_t getNumIgnoredTuples() const
    {
        return ignored_tuples;
    }

    P_Window_Replica(P_Window_Replica &&) = delete; ///< Move constructor is deleted
    P_Window_Replica &operator=(const P_Window_Replica &) = delete; ///< Copy assignment operator is deleted
    P_Window_Replica &operator=(P_Window_Replica &&) = delete; ///< Move assignment operator is deleted
};

} // namespace wf

#endif
