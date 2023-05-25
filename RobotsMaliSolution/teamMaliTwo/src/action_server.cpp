#include "ros/ros.h"
#include "team_mali_two/TrajetAction.h"
#include "team_mali_two/TrajetGoal.h"
#include "actionlib/server/simple_action_server.h"
#include "geometry_msgs/Pose2D.h"
#include <complex>
#include <tuple>
#include <algorithm>
#include "geometry_msgs/Twist.h"

class Move
{
	private:
		ros::NodeHandle node;

		actionlib::SimpleActionServer<team_mali_two::TrajetAction> action;

		team_mali_two::TrajetFeedback feedback;

		team_mali_two::TrajetResult result;
		
		ros::Subscriber sub_pose;

		ros::Publisher pub_cmd;
		
		// definition des constantes
		// ecart entre l'angle du robot et celui du but
		const float angle_precision = 0.01, 
			//  ecart entre la position du robot et celui du but
		      goal_precision = 0.1, 
		      // le regulateur de vitesse
		      kp = 0.4;
	
		geometry_msgs::Pose2D current_pose;
		// fonction callback if goal is send
		void execute(const team_mali_two::TrajetGoal::ConstPtr&);

		// fonction callback for robot position
		void poseCallback(const geometry_msgs::Pose2D::ConstPtr&);
		
		std::pair<float, float> cmdvelRegulator(std::complex<double>&);

	public:
		Move(std::string name);
};


std::pair<float, float> Move::cmdvelRegulator(std::complex<double>& target_point)
{
	auto angle = std::arg(target_point);

	auto angle_diff = atan2(sin(angle - current_pose.theta), cos(angle - current_pose.theta));
	
	float angle_reg = kp*angle_diff;

	if ( std::abs(target_point.real()) < goal_precision && std::abs(target_point.imag()) < goal_precision)
	{
		return {0.0, 0.0};
	}
	else if( std::abs(angle_reg) > angle_precision)
	{
		return {0.0, angle_reg};
	}
	else
	{
		return { 0.45, 0.0};
	}

}
Move::Move(std::string name): action(node, name, boost::bind(&Move::execute, this, _1), false)
{
	ROS_INFO("Demarrage du navigateur par point");

	sub_pose = node.subscribe("pose2d", 10, 
			&Move::poseCallback, 
			this);
	pub_cmd = node.advertise<geometry_msgs::Twist>("/cmd_vel", 10);
	action.start();
}

void Move::poseCallback(const geometry_msgs::Pose2D::ConstPtr& pose)
{

	current_pose = *pose;

}
void Move::execute(const team_mali_two::TrajetGoal::ConstPtr& goal)
{

	ros::Rate rate(10);
	bool success = true;
	auto put_cmdvel = geometry_msgs::Twist();

	result.result.clear();
	for( int i = 0; i < goal -> trajet_x.size(); i++)
	{
		if ( action.isPreemptRequested() )
		{
			ROS_INFO(": le but est annulé");
			action.setPreempted();
			success = false;
			break;
		}

		std::complex<double> point = std::complex<double>{ goal->trajet_x[i] , goal -> trajet_y[i] };
		
		while( ros::ok() )
		{
			//current_pose 
			//{
				std::complex<double> trajet_point = std::complex<double>{ point.real() - current_pose.x, point.imag() - current_pose.y};
				auto cmdvel = cmdvelRegulator(trajet_point);

				if ( cmdvel.first != 0.0 || cmdvel.second != 0.0)
				{
					//auto put_cmdvel = geometry_msgs::Twist();
					put_cmdvel.linear.x = cmdvel.first;
					put_cmdvel.angular.z = cmdvel.second;

					pub_cmd.publish( put_cmdvel);
					rate.sleep();
					continue;
				}
				break;
			//}
		}
		//std::string feedback_string = "test";
		std::string feedback_string = " trajet x : " + std::to_string( goal -> trajet_x[i]) + " trajet y: " + std::to_string( goal -> trajet_y[i] );

		feedback.cordinate = feedback_string;
		result.result.push_back(feedback_string);
		action.publishFeedback(feedback);
		rate.sleep();
	}

	if ( success )
	{
		put_cmdvel.linear.x = 0.0;
		put_cmdvel.angular.z = 0.0;
		pub_cmd.publish(put_cmdvel);

		action.setSucceeded(result);
		ROS_INFO("But atteint");
	}

}

int main(int argc, char** argv)
{
	ros::init(argc, argv, "ActionNode");

	Move move{"trajet"};

	ros::spin();

	return 0;
}

