#! /usr/bin/env python3

import rospy
from parc_robot.gps2cartesian import gps_to_cartesian

def get_cordinate(cordinate) :

    return  cordinate["latitude"],cordinate["longitude"]


def get_param(param) :

    return { "latitude" : rospy.get_param(f"{param}_latitude"),
            "longitude" : rospy.get_param(f"{param}_longitude") 
            }
            


def cordinate() :

    # Récuperation des coordonnées gps des piquets
    coordonne = {"Peg0"+str(i) : rospy.get_param("peg_0"+str(i)) for i in range(1,9)}

    # Récuperation des coordonnées gps du but
    coordonne["goal"] = get_param("goal")

    #coordonnées gps des obstacles
    coordonne["PegA"] = rospy.get_param("peg_A")
    coordonne["PegB"] = rospy.get_param("peg_B")

    #Coordonnées cartésiennes des piquets
    coordonne_cartesian = {"Peg0"+str(i) : gps_to_cartesian(*get_cordinate(coordonne["Peg0"+str(i)])) for i in range(1,9)}

    #coordonnées cartésiennes du goal
    coordonne_cartesian["goal"] = gps_to_cartesian(*get_cordinate(coordonne["goal"]))

    #coordonnées cartésiennes des obstacles
    coordonne_cartesian["PegA"] = gps_to_cartesian(*get_cordinate(coordonne["PegA"]))
    coordonne_cartesian["PegB"] = gps_to_cartesian(*get_cordinate(coordonne["PegB"]))

    rospy.loginfo(coordonne_cartesian)

    return coordonne_cartesian

if __name__ == "__main__" :

    rospy.init_node('Peg_coordinate')

    cordinate()
 
