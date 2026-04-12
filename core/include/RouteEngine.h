#ifndef ROUTE_ENGINE_H
#define ROUTE_ENGINE_H

#include "KDTree.h"
#include "Destination.h"
#include <string>
#include <vector>

struct Assignment {
    std::string truck_id;
    Destination destination;
    float estimated_cost;
};

class RouteEngine {
public:
    RouteEngine() = default;

    void addOrder(const std::string& order_id, const std::string& city,
                  float x, float y, int priority, long long deadline_ts);

    void removeOrder(const std::string& order_id);

    Destination getNextTarget(const std::string& truck_id, float currX, float currY, float fuel, long long now_ts);

    Destination getNearestTarget(float currX, float currY);

    bool assignOrder(const std::string& truck_id, const std::string& order_id,
                     float currX, float currY, float fuel, long long now_ts);

    bool hasOrders() const;

    int pendingCount() const;

private:
    KDTree tree;
    std::vector<Destination> orders;

    void rebuildTree();
    float travelCost(float x1, float y1, float x2, float y2, float fuel) const;
};

#endif