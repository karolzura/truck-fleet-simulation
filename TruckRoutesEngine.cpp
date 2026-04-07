#include <iostream>
#include <vector>
#include <string>
#include <cmath>     
#include <fstream>
struct Destination {
    std:: string name; 
    float x, y;
    bool visited;

};

class RouteEngine{
    private:
        std::vector<Destination> dest;
    public:
        void loadDest(std::string& file);

        Destination getNextDest(float currX, float currY, float currFuel);

        float calculateSpeed(float currFuel, float speed);   


};