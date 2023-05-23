#! /usr/bin/env python3

import rospy
import actionlib
from geometry_msgs.msg import (Twist, Pose2D)
from math import atan2,pi, cos, sin
from cmath import phase
from test_pack.msg import TrajetAction, TrajetResult, TrajetFeedback


class MoveServer() :

    _feedback = TrajetFeedback()
    _result = TrajetResult()

    def __init__(self, server_name, sub_topic_name = "/pose2d", pub_topic_name = "/cmd_vel") :

        """
        Fonctionalité :

            Initialise la classe MoveServer.
        
        Arguments:
            server_name (str): Nom du serveur d'action.
            sub_topic_name (str): Nom du topic d'abonnement pour la pose 2D.
            pub_topic_name (str): Nom du topic de publication pour les commandes de vitesse.
        """

        self.sub = rospy.Subscriber(sub_topic_name, Pose2D, self.callback)
        self.pub = rospy.Publisher(pub_topic_name, Twist, queue_size=10)

        self.current_x = None
        self.cmd_vel = Twist()

        self._action_name = server_name
        self._action_server = actionlib.SimpleActionServer(self._action_name,TrajetAction, \
                                                           execute_cb=self.execute_callback, auto_start=False)

        self._action_server.start()



    def rotation(self, angle, kp=0.4):
        
        """ Fonctionalité : 

                Cette Methode permet d'assurer une transition en douceur entre les angles positifs et négatifs, 
                    permettant au robot de tourner dans la direction la plus courte vers l'angle souhaité.

            Arguments :

                angle (float) : L'angle à atteindre.
                kp (float): Gain proportionnel pour contrôler la vitesse de rotation (par défaut: 0.4).

            Retourne :

                float: Différence d'angle normalisée dans la plage [-π, π].

        """

        
        current_angle_rad = self.current_angle #Angle courant.

        angle_diff_rad = atan2(sin(angle - current_angle_rad), cos(angle - current_angle_rad))
        
        return kp * angle_diff_rad
    

    def cmd_vel_data(self, target_point : complex, angle_precision : float = 0.01, goal_precison : float = 0.1) :

        """
        Fonctionalité :

            Calcule les données de commande de vélocité en fonction du point cible.
        
        Arguments :
            target_point (complex): Point cible au format complexe (x + iy).
            angle_precision (float): Précision de l'angle pour considérer la rotation comme terminée.
            goal_precision (float): Précision de la position pour considérer l'objectif comme atteint.
        
        Retourne:
            dict: Données de commande de vélocité avec les clés "vitesse" et "rotation".
        """

        angle = atan2(target_point.imag, target_point.real)

        

        angle_reg = self.rotation(angle)
        self.diff_x = abs(target_point.real)
        self.diff_y = abs(target_point.imag)

        if self.diff_x < goal_precison and self.diff_y < goal_precison :

            return {
                "vitesse" : 0.0,
                "rotation" : 0.0
            }

        elif abs(angle_reg) > angle_precision :

            return {
                "vitesse" : 0.0,
                "rotation" : angle_reg
            }


        else :

            return {
                "vitesse" : 0.45,
                "rotation" : 0.0
            }



    def callback(self, msg) :

        """
        Fonctionalité :
            Fonction de rappel pour la réception des messages de pose.
        
        Arguments:
            msg (Pose2D): Message de pose contenant les coordonnées x, y et l'angle theta.
        """

        self.current_x = msg.x
        self.current_y = msg.y
        self.current_angle = msg.theta


    
    def execute_callback(self, goal) :

        """
        Fonctionalité :
            Fonction de rappel pour l'exécution de l'action de déplacement.
        
        Arguments:
            goal (TrajetAction): Objectif de déplacement contenant une liste de coordonnées x et y.
        """
        
        rate =  rospy.Rate(10)

        success = True

        for x, y in zip(goal.trajet_x, goal.trajet_y) :

            if self._action_server.is_preempt_requested() :

                rospy.loginfo("%s : Annulé "%(self._action_name))

                self._action_server.set_preempted()

                success = False

                break

            pt = complex(x, y)

            while not rospy.is_shutdown() :

                if self.current_x is not None :

                    target_x = pt.real - self.current_x
                    target_y = pt.imag - self.current_y

                    goal_pose = complex(target_x, target_y)

                    cmd_vel = self.cmd_vel_data(goal_pose)

                    rospy.loginfo("commande velocity : %s"%(cmd_vel))
                   
                    if cmd_vel["vitesse"] != 0.0 or cmd_vel["rotation"] != 0.0 :

                        self.cmd_vel.linear.x = cmd_vel["vitesse"]
                        self.cmd_vel.angular.z = cmd_vel["rotation"]

                        self.pub.publish(self.cmd_vel)

                        rate.sleep()

                        continue

                    break


            trajet = "trajet x : %s y: %s"%(x, y)

            self._feedback.cordinate = trajet
            self._result.result.append(trajet)
            self._action_server.publish_feedback(self._feedback)

            rate.sleep()
                
            
        if success :

            self.cmd_vel.linear.x = 0.0
            self.cmd_vel.angular.z = 0.0

            self.pub.publish(self.cmd_vel)

            self._action_server.set_succeeded(self._result)

            rospy.loginfo("But atteint")


if __name__ == "__main__" :

    rospy.init_node("move_server_node")

    move_server = MoveServer(server_name="trajet")

    rospy.spin()
