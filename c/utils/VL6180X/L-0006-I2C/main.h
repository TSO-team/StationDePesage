#ifndef MAIN_H
#define MAIN_H
//L-0006-I2C:
//Historique: 2018-11-01, Yves Roy, création.
//Programme utilisé pour élaborer piloteI2C et interfaceVL6180X.
//Le programme fait une pause ou se remet en marche quand on appuie sur le bouton
//pause du Beaglebone Blue pendant un court moment. Le fait d'appuyer sur ce
//bouton pendant longtemps met fin à l'exécution du programme.
//Le programme lit les distances produites par un module VL6180X et commande à
//une imprimante 3D d'activer ou d'arrêter son ventilateur.


// usefulincludes is a collection of common system includes for the lazy
// This is not necessary for roboticscape projects but here for convenience
#include <rc_usefulincludes.h> 
// main roboticscape API header
#include <roboticscape.h>
#include "../../Robotics_cape_installer/libraries/rc_defs.h"

#define MODULE_EN_FONCTION      0
#define MODULE_EN_DEMARRAGE     1
#define MODULE_EN_ARRET         2
#define MODULE_EN_PAUSE         3
#define INFORMATION_DISPONIBLE  1
#define INFORMATION_TRAITEE     0
#define REQUETE_EN_COURS        1
#define REQUETE_TRAITEE         0
#define RESULTAT_DISPONIBLE     1
#define RESULTAT_TRAITE         0
#define RESERVE                 1
#define LIBRE                   0

typedef struct
{
    uint8_t information;
    uint8_t etat;
} MODULE;

//configuration

#define NOMBRE_DE_PHASES  1
#define PHASE_SERVICE_BOUTON_PAUSE  0

int neFaitRien(void);

#endif