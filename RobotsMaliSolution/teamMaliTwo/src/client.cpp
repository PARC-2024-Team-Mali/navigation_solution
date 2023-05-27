#include <ros/ros.h>
#include <team_mali_two/TrajetAction.h>
#include <actionlib/client/simple_action_client.h>
#include <iostream>
#include <jsoncpp/json/json.h>
#include <fstream>
#include "data.hpp"


std::complex<double> goal() ;
typedef actionlib::SimpleActionClient<team_mali_two::TrajetAction> Client;


int main(int argc, char** argv)
{
	
	ros::init(argc, argv, "client_sender_poses");

	done() ;

	Client client("trajet", true);
	client.waitForServer();
	team_mali_two::TrajetGoal goal;
	
	int route_id = std::stoi( argv[1] );
	
	ROS_INFO("Demarage du robot sur la route n°: %d", route_id);
	
	if ( route_id == 1 )
		goal.trajet_x = route_1_x, goal.trajet_y = route_1_y;
	else if ( route_id == 2)
		goal.trajet_x = route_2_x, goal.trajet_y = route_2_y;
	else if ( route_id == 3 )
		goal.trajet_x = route_3_x, goal.trajet_y = route_3_y;
	else
		ROS_INFO("Route inrouvable");	

	client.sendGoal(goal);
	client.waitForResult();
	if ( client.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
		std::cout << " la tache est accomplie\n";
	return 0;
}
