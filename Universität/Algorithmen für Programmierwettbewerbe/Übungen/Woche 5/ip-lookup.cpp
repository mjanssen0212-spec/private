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

struct Node {
    int child[2];
    bool is_wildcard;
    bool is_exact;

    Node() {
        child[0] = -1;
        child[1] = -1;
        is_wildcard = false;
        is_exact = false;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<Node> trie;
    trie.emplace_back();

    for (int i = 0; i < n; i++) {
        string s;
        cin >> s;

        int current = 0;

        for (char c : s) {
            if (c == '*') {
                trie[current].is_wildcard = true;
                break;
            }

            int bit = c - '0';

            if (trie[current].child[bit] == -1) {
                trie[current].child[bit] = trie.size();
                trie.emplace_back();
            }

            current = trie[current].child[bit];
        }

        if (s.back() != '*') {
            trie[current].is_exact = true;
        }
    }

    int m;
    cin >> m;

    while (m--) {
        string ip;
        cin >> ip;

        int current = 0;
        bool found = trie[current].is_wildcard;
        bool full_match = false;

        for (int i = 0; i < (int)ip.size(); i++) {
            int bit = ip[i] - '0';

            if (trie[current].child[bit] == -1) break;

            current = trie[current].child[bit];

            if (trie[current].is_wildcard) {
                found = true;
                break;
            }

            if (i == (int)ip.size() - 1) {
                full_match = true;
            }
        }

        if (!found && full_match) {
            found = trie[current].is_exact;
        }

        cout << (found ? "Yes" : "No") << '\n';
    }

    return 0;
}