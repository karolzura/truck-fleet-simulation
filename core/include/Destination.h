#ifndef DESTINATION_H
#define DESTINATION_H

#include <string>

struct Destination {
    std::string name;
    std::string order_id;
    float x, y;
    int priority;
    long long deadline_ts;
    bool visited = false;
    int skip_count = 0;

    Destination(std::string n, std::string oid, float _x, float _y, int p, long long dl)
        : name(n), order_id(oid), x(_x), y(_y), priority(p), deadline_ts(dl) {}
};

#endif