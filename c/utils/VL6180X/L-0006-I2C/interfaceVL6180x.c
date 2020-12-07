#include "main.h"
#include <stdint.h> // for uint8_t types etc
#include <unistd.h>
#include "piloteI2C1.h"
#include "interfaceVL6180x.h"




//définitions privées
typedef struct
{
	uint16_t adresse;
	uint8_t valeur;
} INTERFACEVL6810X_MESSAGE;

#define INTERFACEVL6180X_ADRESSE 0x29 
#define INTERFACEVL6180X_NOMBRE	40

//variables privées
INTERFACEVL6810X_MESSAGE interfaceVL6810xMessage[INTERFACEVL6180X_NOMBRE] =
{
	{0x0207, 0x01}, {0x0208, 0x01}, {0x0096, 0x00}, {0x0097, 0xfd},
	{0x00e3, 0x00}, {0x00e4, 0x04},	{0x00e5, 0x02},	{0x00e6, 0x01},
	{0x00e7, 0x03},	{0x00f5, 0x02},	{0x00d9, 0x05},	{0x00db ,0xce},
	{0x00dc, 0x03},	{0x00dd, 0xf8},	{0x009f, 0x00},	{0x00a3, 0x3c},
	{0x00b7, 0x00},	{0x00bb, 0x3c},	{0x00b2, 0x09},	{0x00ca, 0x09},
	{0x0198, 0x01},	{0x01b0, 0x17},	{0x01ad, 0x00},	{0x00ff, 0x05},
	{0x0100, 0x05},	{0x0199, 0x05},	{0x01a6, 0x1b},	{0x01ac, 0x3e},
	{0x01a7, 0x1f},	{0x0030, 0x00},
	{0x0011, 0x10},// Enables polling for ‘New Sample ready’ when measurement completes
	{0x010a, 0x30},// Set the averaging sample period (compromise between lower noise and increased execution time)
	{0x003f, 0x46},// Sets the light and dark gain (upper nibble). Dark gain should not be changed.
	{0x0031, 0xFF},// sets the # of range measurements after which auto calibration of system is performed 
	{0x0040, 0x63},// Set ALS integration time to 100ms
	{0x002e, 0x01},// perform a single temperature calibration of the ranging sensor 
	{0x001b, 0x09},// *Set default ranging inter-measurement period to 100ms
	{0x003e, 0x31},// *Set default ALS inter-measurement period to 500ms
	{0x0014, 0x24},// *Configures interrupt on ‘New Sample Ready threshold event’
	{0x0016, 0x00} //*change fresh out of set status to 0
};

//fonctions privées
//pas de fonctions privées

//variables publiques
MODULE interfaceVL6180x = {INFORMATION_DISPONIBLE, MODULE_EN_DEMARRAGE};

//fonctions publiques
int interfaceVL6180xEcrit(uint16_t registre, uint8_t donnee)
{
uint8_t message[3];
	message[0] = (uint8_t)(registre >> 8);
	message[1] = (uint8_t)(registre & 0xFF);
	message[2] = donnee;
	if (piloteI2C1EcritDesOctets(message, 3) < 0)
	{
		printf("erreur: interfaceVL6180xEcrit\n");
		return -1;
	}
	return 0;
}

int interfaceVL6180xLit(uint16_t registre, uint8_t *donnee)
{
uint8_t commande[2];
	commande[0] = (uint8_t)(registre >> 8);
	commande[1] = (uint8_t)registre;
	if (piloteI2C1LitDesOctets(commande, 2, donnee, 1) < 0)
	{
		printf("erreur: interfaceVL6180xLit\n");
		return -1;
	}
	return 0;
}

int interfaceVL6180xLitUneDistance(float *distance)
{
uint8_t valeur;
	if (interfaceVL6180xEcrit(0x18, 0x01) < 0)
	{
		printf("erreur: interfaceVL6180xLitUneDistance 1\n");
		return -1;
	}
	if(interfaceVL6180xLit(0x4F, &valeur) < 0)
	{
		printf("erreur: interfaceVL6180xLitUneDistance 2\n");
		return -1;
	}
	while((valeur & 0x7) != 4)
  {
    if (interfaceVL6180xLit(0x4F, &valeur) < 0)
    {
    	printf("erreur: interfaceVL6180xLitUneDistance 3\n");
      return -1;
    }
  }
  if (interfaceVL6180xLit(0x62, &valeur) < 0)
  {
		printf("erreur: interfaceVL6180xLitUneDistance 4\n");
    return -1;
	}
	if (interfaceVL6180xEcrit(0x15, 0x07) < 0)
  {
  	printf("erreur: interfaceVL6180xLitUneDistance 5\n");
    return -1;
	}
	*distance = (float)valeur /10.0;
	return 0;
}

int initialiseInterfaceVL6810x(void)
{
uint8_t index;
uint8_t valeur;
	if (piloteI2C1.etat != MODULE_EN_FONCTION)
	{
  	printf("erreur: initialiseInterfaceVL6180x 1\n");
		return -1;
	}
  
	if (piloteI2C1ConfigureLAdresse(INTERFACEVL6180X_ADRESSE) < 0)
	{
		printf("erreur: initialiseInterfaceVL6810x 2\n");
		return -1;
	}

  if (interfaceVL6180xLit(0x16, &valeur) < 0)
  {
  	printf("erreur: initialiseInterfaceVL6180x 3\n");
    return -1;
  }
	if (valeur != 1)
	{
		printf("message: le VL6180x va être reconfiguré\n");
	}

	for (index = 0; index < INTERFACEVL6180X_NOMBRE; index++)
	{
		if (interfaceVL6180xEcrit(interfaceVL6810xMessage[index].adresse, 
				interfaceVL6810xMessage[index].valeur) < 0)
		{
			printf("erreur: initialiseInterfaceVL6180x %d 4", index);
			return -1;
		}
	}
	
	interfaceVL6180x.etat = MODULE_EN_FONCTION;
	interfaceVL6180x.information = INFORMATION_DISPONIBLE;
	return 0;
}



