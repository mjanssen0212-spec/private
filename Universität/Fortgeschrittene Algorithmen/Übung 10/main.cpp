#include <iostream>
#include <chrono>

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
    // TODO: Ihre Implementierung hier...
public:
    uint64_t sizeInBytes() const {
        return 0;
    }

    // ...
};


// ==========================================
// Aufgabenteil b) LOUDS-Implementierung
// ==========================================

class LOUDSTree {
    // Der BitVector ist der einzige Datenspeicher! Keine Knoten-Objekte.
    BitVector bv;

public:
    // TODO: Passen Sie den Konstruktor an Ihre BaselineTree-Klasse an.
    // Der Konstruktor soll den übergebenen Baum in Level-Order traversieren
    // und die LOUDS-Bits in 'bv' setzen.
    explicit LOUDSTree(const BaselineTree &tree) : bv(1 /* TODO: Richtige Größe berechnen! */) {
        // TODO: Implementierung der LOUDS-Erstellung (BFS Traversierung)

        // WICHTIG: Am Ende muss der Index gebaut werden:
        bv.buildIndex();
    }

    uint64_t sizeInBytes() const {
        return bv.sizeInBytes();
    }

    // --- LOUDS-Operationen (Ausschließlich via rank/select implementieren!) ---

    uint64_t parent(uint64_t i) {
        // TODO
        return 0;
    }

    bool isRoot(uint64_t i) {
        // TODO
        return false;
    }

    bool isLeaf(uint64_t i) {
        // TODO
        return false;
    }

    uint64_t outDegree(uint64_t i) {
        // TODO
        return 0;
    }

    uint64_t childNum(uint64_t i, uint64_t j) {
        // TODO: Geben Sie das j-te Kind von nodeId zurück (j ist 1-basiert)
        return 0;
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
    BaselineTree baseline;

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
