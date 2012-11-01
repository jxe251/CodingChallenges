/*
 * Input comes from stin as two lists of comma-separated integers.
 * The lists are ascending sorted.
 * For an even number of elements, return the lesser of the two.
 *
 * example:
 *   4,5,8
 *   -1,3
 * output:
 *   4
 */

#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>

using namespace std;

vector<int> ReadInput() {
    vector<int> arr;
    string str, item;
    getline(cin, str);
    stringstream ss(str);
    while (getline(ss, item, ','))
        arr.push_back(atoi(item.c_str()));
    return arr;
}

int Median(const vector<int> &sortedVec) {
   int idxLo = 0;
   int idxHi = sortedVec.size() - 1;
   while (idxLo != idxHi) {
       --idxHi;
       if (idxLo == idxHi) break;
       ++idxLo;
   }
   return sortedVec[idxLo];
}

/*
 * Assuming sorted
 */
int MedOfTwoVectors(const vector<int> &sortedA, const vector<int> &sortedB) {
    int idxLoA = 0;
    int idxHiA = sortedA.size() - 1;
    int idxLoB = 0;
    int idxHiB = sortedB.size() - 1;
    int idxLo = 0;
    int idxHi = sortedA.size() + sortedB.size() - 1;

    // cases where vec.size() == 0
    if (idxHiA == -1 && idxHiB == -1) {
        return 0;
    } else if (idxHiA == -1) {
        return Median(sortedB);
    } else if (idxHiB == -1) {
        return Median(sortedA);
    }

    while (idxLo != idxHi) {
        // pop greatest
        auto tmpHiA = idxHiA;
        idxHiA -= sortedA[tmpHiA] >= sortedB[idxHiB];
        idxHiB -= sortedA[tmpHiA] < sortedB[idxHiB];
        --idxHi;
    
        // check if found
        if (idxLo == idxHi) break;

        // pop least
        auto tmpLoA = idxLoA;
        idxLoA += sortedA[tmpLoA] <= sortedB[idxLoB];
        idxLoB += sortedA[tmpLoA] > sortedB[idxLoB];
        ++idxLo;
    }
    // the find condition idxLo == idxHi is:
    // equiv to idxHiB < idxLoB,
    // equiv to !(idxLoB == idxLoB)
    // equiv to !(idxHiA < idxLoA)
    return idxLoA == idxHiA ? sortedA[idxLoA] : sortedB[idxLoB]; 
}

int main() {
    auto arrA = ReadInput();
    auto arrB = ReadInput();
    int median = MedOfTwoVectors(arrA, arrB);
    cout << median << endl;
    return 0;
}
