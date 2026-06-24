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

int main() {
    i32 noOfContestants;
    i32 noOfJudges;
    cin >> noOfContestants >> noOfJudges;

    vector<pair<i32, i32>> votes(noOfJudges);

    for (int i = 0; i < noOfJudges; i++) {
        cin >> votes[i].first >> votes[i].second;
    }

    
}