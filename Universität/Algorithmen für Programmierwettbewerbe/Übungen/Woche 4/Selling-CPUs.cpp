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
    i32 noOfCPUs;
    i32 noOfMerchants;
    cin >> noOfCPUs >> noOfMerchants;

    vector<vector<i32>> prices(noOfMerchants, vector<i32>(noOfCPUs));

    for (int i = 0; i < noOfMerchants; i++) {
        for (int j = 0; j < noOfCPUs; j++) {
            cin >> prices[i][j];
        }
    }

}