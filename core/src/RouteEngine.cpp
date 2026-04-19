#include "../include/RouteEngine.h"
#include <cmath>
#include <algorithm>
#include <limits>

void RouteEngine::rebuildTree() {
    tree.build(orders);
}

float RouteEngine::travelCost(float x1, float y1, float x2, float y2, float fuel) const {
    float dist = std::hypot(x1 - x2, y1 - y2);
    float fuel_cost = dist * 0.3f;
    return dist + fuel_cost;
}

void RouteEngine::addOrder(const std::string& order_id, const std::string& city,
                            float x, float y, int priority, long long deadline_ts) {
    orders.emplace_back(city, order_id, x, y, priority, deadline_ts);
    rebuildTree();
}

void RouteEngine::removeOrder(const std::string& order_id) {
    orders.erase(
        std::remove_if(orders.begin(), orders.end(),
            [&](const Destination& d) { return d.order_id == order_id; }),
        orders.end()
    );
    rebuildTree();
}

bool RouteEngine::hasOrders() const {
    return std::any_of(orders.begin(), orders.end(),
        [](const Destination& d) { return !d.visited; });
}

int RouteEngine::pendingCount() const {
    return (int)std::count_if(orders.begin(), orders.end(),
        [](const Destination& d) { return !d.visited; });
}

Destination RouteEngine::getNextTarget(const std::string& truck_id,
                                        float currX, float currY,
                                        float fuel, long long now_ts) {
    if (orders.empty()) return Destination("BASE", "", 0, 0, 0, 0);

    auto candidates = tree.searchKNN(currX, currY, (int)orders.size());

    Destination* best = nullptr;
    float bestScore = std::numeric_limits<float>::lowest();

    for (auto* c : candidates) {
        if (c->visited) continue;

        float dist = std::hypot(currX - c->x, currY - c->y);
        if (dist > fuel * 10.0f) continue;

        long long time_remaining = c->deadline_ts - now_ts;
        if (time_remaining <= 0) {
            c->skip_count++;
            continue;
        }

        float urgency = 1.0f / (float)(time_remaining + 1);
        float cost    = travelCost(currX, currY, c->x, c->y, fuel);
        float score   = ((float)c->priority * urgency * 1000.0f) - cost + (float)c->skip_count * 0.5f;

        if (score > bestScore) {
            bestScore = score;
            best = c;
        } else {
            c->skip_count++;
        }
    }

    if (best) {
        best->visited = true;
        return *best;
    }
    return Destination("BASE", "", 0, 0, 0, 0);
}

Destination RouteEngine::getNearestTarget(float currX, float currY) {
    if (orders.empty()) return Destination("BASE", "", 0, 0, 0, 0);

    auto candidates = tree.searchKNN(currX, currY, (int)orders.size());

    Destination* nearest = nullptr;
    float minDist = std::numeric_limits<float>::max();

    for (auto* c : candidates) {
        if (c->visited) continue;
        float dist = std::hypot(currX - c->x, currY - c->y);
        if (dist < minDist) {
            minDist = dist;
            nearest = c;
        }
    }

    if (nearest) {
        nearest->visited = true;
        return *nearest;
    }
    return Destination("BASE", "", 0, 0, 0, 0);
}

bool RouteEngine::assignOrder(const std::string& truck_id, const std::string& order_id,
                               float currX, float currY, float fuel, long long now_ts) {
    for (auto& d : orders) {
        if (d.order_id == order_id && !d.visited) {
            float dist = std::hypot(currX - d.x, currY - d.y);
            if (dist > fuel * 10.0f) return false;
            d.visited = true;
            return true;
        }
    }
    return false;
}