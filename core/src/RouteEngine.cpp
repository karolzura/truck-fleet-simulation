#include "../include/RouteEngine.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <cmath>
void RouteEngine::loadDestinations(const std::string& filePath) {
    std::vector<Destination> points;
    std::ifstream file(filePath);
    
    if (!file.is_open()) return;

    std::string line;
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string name, x_s, y_s, p_s;
        
        if (std::getline(ss, name, ',') && 
            std::getline(ss, x_s, ',') && 
            std::getline(ss, y_s, ',') && 
            std::getline(ss, p_s, ',')) {
            
            points.emplace_back(name, std::stof(x_s), std::stof(y_s), std::stoi(p_s));
        }
    }

    tree.build(points);
}

Destination RouteEngine::getNextTarget(float currX, float currY, float fuel) {
    auto candidates = tree.searchKNN(currX, currY, 5);
    
    Destination* best = nullptr;
    float maxScore = -1.0f;

    for (auto* c : candidates) {
        if (c->visited) continue;

        float dist = std::hypot(currX - c->x, currY - c->y);
        

        if (dist > fuel * 10.0f) continue;
        float score = (c->priority + c->skip_count) / (dist + 0.1f);

        if (score > maxScore) {
            maxScore = score;
            best = c;
        } else {
            c->skip_count++; 
        }
    }

    if (best) {
        best->visited = true;
        return *best;
    }
    return Destination("BASE", 0, 0, 0);
}