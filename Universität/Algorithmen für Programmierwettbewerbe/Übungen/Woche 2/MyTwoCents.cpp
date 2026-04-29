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
    i32 noOfPiles;
    cin >> noOfPiles;

    if (noOfPiles < 2 || noOfPiles > 50) {
        return 0;
    }

    i32 sum = 0;

    i32 piles[noOfPiles];
    string noOfCoins;

    for (int i = 0; i < noOfPiles; i++) {
        cin >> piles[i];

        if (piles[i] < 0) {
            return 0;
        }
    }

    int max = piles[0];
    int maxIndex = 0;

    for ( int i = 1; i < noOfPiles; i++) {
        if (max < piles[i]) {
            max = piles[i];
            maxIndex = i;
        }
    }

    for (int i = 0; i < noOfPiles; i++) {
        sum += piles[i];
    }

    if (sum % 2 == 0 && sum - max >= max) {
        cout << "yes" << endl;

        for (int j = 0; j < sum/2; j++) {
            i32 currentMax = piles[0];
            maxIndex = 0;
            i32 secondMax = 0;
            i32 secondMaxIndex = -1;

            for (int i = 1; i < noOfPiles; i++) {

                if (currentMax < piles[i]) {
                    secondMax = currentMax;
                    secondMaxIndex = maxIndex;
                    maxIndex = i;
                    currentMax = piles[i];
                }
                else if (secondMax < piles[i]) {
                    secondMax = piles[i];
                    secondMaxIndex = i;
                }
            }

            piles[secondMaxIndex] = piles[secondMaxIndex] - 1;
            piles[maxIndex] = piles[maxIndex] - 1;

            if (maxIndex > secondMaxIndex) {
                cout << secondMaxIndex + 1 << " " << maxIndex + 1 << endl;
            } else {
                cout << maxIndex + 1 << " " << secondMaxIndex + 1 << endl;
            }
        }
    }
    else {
        cout << "no" << endl;
    }

}