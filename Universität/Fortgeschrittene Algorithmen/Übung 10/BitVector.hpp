#pragma once
#include <vector>
#include <cstdint>
#include <stdexcept>
#include <algorithm>

class BitVector {
    std::vector<uint64_t> data;
    std::vector<uint32_t> rankIndex;
    uint64_t numBits;
    bool isBuilt = false;
    static constexpr uint64_t BLOCK_SIZE_BITS = 512;
    static constexpr uint64_t WORDS_PER_BLOCK = BLOCK_SIZE_BITS / 64;

    static uint64_t countSetBits(uint64_t n) {
        return std::popcount(n);
    }

public:
    explicit BitVector(uint64_t n) : numBits(n) {
        data.resize((n + 63) / 64, 0);
    }

    // Bit setzen, nur während der Initialisierung erlaubt
    void setBit(uint64_t index) {
        if (isBuilt) throw std::runtime_error("BitVector is already built (read-only).");
        if (index >= numBits) throw std::out_of_range("Bit index out of range.");
        data[index / 64] |= 1ULL << (index % 64);
    }

    // Index aufbauen, muss nach dem Setzen aller Bits und vor der ersten Abfrage gerufen werden
    void buildIndex() {
        if (isBuilt) return;
        rankIndex.clear();
        rankIndex.reserve(data.size() / WORDS_PER_BLOCK + 2);

        uint32_t currentRank = 0;
        for (size_t i = 0; i < data.size(); ++i) {
            if (i % WORDS_PER_BLOCK == 0) {
                rankIndex.push_back(currentRank);
            }
            currentRank += countSetBits(data[i]);
        }
        rankIndex.push_back(currentRank);
        isBuilt = true;
    }

    // Anzahl der Einsen im Bereich [0, index)
    uint64_t rank1(uint64_t index) const {
        if (!isBuilt) throw std::runtime_error("Index not built.");
        if (index > numBits) index = numBits;

        uint64_t blockIdx = index / BLOCK_SIZE_BITS;
        uint64_t result = rankIndex[blockIdx];
        uint64_t startWord = blockIdx * WORDS_PER_BLOCK;
        uint64_t endWord = index / 64;

        for (uint64_t i = startWord; i < endWord; ++i) {
            result += countSetBits(data[i]);
        }

        uint64_t bitsInLastWord = index % 64;
        if (bitsInLastWord > 0) {
            result += countSetBits(data[endWord] & ((1ULL << bitsInLastWord) - 1));
        }
        return result;
    }

    uint64_t rank0(uint64_t index) const {
        return index - rank1(index);
    }

    // Gibt den Index der k-ten Eins zurück (k ist 1-basiert)
    uint64_t select1(uint64_t k) const {
        if (!isBuilt) throw std::runtime_error("Index not built.");
        if (k == 0) return -1;

        auto it = std::upper_bound(rankIndex.begin(), rankIndex.end(), k);
        uint64_t blockIdx = std::distance(rankIndex.begin(), it) - 1;
        uint64_t currentRank = rankIndex[blockIdx];
        uint64_t wordIdx = blockIdx * WORDS_PER_BLOCK;

        while (wordIdx < data.size()) {
            uint64_t count = countSetBits(data[wordIdx]);
            if (currentRank + count >= k) {
                uint64_t temp = data[wordIdx];
                for (int bit = 0; bit < 64; ++bit) {
                    if ((temp >> bit) & 1) {
                        currentRank++;
                        if (currentRank == k) return wordIdx * 64 + bit;
                    }
                }
            }
            currentRank += count;
            wordIdx++;
        }
        return -1; // Nicht gefunden
    }

    // Gibt den Index der k-ten Null zurück (k ist 1-basiert)
    uint64_t select0(uint64_t k) const {
        if (!isBuilt) throw std::runtime_error("Index not built.");
        // Binäre Suche über rank0
        uint64_t low = 0, high = numBits;
        uint64_t ans = -1;
        while (low <= high) {
            uint64_t mid = low + (high - low) / 2;
            if (rank0(mid + 1) >= k) {
                ans = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return ans;
    }

    // Speicherverbrauch in Bytes (inkl. Overhead)
    uint64_t sizeInBytes() const {
        return (data.capacity() * sizeof(uint64_t)) +
               (rankIndex.capacity() * sizeof(uint32_t)) +
               sizeof(*this);
    }

    uint64_t length() const { return numBits; }
};
