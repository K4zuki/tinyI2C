/** uart_i2c_conv for LPC824
*/

#include "mbed.h"

Serial pc(USBTX,USBRX);
I2C dev1(I2C_SDA, I2C_SCL);//11,10 hard coded

I2C dev2(P0_6, P0_14);//6,14 | A0, A1
I2C dev3(P0_23, P0_22);//23,22 | A2, A3
I2C dev4(P0_21, P0_20);//21,20 | A4, A5
/*
I2C dev2(P0_16, P0_27);
I2C dev3(P0_26, P0_25);
I2C dev4(P0_24, P0_15);
*/
DigitalInOut _GPIO0(LED1); // D0
DigitalInOut _GPIO1(LED2); // D1
DigitalInOut _GPIO2(LED3); // D2
DigitalInOut _GPIO3(D3); // D3
DigitalInOut _GPIO4(D4); // D4
DigitalInOut _GPIO5(D5); // D5
DigitalInOut _GPIO6(D6); // D6
DigitalInOut _GPIO7(D7); // D7
/*
DigitalInOut _GPIO0(P0_17);
DigitalInOut _GPIO1(P0_18);
DigitalInOut _GPIO2(P0_19);
DigitalInOut _GPIO3(P0_20);
DigitalInOut _GPIO4(P0_21);
DigitalInOut _GPIO5(P0_22);
DigitalInOut _GPIO6(P0_23);
DigitalInOut _GPIO7(P0_14);
*/

SPI _spi(D11, D12, D13); // mosi, miso, sclk
/*
SPI _spi(P0_6, P0_7, P0_8); // mosi, miso, sclk
DigitalOut _cs(P0_9) // CS
*/
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

/**
"C| '0'| P"
"C| '1'| P"
"C| '2'| P"
"C| '3'| P"
"S| 0x_8 _0| 0x_0 _4| 0x_D _E _A _D _B _E _A _F| P"
"S| 0x_8 _0| 0x_0 _4| 0x_D _E _A _D _B _E _A _F| S| 0x_8 _1| 0x_0 _4| P"
"S| 0x_8 _1| 0x_0 _4| P"
"R| '0'| P"
"R| '0'| '1'| ...| P"
"W| '0' 0x_a _a| P"
"W| '0' 0x_a _a| '1' 0x_b _b| ...| P"
"I| P"
"O| 0x_a _a| P"
*/
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

    DigitalInOut* gpio0[]={
        &_GPIO0,
        &_GPIO1,
        &_GPIO2,
        &_GPIO3,
        &_GPIO4,
        &_GPIO5,
        &_GPIO6,
        &_GPIO7,
    };
    for(int k=0; k<8; k++){
        gpio0[k]->input();
        gpio0[k]->mode(PullUp);
    }

    int ack = 0;
    int plength = 0;
    char recieve[] = {
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
    };
    char send[] = {
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
        0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0A, 0x0F, 0xD0, 0xE0, 0xA0, 0xD0, 0xB0, 0xE0, 0xA0, 0xF0, 
    };

    char read = 0;
    int address = 0;
    int data = 0;
    int _data = 0;
    int length = 0;
    int channel = 0;
    bool CE = false;
    enum command_e {
        CMD_S='S',
        CMD_P='P',
        CMD_C='C',
        CMD_R='R',
        CMD_W='W',
        CMD_I='I',
        CMD_O='O',
    };
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
    static const uint8_t chip_id=ID_LPC824;
    static uint8_t registers[]={
        chip_id,
        0xBB,
        0xCC,
//        0b00000000, // all 0
//        0b00000000, // all input
    };

    int i=0;
    while(1) {
        i=0;
        length=0;
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
                case CMD_C:
                {
                    channel=recieve[i+1];
                    switch(channel) {
                        case CH0:
                        {
                            channel = CH0;
                            dev=&dev1;
                            break;
                        }
                        case CH1:
                        {
                            channel = CH1;
                            dev=&dev2;
                            break;
                        }
                        case CH2:
                        {
                            channel = CH2;
                            dev=&dev3;
                            break;
                        }
                        case CH3:
                        {
                            channel = CH3;
                            dev=&dev4;
                            break;
                        }
                        default:
                        {
                            channel = CH0;
                            dev=&dev1;
                            break;
                        }
                    }
                    i+=(2);
                    break;
                }
                case CMD_S:
                {
                    s = true;
                    ack = plength - 2 - (i+1) + (recieve[i+2] & 0x01);
                    if(ack >= 4){ //valid packet
                        address = 0xff & (recieve[i+1] << 4 | (recieve[i+2] & 0x0F));
                        length = 0xff & (recieve[i+3] << 4 | (recieve[i+4] & 0x0F));

                        if( (address&0x01)) { //read
                            dev->read(address, send, length, false); //added
                            i+=(5);
                        } else { // write
                            for(int j=0; j < (length * 2); j+=2) {
                                ack = 0xff&((recieve[5+j] << 4) | (recieve[6+j] & 0x0F));
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
                case CMD_P:
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
                case CMD_R:
                {
                    length = plength - 2;
                    if(length<1){
                        pc.printf("bad packet! %d\n\r",length);
                        i = plength + 1;
                        length = 0;
                    }else{
                        for(int j=0; j<length; j++){
                            address = recieve[i+1+j];
                            switch(address){
                                case CHIP_ID:
                                {
                                    data = chip_id;
//                                    send[j] = chip_id;
                                    break;
                                }
                                case GPIO_STAT:
                                {
                                    data = registers[GPIO_STAT-'0'];
//                                    send[j] = (char)data;
                                    break;
                                }
                                case GPIO_CONF:
                                {
                                    data = registers[GPIO_CONF-'0'];
//                                    send[j] = (char)data;
                                    break;
                                }
                                default:
                                {
                                    data = 0xAA;
//                                    send[j] = 0xAA;
                                    break;
                                }
                            }
                            send[j] = (char)data;
                        }
                        i += (length+1);
//                        pc.printf("command R is not implemented, ");
                    }
                    break;
                }
                case CMD_W:
                {
                    length = plength - 2;
                    if(length < 3){
                        pc.printf("bad packet! %d\n\r",length);
                        i = plength + 1;
                        length = 0;
                    }else{
                        for(int j=0; j<length; j+=3){
                            address = recieve[i+1+j];
                            data = 0xff & (recieve[i+2+j] << 4 | (recieve[i+3+j] & 0x0F));
                            switch(address){
                                case CHIP_ID:
                                {
                                    //READ ONLY: do nothing
                                    data = registers[CHIP_ID-'0'];
//                                    *(send+j) = registers[CHIP_ID-'0'];
                                    break;
                                }
                                case GPIO_STAT:
                                {
                                    //READ ONLY from this command: do nothing
                                    data = registers[GPIO_STAT-'0'];
//                                    *(send+j) = registers[GPIO_STAT-'0'];
                                    break;
                                }
                                case GPIO_CONF:
                                {
                                    registers[GPIO_CONF-'0'] = data;
//                                    data = 0;
                                    for(int k=0; k<8; k++){
                                        if(data&0x01){//output
                                            gpio0[k]->output();
                                        }else{//input
                                            gpio0[k]->input();
                                            gpio0[k]->mode(PullUp);
                                        }
                                        data >>= 1;
                                    }
                                    data = registers[GPIO_CONF-'0'];
//                                    *(send+j) = registers[GPIO_CONF-'0'];
                                    break;
                                }
                                default:
                                {
                                    break;
                                }
                            }
                            send[j/3] = (char)data;
                        }
                        i += length+1;
                        length /= 3;
                    }
//                    pc.printf("command W is not implemented, ");
                    break;
                }
                case CMD_I:
                {
                    length = plength - 2;
                    data = 0;
                    if(length != 0){
                        pc.printf("bad packet! %d\n\r",length);
                        i = plength + 1;
                        length = 0;
                    }else{
                        for(int j=0; j<8; j++){
                            _data = gpio0[j]->read();
                            data |= (_data << j);
                        }
                        registers[GPIO_STAT-'0'] = data;
                        send[0] = data;
                        length = 1;
                    }
//                    pc.printf("command I is not implemented, ");
                    i+=length;
                    break;
                }
                case CMD_O:
                {
                    length = plength - 2;
                    if(length != 2){
                        pc.printf("bad packet! %d\n\r",length);
                        i = plength + 1;
                        length = 0;
                    }else{
                        data = 0xff & (recieve[i+1] << 4 | (recieve[i+2] & 0x0F));
                        _data = registers[GPIO_CONF-'0'];
                        send[0] = (char)data;
                        for(int j=0; j<8; j++){
                            if(_data&0x01){ // output
                                gpio0[j]->write(data&0x01);
                            }else{ // input
                                ; // do nothing
                            }
                            data >>= 1;
                            _data >>= 1;
                        }
                        i += length+1;
                        length = 1;
                    }
//                    pc.printf("command O is not implemented, ");
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
                    pc.printf("command %c is not implemented\n\r", recieve[i]);
                    i=plength;
                    break;
                }
            }
        }
        i=0;
        length=0;
    }
}
