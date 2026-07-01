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

const i64 INF = -1; // unreachable marker

vector<i64> bfs(i64 start, i64 n, vector<vector<i64>>& adj) {
    vector<i64> dist(n + 1, INF);
    dist[start] = 0;
    queue<i64> q;
    q.push(start);
    while (!q.empty()) {
        i64 u = q.front();
        q.pop();
        for (i64 v : adj[u]) {
            if (dist[v] == INF) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    return dist;
}

int main() {
    i64 noOfIntersections;
    i64 noOfStreets;

    cin >> noOfIntersections >> noOfStreets;

    i64 n = noOfIntersections;
    vector<vector<i64>> adj(n + 1);
    vector<pair<i64, i64>> edges(noOfStreets);

    for (i64 i = 0; i < noOfStreets; i++) {
        i64 a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
        edges[i] = {a, b};
    }

    vector<i64> dist1 = bfs(1, n, adj);
    vector<i64> distT = bfs(n, n, adj);
    i64 d = dist1[n];

    bool possible = false;
    for (auto& [u, v] : edges) {
        if (dist1[u] == INF || dist1[v] == INF) continue;
        if (dist1[u] != dist1[v]) continue; 

        bool uOnDag = (distT[u] != INF && dist1[u] + distT[u] == d);
        bool vOnDag = (distT[v] != INF && dist1[v] + distT[v] == d);

        if (uOnDag || vOnDag) {
            possible = true;
            break;
        }
    }

    cout << (possible ? "possible" : "impossible") << "\n";
}