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

int main() {
    i32 noOfContestants;
    i32 noOfJudges;
    cin >> noOfContestants >> noOfJudges;

    vector<Edge> edges;

    vector<pair<i32, i32>> votes(noOfJudges);

    for (int i = 0; i < noOfJudges; i++) {
        cin >> votes[i].first >> votes[i].second;
    }

    for (auto vote : votes) {
        i32 first = vote.first;
        i32 second = vote.second;

        Edge a = {first * -1, second};
        Edge b = {first, second * -1};

        edges.push_back(a);
        edges.push_back(b);
    }
}