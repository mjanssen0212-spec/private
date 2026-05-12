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
     i64 noOfPiesAvailable;

     for (int i = 0; i < noOfTestCases; i++) {
          i32 noOfHouseholds;
          i32 maxPonies = 0;

          cin >> noOfHouseholds >> noOfPiesAvailable;

          vector<i32> ponies(noOfHouseholds);

          for (int j = 0; j < noOfHouseholds; j++) {
               cin >> ponies[j];
               maxPonies = max(maxPonies, ponies[j]);
          }

          i32 left = 1;
          i32 right = maxPonies;

          while (left < right) {
               i32 mid = (left + right) / 2;
               i64 piesNeeded = 0;

               bool possible = true;
               for (i32 noPonies: ponies) {
                    piesNeeded += (noPonies + mid-1) / mid;

                    if (piesNeeded > noOfPiesAvailable) {
                         possible = false;
                         break;
                    }
               }

               if (possible) {
                    right = mid;
               } else {
                    left = mid + 1;
               }
          }

          cout << left << endl;

     }


}