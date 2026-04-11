#include "../include/KDTree.h"
#include <algorithm>
#include <cmath>

void KDTree::build(std::vector<Destination>& points) {
    if (points.empty()) return;
    
    root = buildRecursive(points.begin(), points.end(), 0);
}

std::unique_ptr<KDNode> KDTree::buildRecursive(
    std::vector<Destination>::iterator begin, 
    std::vector<Destination>::iterator end, 
    int depth) 
{
    if (begin == end) return nullptr;

    int axis = depth % 2;
    auto mid = begin + std::distance(begin, end) / 2;

    std::nth_element(begin, mid, end, [axis](const Destination& a, const Destination& b) {
        if (axis == 0) return a.x < b.x;
        return a.y < b.y;
    });

    auto node = std::make_unique<KDNode>(*mid);
    node->left = buildRecursive(begin, mid, depth + 1);
    node->right = buildRecursive(mid + 1, end, depth + 1);

    return node;
}

void KDTree::searchRecursive(KDNode* node, float x, float y, int k, int depth, std::vector<std::pair<float, Destination*>>& neighbors) {
    if (node == nullptr) return;

    float d = std::hypot(x - node->dest.x, y - node->dest.y);
    if (neighbors.size() < k || d < neighbors.back().first) {
        if (neighbors.size() >= k) neighbors.pop_back(); 
        neighbors.push_back({d, &(node->dest)});
        
        std::sort(neighbors.begin(), neighbors.end());
    }

    int axis = depth % 2;
    float diff = (axis == 0) ? (x - node->dest.x) : (y - node->dest.y);
    
    KDNode* near = (diff < 0) ? node->left.get() : node->right.get();
    KDNode* far = (diff < 0) ? node->right.get() : node->left.get();

    searchRecursive(near, x, y, k, depth + 1, neighbors);
    
    if (std::abs(diff) < neighbors.back().first || neighbors.size() < k) {
        searchRecursive(far, x, y, k, depth + 1, neighbors);
    }
}

std::vector<Destination*> KDTree::searchKNN(float x, float y, int k) {
    std::vector<std::pair<float, Destination*>> neighbors;
    searchRecursive(root.get(), x, y, k, 0, neighbors);

    std::vector<Destination*> result;
    for (auto& p : neighbors) result.push_back(p.second);
    return result;
}