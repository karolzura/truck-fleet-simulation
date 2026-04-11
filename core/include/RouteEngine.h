#ifndef ROUTE_ENGINE_H
#define ROUTE_ENGINE_H

#include "KDTree.h"
#include "Destination.h"
#include <string>
#include <vector>

class RouteEngine {
public:
    RouteEngine() = default;

    void loadDestinations(const std::string& filePath);

    Destination getNextTarget(float currX, float currY, float fuel);

private:

    KDTree tree;
    float calculateScore(const Destination& d, float dist);
};

#endif