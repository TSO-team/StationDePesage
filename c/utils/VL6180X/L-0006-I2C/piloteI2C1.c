#include "main.h"
#include <linux/i2c-dev.h> //for IOCTL defs

#include "piloteI2C1.h"
#define PILOTEI2C1_FICHIER "/dev/i2c-1" 

//variables privées
uint8_t piloteI2C1Adresse;
int piloteI2C1Fichier;

//fonctions privées
//pas de fonctions privées

//variables publiques
MODULE piloteI2C1 = {INFORMATION_DISPONIBLE, MODULE_EN_DEMARRAGE};

//fonctions publiques
int piloteI2C1FermeLeBus(void)
{
	if (close(piloteI2C1Fichier) < 0)
	{
		printf("erreur: piloteI2C1FermeLeBus");
	    return -1;
	}
    piloteI2C1Adresse = 0;
	piloteI2C1.etat = MODULE_EN_ARRET;
	piloteI2C1.information = INFORMATION_DISPONIBLE;
	return 0;
}

int piloteI2C1EcritDesOctets(uint8_t *source, uint8_t nombreDOctetsAEcrire)
{
	if(write(piloteI2C1Fichier, source, nombreDOctetsAEcrire) != nombreDOctetsAEcrire)
	{
		printf("erreur: piloteI2C1EcritDesOctets\n");
		close(piloteI2C1Fichier);
		return -1;
	}
	return 0;
}

int piloteI2C1LitDesOctets(uint8_t *commande, uint8_t longueurDeLaCommande,
		uint8_t *destination, uint8_t nombreDOctetsALire)
{
    if (piloteI2C1EcritDesOctets(commande, longueurDeLaCommande) < 0)
    {
    	printf("erreur: piloteI2C1LitDesOctets 1\n");
    	close(piloteI2C1Fichier);
    	return -1;
    }
	if (read(piloteI2C1Fichier, destination, nombreDOctetsALire) != nombreDOctetsALire)
	{
		printf("erreur: piloteI2C1LitDesOctets 2\n");
		close(piloteI2C1Fichier);
		return -1;
	}
	return 0;
}

int piloteI2C1ConfigureLAdresse(uint8_t adresse)
{
	if(piloteI2C1Adresse == adresse)
	{
		return 0;
	}
	if(ioctl(piloteI2C1Fichier, I2C_SLAVE, adresse) < 0)
	{
		printf("erreur: piloteI2C1ConfigureLAdresse\n");
		close(piloteI2C1Fichier);
		return -1;
	}
	piloteI2C1Adresse = adresse;
	return 0;
}

int initialilsePiloteI2C1(void) {
    piloteI2C1Adresse = 0x00;
    piloteI2C1Fichier = open(PILOTEI2C1_FICHIER, O_RDWR);
    if(piloteI2C1Fichier == -1) {
		printf("erreur: initialilsePiloteI2C1 1\n");
		return -1;
	}
	if(ioctl(piloteI2C1Fichier, I2C_SLAVE, piloteI2C1Adresse) < 0)
	{
		printf("erreur: initialisePiloteI2C1 2\n");
		close(piloteI2C1Fichier);
		return -1;
	}
	piloteI2C1.etat = MODULE_EN_FONCTION;
	piloteI2C1.information = INFORMATION_DISPONIBLE;
	return 0;
}
