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
    i64 noOfTestCases;

    cin >> noOfTestCases;

    for (int i = 1; i <= noOfTestCases; i++) {
        i64 noOfSettlements;
        cin >> noOfSettlements;

        vector<pair<i64, i64>> settlements(noOfSettlements);
        vector<vector<i64>> matrix(noOfSettlements, vector<i64>(noOfSettlements, 10000));

        for (int j = 0; j < noOfSettlements; j++) {
            i64 x;
            i64 y;
            cin >> x >> y;

            settlements[j].first = x;
            settlements[j].second = y;
        }

        for (int k = 0; k < noOfSettlements; k++) {
            auto settlement = settlements[k];
            for (int l = 0; l < noOfSettlements; l++) {
                auto settlement2 = settlements[l];
                auto dist = sqrt((settlement.first - settlement2.first) * (settlement.first - settlement2.first)
                    + (settlement.second - settlement2.second) * (settlement.second - settlement2.second));

                if (dist > 10) {
                    dist = 10000;
                }

                matrix[k][l] = dist;
            }
        }
    }

}