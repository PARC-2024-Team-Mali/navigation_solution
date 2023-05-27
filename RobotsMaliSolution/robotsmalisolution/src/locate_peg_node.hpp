#include "ros/ros.h"
#include "parc_robot/gps2cartesian.h"
#include <unordered_map>
#include "map"


std::unordered_map<std::string, std::map<std::string, double> > gps;
std::unordered_map<std::string, std::pair<double, double> > cartesian;

void get_gps(const std::string& name) {
   
    
    std::map<std::string, double> m;

    ros::param::get(name, m);
   

    gps[name] = m;

}

void goal_obs() {

    double lati, longi;
     
    ros::param::get("goal_longitude", longi);
    ros::param::get("goal_latitude", lati);

    gps["goal"]["longitude"] = longi;
    gps["goal"]["latitude"] = lati;


    get_gps("peg_A");
    get_gps("peg_B");

    for (int i = 1; i <= 8; ++i){

        get_gps("peg_0" + std::to_string(i));
        
    }
   

}

void get_cordinate() {

    goal_obs();

    for (const auto& g : gps){

        auto position = gps_to_cartesian(gps[g.first]["latitude"], gps[g.first]["longitude"]) ;

        cartesian[g.first] = std::make_pair(position.x, position.y) ;
    }


}
