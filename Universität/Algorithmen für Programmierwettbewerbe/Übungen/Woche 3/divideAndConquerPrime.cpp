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
i32 noOfFactors;

long long mul_mod(long long a, long long b, long long m) {
    // Wenn verfügbar, nutze __int128 für 128-Bit Arithmetik
    return (__int128)a * b % m;
}

long long power(long long base, long long exp, long long mod) {
    long long res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp % 2 == 1) res = mul_mod(res, base, mod);
        base = mul_mod(base, base, mod);
        exp /= 2;
    }
    return res;
}

bool isPrime(i64 n) {
    if (n <= 1) {
        return false;
    }

    if (n == 2 || n == 3) {
        return true;
    }

    if (n % 2 == 0) {
        return false;
    }

    i64 d = n - 1;

    i64 s = 0;

    while (d%2 == 0) {
        d = d/2;
        s++;
    }

    vector<i32> primes = {2, 3, 5, 7, 11, 13, 17, 19, 23};

    for (i32 prime : primes) {
        if (prime >= n) {
            continue;
        }

        i64 x = power(prime, d, n);

        if (x == 1 || x == n - 1) {
            continue;
        }

        bool probablyPrime = false;

        for (i32 i = 1; i < s; i++) {
            x = mul_mod(x, x, n);
            if (x == n - 1) {
                probablyPrime = true;
                break;
            }
        }

        if (!probablyPrime) {
            return false;
        }
    }

    return true;
}

i64 findeFaktor(i64 n, i32 constant) {
    i64 x = 2;
    i64 y = 2;
    i64 ggT = 1;

    while (ggT == 1) {
        x = (mul_mod(x, x, n) + constant) % n;
        y = (mul_mod(y, y, n) + constant) % n;
        y = (mul_mod(y, y, n) + constant) % n;

        ggT = gcd((x > y ? x - y : y - x), n);

        if (ggT == n) {
            return findeFaktor(n, constant + 1);
        }
    }

    return ggT;
}

map<i64, i64> findePrimeFaktor(i64 n) {
    map<i64, i64> primeFactors = map<i64, i64> {};
    i64 rest = n;

    while (rest%2==0) {
        rest = rest/2;
        primeFactors[2] = primeFactors[2]+1;
    }

    while (rest > 1) {
            if (isPrime(rest)) {
                primeFactors[rest] = primeFactors[rest]+1;
                break;
            }

            i64 faktor = findeFaktor(rest, 1);

            if (isPrime(faktor)) {
                primeFactors[faktor] = primeFactors[faktor]+1;
            } else {

            map helper = findePrimeFaktor(faktor);

            for (auto& [key, value] : helper) {
                primeFactors[key] = primeFactors[key]+value;
            }
        }

        rest = rest/faktor;
    }

    return primeFactors;
}


int main() {

    cin >> sizeOfArmy >> noOfFactors;

    map<i64, i64> worldPrimeFactors = map<i64, i64> {};

    for (int i = 0; i < noOfFactors; i++){
        i64 key;
        i64 value;
        cin >> key >> value;
        worldPrimeFactors[key] = value;
    }

    map<i64, i64> armyPrimeFactors = findePrimeFaktor(sizeOfArmy);

    i64 maxDivide = 1;

    for (auto& [key, value] : armyPrimeFactors) {
        i64 valueWorld = worldPrimeFactors[key];

        if (valueWorld != 0) {
            for (i64 i = 0; i < min(value, valueWorld); i++) {
                maxDivide *= key;
            }
        }
    }

    cout << maxDivide << endl;

}