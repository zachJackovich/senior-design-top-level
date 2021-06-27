/*================================================================================
 * File Name: main.c
 * Author: Zach Jackovich
 * Project: Senior Design
 * Revision: Initial Development
 * Notes: Main.c for our Senior Design project targeting the MSP430FR6989 Device
 *================================================================================*/
#include <msp430.h> 
//include stdio for debugging purposes during development
#include <stdio.h>



int main(void)
{
	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer
	//set low power mode?
	//set internal VLO clock source?
	//set up ISRs for most of the functionality we need to implement? -saves power and resources
	


	return 0;
}
