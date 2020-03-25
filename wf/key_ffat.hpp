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

/** 
 *  @file    key_ffat.hpp
 *  @author  Gabriele Mencagli
 *  @date    12/03/2020
 *  
 *  @brief Key_FFAT operator executing a windowed query in parallel
 *         on multi-core CPUs using the FlatFAT algorithm
 *  
 *  @section Key_FFAT (Description)
 *  
 *  This file implements the Key_FFAT operator able to execute windowed queries on a
 *  multicore. The operator executes streaming windows in parallel on the CPU cores.
 *  Only windows belonging to different sub-streams can be executed in parallel, while
 *  windows of the same sub-stream are executed rigorously in order. However, windows
 *  are efficiently processed using the FlatFAT algorithm.
 *  
 *  The template parameters tuple_t and result_t must be default constructible, with
 *  a copy constructor and copy assignment operator, and they must provide and implement
 *  the setControlFields() and getControlFields() methods.
 */ 

#ifndef KEY_FFAT_H
#define KEY_FFAT_H

/// includes
#include <ff/pipeline.hpp>
#include <ff/all2all.hpp>
#include <ff/farm.hpp>
#include <ff/optimize.hpp>
#include <basic.hpp>
#include <win_seqffat.hpp>
#include <kf_nodes.hpp>

namespace wf {

/** 
 *  \class Key_FFAT
 *  
 *  \brief Key_FFAT operator executing a windowed query in parallel on multi-core CPUs
 *         leveraging the FlatFAT algorithm
 *  
 *  This class implements the Key_FFAT operator executing windowed queries in parallel on
 *  a multicore. In the operator, only windows belonging to different sub-streams can be
 *  executed in parallel. However, windows of the same substream are executed efficiently
 *  by using the FlatFAT algorithm.
 */ 
template<typename tuple_t, typename result_t>
class Key_FFAT: public ff::ff_farm
{
public:
    /// type of the lift function
    using winLift_func_t = std::function<void(const tuple_t &, result_t &)>;
    /// type of the rich lift function
    using rich_winLift_func_t = std::function<void(const tuple_t &, result_t &, RuntimeContext &)>;
    /// type of the combine function
    using winComb_func_t = std::function<void(const result_t &, const result_t &, result_t &)>;
    /// type of the rich combine function
    using rich_winComb_func_t = std::function<void(const result_t &, const result_t &, result_t &, RuntimeContext &)>;
    /// type of the closing function
    using closing_func_t = std::function<void(RuntimeContext &)>;
    /// type of the functionto map the key hashcode onto an identifier starting from zero to pardegree-1
    using routing_func_t = std::function<size_t(size_t, size_t)>;

private:
    // type of the Win_SeqFFAT to be created
    using win_seqffat_t = Win_SeqFFAT<tuple_t, result_t>;
    // type of the KF_Emitter node
    using kf_emitter_t = KF_Emitter<tuple_t>;
    // type of the KF_Collector node
    using kf_collector_t = KF_Collector<result_t>;
    // friendships with other classes in the library
    friend class MultiPipe;
    // parallelism of the Key_FFAT
    size_t parallelism;
    // window type (CB or TB)
    win_type_t winType;
    bool used; // true if the operator has been added/chained in a MultiPipe

public:
    /** 
     *  \brief Constructor I
     *  
     *  \param _winLift_func the lift function to translate a tuple into a result
     *  \param _winComb_func the combine function to combine two results into a result
     *  \param _win_len window length (in no. of tuples or in time units)
     *  \param _slide_len slide length (in no. of tuples or in time units)
     *  \param _triggering_delay (triggering delay in time units, meaningful for TB windows only otherwise it must be 0)
     *  \param _winType window type (count-based CB or time-based TB)
     *  \param _pardegree parallelism degree of the Key_Farm operator
     *  \param _name string with the unique name of the operator
     *  \param _closing_func closing function
     *  \param _routing_func function to map the key hashcode onto an identifier starting from zero to pardegree-1
     */ 
    Key_FFAT(winLift_func_t _winLift_func,
             winComb_func_t _winComb_func,
             uint64_t _win_len,
             uint64_t _slide_len,
             uint64_t _triggering_delay,
             win_type_t _winType,
             size_t _pardegree,
             std::string _name,
             closing_func_t _closing_func,
             routing_func_t _routing_func):
             parallelism(_pardegree),
             winType(_winType),
             used(false)         
    {
        // check the validity of the windowing parameters
        if (_win_len == 0 || _slide_len == 0) {
            std::cerr << RED << "WindFlow Error window length or slide in Key_Farm cannot be zero" << DEFAULT_COLOR << std::endl;
            exit(EXIT_FAILURE);
        }
        // check the use of sliding windows
        if (_slide_len >= _win_len) {
            std::cerr << RED << "WindFlow Error: Key_FFAT can be used with sliding windows only (s<w)" << DEFAULT_COLOR << std::endl;
            exit(EXIT_FAILURE);
        }
        // check the validity of the parallelism degree
        if (_pardegree == 0) {
            std::cerr << RED << "WindFlow Error: Key_FFAT has parallelism zero" << DEFAULT_COLOR << std::endl;
            exit(EXIT_FAILURE);
        }
        // std::vector of Win_SeqFFAT
        std::vector<ff_node *> w(_pardegree);
        // create the Win_SeqFFAT
        for (size_t i = 0; i < _pardegree; i++) {
            OperatorConfig configSeq(0, 1, _slide_len, 0, 1, _slide_len);
            auto *ffat = new win_seqffat_t(_winLift_func, _winComb_func, _win_len, _slide_len, _triggering_delay, _winType, _name + "_kff", _closing_func, RuntimeContext(_pardegree, i), configSeq);
            w[i] = ffat;
        }
        ff::ff_farm::add_workers(w);
        ff::ff_farm::add_collector(nullptr);
        // create the Emitter node
        ff::ff_farm::add_emitter(new kf_emitter_t(_routing_func, _pardegree));
        // when the Key_FFAT will be destroyed we need aslo to destroy the emitter, workers and collector
        ff::ff_farm::cleanup_all();
    }

    /** 
     *  \brief Constructor II
     *  
     *  \param _rich_winLift_func the rich lift function to translate a tuple into a result
     *  \param _rich_ winComb_func the rich combine function to combine two results into a result
     *  \param _win_len window length (in no. of tuples or in time units)
     *  \param _slide_len slide length (in no. of tuples or in time units)
     *  \param _triggering_delay (triggering delay in time units, meaningful for TB windows only otherwise it must be 0)
     *  \param _winType window type (count-based CB or time-based TB)
     *  \param _pardegree parallelism degree of the Key_Farm operator
     *  \param _name string with the unique name of the operator
     *  \param _closing_func closing function
     *  \param _routing_func function to map the key hashcode onto an identifier starting from zero to pardegree-1
     */ 
    Key_FFAT(rich_winLift_func_t _rich_winLift_func,
             rich_winComb_func_t _rich_winComb_func,
             uint64_t _win_len,
             uint64_t _slide_len,
             uint64_t _triggering_delay,
             win_type_t _winType,
             size_t _pardegree,
             std::string _name,
             closing_func_t _closing_func,
             routing_func_t _routing_func):
             parallelism(_pardegree),
             winType(_winType),
             used(false)         
    {
        // check the validity of the windowing parameters
        if (_win_len == 0 || _slide_len == 0) {
            std::cerr << RED << "WindFlow Error window length or slide in Key_Farm cannot be zero" << DEFAULT_COLOR << std::endl;
            exit(EXIT_FAILURE);
        }
        // check the use of sliding windows
        if (_slide_len >= _win_len) {
            std::cerr << RED << "WindFlow Error: FlatFAT can be used with sliding windows only (s<w)" << DEFAULT_COLOR << std::endl;
            exit(EXIT_FAILURE);
        }
        // check the validity of the parallelism degree
        if (_pardegree == 0) {
            std::cerr << RED << "WindFlow Error: Key_FFAT has parallelism zero" << DEFAULT_COLOR << std::endl;
            exit(EXIT_FAILURE);
        }
        // std::vector of Win_SeqFFAT
        std::vector<ff_node *> w(_pardegree);
        // create the Win_SeqFFAT
        for (size_t i = 0; i < _pardegree; i++) {
            OperatorConfig configSeq(0, 1, _slide_len, 0, 1, _slide_len);
            auto *ffat = new win_seqffat_t(_rich_winLift_func, _rich_winComb_func, _win_len, _slide_len, _triggering_delay, _winType, _name + "_kff", _closing_func, RuntimeContext(_pardegree, i), configSeq);
            w[i] = ffat;
        }
        ff::ff_farm::add_workers(w);
        ff::ff_farm::add_collector(nullptr);
        // create the Emitter node
        ff::ff_farm::add_emitter(new kf_emitter_t(_routing_func, _pardegree));
        // when the Key_FFAT will be destroyed we need aslo to destroy the emitter, workers and collector
        ff::ff_farm::cleanup_all();
    }

    /** 
     *  \brief Get the parallelism degree of the Key_FFAT
     *  \return parallelism degree of the Key_FFAT
     */ 
    size_t getParallelism() const
    {
        return parallelism;
    }

    /** 
     *  \brief Get the window type (CB or TB) utilized by the operator
     *  \return adopted windowing semantics (count- or time-based)
     */ 
    win_type_t getWinType() const
    {
        return winType;
    }

    /** 
     *  \brief Check whether the Key_FFAT has been used in a MultiPipe
     *  \return true if the Key_FFAT has been added/chained to an existing MultiPipe
     */
    bool isUsed() const
    {
        return used;
    }

    /** 
     *  \brief Get the number of dropped tuples by the Key_FFAT
     *  \return number of tuples dropped during the processing by the Key_FFAT
     */ 
    size_t getNumDroppedTuples() const
    {
        size_t count = 0;
        auto workers = this->getWorkers();
        for (auto *w: workers) {
            auto *seq = static_cast<win_seqffat_t *>(w);
            count += seq->getNumDroppedTuples();
        }
        return count;
    }

    /// deleted constructors/operators
    Key_FFAT(const Key_FFAT &) = delete; // copy constructor
    Key_FFAT(Key_FFAT &&) = delete; // move constructor
    Key_FFAT &operator=(const Key_FFAT &) = delete; // copy assignment operator
    Key_FFAT &operator=(Key_FFAT &&) = delete; // move assignment operator
};

} // namespace wf

#endif
