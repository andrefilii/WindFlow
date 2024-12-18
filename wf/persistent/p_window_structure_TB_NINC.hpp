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
 *  @file    p_window_structure.hpp
 *  @author  Gabriele Mencagli and Simone Frassinelli
 *  
 *  @brief Persistent streaming windows
 *  
 *  @section P_Window (Description)
 *  
 *  This file implements the classes used by the WindFlow library to support
 *  streaming windows with persistent operators.
 */ 

#ifndef P_WINDOW_TB_NINC_H
#define P_WINDOW_H

// includes
#include<optional>
#include<functional>
#include<basic.hpp>

namespace wf {

// class P_Window
template<typename tuple_t, typename result_t>
class P_Window_TB_NINC
{
private:
    using wrapper_t = wrapper_tuple_t<tuple_t>; // alias for the wrapped tuple type
    using triggerer_t = std::function<win_event_t(uint64_t)>; // triggerer type of the window
    uint64_t lwid; // local identifier of the window (starting from zero)
    uint64_t gwid; // global identifier of the window (starting from zero)
    triggerer_t triggerer; // triggerer used by the window
    uint64_t num_tuples; // number of tuples raising a IN event
    uint64_t result_timestamp; // timestamp of the window result

public:
    // Constructor
    P_Window_TB_NINC(uint64_t _lwid,
             uint64_t _gwid,
             triggerer_t _triggerer,
             uint64_t _win_len,
             uint64_t _slide_len):
             lwid(_lwid),
             gwid(_gwid),
             triggerer(_triggerer),
             num_tuples(0)
    {
        result_timestamp = gwid * _slide_len + _win_len - 1;
    }

    // Evaluate the status of the window given a new wrapped tuple
    win_event_t onTuple(const tuple_t &_tuple,
                        uint64_t _index,
                        uint64_t _ts)
    {
        assert(_index == _ts); // sanity check
        win_event_t event = triggerer(_index); // evaluate the triggerer
        if (event == win_event_t::IN) {
            num_tuples++;
        }
        else if (event == win_event_t::FIRED) {
        }
        return event;
    }

    // Get the local window identifier
    uint64_t getLWID() const
    {
        return lwid;
    }

    // Get the global window identifier
    uint64_t getGWID() const
    {
        return gwid;
    }

    // Get the number of tuples that raised a IN event
    size_t getSize() const
    {
        return num_tuples;
    }

    // Get the timestamp of the window result
    uint64_t getResultTimestamp() const
    {
        return result_timestamp;
    }
};

} // namespace wf

#endif
