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

using Graph = vector<vector<double>>;
const double INF = 1e9;

Graph floyd_warshall(Graph dist) {
    i64 n = dist.size();
    for (i64 k = 0; k < n; k++)
        for (i64 i = 0; i < n; i++)
            for (i64 j = 0; j < n; j++)
                if (dist[i][k] + dist[k][j] < dist[i][j])
                    dist[i][j] = dist[i][k] + dist[k][j];
    return dist;
}

int main() {
    i64 noOfTestCases;

    cin >> noOfTestCases;

    for (int i = 1; i <= noOfTestCases; i++) {
        i64 noOfSettlements;
        cin >> noOfSettlements;

        vector<pair<double, double>> settlements(noOfSettlements);
        vector<vector<double>> matrix(noOfSettlements, vector<double>(noOfSettlements, INF));

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
                auto dist = sqrt(((double)settlement.first - (double)settlement2.first) * ((double)settlement.first - (double)settlement2.first)
                    + ((double)settlement.second - (double)settlement2.second) * ((double)settlement.second - (double)settlement2.second));

                if (dist > 10) {
                    dist = INF;
                }

                matrix[k][l] = dist;
            }
        }

        Graph distances = floyd_warshall(matrix);

        double max = 0;

        for (auto& row : distances) {
            for (auto& dist : row) {
                if (dist > max) {
                    max = dist;
                }
                if (max >= INF/2) {
                    break;
                }
            }
        }
        cout << "Case #" << i << ": " << endl;
        if (max >= INF/2) {
            cout << "Abandon Quest" << endl;
        } else {
            cout << fixed << setprecision(4) << max << endl;
        }

        cout << endl;
    }

}