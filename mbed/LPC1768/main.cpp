/** uart_i2c_conv for LPC1768
*/

#include "mbed.h"
//#define isuse_USB_SERIAL

#ifdef isuse_USB_SERIAL
#include "USBSerial.h"
USBSerial pc;
#else
Serial pc(USBTX,USBRX);
#endif
I2C dev1(p28, p27);
I2C dev2(p9, p10);
I2C* dev=&dev1;

int main()
{
    I2C* dev=&dev1;
#ifndef isuse_USB_SERIAL
    pc.baud(115200);
#endif

    bool s = false;
    dev1.frequency(400000);//400k
    dev2.frequency(400000);//400k

    int ack=0;
    int plength=0;
    char recieve[256];
    char send[256];
    char read=0;
    int address=0,length=0,channel=0;
    enum reg {
        I2C0adr='0',
        I2C1adr='1',
    };

//"C0P"
//"C1P"
//"C2P"
//"C3P"
//"S| 0x_8 _0| 0x_0 _4| 0x_D _E _A _D _B _E _A _F| P"
//"S| 0x_8 _0| 0x_0 _4| 0x_D _E _A _D _B _E _A _F| S| 0x_8 _1| 0x_0 _4| P"
//"S| 0x_8 _1| 0x_0 _4| P"

    int i=0;
    while(1) {
        while(true) {
            read=pc.getc();
            recieve[i]=read;
            i++;
            if(read == 'P') {
                plength=i;
                break;
            }
        }
        i=0;
        while(i < plength) {
            switch(recieve[i]) {
                case 'C':
                {
                    channel=recieve[i+1];
                    switch(channel) {
                        case I2C0adr:
                        {
                            bus=~0x01;
                            channel='0';
                            dev=&dev1;
                            break;
                        }
                        case I2C1adr:
                        {
                            bus=~0x02;
                            channel='1';
                            dev=&dev2;
                            break;
                        }
                        default:
                        {
                            channel='0';
                            dev=&dev1;
                            break;
                        }
                    }
                    i+=(2);
                    break;
                }
                case 'S':
                {
                    s = true;
                    ack = plength - 2 - (i+1) + (recieve[i+2] & 0x01);
                    if( ack >= 4){ //valid packet
                        address = 0xff & (recieve[i+1] << 4 | (recieve[i+2] & 0x0F));
                        length = 0xff & (recieve[i+3] << 4 | (recieve[i+4] & 0x0F));
                    }else{
                        pc.printf("bad packet! %d, %d, %02X, %d\n\r",plength,i,recieve[(i+2)]&0x0F,ack);
                        i = plength + 1;
                        break;
                    }
                    dev->start();
                    ack=dev->write(address);
                    if( (address&0x01)) {//read
                        for(int j=0; j<length; j++) {
                            send[j] = dev->read(1);
                        }
                        i+=(5);
                    } else {//write
                        for(int j=0; j < (length * 2); j+=2) {
                            ack = dev->write( 0xff&(recieve[5+j] << 4 | (recieve[6+j] & 0x0F)) );
                        }
                        i+=(5 + length * 2);
                        length=0;
                    }
                    break;
                }
                case 'P':
                    if(s){
                        dev->stop();
                        s=false;
                    }
                    i=plength;
                    for(int j=0; j<length; j++) {
                        pc.printf("%02X,",send[j]);
                    }
                    pc.printf("ok\n\r");
                    break;
                case 'R':
                {
                    pc.printf("command R is not implemented\n\r");
                    i=plength;
                    break;
                }
                case 'W':
                {
                    pc.printf("command W is not implemented\n\r");
                    i=plength;
                    break;
                }
                case 'I':
                {
                    pc.printf("command I is not implemented\n\r");
                    i=plength;
                    break;
                }
                case 'O':
                {
                    pc.printf("command O is not implemented\n\r");
                    i=plength;
                    break;
                }
                case 'Z':
                {
                    pc.printf("command Z is not implemented\n\r");
                    i=plength;
                    break;
                }
                default:
                {
                    pc.printf("command ? is not implemented\n\r");
                    i=plength;
                    break;
                }
            }
        }
        i=0;
        length=0;
    }
}
