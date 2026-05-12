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
//#define double einfachnichtbenutzen
// und los

int main() {

    i32 noOfTestCases;
    cin >> noOfTestCases;

    for (int i = 0; i < noOfTestCases; i++) {
        i32 noOfContestants;
        cin >> noOfContestants;

        vector<i32> points(noOfContestants);
        i32 totalPoints = 0;
        for (int j = 0; j < noOfContestants; j++) {
            cin >> points[j];
            totalPoints += points[j];
        }

        i32 requiredPoints = (totalPoints*2)/noOfContestants;
        i32 max = *max_element(points.begin(), points.end());
        if (max >= requiredPoints) {
            requiredPoints = ((totalPoints-max)+totalPoints)/(noOfContestants-1);
        }

        for (int j = 0; j < noOfContestants; j++) {
            if (points[j] >= requiredPoints) {
                cout << "0 ";
                continue;
            }

            i32 missingPoints = requiredPoints - points[j];

            cout << setprecision(10) << ((long double)missingPoints / totalPoints) * 100 << " ";
        }

        cout << endl;

    }

}