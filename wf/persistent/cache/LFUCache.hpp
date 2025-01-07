#ifndef LFU_CACHE_HPP
#define LFU_CACHE_HPP

#include "Cache.hpp"
#include <unordered_map>
#include <list>

template <typename Key, typename Value>
class LFUCache : public Cache<Key, Value> {
private:
    typedef size_t Frequency;
    typedef std::pair<Frequency, Value> FrequencyValuePair;
    typedef std::list<Key> KeyList;
    typedef typename KeyList::iterator KeyListIt;

    typedef std::unordered_map<Frequency, KeyList> FrequencyListMap; // Mappa frequenza -> lista di chiavi
    typedef std::unordered_map<Key, KeyListIt> KeyNodeMap; // Mappa chiave -> iteratore nella lista
    typedef std::unordered_map<Key, FrequencyValuePair> EntryMap; // Mappa chiave -> (frequenza, valore)



    size_t maxCapacity;
    size_t minFrequency;
    size_t currentSize;

    FrequencyListMap frequencyList; // Mappa frequenza -> lista di chiavi
    KeyNodeMap keyNode; // Mappa chiave -> iteratore
    EntryMap frequency; // Mappa chiave -> (frequenza, valore)

public:
    explicit LFUCache(size_t capacity) : maxCapacity(capacity), minFrequency(0), currentSize(0) {}

    void put(const Key& key, const Value& value) override {
        if (maxCapacity <= 0)
            return; // Capacity is zero or negative, do nothing

        if (keyNode.find(key) != keyNode.end()) {
            // Key already exists, update its value and frequency
            frequency[key].second = value;
            get(key);
            return;
        }

        if (currentSize == maxCapacity) {
            // Cache is full, evict the least frequently used key
            Key minFreqBack = frequencyList[minFrequency].back();
            keyNode.erase(minFreqBack);
            frequency.erase(minFreqBack);
            frequencyList[minFrequency].pop_back();
            currentSize--;
        }

        // Add the new key to the cache
        currentSize++;
        minFrequency = 1;
        frequencyList[minFrequency].push_front(key);
        keyNode[key] = frequencyList[minFrequency].begin();
        frequency[key].first = 1, frequency[key].second = value;
    }

    std::optional<Value> get(const Key& key) override {
        if (keyNode.find(key) == keyNode.end())
            return std::nullopt; // Key not found

        Frequency keyFreq = frequency[key].first;
        frequencyList[keyFreq].erase(keyNode[key]);

        frequency[key].first++;
        frequencyList[frequency[key].first].push_front(key);
        keyNode[key] = frequencyList[frequency[key].first].begin();

        if (frequencyList[minFrequency].size() == 0)
            minFrequency++; // Update minFrequency if the list is empty

        return frequency[key].second; // Return the value of the key
    }

    bool exists(const Key& key) const override {
        return keyNode.find(key) != keyNode.end();
    }

    void remove(const Key& key) override {
        if (keyNode.find(key) == keyNode.end()) {
            return; // La chiave non esiste
        }

        Frequency keyFreq = frequency[key].first;
        frequencyList[keyFreq].erase(keyNode[key]);
        frequency.erase(key);
        keyNode.erase(key);

        if (frequencyList[minFrequency].empty()) {
            minFrequency++; // Aggiorna minFrequency se la lista è vuota
        }

        currentSize--; // Decrementa la dimensione della cache
    }

    void clear() override {
        frequencyList.clear();
        keyNode.clear();
        frequency.clear();
        minFrequency = 0;
        currentSize = 0;
    }

    size_t size() const override {
        return currentSize;
    }

    size_t capacity() const override {
        return maxCapacity;
    }
};

#endif // LFU_CACHE_HPP