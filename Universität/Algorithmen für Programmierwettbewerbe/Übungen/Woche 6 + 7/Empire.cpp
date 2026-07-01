// einmal mit allem bitte
#include <bits/stdc++.h>
// wer will schon immer std:: schreiben
using namespace std;
// schreibfaul aber wissen was drin ist
typedef int32_t i32;
typedef int64_t i64;
typedef uint32_t u32;
typedef uint64_t u64;
// besser ist das
#define float fliesskommazahlensindboese
#define double einfachnichtbenutzen
// und los

#define WGraph vector<unordered_map<i64,i64>>
using Edge = pair<i64, i64>;
template < class T > using MinHeap = priority_queue<pair<i64,T>, vector<pair<i64,T>>, greater<>>;

struct Planet {
    i32 number;
    i32 x;
    i32 y;
    i32 z;
};

struct DSU {
    vector<i64> parent;
    vector<i64> sz;

    explicit DSU(i64 n) : parent(n), sz(n, 1) {
        iota(parent.begin(), parent.end(), 0);
    }

    i64 find(i64 x) {
        if (parent[x] == x) {
            return x;
        }
        return parent[x] = find(parent[x]);
    }

    bool unite(i64 a, i64 b) {
        a = find(a);
        b = find(b);
        if (a == b) {
            return false;
        }
        if (sz[a] < sz[b]) {
            swap(a, b);
        }
        parent[b] = a;
        sz[a] += sz[b];
        return true;
    }

    bool query(i64 x, i64 y) {
        return find(x) == find(y);
    }
};

vector<Edge> kruskal(const WGraph& adjList, DSU& dsu) {
    vector<Edge> tree;
    MinHeap<Edge> heap;
    for (i64 v = 0; v < adjList.size(); v++) {
        for (auto& [w,weight] : adjList[v]) {
            if (v < w) {
                heap.push({weight, {v, w}});
            }
        }
    }
    while (!heap.empty()) {
        Edge edge = heap.top().second;
        heap.pop();
        if (dsu.unite(edge.first, edge.second)) {
            tree.push_back(edge);
        }
    }
    return tree;
}

int main() {
    i32 noOfPlanets;
    cin >> noOfPlanets;

    vector<Planet> planets(noOfPlanets);
    WGraph graph(noOfPlanets);

    for (int i = 0; i < noOfPlanets; i++) {
        planets[i].number = i;
        cin >> planets[i].x >> planets[i].y >> planets[i].z;
    }

    auto add_edge = [&](i64 u, i64 v, i64 w) {
        auto it = graph[u].find(v);
        if (it == graph[u].end() || w < it->second) {
            graph[u][v] = w;
            graph[v][u] = w;
        }
    };

    sort(planets.begin(), planets.end(), [](const Planet& a, const Planet& b) { return a.x < b.x; });

    for (int i = 0; i < noOfPlanets-1; i++) {
        auto p = planets[i];
        auto q = planets[i+1];
        auto dist = q.x - p.x;
        add_edge(p.number, q.number, dist);
    }

    sort(planets.begin(), planets.end(), [](const Planet& a, const Planet& b) { return a.y < b.y; });

    for (int i = 0; i < noOfPlanets-1; i++) {
        auto p = planets[i];
        auto q = planets[i+1];
        auto dist = q.y - p.y;
        add_edge(p.number, q.number, dist);
    }

    sort(planets.begin(), planets.end(), [](const Planet& a, const Planet& b) { return a.z < b.z; });

    for (int i = 0; i < noOfPlanets-1; i++) {
        auto p = planets[i];
        auto q = planets[i+1];
        auto dist = q.z - p.z;
        add_edge(p.number, q.number, dist);
    }

    DSU dsu(noOfPlanets);
    
    vector<Edge> mst = kruskal(graph, dsu);
    i64 totalCost = 0;
    for (const auto& [u, v] : mst) {
        totalCost += graph[u].at(v);
    }

    cout << totalCost << '\n';
}
