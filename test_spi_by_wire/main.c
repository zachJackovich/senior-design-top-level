#include <msp430.h> 
#include <msp430fr6989.h>

//Peripheral Pin Assignments
#define P3P0    BIT0                   // Pin P3.0
#define P3P1    BIT1                   // Pin P3.1
#define P3P2    BIT2                   // Pin P3.2
#define P4P0    BIT0                   // Pin P4.0

//Global Variables
volatile unsigned int i;                          // Volatile to prevent optimization

int main(void)
{
    WDTCTL = WDTPW | WDTHOLD;                   // Stop watchdog timer
    PM5CTL0 &= ~LOCKLPM5;                       // Disable the GPIO power-on default high-impedance mode

    //Set GPIOs as outputs
    P3DIR |= P3P0;
    P3DIR |= P3P1;
    P3DIR |= P3P2;
    P4DIR |= P4P0;

    //Clear GPIOs to start
    P3OUT &= ~P3P0;
    P3OUT &= ~P3P1;
    P3OUT &= ~P3P2;

    P4OUT |= P4P0; // Set this one High and keep High forever, easy test probe right off the rip to verify it programmed correctly

    // Enable Global Interrupts - Entered low power mode this happens automatically
    _enable_interrupts();

    while(1)
    {
        P3OUT ^= P3P0; // turn on (This will toggle every 1/2 second)
        P3OUT ^= P3P1; // turn on (This will toggle every 1 second)
        P3OUT ^= P3P2; // turn on (This will toggle every 2 seconds)

        __delay_cycles(500000); // 0.5 sec delay

        P3OUT ^= P3P0; // turn off

        __delay_cycles(500000); // 0.5 sec delay

        P3OUT ^= P3P0; // turn on
        P3OUT ^= P3P1; // turn off

        __delay_cycles(500000); // 0.5 sec delay

        P3OUT ^= P3P0; // turn off

        __delay_cycles(500000); // 0.5 sec delay


    }
}
