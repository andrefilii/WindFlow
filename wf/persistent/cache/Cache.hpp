#ifndef CACHE_HPP
#define CACHE_HPP

#include <optional>

template <typename Key, typename Value>
class Cache {
public:
    virtual ~Cache() = default;

    // Inserisce un valore associato a una chiave nella cache
    virtual void put(const Key& key, const Value& value) = 0;

    // Recupera un valore associato a una chiave (std::nullopt se non trovato)
    virtual std::optional<Value> get(const Key& key) = 0;

    // Rimuove un elemento dalla cache
    virtual void remove(const Key& key) = 0;

    // Svuota la cache
    virtual void clear() = 0;

    // Controlla se una chiave è presente nella cache
    virtual bool exists(const Key& key) const = 0;

    // Restituisce il numero di elementi nella cache
    virtual size_t size() const = 0;

    // Restituisce la capacità massima della cache
    virtual size_t capacity() const = 0;
};

#endif // CACHE_HPP
