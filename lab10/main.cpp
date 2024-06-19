#include <iostream>

#include "listops.h"



using listops::Node;


Node * list_from_args(int argc, char *argv[]) {
    int vals[argc];

    for (int i = 0; i < argc; i++)
        vals[i] = atoi(argv[i]);

    Node *h;
    listops::mklist(argc, vals, h);

    return h;
}

void print_list(Node *h) {
    for ( ; h != NULL; h = h->next)
        std::cout << h->val << " ";
    std::cout << std::endl;
}


int main(int argc, char *argv[]) {

    Node *h = list_from_args(argc-1, argv+1);

    print_list(h);

    listops::reverse(h, h);

    print_list(h);
}

