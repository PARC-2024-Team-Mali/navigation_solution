#! /usr/bin/env python3

import sys
import rospy 
import actionlib
from test_pack.msg import TrajetAction, TrajetGoal
from work_module import get_middle_segment, avoid_rotate_decision
from peg_location import cordinate


arg = sys.argv
cor = cordinate()

def feedback_callback(msg) :

    """
    Fonctionalité :
        Fonction de rappel pour la rétroaction de l'action en cours.
    
    Arguments:
        msg : Message de rétroaction contenant l'état actuel du trajet.
    """

    rospy.loginfo("Trajet en %s en cour"%msg) 

def move_client() :

    """
    Fonctionalité :
        Fonction cliente pour exécuter l'action de déplacement.
    
    Retourne:
        TrajetResult : Résultat de l'action de déplacement.
    """

    client = actionlib.SimpleActionClient('trajet',TrajetAction)

    client.wait_for_server()

    goal = TrajetGoal()

    target = complex(*cor["goal"])

    target_1 = complex(*cor["Peg02"]) 
    target_2 = complex(*cor["Peg03"]) 
    target_3 = complex(*cor["Peg06"])
    target_4 = complex(*cor["Peg04"])
    target_5 = complex(*cor["Peg05"]) 
    target_6 = complex(*cor["Peg08"]) 
    target_7 = complex(*cor["Peg07"])
    target_8 = complex(*cor["Peg01"])

    OBSTACLE_POINT1 = complex(*cor["PegA"]) 
    OBSTACLE_POINT2 = complex(*cor["PegB"])

    other_point1 = avoid_rotate_decision(OBSTACLE_POINT1, vtranslate=True)
    other_point2 = avoid_rotate_decision(OBSTACLE_POINT2, vtranslate=True)

    obs1_middle = get_middle_segment(OBSTACLE_POINT1, other_point1)
    obs2_middle = get_middle_segment(OBSTACLE_POINT2, other_point2)

    avoid_obs1_x, avoid_obs1_y = obs1_middle.real, obs1_middle.imag 
    avoid_obs2_x, avoid_obs2_y = obs2_middle.real, obs2_middle.imag
   
    but1 = get_middle_segment(target_1, target_2)
    but2 = get_middle_segment(target_2, target_3)
    but3 = get_middle_segment(target_4, target_5)
    but4 = get_middle_segment(target_5, target_6)
    but5 = get_middle_segment(target_3, target_7)
    but6 = get_middle_segment(target_4, target_8)

    rotation1 = avoid_rotate_decision(but1)
    rotation2 = avoid_rotate_decision(but2)
    rotation3 = avoid_rotate_decision(but3)
    rotation4 = avoid_rotate_decision(but4)
    rotation5 = avoid_rotate_decision(but5)
    rotation6 = avoid_rotate_decision(but6)

    goal_x1, goal_y1 = rotation1.real, rotation1.imag
    goal_x2, goal_y2 = rotation2.real, rotation2.imag 
    goal_x3, goal_y3 = rotation3.real, rotation3.imag 
    goal_x4, goal_y4 = rotation4.real, rotation4.imag 
    goal_x5, goal_y5 = rotation5.real, rotation5.imag
    goal_x6, goal_y6 = rotation6.real, rotation6.imag

    but3_real = but3.real - .051
    but3_imag = but3.imag - .051
    but2_real = but2.real - .052
    but2_imag = but2.imag - .052
    
    #route1
    if arg[1] == "1" :

        goal.trajet_x = [but6.real, avoid_obs1_x, goal_x1, goal_x2, but2_real, but3.real, goal_x3, goal_x4, but4.real, avoid_obs2_x, but5.real, target.real] 
        goal.trajet_y = [but6.imag, avoid_obs1_y, goal_y1, goal_y2, but2_imag, but3.imag, goal_y3, goal_y4, but4.imag, avoid_obs2_y, but5.imag, target.imag]

    #route2
    elif arg[1] == "2" :
    
        goal.trajet_x = [but5.real, avoid_obs2_x, but4.real, goal_x4, goal_x3, but3_real, but2.real, goal_x2, goal_x1, avoid_obs1_x, but6.real, target.real]
        goal.trajet_y = [but5.imag, avoid_obs2_y, but4.imag, goal_y4, goal_y3, but3_imag, but2.imag, goal_y2, goal_y1, avoid_obs1_y, but6.imag, target.imag]

    #route3
    elif arg[1] == "3" :

        goal.trajet_x = [but4.real, avoid_obs2_x, but5.real, goal_x5, goal_x2, but2_real, but3.real, goal_x3, goal_x6, but6.real, avoid_obs1_x, target.real]
        goal.trajet_y = [but4.imag, avoid_obs2_y, but5.imag, goal_y5, goal_y2, but2_imag, but3.imag, goal_y3, goal_y6, but6.imag, avoid_obs1_y, target.imag]

    client.send_goal(goal, feedback_cb=feedback_callback)

    client.wait_for_result()

    result = client.get_result()

    return result


if __name__ =="__main__" :

    try :

        rospy.init_node('move_client_node')

        result = move_client()
        print(result)

    except rospy.ROSInterruptException as e :

        print(e)

