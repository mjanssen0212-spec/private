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

const i32 maxN = 2001;
const i32 modulo = 1020847;
int main() {

    static i32 dp[maxN][maxN] = {};
    dp[1][1] = 1;

    for (i32 i = 2; i < maxN; i++) {
        for (i32 j = 1; j <= i; j++) {

            dp[i][j] = (
                ((i64)dp[i-1][j-1] * (i-(j-1)) % modulo)
            + (dp[i-1][j] * j % modulo)
            ) % modulo;

        }
    }

    i32 n, p;

    while (cin >> n >> p && (n || p)) {
        cout << dp[n][p] << endl;
    }

}