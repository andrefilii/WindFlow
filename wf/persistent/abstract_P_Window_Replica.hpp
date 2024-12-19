#ifndef ABS_P_WIN_REPLICA_H
#define ABS_P_WIN_REPLICA_H

#include <basic_emitter.hpp>
#include <stats_record.hpp> // se WF_TRACING_ENABLED è definito
#include<persistent/db_handle.hpp>

namespace wf {

template<typename win_func_t, typename keyextr_func_t>
class Abstract_P_Window_Replica : public Basic_Replica
{
private:
    template<typename T1, typename T2> friend class P_Keyed_Windows;
public:
    virtual ~Abstract_P_Window_Replica() = default;

    // Metodi astratti
    virtual void receiveBatches(bool _input_batching) = 0;
    virtual void setEmitter(Basic_Emitter* _emitter) = 0;
    virtual bool isTerminated() const = 0;
    virtual void setExecutionMode(Execution_Mode_t _execution_mode) = 0;

#if defined(WF_TRACING_ENABLED)
    virtual Stats_Record getStatsRecord() const = 0;
#endif

    void eosnotify(ssize_t id) override {
        Basic_Replica::eosnotify(id); // Richiama l'implementazione di base
    }

    void* svc(void* _in) override {
        return Basic_Replica::svc(_in); // Richiama l'implementazione di base
    }
};

}
#endif