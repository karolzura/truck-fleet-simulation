#ifndef DESTINATION_H
#define DESTINATION_H

#include <string>

struct Destination {
    std::string name;
    float x, y;
    int priority;
    bool visited = false;
    int skip_count = 0;

    Destination(std::string n, float _x, float _y, int p) 
        : name(n), x(_x), y(_y), priority(p) {}
};

#endif