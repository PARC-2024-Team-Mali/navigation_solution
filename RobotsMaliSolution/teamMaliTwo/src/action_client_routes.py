#! /usr/bin/env python3

import sys
import json
import os

import rospy
import actionlib
from team_mali_two.msg import TrajetAction, TrajetGoal

routes = { "1": "route_1", "2": "route_2", "3": "route_3"}

def feedback_callback(msg) :

    rospy.loginfo("Trajet en %s en cour"%msg) 

def move_client(route: dict):

    client = actionlib.SimpleActionClient('trajet',TrajetAction)

    client.wait_for_server()

    goal = TrajetGoal()
    goal.trajet_x = route["x"]
    goal.trajet_y = route["y"] 

    client.send_goal(goal, feedback_cb=feedback_callback)

    client.wait_for_result()

    result = client.get_result()

    return result


if __name__ =="__main__" :

    try :
        if sys.argv[1] in routes:
            routes_file_name = f"{os.path.dirname(sys.argv[0] )}/routes.json"
            route_dict = json.load(open( routes_file_name) )
            rospy.init_node('move_client_node')
            
            rospy.loginfo("Demarrage pour la route : %s"% routes[ sys.argv[1] ]  )
            result = move_client( route_dict[ routes[ sys.argv[1] ] ] )
            print(result)
        else:
            rospy.loginfo("Route est inconnue, arret du programme", sys.argv[1] )

    except rospy.ROSInterruptException as e :

        print(e)
