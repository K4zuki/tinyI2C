/** uart_i2c_conv for LPC11UXX
*/

#include "mbed.h"
#include "I2C_FmPlus.h"
#define isuse_USB_SERIAL

#if defined(TARGET_LPC11U35_401) || defined(TARGET_LPC11U35_501) || defined(TARGET_LPC11U24) 
#include "USBSerial.h"
USBSerial pc;
#else
Serial pc(USBTX, USBRX);
#endif
I2C_FmPlus dev1( P0_5, P0_4 );

int main()
{
    I2C_FmPlus* dev = &dev1;
#ifndef isuse_USB_SERIAL
    pc.baud(115200);
#endif

    bool s = false;
    dev1.frequency(1000000);//1M

    int ack = 0;
    int plength = 0;
    char recieve[256];
    char send[256];
    char read = 0;
    int address = 0;
    int data = 0;
    int _data = 0;
    int length = 0;
    int channel = 0;
    bool CE = false;
    enum channel_e {
        CH0 = '0',
        CH1 = '1',
        CH2 = '2',
        CH3 = '3',
    };
    enum register_e {
        CHIP_ID = '0',
        GPIO_STAT = '1',
        GPIO_CONF = '2',
    };
    enum chipID_e {
        ID_LPC824 = '0',
        ID_LPC1768 = '1',
        ID_LPC11UXX = '2',
    };
    uint8_t chip_id=ID_LPC11UXX;
    uint8_t registers[]={
        chip_id,
        0b00000000, // all 0
        0b00000000, // all input
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
                            channel='0';
                            dev=&dev1;
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
/* hidden
                        dev->start();
                        ack=dev->write(address);
*/
                        if( (address&0x01)) {//read
                            dev->read(address, send, length, false); //added
                            s=false; //added
/* hidden
                            for(int j=0; j<length; j++) {
                                send[j] = dev->read(1);
                            }
*/
                            i+=(5);
                        } else {//write
                            for(int j=0; j < (length * 2); j+=2) {
                                ack = dev->write( 0xff&(recieve[5+j] << 4 | (recieve[6+j] & 0x0F)) );
                                *(send+(j/2)) = ack; //added
                            }
                            dev->write(address, send, length, true); //added
                            i+=(5 + length * 2);
                            length=0;
                        }
                    }else{
                        pc.printf("bad packet! %d, %d, %02X, %d\n\r",plength,i,recieve[(i+2)]&0x0F,ack);
                        i = plength;
                    }
                    break;
                }
                case 'P':
                {
                    if(s){
                        dev->stop();
                        s = false;
                    }
                    i = plength;
                    for(int j=0; j<length; j++) {
                        pc.printf("%02X,",send[j]);
                    }
                    pc.printf("ok\n\r");
                    break;
                }
                case 'R':
                {
                    length = plength - 2;
                    for(int j=0; j<length; j++){
                        address = recieve[1+j];
                        switch(address){
                            case CHIP_ID:
                            {
                                *(send+j) = registers[CHIP_ID];
                                break;
                            }
                            case GPIO_STAT:
                            {
                                *(send+j) = registers[GPIO_STAT];
                                break;
                            }
                            case GPIO_CONF:
                            {
                                *(send+j) = registers[GPIO_CONF];
                                break;
                            }
                            default:
                            {
                                break;
                            }
                        }
                    }
                    i += length;
                    pc.printf("command R is not implemented\n\r");
                    break;
                }
                case 'W':
                {
                    length = plength - 2;
                    if(length < 3){
                        pc.printf("bad packet! %d\n\r",length);
                        i = plength + 1;
                    }else{
                        for(int j=0; j<length; j+=3){
                            address = recieve[i+1+j];
                            data = 0xff & (recieve[i+1+j] << 4 | (recieve[i+2+j] & 0x0F));
                            switch(address){
                                case CHIP_ID:
                                {
                                    //READ ONLY: do nothing
                                    *(send+j) = registers[CHIP_ID];
                                    break;
                                }
                                case GPIO_STAT:
                                {
                                    //READ ONLY from this command: do nothing
                                    *(send+j) = registers[GPIO_STAT];
                                    break;
                                }
                                case GPIO_CONF:
                                {
                                    registers[GPIO_CONF] = data;
                                    *(send+j) = registers[GPIO_CONF];
                                    break;
                                }
                                default:
                                {
                                    break;
                                }
                            }
                        }
                    }
                    i += length;
                    pc.printf("command W is not implemented\n\r");
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
                case 'E':
                {
                    pc.printf("command E is not implemented\n\r");
                    i=plength;
                    break;
                }
                case 'V':
                {
                    pc.printf("command V is not implemented\n\r");
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
