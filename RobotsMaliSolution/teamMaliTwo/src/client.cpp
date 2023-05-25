#include <ros/ros.h>
#include <team_mali_two/TrajetAction.h>
#include <actionlib/client/simple_action_client.h>

typedef actionlib::SimpleActionClient<team_mali_two::TrajetAction> Client;

int main(int argc, char** argv)
{
	ros::init(argc, argv, "client_sender_poses");
	Client client("trajet", true);
	client.waitForServer();
	team_mali_two::TrajetGoal goal;

	goal.trajet_x.push_back( std::stod(argv[1]));
	goal.trajet_y.push_back( std::stod(argv[2]));


	client.sendGoal(goal);
	client.waitForResult();
	if ( client.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
		std::cout << " la tache est accomple\n";
	return 0;
}
