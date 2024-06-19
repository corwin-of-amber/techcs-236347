#include <iostream>

#include "scanner.h"


int main(int argc, char *argv[]) {
    std::string s;
    bool result;
    std::cerr << "Type in some words (one per line):" << std::endl;
    while (1) {
        std::getline(std::cin, s);
        if (!std::cin.good()) break;
        ANONYMOUS::match(s.size(), (char*)s.c_str(), result);
        std::cout << " = " << result << std::endl;
    }
}

