#include <iostream>
#include <vector>
#include <string>
#include <cmath>     
#include <fstream>
#include <sstream>
#include <algorithm>
int DestQuantity = 1000;

struct Destination {
    std:: string name; 
    float x, y;
    int priority;
    bool visited = false;

};

class RouteEngine{
    private:
        std::vector<Destination> dest;
    public:
        void loadDest(const std::string& File){
            std::ifstream file(File);
            if(!file.is_open()) throw std::runtime_error("No file loaded");
            dest.reserve(DestQuantity);
            std::string line;
            while(std::getline(file,line)){
                if(line.empty()) continue;
                std::stringstream ss(line);
                std::string name, x_str, y_str, priority_str;
                if(std::getline(ss, name, ',') && 
                std::getline(ss, x_str, ',') && 
                std::getline(ss, y_str, ',') && 
                std::getline(ss, priority_str,',')){
                    try{
                        dest.push_back({
                            name, std::stof(x_str),std::stof(y_str),std::stoi(priority_str)
                        });
                    }
                    catch(...){continue;}
                }


                
            }
        }

        Destination getNextDest(float currX, float currY, float currFuel){
            Destination* best = nullptr;
            float max = -1.0f;
            for(auto& d:dest){
                if(d.visited) continue;
                float dist = std::hypot(currX - d.x,currY - d.y);
                float score = d.priority/(dist +0.1f);
                if(dist>(currFuel*10)) continue;
                if(score>max){
                    max = score;
                    best =&d;
                }
            }
            if(best != nullptr){
                best->visited = true;
                return *best;
            }
            return {"BASE",0.0f, 0.0f,0,true};  
        }

        float calculateSpeed(float currFuel, float speed);   


};

int main(){
    return 0;
}