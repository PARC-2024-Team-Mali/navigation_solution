#! /usr/bin/env python3

def get_middle_segment(complex_1 : complex, complex_2 : complex) -> complex :

    """
    Fonctionalité :
        Calculer le milieu d'un segment donné sous forme de complexe.

    Arguments:
        complex_1 : Premier point du segment.
        complex_2 : Deuxième point du segment.

    Retourne:
        complex: Milieu du segment.
    """
    middle = (complex_1 + complex_2)/2

    return middle

def avoid_rotate_decision(translate_point : complex ,vtranslate = False, vprecision : float = 1.0, hprecision : float = 1.0) -> complex :

    """
    Fonctionalité :
        Effectuer une translation verticale ou horizontale des points en fonction de certaines conditions.

    Arguments:
        translate_point : Le point à éviter ou à déplacer.
        vtranslate : Indique si une translation verticale doit être effectuée (par défaut : False).
        vprecision : La valeur de précision pour la translation verticale (par défaut : 1.0).
        hprecision : La valeur de précision pour la translation horizontale (par défaut : 1.0).

    Retourne:
        complex : Le point résultant après la translation.
    """
    
    
    other_point_x, other_point_y = translate_point.real, translate_point.imag

    if vtranslate :

        if other_point_x < 0 and other_point_y < 0 :

            other_point_y -= vprecision

        else :

            other_point_y += vprecision

    else :

        if other_point_x  < 0 :

            other_point_x -= hprecision

        else :

            other_point_x += hprecision
    
    return complex(other_point_x, other_point_y)


