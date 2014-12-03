#include "mbed.h"

Serial pc(USBTX,USBRX);
//Serial mon(D1,NC);
/*
    D5 = P0_28,
    D6 = P0_16, // LED_GREEN
    D7 = P0_17,
    D8 = P0_13,
    D9 = P0_27, // LED_BLUE
    D10 = P0_15,
    D11 = P0_26,
    D12 = P0_25,
    D13 = P0_24,
*/
I2C dev1(I2C_SDA,I2C_SCL);//11,10 hard coded
I2C dev2(A0,A1);//6,14
I2C dev3(A2,A3);//23,22
I2C dev4(A4,A5);//21,20
BusOut bus(LED1,LED2,LED3,LED4);
//DigitalOut led1(LED1);
//DigitalOut led2(LED2);
//DigitalOut led3(LED3);
//DigitalOut led4(LED4);

//Table 3. ASCII commands supported by SC18IM700
//ASCII command Hex value Command function
//[X] S 0x53 I2C-bus START
//[X] P 0x50 I2C-bus STOP
//[_] R 0x52 read SC18IM700 internal register
//[_] W 0x57 write to SC18IM700 internal register
//[_] I 0x49 read GPIO port
//[_] O 0x4F write to GPIO port
//[_] Z 0x5A power down
//[X] C 0x43 change channel

int main()
{
    I2C* dev=&dev1;
    pc.baud(115200);
//mon.baud(115200);
//pc.printf("%08X\n\r",LPC_IOCON->PIO0_11 );
//pc.printf("%08X\n\r",LPC_IOCON->PIO0_10 );
LPC_IOCON->PIO0_11 &= ~(0x02<<8);
LPC_IOCON->PIO0_11 |= (0x02<<8);
LPC_IOCON->PIO0_10 &= ~(0x02<<8);
LPC_IOCON->PIO0_10 |= (0x02<<8);
//pc.printf("%08X\n\r",LPC_IOCON->PIO0_11 );
//pc.printf("%08X\n\r",LPC_IOCON->PIO0_10 );

    bool s=false;
    dev1.frequency(800000);//100k
    dev2.frequency(400000);//100k
    dev3.frequency(400000);//100k
    dev4.frequency(400000);//100k

pc.printf("%08X\n\r",LPC_IOCON->PIO0_11 );
pc.printf("%08X\n\r",LPC_IOCON->PIO0_10 );
//LPC_I2C0->CLKDIV &= 0xFFFFFF00;
//LPC_I2C0->CLKDIV |= 0x05;
//LPC_I2C0->MSTTIME &= 0xFFFFFF00;
//LPC_I2C0->MSTTIME |= 0x11;
//pc.printf("%08X\n\r",LPC_SYSCON->SYSAHBCLKDIV );
pc.printf("%08X\n\r",LPC_I2C0->CLKDIV );
pc.printf("%08X\n\r",LPC_I2C0->MSTTIME );
//    int data=0x50;
    int ack=0;
    int plength=0;
    char recieve[256];
char send[256];
    char read=0;
    int address=0,length=0,channel=0;
    enum reg {
        I2C0adr='0',
        I2C1adr='1',
        I2C2adr='2',
        I2C3adr='3',
    };
//"C0P"
//"S| 0x08 0x00| 0x00 0x04| 0xD0E0A0D0B0E0A0F|P"
//"C1P"
//"S(0x80)(4)(0xDEADBEAF)P"
//"C2P"
//"S(0x80)(4)(0xDEADBEAF)P"
//"C3P"
//"S(0x80)(4)(0xDEADBEAF)P"
//dev1.start();
//dev1.write(address);
//dev1.stop();

    int i=0;
    while(1) {
        while(true) {
////            led1=0;
            read=pc.getc();
            recieve[i]=read;
//pc.printf("%02X,",read); //debug
            i++;
            if(read == 'P') {
                plength=i;
////                led1=1;
//pc.printf("P\n\r");
                break;
            }
        }
for(i=0;i<plength;i++){
//mon.printf("%02X,",recieve[i]); //debug
}
        i=0;
        while(i<plength) {
//mon.printf("%c,",recieve[i]);
            switch(recieve[i]) {
                case 'C':
                {
                    channel=recieve[i+1];
                    switch(channel) {
                        case I2C0adr:
                        {
                            bus=~0x01;
//pc.printf("ch0 is selected,");
                            channel='0';
                            dev=&dev1;
                            break;
                        }
                        case I2C1adr:
                        {
                            bus=~0x02;
//pc.printf("ch1 is selected,");
                            channel='1';
                            dev=&dev2;
                            break;
                        }
                        case I2C2adr:
                        {
                            bus=~0x04;
//pc.printf("ch2 is selected,");
                            channel='2';
                            dev=&dev3;
                            break;
                        }
                        case I2C3adr:
                        {
                            bus=~0x08;
//pc.printf("ch3 is selected,");
                            channel='3';
                            dev=&dev4;
                            break;
                        }
                        default:
                        {
//pc.printf("ch? is not implemented,");
                            channel='0';
                            dev=&dev1;
                            break;
                        }
                    }
                    i+=(2);
                    break;
                }
// S|0xD0|0x01|0xAA|S|0xD1|0x01|P
                case 'S':
                {
                    s=true;
//ack=((plength-i)>>1)+(0x01&recieve[(i+2)]);
ack=plength-2-(i+1)+(0x01&recieve[(i+2)]);
if( ack >=4){
//if(plength>=4){
                        address=0xff&(recieve[i+1]<<4|(recieve[i+2]&0x0F));
                        length=0xff&(recieve[i+3]<<4|(recieve[i+4]&0x0F));
}else{
    pc.printf("bad packet! %d, %d, %02X, %d\n\r",plength,i,recieve[(i+2)]&0x0F,ack);
//mon.printf("bad packet! %d, %d, %02X, %d\n\r",plength,i,recieve[(i+2)]&0x0F,ack);
    i=plength+1;
    break;
}
//pc.printf("addr=%02X, length=%d,",address,length);
//dev1.start();
//dev1.write(address);
                    dev->start();
ack=dev->write(address);
//if(ack==0){
//    dev->stop();
//    pc.printf("0x%02X returned %d\n\r",address,ack);
//    i=plength+1;
//    break;
//}
////                    dev->write(address);
                    if( (address&0x01)) {//read
//pc.printf("read from ch%c,",channel);
                        for(int j=0; j<length; j++) {
send[j]=dev->read(1);
////                            pc.printf("%02X,",dev->read(1));
//pc.printf("%02X,",dev1.read(0));
                        }
                        i+=(5);
                    } else {//write
//pc.printf("write to ch%c, ",channel);
                        for(int j=0; j<(length*2); j+=2) {
//pc.printf("%02X,",recieve[3+j]);
//dev1.write(recieve[3+j]);
                            ack=dev->write( 0xff&(recieve[5+j] << 4 | (recieve[6+j] & 0x0F)) );
//pc.printf("ack=%d\n\r",ack);
                        }
                        i+=(5+length*2);
                        length=0;
                    }
                    break;
                }
                case 'P':
//dev1.stop();
                    if(s){
                        dev->stop();
                        s=false;
                    }
                    i=plength;
                    for(int j=0; j<length; j++) {
                        pc.printf("%02X,",send[j]);
//mon.printf("%02X,",send[j]);
                    }
                    pc.printf("ok\n\r");
//mon.printf("ok\n\r");
                    break;
                case 'R':
                    pc.printf("command R is not implemented\n\r");
//mon.printf("command R is not implemented\n\r");
                    i=plength;
                    break;
                case 'W':
                    pc.printf("command W is not implemented\n\r");
//mon.printf("command W is not implemented\n\r");
                    i=plength;
                    break;
                case 'I':
                    pc.printf("command I is not implemented\n\r");
//mon.printf("command I is not implemented\n\r");
                    i=plength;
                    break;
                case 'O':
                    pc.printf("command O is not implemented\n\r");
//mon.printf("command O is not implemented\n\r");
                    i=plength;
                    break;
                case 'Z':
                    pc.printf("command Z is not implemented\n\r");
//mon.printf("command Z is not implemented\n\r");
                    i=plength;
                    break;
                default:
                    pc.printf("command ? is not implemented\n\r");
//mon.printf("command %02X is not implemented\n\r",recieve[i]);
                    i=plength;
                    break;
            }
        }
        i=0;
        length=0;
    }
}
