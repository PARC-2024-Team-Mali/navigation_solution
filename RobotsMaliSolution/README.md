# **Introduction**

* **Approche Task1:**

> ***Notre approche est une approche Mathématiques basées sur les nombres complexes, plus précisement les transformations du plan à savoir `la translation` et `la rotation`**.* ***On fournit des points cibles au robot  et le robot fait la translation et la rotation nécessaire pour atteindre ces points.***
>
> `NB : Chaque point est transformé en nombre complexe à savoir les points cibles et la position du robot à chaque instant.`
>
> ***`La translation :`***  *est effectuée entre un point cible et la position du robot à chaque instant, et elle est faite ainsi : on soustrait la partie réelle du point cible de la partie réelle de la position du robot à chaque instant et la même chose est faite sur les parties imaginaires.*
>
> ***`La rotation  :`*** *est effectuée en utilisant le resultat précedent effectuer dans la translation.  On calcule l'angle entre les parties réelles soustraites et les parties imaginaires soustraites en utilisant les fonctions trigonométriques appropriées. Une contrainte est ensuite appliquée  sur l'angle trouvé pour qu'il soit toujours dans [-π, π] , permettant au robot de tourner dans la direction la plus courte vers le point souhaité .*

---

# Dépendences

* > **Task1 :** ***Pour la réalisation de notre approche nous n'avons pas installer de package.***

# Description et Exécution de commande(s)
> **Route 1 temps d'execution 2 minute 15 seconde
> **Route 2 temps d'execution 2 minute 10 seconde
> **Route 3 temps d'execution 2 minute 5 seconde
> **Task1 : Pour l'exécution de notre solution on fait :**
>
> * **`roslaunch team_mali_one task1_solution.launch route:=Route` .**
> * **Route désigne la route choisit, par défaut la route1 est chosit.**
