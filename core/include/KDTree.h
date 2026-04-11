#ifndef KDTREE_H
#define KDTREE_H

#include "Destination.h"
#include <vector>
#include <memory>

struct KDNode {
    Destination dest;
    std::unique_ptr<KDNode> left;
    std::unique_ptr<KDNode> right;

    KDNode(Destination d) : dest(d), left(nullptr), right(nullptr) {}
};

class KDTree {
public:
    void build(std::vector<Destination>& points);


    std::vector<Destination*> searchKNN(float x, float y, int k);

private:
    std::unique_ptr<KDNode> root;
    
    std::unique_ptr<KDNode> buildRecursive(
    std::vector<Destination>::iterator begin, 
    std::vector<Destination>::iterator end, 
    int depth
    );
    
    void searchRecursive(
        KDNode* node, 
        float x, float y, 
        int k, 
        int depth, 
        std::vector<std::pair<float, Destination*>>& neighbors
    );
};

#endif