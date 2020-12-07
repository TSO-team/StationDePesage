#ifndef PILOTEI2C1_H
#define PILOTEI2C1_H

extern MODULE piloteI2C1;

int piloteI2C1FermeLeBus(void);
int piloteI2C1EcritDesOctets(uint8_t *source, uint8_t nombreDOctetsAEcrire);
int piloteI2C1LitDesOctets(uint8_t *commande, uint8_t longueurDeLaCommande,
		uint8_t *destination, uint8_t nombreDOctetsALire);
int piloteI2C1ConfigureLAdresse(uint8_t adresse);
int initialilsePiloteI2C1(void);

#endif