#include <iostream>
#include <vector>
#include <string>
#include <cmath>     
#include <fstream>
/*struct Destination {
    std:: string name; 
    float x, y;
    int priority;
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

void RouteEngine:: loadDest(std::string& file){
    dest.reserve(1000);

}
*/
int main(){
    std::fstream File;
    File.open("destinations.txt", std::ios::in);
    std::string dane;
    getline(File,dane);
    std::cout<<dane;
    return 0;
}