#ifndef LRU_CACHE_HPP
#define LRU_CACHE_HPP

#include "Cache.hpp"
#include <unordered_map>
#include <list>

template <typename Key, typename Value>
class LRUCache : public Cache<Key, Value> {
private:
    typedef std::pair<Key, Value> EntryPair;
    typedef std::list<EntryPair> CacheList;
    typedef typename CacheList::iterator CacheListIt;
    typedef std::unordered_map<Key, CacheListIt> CacheMap;

    size_t maxCapacity;
    CacheList cacheList;
    CacheMap cacheMap;

public:

    explicit LRUCache(size_t capacity) : maxCapacity(capacity) {}

    void put(const Key& key, const Value& value) override {
        auto it = cacheMap.find(key);
        cacheList.push_front(EntryPair(key, value));
        if (it != cacheMap.end()) {
            cacheList.erase(it->second);
            cacheMap.erase(it);
        } 
        
        cacheMap[key] = cacheList.begin();

        if (cacheMap.size() > maxCapacity) {
           auto last = cacheList.end();
           last--;
           cacheMap.erase(last->first);
           cacheList.pop_back();
        }
    }

    std::optional<Value> get(const Key& key) override {
        auto it = cacheMap.find(key);
        if (it == cacheMap.end()) {
            return std::nullopt;
        }
        // sposta la chiave in cima
        cacheList.splice(cacheList.begin(), cacheList, it->second);
        return it->second->second;
    }

    bool exists(const Key& key) const override {
        return cacheMap.find(key) != cacheMap.end();
    }

    void remove(const Key& key) override {
        auto it = cacheMap.find(key);
        if (it != cacheMap.end()) {
            cacheList.erase(it->second);
            cacheMap.erase(it);
        }
    }

    void clear() override {
        cacheList.clear();
        cacheMap.clear();
    }

    size_t size() const override {
        return cacheMap.size();
    }

    size_t capacity() const override {
        return maxCapacity;
    }
};

#endif // LRU_CACHE_HPP
