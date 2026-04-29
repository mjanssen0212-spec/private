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

    vector<vector<i64>> snowflakeCases(noOfTestCases);

    for (int i = 0; i < noOfTestCases; i++) {
        i32 n;

        cin >> n;
        vector<i64> snowflakes(n);

        for (int j = 0; j < n; j++) {
            cin >> snowflakes[j];
        }

        snowflakeCases[i] = snowflakes;
    }

    for (int i = 0; i < noOfTestCases; i++) {
        const vector<i64>& snowflakes = snowflakeCases[i];
        set<i64> box;
        i32 leftBound = 0;
        i32 maxBoxSize = 0;

        for (int rightBound = 0; rightBound < snowflakes.size(); rightBound++) {

            while (box.count(snowflakes[rightBound]) > 0) {
                box.erase(snowflakes[leftBound]);
                leftBound++;
            }

            box.insert(snowflakes[rightBound]);

            maxBoxSize = max(maxBoxSize, rightBound - leftBound + 1);
        }

        cout << maxBoxSize << endl;
    }
}