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

i64 sizeOfArmy;
i64 noOfFactors;
i64 maxTeilerGlobal = 1;
vector<pair<i64, i64>> primeFactors;

void teiler(i64 index, __int128 currentMaxTeiler) {

    if (index >= noOfFactors)
        return;


    teiler(index + 1, currentMaxTeiler);

    i64 factor = primeFactors[index].first;
    i64 amount = primeFactors[index].second;

    __int128 tempMax = currentMaxTeiler;

    for (i64 i = 0; i < amount; i++) {
        tempMax *= factor;
        if (tempMax > sizeOfArmy) break;

        if (tempMax >= maxTeilerGlobal) {
            maxTeilerGlobal = tempMax;
        }
        teiler(index + 1, tempMax);
    }

}

int main() {

    cin >> sizeOfArmy >> noOfFactors;

    primeFactors.resize(noOfFactors);

    for (int i = 0; i < noOfFactors; i++){
        i64 key;
        i64 value;
        cin >> key >> value;
        primeFactors[i].first = key;
        primeFactors[i].second = value;
    }

    teiler(0, 1);

    cout << maxTeilerGlobal << endl;
}