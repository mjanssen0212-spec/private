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

    i32 noOfTestCases;
    cin >> noOfTestCases;

    for (int i = 0; i < noOfTestCases; i++) {
        // i32 totalCoins = 0;
        i32 noOfMonsters;
        cin >> noOfMonsters;

        vector<i32> coins(noOfMonsters);

        for (int j = 0; j < noOfMonsters; j++) {
            cin >> coins[j];

        }

        vector<pair<i32, i32>> buffer(noOfMonsters);

        for (int j = 0; j < noOfMonsters; j++) {
            if (j == 0) {
                buffer[j].first = 0;
                buffer[j].second = coins[j];
                continue;
            }

            buffer[j].first = max(buffer[j-1].first, buffer[j-1].second);
            buffer[j].second = buffer[j-1].first + coins[j];
        }


        cout << max(buffer[noOfMonsters-1].first, buffer[noOfMonsters-1].second) << endl;

    }

}