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
    i32 noOfPieces;
    cin >> noOfPieces;

    vector<string> pieces(noOfPieces);
    i32 invalidPieces = 0;
    i32 lastIndex = 0;


    for (int i = 0; i < noOfPieces; i++) {
        string piece;
        cin >> piece;


        stack<char> isValid;
        bool brokeLoop = false;
        for (char c : piece) {
            if (c == '(') {
                isValid.push(c);
            } else {
                if (isValid.empty()) {
                    pieces[lastIndex] = piece;
                    lastIndex++;
                    invalidPieces++;
                    brokeLoop = true;
                    break;
                }
                isValid.pop();
                }
        }

        if (!isValid.empty() && !brokeLoop) {
            pieces[lastIndex] = piece;
            lastIndex++;
            invalidPieces++;
        }
    }

    if (invalidPieces == 0) {
        cout << "YES" << endl;
        return 0;
    }

    i32 noOfOpen = 0;
    i32 noOfClose = 0;

    for (string piece : pieces) {
        noOfOpen += count(piece.begin(), piece.end(), '(');
        noOfClose += count(piece.begin(), piece.end(), ')');
    }

    if (noOfOpen != noOfClose) {
        cout << "NO" << endl;
        return 0;
    }

    bool validStart = false;
    bool validEnd = false;

    stack <i32> onlyOpen;
    stack <i32> onlyClose;

    for (string piece : pieces) {
        if (validStart && validEnd) {
            break;
        }



        if (piece.front() == '(') {
            stack<char> isValidStart;

            for (char c : piece) {
                if (c == '(') {
                    isValidStart.push(c);
                } else {
                    if (isValidStart.empty()) {
                        break;
                    } else {
                        isValidStart.pop();
                    }
                }
            }

            if (!isValidStart.empty()) {
                validStart = true;
            }

        } else if (piece.back() == ')'){
            validEnd = true;
        }
    }

    if (validStart && validEnd) {
        cout << "YES" << endl;
    } else {
        cout << "NO" << endl;
    }

    return 0;
}