/** uart_i2c_conv for LPC824
*/

#include "mbed.h"

Serial pc(USBTX,USBRX);
I2C dev1(I2C_SDA, I2C_SCL);//11,10 hard coded
I2C dev2(P0_6, P0_14);//6,14
I2C dev3(P0_23, P0_22);//23,22
I2C dev4(P0_21, P0_20);//21,20

//DigitalInOut _GPIO0(D0);
//DigitalInOut _GPIO1(D1);
//DigitalInOut _GPIO2(D2);
//DigitalInOut _GPIO3(D3);
//DigitalInOut _GPIO4(D4);
//DigitalInOut _GPIO5(D5);
//DigitalInOut _GPIO6(D6);
//DigitalInOut _GPIO7(D7);

//Table 3. ASCII commands supported by SC18IM700
//ASCII command Hex value Command function
//[X] S 0x53 I2C-bus START
//[X] P 0x50 I2C-bus STOP
//[?] R 0x52 read SC18IM700 internal register
//[?] W 0x57 write to SC18IM700 internal register
//[?] I 0x49 read GPIO port
//[?] O 0x4F write to GPIO port
//[_] Z 0x5A power down
//[X] C 0x43 change channel
//[_] E 0x45 enable chip
//[_] V 0x__ enable VDDIO output to chip

int main()
{
    I2C* dev=&dev1;
    pc.baud(115200);

    LPC_IOCON->PIO0_11 &= ~(0x02<<8);
    LPC_IOCON->PIO0_11 |= (0x02<<8);
    LPC_IOCON->PIO0_10 &= ~(0x02<<8);
    LPC_IOCON->PIO0_10 |= (0x02<<8);

    bool s = false;
    dev1.frequency(800000);//800k not work at 1M? too large pullup?
    dev2.frequency(400000);//400k
    dev3.frequency(400000);//400k
    dev4.frequency(400000);//400k

    int ack=0;
    int plength=0;
    char recieve[256];
    char send[256];
    char read=0;
    int address=0;
    int length=0;
    int channel=0;
    bool CE=false;
    enum channel_e {
        CH0 = '0',
        CH1 = '1',
        CH2 = '2',
        CH3 = '3',
    };
    enum register_e {
        CHIP_ID = '0'
        GPIO_STAT = '1',
        GPIO_CONF = '2',
    };
    enum chipID_e {
        ID_LPC824 = '0',
        ID_LPC1768 = '1',
        ID_LPC11UXX = '2',
    };
    uint8_t chip_id=ID_LPC824;
    uint8_t registers[]={
        chip_id,
        0b00000000,
        0b00000000,
    };

//"C0P"
//"C1P"
//"C2P"
//"C3P"
//"S| 0x_8 _0| 0x_0 _4| 0x_D _E _A _D _B _E _A _F| P"
//"S| 0x_8 _0| 0x_0 _4| 0x_D _E _A _D _B _E _A _F| S| 0x_8 _1| 0x_0 _4| P"
//"S| 0x_8 _1| 0x_0 _4| P"
//"R| '0'| P"
//"R| '0'| '1'| P"
//"W| '0' 0x_a _a| P"
//"W| '0' 0x_a _a| '1' 0x_b _b| P"
//"I| P"
//"O| 0x_a _a| P"

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
                        case CH0:
                        {
                            channel='0';
                            dev=&dev1;
                            break;
                        }
                        case CH1:
                        {
                            channel='1';
                            dev=&dev2;
                            break;
                        }
                        case CH2:
                        {
                            channel='2';
                            dev=&dev3;
                            break;
                        }
                        case CH3:
                        {
                            channel='3';
                            dev=&dev4;
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
                    break;
                }
                case 'P':
                {
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
                }
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
