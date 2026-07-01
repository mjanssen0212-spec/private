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

struct Edge {
    i32 u;
    i32 v;
};

using Graph = vector<vector<i64>>;

i64 counter = 0;



void dfs1(i64 u, Graph& adjList, vector<bool>& visited,
stack<i64>& s) {
    if (visited[u])
        return;
    visited[u] = true;
    for (i64 v: adjList[u])
        dfs1(v, adjList, visited, s);
    s.push(u);
}
void dfs2(i64 u, Graph& adjList, vector<bool>& visited,
vector<i64>& component) {
    if (visited[u])
        return;
    visited[u] = true;
    for (i64 v: adjList[u])
        dfs2(v, adjList, visited, component);
    component[u] = counter;
}

void addEdge(i64 a, i64 b, i64 n, Graph& adjList) {
    // map a literal to its node index in the implication graph
    i64 u = (a > 0) ? a : n - a;
    i64 v = (b > 0) ? b : n - b;
    adjList[u].push_back(v);
}

vector<i64> kosaraju(i64 n, Graph& adjList) {
    vector<bool> visited(n, false);
    vector<bool> visitedInv(n, false);
    Graph adjInv(n);
    stack <i64> s;
    vector<i64> component(n);

    // Create inverted graph
    for (i64 u = 0; u < n; u++)
        for (i64 v : adjList[u])
            adjInv[v].push_back(u);
    // first traverse the graph
    for (int i = 0; i < n; i++)
        if (!visited[i])
            dfs1(i, adjList, visited, s);
    // then traverse the inverted graph
    while (!s.empty()) {
        i64 u = s.top();
        s.pop();
        if (!visitedInv[u]) {
            dfs2(u, adjInv, visitedInv, component);
            counter++;
        }
    }
    return component;
}

bool solve(i64 n, vector<pair<i64,i64>>& clauses) {
    // Create graph
    Graph adjList = Graph(2*n+1);
    for (auto& [x,y] : clauses) {
        // variable −x is mapped to n+x = n−(−x)
        addEdge(-x, y, n, adjList);
        addEdge(-y, x, n, adjList);

    }
    vector<i64> component = kosaraju(2*n+1, adjList);
    for (i64 i = 1; i <= n; i++) {
        // check whether 2 variables lie in the same component
        if (component[i] == component[i + n]) {
            return false;
        }
    }
    return true;
}

int main() {
    i32 noOfContestants;
    i32 noOfJudges;

    while (cin >> noOfContestants >> noOfJudges) {
        vector<pair<i64, i64>> votes(noOfJudges+1);

        votes[0] = {1,1};

        for (int i = 1; i <= noOfJudges; i++) {
            cin >> votes[i].first >> votes[i].second;
        }


        if (solve(noOfContestants, votes)) {
            cout << "yes" << endl;
        } else {
            cout << "no" << endl;
        }
    }
}
