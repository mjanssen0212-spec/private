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
    i32 noOfIntersections;
    i32 noOfStreets;

    cin >> noOfIntersections >> noOfStreets;

    vector<vector<i32>> matrix(noOfIntersections, vector<i32>(noOfIntersections, 0));

    for (int i = 0; i < noOfStreets; i++) {
        i32 from;
        i32 to;
        cin >> from >> to;
        matrix[from][to] = 1;
    }
}