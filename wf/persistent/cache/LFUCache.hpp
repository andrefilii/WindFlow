#ifndef LFU_CACHE_HPP
#define LFU_CACHE_HPP

#include "Cache.hpp"
#include <unordered_map>
#include <list>

template <typename Key, typename Value>
class LFUCache : public Cache<Key, Value> {
private:
    struct CacheNode {
        Key key;
        Value value;
        size_t frequency;

        CacheNode(Key k, Value v, size_t freq) : key(k), value(v), frequency(freq) {}
    };

    typedef std::list<CacheNode> NodeList;
    typedef typename NodeList::iterator NodeListIt;

    size_t maxCapacity;
    size_t minFrequency;

    // Mappa chiave -> nodo della lista
    std::unordered_map<Key, NodeListIt> cacheMap;

    // Mappa frequenza -> lista di nodi
    std::unordered_map<size_t, NodeList> frequencyMap;

    void updateFrequency(NodeListIt nodeIt) {
        size_t freq = nodeIt->frequency;
        frequencyMap[freq].erase(nodeIt);
        if (frequencyMap[freq].empty()) {
            frequencyMap.erase(freq);
            if (minFrequency == freq) {
                minFrequency++;
            }
        }
        nodeIt->frequency++;
        frequencyMap[nodeIt->frequency].push_front(*nodeIt);
        cacheMap[nodeIt->key] = frequencyMap[nodeIt->frequency].begin();
    }

public:
    explicit LFUCache(size_t capacity) : maxCapacity(capacity), minFrequency(0) {}

    void put(const Key& key, const Value& value) override {
        if (maxCapacity == 0) return;

        auto it = cacheMap.find(key);
        if (it != cacheMap.end()) {
            auto nodeIt = it->second;
            nodeIt->value = value;
            updateFrequency(nodeIt);
            return;
        }

        if (cacheMap.size() >= maxCapacity) {
            auto& list = frequencyMap[minFrequency];
            auto lastNodeIt = list.back();
            cacheMap.erase(lastNodeIt.key);
            list.pop_back();
            if (list.empty()) {
                frequencyMap.erase(minFrequency);
            }
        }

        minFrequency = 1;
        frequencyMap[minFrequency].emplace_front(key, value, minFrequency);
        cacheMap[key] = frequencyMap[minFrequency].begin();
    }

    std::optional<Value> get(const Key& key) override {
        auto it = cacheMap.find(key);
        if (it == cacheMap.end()) {
            return std::nullopt;
        }
        auto nodeIt = it->second;
        updateFrequency(nodeIt);
        return nodeIt->value;
    }

    bool exists(const Key& key) const override {
        return cacheMap.find(key) != cacheMap.end();
    }

    void remove(const Key& key) override {
        auto it = cacheMap.find(key);
        if (it != cacheMap.end()) {
            auto nodeIt = it->second;
            size_t freq = nodeIt->frequency;
            frequencyMap[freq].erase(nodeIt);
            if (frequencyMap[freq].empty()) {
                frequencyMap.erase(freq);
                if (minFrequency == freq) {
                    minFrequency++;
                }
            }
            cacheMap.erase(it);
        }
    }

    void clear() override {
        cacheMap.clear();
        frequencyMap.clear();
        minFrequency = 0;
    }

    size_t size() const override {
        return cacheMap.size();
    }

    size_t capacity() const override {
        return maxCapacity;
    }
};

#endif // LFU_CACHE_HPP
