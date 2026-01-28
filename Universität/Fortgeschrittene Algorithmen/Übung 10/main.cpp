#include <iostream>
#include <chrono>
#include <vector>
#include <queue>
#include <random>

#include "BitVector.hpp"

// ==========================================
// Aufgabenteil a) Baseline-Implementierung
// ==========================================

// TODO: Implementieren Sie hier Ihre eigene Baum-Klasse ("BaselineTree").
// Sie haben die Wahl: Pointer, Adjazenzliste oder -Matrix, Mengen etc.
//
// Anforderungen an diese Klasse:
// 1. Muss einen allgemeinen Baum speichern können.
// 2. Muss eine Methode `uint64_t sizeInBytes()` besitzen, die den
//    gesamten Speicherverbrauch (inkl. Overhead) berechnet.
// 3. Sollte Methoden/Strukturen bieten, um den Baum traversieren zu können,
//    damit er später in LOUDS umgewandelt werden kann.

class BaselineTree {
private:
    struct Node {
        std::vector<Node*> children;
        
        ~Node() {
            for (auto* child : children) {
                delete child;
            }
        }
    };
    
    Node* root;
    uint64_t nodeCount;

public:
    BaselineTree() : root(new Node()), nodeCount(1) {}

    ~BaselineTree() {
        delete root;
    }

    // Fügt einen neuen Knoten als Kind des Elternknotens hinzu
    // parent_index: 0-basierter Index in Level-Order-Traversierung
    void addChild(uint64_t parent_index) {
        if (parent_index >= nodeCount) {
            throw std::out_of_range("Parent index out of range");
        }
        
        // Finde den Elternknoten in Level-Order
        std::queue<Node*> q;
        q.push(root);
        uint64_t current_index = 0;
        
        while (!q.empty() && current_index < parent_index) {
            Node* node = q.front();
            q.pop();
            current_index++;
            
            for (auto* child : node->children) {
                q.push(child);
            }
        }
        
        if (!q.empty() && current_index == parent_index) {
            Node* parent = q.front();
            parent->children.push_back(new Node());
            nodeCount++;
        }
    }

    // Erstellt einen zufälligen Baum mit n Knoten
    void createRandomTree(uint64_t n, std::mt19937& rng) {
        if (n <= 1) return;
        
        std::uniform_int_distribution<uint64_t> dist(0, 0);
        
        for (uint64_t i = 1; i < n; ++i) {
            // Wähle einen zufälligen existierenden Knoten als Elternknoten
            dist = std::uniform_int_distribution<uint64_t>(0, nodeCount - 1);
            uint64_t parent = dist(rng);
            addChild(parent);
        }
    }

    uint64_t sizeInBytes() const {
        // Größe aller Node-Strukturen und Vektoren
        uint64_t size = sizeof(BaselineTree);
        size += nodeCount * sizeof(Node);
        
        // Berechne Overhead der Vektoren
        std::queue<const Node*> q;
        q.push(root);
        
        while (!q.empty()) {
            const Node* node = q.front();
            q.pop();
            
            // Vector-Overhead: capacity * sizeof(Node*)
            size += node->children.capacity() * sizeof(Node*);
            
            for (auto* child : node->children) {
                q.push(child);
            }
        }
        
        return size;
    }

    const Node* getRoot() const {
        return root;
    }

    uint64_t getNodeCount() const {
        return nodeCount;
    }

    // Level-Order-Traversierung für LOUDS-Konvertierung
    std::vector<std::vector<const Node*>> getLevelOrder() const {
        std::vector<std::vector<const Node*>> levels;
        if (!root) return levels;
        
        std::queue<const Node*> q;
        q.push(root);
        
        while (!q.empty()) {
            size_t levelSize = q.size();
            std::vector<const Node*> currentLevel;
            
            for (size_t i = 0; i < levelSize; ++i) {
                const Node* node = q.front();
                q.pop();
                currentLevel.push_back(node);
                
                for (auto* child : node->children) {
                    q.push(child);
                }
            }
            
            levels.push_back(currentLevel);
        }
        
        return levels;
    }
    
    friend class LOUDSTree;
};


// ==========================================
// Aufgabenteil b) LOUDS-Implementierung
// ==========================================

class LOUDSTree {
    // Der BitVector ist der einzige Datenspeicher! Keine Knoten-Objekte.
    BitVector bv;

public:
    // TODO: Passen Sie den Konstruktor an Ihre BaselineTree-Klasse an.

    explicit LOUDSTree(const BaselineTree &tree) : bv(tree.getNodeCount()*2 + 1) {

        
        bv.setBit(0);
        uint64_t bitPos = 1;
        
        auto levels = tree.getLevelOrder();
        
        for (const auto& level : levels) {
            for (const auto* node : level) {
                bitPos++;
                
                for (size_t i = 0; i < node->children.size(); ++i) {
                    if (bitPos < bv.length()) {
                        bv.setBit(bitPos);
                    }
                    bitPos++;
                }
            }
        }

        // WICHTIG: Am Ende muss der Index gebaut werden:
        bv.buildIndex();
    }

    uint64_t sizeInBytes() const {
        return bv.sizeInBytes();
    }

    // --- LOUDS-Operationen (Ausschließlich via rank/select implementieren!) ---

    uint64_t parent(uint64_t i) {
        if (i <= 1) return 0;
        uint64_t pos = bv.select0(i);
        return bv.rank0(pos);
    }

    bool isRoot(uint64_t i) {
        return i == 1;
    }

    bool isLeaf(uint64_t i) {
        return outDegree(i) == 0;
    }

    uint64_t outDegree(uint64_t i) {
        uint64_t pos_start = bv.select0(i);
        uint64_t pos_end = bv.select0(i + 1);
        
        return pos_end - pos_start - 1;
    }

    uint64_t childNum(uint64_t i, uint64_t j) {
        uint64_t degree = outDegree(i);
        if (j < 1 || j > degree) {
            return 0;
        }
        
        uint64_t pos_start = bv.select0(i);
        uint64_t pos_child = pos_start + j;
        
        return bv.rank0(pos_child + 1);
    }
};


int main() {
    // Parameter für den Benchmark, 1 Million Knoten
    const uint64_t N = 1000000;

    std::cout << "--- Start der Uebung: LOUDS (N=" << N << ") ---" << std::endl;

    // 1. Baseline Tree erstellen
    std::cout << "[Init] Erstelle Baseline Tree..." << std::endl;
    // TODO: Erzeugen Sie hier einen zufälligen Baum mit N Knoten.
    // Nutzen Sie std::mt19937 für reproduzierbare Zufallszahlen.
    std::mt19937 rng(42); // Seed für reproduzierbare Ergebnisse
    BaselineTree baseline;
    baseline.createRandomTree(N, rng);

    // 2. LOUDS Tree erstellen
    std::cout << "[Init] Konvertiere zu LOUDS..." << std::endl;
    LOUDSTree louds(baseline);

    // 3. Speichermessung
    uint64_t bytesBaseline = baseline.sizeInBytes();
    uint64_t bytesLouds = louds.sizeInBytes();

    std::cout << "Speicher Baseline: " << bytesBaseline / (1024.0 * 1024.0) << " MB" << std::endl;
    std::cout << "Speicher LOUDS:    " << bytesLouds / (1024.0 * 1024.0) << " MB" << std::endl;
    if (bytesLouds > 0) {
        std::cout << "Faktor: " << (double) bytesBaseline / bytesLouds << "x" << std::endl;
    }

    // 4. Laufzeitmessung (Parent Operation)
    std::cout << "[Benchmark] Starte 1.000.000 Parent-Abfragen..." << std::endl;
    uint64_t checksum = 0;

    auto start = std::chrono::high_resolution_clock::now();
    for (uint64_t i = 2; i <= N; ++i) {
        checksum += louds.parent(i);
    }
    auto end = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
    std::cout << "Zeit LOUDS: " << duration << " ms" << std::endl;
    std::cout << "Checksum: " << checksum << std::endl;

    return 0;
}
