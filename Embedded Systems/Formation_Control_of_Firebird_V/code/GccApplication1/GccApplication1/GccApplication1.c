
#include <avr/io.h>
#define F_CPU 14745600UL
#include "wifi.h"
#include "dmb.h"
#include <util/delay.h>
int c=1;int motionflag=0;


unsigned long int ShaftCountLeft = 0; //to keep track of left position encoder
unsigned long int ShaftCountRight = 0; //to keep track of right position encoder
unsigned int Degrees; //to accept angle in degrees for turning

//Function to configure INT4 (PORTE 4) pin as input for the left position encoder
void left_encoder_pin_config (void)
{
	DDRE  = DDRE & 0xEF;  //Set the direction of the PORTE 4 pin as input
	PORTE = PORTE | 0x10; //Enable internal pull-up for PORTE 4 pin
}

//Function to configure INT5 (PORTE 5) pin as input for the right position encoder
void right_encoder_pin_config (void)
{
	DDRE  = DDRE & 0xDF;  //Set the direction of the PORTE 4 pin as input
	PORTE = PORTE | 0x20; //Enable internal pull-up for PORTE 4 pin
}

//Function to initialize ports
void port_init1()
{
	motion_pin_config(); //robot motion pins config
	left_encoder_pin_config(); //left encoder pin config
	right_encoder_pin_config(); //right encoder pin config
}

void left_position_encoder_interrupt_init (void) //Interrupt 4 enable
{
	cli(); //Clears the global interrupt
	EICRB = EICRB | 0x02; // INT4 is set to trigger with falling edge
	EIMSK = EIMSK | 0x10; // Enable Interrupt INT4 for left position encoder
	sei();   // Enables the global interrupt
}

void right_position_encoder_interrupt_init (void) //Interrupt 5 enable
{
	cli(); //Clears the global interrupt
	EICRB = EICRB | 0x08; // INT5 is set to trigger with falling edge
	EIMSK = EIMSK | 0x20; // Enable Interrupt INT5 for right position encoder
	sei();   // Enables the global interrupt
}

//ISR for right position encoder
ISR(INT5_vect)
{
	ShaftCountRight++;  //increment right shaft position count
}


//ISR for left position encoder
ISR(INT4_vect)
{
	ShaftCountLeft++;  //increment left shaft position count
}

//Function used for turning robot by specified degrees
void angle_rotate(unsigned int Degrees)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = (float) Degrees/ 4.090; // division by resolution to get shaft count
	ReqdShaftCountInt = (unsigned int) ReqdShaftCount;
	ShaftCountRight = 0;
	ShaftCountLeft = 0;

	while (1)
	{
		if((ShaftCountRight >= ReqdShaftCountInt) | (ShaftCountLeft >= ReqdShaftCountInt))
		break;
	}
	stop(); //Stop robot
}

//Function used for moving robot forward by specified distance

void linear_distance_mm(unsigned int DistanceInMM)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = DistanceInMM / 5.338; // division by resolution to get shaft count
	ReqdShaftCountInt = (unsigned long int) ReqdShaftCount;
	
	ShaftCountRight = 0;
	while(1)
	{
		if(ShaftCountRight > ReqdShaftCountInt)
		{
			break;
		}
	}
	stop(); //Stop robot
}

void forward_mm(unsigned int DistanceInMM)
{
	forward();
	linear_distance_mm(DistanceInMM);
}

void back_mm(unsigned int DistanceInMM)
{
	back();
	linear_distance_mm(DistanceInMM);
}

void left_degrees(unsigned int Degrees)
{
	// 88 pulses for 360 degrees rotation 4.090 degrees per count
	left(); //Turn left
	angle_rotate(Degrees);
}



void right_degrees(unsigned int Degrees)
{
	// 88 pulses for 360 degrees rotation 4.090 degrees per count
	right(); //Turn right
	angle_rotate(Degrees);
}


void soft_left_degrees(unsigned int Degrees)
{
	// 176 pulses for 360 degrees rotation 2.045 degrees per count
	soft_left(); //Turn soft left
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

void soft_right_degrees(unsigned int Degrees)
{
	// 176 pulses for 360 degrees rotation 2.045 degrees per count
	soft_right();  //Turn soft right
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

void soft_left_2_degrees(unsigned int Degrees)
{
	// 176 pulses for 360 degrees rotation 2.045 degrees per count
	soft_left_2(); //Turn reverse soft left
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

void soft_right_2_degrees(unsigned int Degrees)
{
	// 176 pulses for 360 degrees rotation 2.045 degrees per count
	soft_right_2();  //Turn reverse soft right
	Degrees=Degrees*2;
	angle_rotate(Degrees);
}

//Function to initialize all the devices
void init_devicess()
{
	cli(); //Clears the global interrupt
	port_init1();  //Initializes all the ports
	left_position_encoder_interrupt_init();
	right_position_encoder_interrupt_init();
	sei();   // Enables the global interrupt
}


int main()
{
	
	
	dmb_drive();            //bot 1 leader
	set_velocity(150,150);
	init_devicess();
	init_devices5();
	_delay_ms(4000);
	connectDevice();
	if (parseOK("AT"))
	{
		disp(st);
	}
	_delay_ms(6000);
	if(startServer())
	disp(st);
	else
	disp(st[13]+st[14]+st[15]);
	while(1)
	{
		_delay_ms(500);
		if (strcmp(num,"111")==0)
		{
			numreset();
			disp("started");
			_delay_ms(200);       
			
			forward_mm(200); //Moves robot forward 100mm
			stop();
			_delay_ms(8000);      //major delay
			right_degrees(360); //Rotate robot right by 90 degrees
			stop();
			
			
		}
		else if (strcmp(num,"000")==0)
		{
			numreset();
			stop();
		}
		}
	
	
	/*cli();             // bot 2
	adc_init();
	adc_pin_config();
	sei();
	set_velocity(150,150);
	init_devices5();
	init_devicess();
	delay(400);
	_delay_ms(3000);
	connectDevice();
	if(parseOK("AT"))
	disp(st);
	delay(5000);
	_delay_ms(3000);
	if(connectIP1())
	disp("Connctd Bot");
	else
	disp("not conn");
	_delay_ms(2000);
	sendmsgs("111`");
	_delay_ms(500);
	dmb_drive();
	_delay_ms(500);
	
	parseOK("AT+CIPCLOSE=2");
	
	_delay_ms(1000);
	
	if(startServer())
	disp(st);
	else
	disp(st[13]+st[14]+st[15]);
	while(1)
	{
		_delay_ms(500);
		if (strcmp(num,"222")==0)
		{
			numreset();
			disp("started");
			_delay_ms(500);       //major delay
			
			forward_mm(200); //Moves robot forward 100mm
			stop();
			_delay_ms(500);			
		}
		else if (strcmp(num,"000")==0)
		{
			numreset();
			stop();
		}
		}*/
	
	

	/*cli();             // bot 3
	adc_init();
	adc_pin_config();
	sei();
	set_velocity(150,150);
	init_devices5();
	init_devicess();
	delay(400);
	_delay_ms(3000);
	connectDevice();
	if(parseOK("AT"))
	disp(st);
	delay(5000);
	_delay_ms(3000);
	if(connectIP2())
	disp("Connctd Bot");
	else
	disp("not conn");
	_delay_ms(2000);
	sendmsgs("222`");
	_delay_ms(500);
	dmb_drive();
	_delay_ms(500);
	
	parseOK("AT+CIPCLOSE=2");
	
	_delay_ms(1000);
	
	if(startServer())
	disp(st);
	else
	disp(st[13]+st[14]+st[15]);
	while(1)
	{
		_delay_ms(500);
		if (strcmp(num,"333")==0)
		{
			numreset();
			disp("started");
			_delay_ms(500);       //major delay
			
			forward_mm(200); //Moves robot forward 100mm
			stop();
			_delay_ms(500);
		}
		else if (strcmp(num,"000")==0)
		{
			numreset();
			stop();
		}
	}*/
		
		
	
	/*cli();             // bot 4
	adc_init();
	adc_pin_config();
	sei();
	set_velocity(150,150);
	init_devices5();
	init_devicess();
	delay(400);
	_delay_ms(3000);
	connectDevice();
	if(parseOK("AT"))
	disp(st);
	delay(5000);
	if(connectIP3())
	disp("Connctd Bot");
	else
	disp("not conn");
	_delay_ms(2000);
	sendmsgs("333`");
	_delay_ms(500);
	dmb_drive();
	_delay_ms(500);
	
	parseOK("AT+CIPCLOSE=2");
	
	_delay_ms(1000);
	
	if(startServer())
	disp(st);
	else
	disp(st[13]+st[14]+st[15]);
	while(1)
	{
		_delay_ms(500);
		if (strcmp(num,"444")==0)
		{
			numreset();
			disp("started");
			_delay_ms(500);       //major delay
			
			forward_mm(200); //Moves robot forward 100mm
			stop();
			_delay_ms(500);
		}
		else if (strcmp(num,"000")==0)
		{
			numreset();
			stop();
		}
	}*/	
	
	
	/*cli();             // bot 5
	adc_init();
	adc_pin_config();
	sei();
	set_velocity(150,150);
	init_devices5();
	init_devicess();
	delay(400);
	_delay_ms(3000);
	connectDevice();
	if(parseOK("AT"))
	disp(st);
	delay(5000);
	if(connectIP4())
	disp("Connctd Bot");
	else
	disp("not conn");
	_delay_ms(2000);
	sendmsgs("444`");
	_delay_ms(500);
	dmb_drive();
	_delay_ms(4000);
	
	forward_mm(200); //Moves robot forward 100mm
	stop();
	_delay_ms(500);*/
	
		
	}		
	
	
	/*	
		forward_mm(100); //Moves robot forward 100mm
		stop();
		_delay_ms(500);
		
		back_mm(100);   //Moves robot backward 100mm
		stop();
		_delay_ms(500);
		
		left_degrees(90); //Rotate robot left by 90 degrees
		stop();
		_delay_ms(500);
		
		right_degrees(90); //Rotate robot right by 90 degrees
		stop();
		_delay_ms(500);
		
	*/
		
	
	
	
	
	
 
       