                                                                                                                       /********************************************************************************
/******************************************************************************
Wifi Library for esp8266
Author: DarkMatterBots
All Rights Reserved under OPEN LICENCE
OPEN-Sourced // Cheers! 

********************************************************************************/

#include<avr/io.h>
#include<avr/interrupt.h>
#include<util/delay.h>
#include<stdlib.h>
#include<string.h>

char data; //to store received data from UDR1
char st[100], num[100];int i=0,j,m=0,check=0,flag=0,cf1=0,cf2=0,cf3=0;
char decode1(char data);
int connectDevice();
void uart2_init(void)
{
 UCSR2B = 0x00; //disable while setting baud rate
 UCSR2A = 0x00;
 UCSR2C = 0x06;
 UBRR2L = 0x47; //set baud rate lo
 UBRR2H = 0x00; //set baud rate hi
 UCSR2B = 0x98;
}


SIGNAL(SIG_USART2_RECV) 		// ISR for receive complete interrupt
{
	data = UDR2;
   if(data==':')
   flag=1;
   if(data=='`')
   flag=0;
      
  if (flag==0)
  {
      if((data>='A'&&data<='Z' )||(data>='0'&& data<='9'))
       {
        st[i++]=decode1(data);
       }	   		      
  }
	else
	{
		if((data>='A'&&data<='Z' )||(data>='0'&& data<='9'))
		{
			num[m++]=decode1(data);
			_delay_ms(1);
		}
	}
	
}

void resetCon()
{
	cf1=cf2=cf3=0;
}

char decode1(char data)
{
 switch(data)
 {
  case 'A':return 'A';
           break;
  case 'B':return 'B';
           break;
  case 'C':return 'C';
           break;
  case 'D':return 'D';
           break;
  case 'E':return 'E';
           break;
  case 'F':return 'F';
           break;
  case 'G':return 'G';
           break;
  case 'H':return 'H';
           break;
  case 'I':return 'I';
           break; 
  case 'J':return 'J';
           break;
  case 'K':return 'K';
           break;
  case 'L':return 'L';
           break;
  case 'M':return 'M';
           break;
  case 'N':return 'N';
           break;
  case 'O':return 'O';
            break;
  case 'P':return 'P';
            break;
  case 'Q':return 'Q';
            break;
  case 'R':return 'R';
            break;
  case 'S':return 'S';
            break;
  case 'T':return 'T';
            break;
  case 'U':return 'U';
            break;
  case 'V':return 'V';
            break;
  case 'W':return 'W';
            break;
  case 'X':return 'X';
            break;
  case 'Y':return 'Y';
            break;
  case 'Z':return 'Z';
            break;
  case '0':return '0';
            break;
  case '1':return '1';
            break;
  case '2':return '2';
            break;
  case '3':return '3';
            break;
  case '4':return '4';
            break;
  case '5':return '5';
            break;
  case '6':return '6';
            break;
  case '7':return '7';
            break;
  case '8':return '8';
            break;
  case '9':return '9';
            break;
  case ',':return ',';
            break;
  case '.':return '.';
            break;
  case '/':return '/';
            break;
  case ':':return ':';
            break;
  case ';':return ';';
            break;
  case '+':return '+';
            break;
  case '=':return '=';
            break; 
  case '?':return '?';
            break;
  case '\n':return '#';
    
	        break;
  case '\r':return '#';
            break;
 /* case 'A':return 'A';
            break;
  case 'A':return 'A';
            break;
  case 'A':return 'A';
            break;
  case 'A':return 'A';
            break;
  case 'A':return 'A';
            break;
  case 'A':return 'A';
            break;
  case 'A':return 'A';
            break;
*/


 default: return 'm';
 }


}


int checkDevice()
{
 init_devices5(); //housekeeping stuff
    while(check!=1)
	{
    
	 UDR2 = 0x41 ;
	 UDR2 = 0x54;
	 _delay_ms(100);
	 UDR2== 0xA;
	 _delay_ms(100);
	 UDR2=0xD;
	 UDR2=0xA;

     _delay_ms(400);

	 
	 if(strcmp(st,"ATOK")==0)
	 check=1;
	}
	return 1;  
}

void reset()
{
     for(j=0;j<=i;j++)
	 {
	  st[j]='\0'; 
	 }
	 i=0;	
}
void numreset()
{
	int j;
	for(j=0;j<=m;j++)
	{
		num[j]='\0';
	}
	m=0;
}

char receiveData()
{
 return st;
}




int parseOK(char *ch)
{
 //asm("wdr");
  reset();
  while(*ch != '\0')
	{
		UDR2=*ch;
		ch++;
		_delay_ms(1);

	}
	_delay_ms(100);
	 UDR2== 0xA;
	 _delay_ms(100);
	 UDR2=0xD;
	 UDR2=0xA;
	 _delay_ms(500); 

    if(st[i-2]=='O'&&st[i-1]=='K')
	return 1;
	else
	return 0;

}




/*void sendData(char *ch)
{
  char result[50];
  check=0; 
  reset();
  
  while(*ch != '\0')
	{
		UDR2=*ch;
		ch++;
		_delay_ms(50);

	}
	_delay_ms(100);
	 UDR2== 0xA;
	 _delay_ms(100);
	 UDR2=0xD;
	 UDR2=0xA;	
 }*/




//Function To Initialize all The Devices
void init_devices5()
{
 cli(); //Clears the global interrupts
 uart2_init(); //Initailize UART1 for serial communiaction
 sei();   //Enables the global interrupts
}


int connectDevice()
{
  init_devices5();
  if(parseOK("AT"))
   {
     if(parseOK("AT+CIPMUX=1"))
     {
      //disp("WIFI SETUP COMPL");
	  _delay_ms(1000);
	  return 1;
	  }
	  else
	  {
       //disp("CIPMUX NOT SET");
	   //return 0;
	   }
    }
   else;
   {
   // disp("ESP CONN. ERROR");
     return 0;
   }
   
  //parseOK("AT+CIPSTART=2,\"TCP\",\"192.168.0.8\",80")
  //parseOK("AT+CIPSEND=2,10")
}

int connectIP1()//char *ch)       //L
{
 return parseOK("AT+CIPSTART=2,\"TCP\",\"192.168.0.6\",80");
 cf1=1;
 _delay_ms(500);
 
}

int connectIP2()//char *ch)     // Bot2
{
	return parseOK("AT+CIPSTART=2,\"TCP\",\"192.168.0.3\",80");
	cf1=1;
	_delay_ms(500);
	
}

int connectIP3()//char *ch)    // Bot3
{
	return parseOK("AT+CIPSTART=2,\"TCP\",\"192.168.0.5\",80");
	cf1=1;
	_delay_ms(500);
	
}

int connectIP4()//char *ch)     // Bot 4
{
	return parseOK("AT+CIPSTART=2,\"TCP\",\"192.168.0.7\",80");
	cf1=1;
	_delay_ms(500);
	
}

int connectIP5()//char *ch)
{
	return parseOK("AT+CIPSTART=2,\"TCP\",\"192.168.0.9\",80");
	cf1=1;
	_delay_ms(500);
	
}

int startServer()
{
	return parseOK("AT+CIPSERVER=1,80");
	_delay_ms(500);
}

void sendmsg1(char q[])
{ 
 char p[]="AT+CIPSEND=0,4";
 parseOK(p);
 _delay_ms(400); 
 parseOK(q);
}
void sendmsgs(char q[])
{
	char p[]="AT+CIPSEND=2,4";
	parseOK(p);
	_delay_ms(400);
	parseOK(q);
}
void IPDParseBegin()
{
	flag=1;
}	
void IPDParseEnd()
{
	flag=0;
	numreset();
}
