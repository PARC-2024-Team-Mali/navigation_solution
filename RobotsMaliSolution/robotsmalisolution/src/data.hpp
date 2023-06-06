#include <ros/ros.h>
#include <vector>
#include <unordered_map>
#include <string>
#include <array>
#include <tuple>
#include "math_module.hpp"
#include "locate_peg_node.hpp"



using namespace std;

vector<double> route_1_x;
vector<double> route_1_y; 



vector<double> route_2_x; 
vector<double> route_2_y; 

vector<double> route_3_x;
vector<double> route_3_y;

//get the cartesian value of the peg.
complex<double> get_values(const string& name){

    get_cordinate();

    return complex<double>(cartesian[name].first, cartesian[name].second);
}


void done() {

    complex<double> goal(get_values("goal"));

    complex<double> goal_1(get_values("peg_01"));
    complex<double> goal_2(get_values("peg_02"));
    complex<double> goal_3(get_values("peg_03"));
    complex<double> goal_4(get_values("peg_04"));
    complex<double> goal_5(get_values("peg_05"));
    complex<double> goal_6(get_values("peg_06"));
    complex<double> goal_7(get_values("peg_07"));
    complex<double> goal_8(get_values("peg_08"));

    //cout  << goal_1.real()  << " "  << goal_1.imag()  << endl;
    //cout  << goal_2.real()  << " "  << goal_2.imag()  << endl;

    complex<double> obstacle_1 = (get_values("peg_A"));
    complex<double> obstacle_2 = (get_values("peg_B"));

    //cout  << obstacle_1.real()  << " "  << obstacle_1.imag()  << endl;

    complex<double> val_1(get_middle(goal_1, goal_4));
    complex<double> val_2(get_middle(goal_2, goal_3));
    complex<double> val_3(get_middle(goal_3, goal_6));
    complex<double> val_4(get_middle(goal_4, goal_5));
    complex<double> val_5(get_middle(goal_5, goal_8));
    complex<double> val_6(get_middle(goal_6, goal_7));

    //cout  << val_2.real()  << " "  << val_2.imag()  << endl;
 
    complex<double> valu_1(translation(val_1));
    complex<double> valu_2(translation(val_2));
    complex<double> valu_3(translation(val_3));
    complex<double> valu_4(translation(val_4));
    complex<double> valu_5(translation(val_5));
    complex<double> valu_6(translation(val_6));
    
    complex<double> obs1_p(translation(obstacle_1, true));
    complex<double> obs2_p(translation(obstacle_2, true));

    complex<double> obs_1(get_middle(obstacle_1, obs1_p));
    complex<double> obs_2(get_middle(obstacle_2, obs2_p));

    double val_3_real__ = val_3.real() - 0.051;
    double val_3_imag__ = val_3.imag() - 0.051;

    double val_4_real__ = val_4.real() - 0.052;
    double val_4_imag__ = val_4.imag() - 0.052;
    
    //cout  << obs_1.real()  << " "  << obs_1.imag()  << endl;
    //cout  << valu_2.real()  << " "  << valu_2.imag()  << endl;

    route_1_x = {val_1.real(), obs_1.real(), valu_2.real(), valu_3.real(), val_3_real__, val_4.real(), valu_4.real(), valu_5.real(), val_5.real(), obs_2.real(),val_6.real(), goal.real()};
    route_1_y = {val_1.imag(), obs_1.imag(), valu_2.imag(), valu_3.imag(), val_3_imag__, val_4.imag(), valu_4.imag(), valu_5.imag(), val_5.imag(), obs_2.imag(),val_6.imag(), goal.imag()};

    route_2_x = {val_6.real(), obs_2.real(), val_5.real(), valu_5.real(), valu_4.real(), val_4_real__, val_3.real(), valu_3.real(), valu_2.real(), obs_1.real(), val_1.real(), goal.real()};
    route_2_y = {val_6.imag(), obs_2.imag(), val_5.imag(), valu_5.imag(), valu_4.imag(), val_4_imag__, val_3.imag(), valu_3.imag(), valu_2.imag(), obs_1.imag(), val_1.imag(), goal.imag()};
    
    route_3_x = {val_5.real(), obs_2.real(), val_6.real(), valu_6.real(), valu_3.real(), val_3_real__, val_4.real(), valu_4.real(), valu_1.real(), val_1.real(), obs_1.real(), goal.real()};
    route_3_y = {val_5.imag(), obs_2.imag(), val_6.imag(), valu_6.imag(), valu_3.imag(), val_3_imag__, val_4.imag(), valu_4.imag(), valu_1.imag(), val_1.imag(), obs_1.imag(), goal.imag()};
}

