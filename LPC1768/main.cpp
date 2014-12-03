#include "mbed.h"
//#define isuse_USB_SERIAL

#ifdef isuse_USB_SERIAL
#include "USBSerial.h"
USBSerial pc;
#else
Serial pc(USBTX,USBRX);
#endif
I2C dev1(p9,p10);
I2C dev2(p28,p27);
I2C* dev=&dev1;
BusOut bus(LED1,LED2);

//Table 3. ASCII commands supported by SC18IM700
//ASCII command Hex value Command function
//[X] S 0x53 I2C-bus START
//[X] P 0x50 I2C-bus STOP
//[_] R 0x52 read SC18IM700 internal register
//[_] W 0x57 write to SC18IM700 internal register
//[_] I 0x49 read GPIO port
//[_] O 0x4F write to GPIO port
//[_] Z 0x5A power down

int main()
{
#ifndef isuse_USB_SERIAL
    pc.baud(115200);
#endif
    dev1.frequency(100000);//100k
    dev2.frequency(100000);//100k

    int plength=0;
    char recieve[256];
    char read=0;
    int address=0,length=0,channel=0;
    enum reg {
        I2C0adr='0',
        I2C1adr='1',
        I2C2adr='2',
        I2C3adr='3',
    };
    int i=0;
    while(1) {
        while(true) {
            read=pc.getc();
            recieve[i]=read;
//pc.printf("%02X,",read);
            i++;
            if(read == 'P') {
                plength=i;
//pc.printf("P\n\r");
                break;
            }
        }
        i=0;
        while(i<plength) {
            switch(recieve[i]) {
                case 'C':
                    channel=recieve[i+1];
                    switch(channel) {
                        case I2C0adr:
                            bus=0x01;
//pc.printf("ch0 is selected,");
                            channel='0';
                            dev=&dev1;
                            break;
                        case I2C1adr:
                            bus=0x02;
//pc.printf("ch1 is selected,");
                            channel='1';
                            dev=&dev2;
                            break;
/** LPC1768 has only two I2C channels
                        case I2C2adr:
                            bus=0x04;
//pc.printf("ch2 is not implemented,");
                            channel='0';
                            //dev=&dev3;
                            break;
                        case I2C3adr:
                            bus=0x08;
//pc.printf("ch3 is not implemented,");
                            channel='0';
                            //dev=&dev4;
                            break;
*/
                        default:
                            channel='0';
                            dev=&dev1;
                            break;
                    }
                    i+=(2);
                    break;
                case 'S':
                    address=recieve[i+1];
                    length=recieve[i+2];
//pc.printf("addr=%02X, length=%d,",address,length);
                    dev->start();
                    dev->write(address);
                    if( (address&0x01)) {//read
//pc.printf("read from ch%c,",channel);
                        for(int j=0; j<length; j++) {
                            pc.putc(dev->read(0));
//pc.printf("%02X,",dev->read(0));
                        }
                        i+=(3);
                    } else {//write
//pc.printf("write to ch%c, ",channel);
                        for(int j=0; j<length; j++) {
//pc.printf("%02X,",recieve[3+j]);
                            dev->write(recieve[3+j]);
                        }
                        i+=(3+length);
                    }
                    break;
                case 'P':
                    dev->stop();
                    i=plength;
                    pc.printf("ok\n\r");
                    break;
                case 'R':
                    pc.printf("command R is not implemented\n\r");
                    i=plength;
                    break;
                case 'W':
                    pc.printf("command W is not implemented\n\r");
                    i=plength;
                    break;
                case 'I':
                    pc.printf("command I is not implemented\n\r");
                    i=plength;
                    break;
                case 'O':
                    pc.printf("command O is not implemented\n\r");
                    i=plength;
                    break;
                case 'Z':
                    pc.printf("command Z is not implemented\n\r");
                    i=plength;
                    break;
                default:
                    pc.printf("command ? is not implemented\n\r");
                    i=plength;
                    break;
            }
        }
        i=0;

    }
}
