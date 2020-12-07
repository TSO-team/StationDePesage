/*******************************************************************************
* essaiVL6180x
*
* Programme utilisé pour développer intefaceVL6180x et piloteI2C 
*  
*******************************************************************************/

#include "main.h"
#include "piloteTTY.h"
#include "piloteI2C1.h"
#include "serviceBaseDeTemps.h"
#include "interfaceVL6180x.h"
#include "processusBoutonPause.h"

int neFaitRien(void)
{
	return 0;
}

int initialiseMain(void)
{

	// do your own initialization here
	if (initialisePiloteTTYUSB0() < 0)
	{
		printf("erreur: initialiseMain 1");
		return -1;
	}
	if (initialilsePiloteI2C1() < 0)
	{
		printf("erreur: initialiseMain 2\n");
		return -1;
	}
	
	initialiseServiceBaseDeTemps();

	if (initialiseInterfaceVL6810x() < 0)
	{
		printf("erreur: initialiseMain 3\n");
		return -1;
	}

	if (initialiseServiceBoutonPause() < 0)
	{
		printf("erreur: initialiseMain 4\n");
		return -1;
	}

	// done initializing so set state to RUNNING
	rc_set_state(RUNNING); 
	return 0;
}

/*******************************************************************************
* int main() 
*
* Requis avec roboticscape
* - call to rc_initialize() at the beginning
* - main while loop that checks for EXITING condition
* - rc_cleanup() at the end
*******************************************************************************/
int main()
{
	if(rc_initialize())
	{
		fprintf(stderr,"erreur: main: êtes-vous root?\n");
		return -1;
	}
	if (initialiseMain() < 0)
	{
		printf("erreur: main 1\n");
		rc_cleanup();
		return -1;
	}

	while(rc_get_state()!=EXITING)
	{
		gereServiceBaseDeTemps();
		usleep(200000);
	}
	rc_cleanup(); 
	return 0;
}
