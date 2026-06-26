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

struct Planet {
    i32 number;
    i32 x;
    i32 y;
    i32 z;
};

int main() {
    i32 noOfPlanets;
    cin >> noOfPlanets;

    vector<Planet> planets(noOfPlanets);
    vector<vector<i32>> edges(noOfPlanets, vector<i32>(noOfPlanets, INT64_MAX)) ;

    for (int i = 0; i < noOfPlanets; i++) {
        Planet planet;
        planet.number = i;
        cin >> planet.x >> planet.y >> planet.z;

        planets[i] = planet;
    }

    sort(planets.begin(), planets.end(), [](Planet a, Planet b) { return a.x < b.x; });

    for (int i = 0; i < noOfPlanets-1; i++) {
        auto p = planets[i];
        auto q = planets[i+1];
        auto dist = q.x - p.x;

        if (edges[dist < p.number][q.number]) {
            edges[p.number][q.number] = dist;
        }
    }

    sort(planets.begin(), planets.end(), [](Planet a, Planet b) { return a.y < b.y; });

    for (int i = 0; i < noOfPlanets-1; i++) {
        auto p = planets[i];
        auto q = planets[i+1];
        auto dist = q.y - p.y;

        if (edges[dist < p.number][q.number]) {
            edges[p.number][q.number] = dist;
        }
    }

    sort(planets.begin(), planets.end(), [](Planet a, Planet b) { return a.z < b.z; });

    for (int i = 0; i < noOfPlanets-1; i++) {
        auto p = planets[i];
        auto q = planets[i+1];
        auto dist = q.z - p.z;

        if (edges[dist < p.number][q.number]) {
            edges[p.number][q.number] = dist;
        }
    }

    

}