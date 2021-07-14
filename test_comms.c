//***************************************************************************************
//  MSP430 Test GPIO Connection to Raspberry Pi
//
//  Description; Toggle P1.3 by xor'ing P1.3 inside of a software loop.
//  ACLK = n/a, MCLK = SMCLK = default DCO
//
//                MSP430FR6xxx
//             ------------------
//         /|\|               XIN|-
//          | |                 |
//          --|RST           XOUT|-
//            |                 |
//            |              P1.3|-->GPIO to Raspberry Pi
//
//  Texas Instruments, Inc
//  July 2013
//***************************************************************************************
#include <msp430.h>
#include <msp430fr6989.h>

//Peripheral Pin Assignments
#define ECHO             BIT5               // Pin P1.5 - Echo from the Sonar Sensor
#define TRIG             BIT4               // Pin P1.4 - Trigger to Sonar Sensor
#define SIG_TO_RUN_PI    BIT0               // Pin P3.0 - Output to both RPi's Signaling that someone is within 1m and they will start running FR and Pin# Authentication
#define redLED           BIT0               // Pin P1.0 - Red LED
#define greenLED         BIT7               // Pin P9.7 - Green LED

//Global Variables
unsigned int up_counter = 0;
unsigned int distance_cm = 0;
volatile unsigned int i;                    // Volatile to prevent optimization

void main(void) {
    WDTCTL = WDTPW | WDTHOLD;               // Stop watchdog timer
    PM5CTL0 &= ~LOCKLPM5;                   // Disable the GPIO power-on default high-impedance mode
                                            // to activate previously configured port settings

    // Configure GPIO to Pi and LEDs
    P3DIR  |=  SIG_TO_RUN_PI;                  // Set GPIO to output direction
    P3SEL0 &= ~SIG_TO_RUN_PI;                  // Set SIG_TO_RUN_PI bit to GPIO => 00b = General-purpose I/O is selected
    P3SEL1 &= ~SIG_TO_RUN_PI;                  // Set SIG_TO_RUN_PI bit to GPIO => 00b = General-purpose I/O is selected
    P3OUT  &= ~SIG_TO_RUN_PI;                  // Initialize the GPIO Pin as OFF
    P1DIR |= redLED;                           // Direct pin as output
    P1OUT &= ~redLED;                          // Initialize the LED Off
    P9DIR |= greenLED;                         // Direct pin as output
    P9OUT &= ~greenLED;                        // Initialize the LED Off

    // Configure Sonar Sensor Signals
    P1DIR |= TRIG;              // Set Trigger pin as Output
    P1DIR &= ~ECHO;             // Set Echo pin as Input
    P1OUT &= ~TRIG;             // Initialize/clear trigger low
    P1SEL0 |= ECHO;             // Set ECHO as (Capture Input [CCI]) AKA event trigger for TimerA from Port1
    P1SEL1 |= ECHO;             // Set ECHO as (Capture Input [CCI]) AKA event trigger for TimerA from Port1

    /* Timer A Channel 0 Capture Control Register:
     * Capture Mode 3 (Rising and Falling Edge)
     * Capture Compare Input Select - CCIxA
     * Set SCS for Synchronous Capture
     * Set CAP for Capture Mode
     * Set Capture Compare Interrupt Enable    */
    TA0CCTL0 = ( CM_3 | CCIS_0 | SCS | CAP | CCIE );

    /* Timer A Channel 0 Control register:
     * Timer A Source Select 1 - SMCLK source - default source is from DCOCLK internal digitally controlled oscillator
     * Mode Control: Continuous Mode
     * Input Divider: Divide by 1
     * Set Timer A Clear    */
    TA0CTL = ( TASSEL_2 | MC_2 | ID_0 | TACLR );

    // Enable Global Interrupts - Entered low power mode this happens automatically
    _enable_interrupts();

    /*
    for(;;) {
        P1OUT ^= SIG_TO_RUN_PI;                // Toggle GPIO using exclusive-OR
        P1OUT ^= redLED;                    // Toggle LED to monitor timing with RPi

        i = 100000;                         // SW Delay
        do i--;
        while(i != 0);
    }*/

    while (1)
    {
        // measuring the distance
        P1OUT |= TRIG;                    // Assert Trigger
        __delay_cycles(10);               // 10us wide
        P1OUT &= ~TRIG;                   // De-assert Trigger
        P9OUT ^= greenLED;                // Toggle Green LED so we know we are running
        __delay_cycles(500000);           // 0.5sec measurement cycle
    }
}

//Timer A Capture Mode => CCI (Capture/Compare Input) is the Echo Pin
#pragma vector=TIMER0_A0_VECTOR
__interrupt void T0A0_ISR(void)
{

    if (TA0CCTL0 & CCI)            // Rising edge
    {
        up_counter = TA0CCR0;      // Copy counter to variable
    }
    else                        // Falling edge
    {
        // Formula: Distance in cm = (Time in uSec)/58
        distance_cm = (TA0CCR0 - up_counter)/58;
        if(distance_cm < 100)             // Within 1m or 100cm
        {
            // Set GPIO to the Pi to signal running the facial and pin# authentication
            P3OUT |= SIG_TO_RUN_PI;
            P1OUT |= redLED;            // TURN ON RED LED FOR TESTING

            // Wait for 2 mins, while checking the 2 input GPIOs from the Pi's (meaning someone has been authenticated)
            for(i = 0; i < 240; i++)
            {
                __delay_cycles(500000);           // 0.5sec measurement cycle
                // Now check the 2 input GPIO's every 0.5 seconds for if the user has been recognized
                /*if((P3OUT & FACIAL) && (P3OUT & PIN))
                {
                    unlock_door();
                    break;
                }*/
            }
        }
        else
        {
            //Clear the GPIO to the Pi's signaling not to run the High-Level software
            P3OUT &= ~SIG_TO_RUN_PI;
            P1OUT &= ~redLED;            // TURN OFF RED LED FOR TESTING
        }
    }

    //Hardware automatically clears the CCIFG in TA0CCTL0 but we're winging it so...
    TA0CCTL0 &= ~CCIFG;
    TA0CTL &= ~TAIFG;      //Clear TA0CTL interrupt flag
}

