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
    cin.ignore();

    while (noOfTestCases > 0) {
        noOfTestCases--;

        string pattern, text;

        getline(cin, pattern);
        getline(cin, text);

        i32 delimPos = -1;
        bool isPlus = false;

        for (int j = 0; j < (i32)pattern.size(); j++) {
            if (pattern[j] == '*' || pattern[j] == '+') {
                delimPos = j;
                isPlus = (pattern[j] == '+');
                break;
            }
        }


        if (delimPos == -1) {
            cout << (pattern == text ? "yes" : "no") << '\n';
            continue;
        }

        string prefix = pattern.substr(0, delimPos);
        string suffix = pattern.substr(delimPos + 1);

        i32 minLen = (i32)prefix.size() + (i32)suffix.size() + (isPlus ? 1 : 0);

        if ((i32)text.size() < minLen) {
            cout << "no\n";
            continue;
        }

        bool isMatch = true;

        if (text.substr(0, prefix.size()) != prefix) {
            isMatch = false;
        }

        if (isMatch && !suffix.empty()) {
            if (text.substr(text.size() - suffix.size()) != suffix) {
                isMatch = false;
            }
        }

        cout << (isMatch ? "yes" : "no") << '\n';
    }
}