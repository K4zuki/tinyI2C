/** uart_i2c_conv for LPC824
*/

//hoge

#include "mbed.h"
#define QUAD_I2C
/** replaceD
//Serial pc(USBTX,USBRX); // P0_7, P0_18
*/
Serial pc(P0_4, P0_0);
//P0_13, P0_1

I2C dev1(I2C_SDA, I2C_SCL);//11,10 hard coded, 220 ohm pull-up

#ifdef QUAD_I2C
I2C dev2(P0_6, P0_14);//6,14 | A0, A1
I2C dev3(P0_23, P0_22);//23,22 | A2, A3
I2C dev4(P0_21, P0_20);//21,20 | A4, A5
/** replace
I2C dev2(P0_16, P0_27);
I2C dev3(P0_26, P0_25);
I2C dev4(P0_24, P0_15);
*/
#else
DigitalInOut _GPIO10(P0_15);
DigitalInOut _GPIO11(P0_24);
DigitalInOut _GPIO12(P0_25);
DigitalInOut _GPIO13(P0_26);
DigitalInOut _GPIO14(P0_27);
DigitalInOut _GPIO15(P0_16);
DigitalInOut _GPIO16(P0_28);
DigitalInOut _GPIO17(P0_12);
#endif

DigitalInOut _GPIO00(D2); // P0_19
DigitalInOut _GPIO01(D3); // P0_12
DigitalInOut _GPIO02(D4); // P0_18
DigitalInOut _GPIO03(D5); // P0_28
DigitalInOut _GPIO04(D6); // P0_16
DigitalInOut _GPIO05(D7); // P0_17
DigitalInOut _GPIO06(D8); // P0_13
DigitalInOut _GPIO07(D9); // P0_27
/** replace
DigitalInOut _GPIO00(P0_17);
DigitalInOut _GPIO01(P0_18);
DigitalInOut _GPIO02(P0_19);
DigitalInOut _GPIO03(P0_20);
DigitalInOut _GPIO04(P0_21);
DigitalInOut _GPIO05(P0_22);
DigitalInOut _GPIO06(P0_23);
DigitalInOut _GPIO07(P0_14);
*/

SPI _spi(D11, D12, D13); // mosi, miso, sclk
DigitalOut _cs(D10); // CS
/** replace
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
"I| '0'| P"
"O| '0'| 0x_a _a| P"
*/
int main()
{
    I2C* dev=&dev1;
    pc.baud(115200);

    bool s = false;
    dev1.frequency(900000);//900k; works around 940kHz with 200ohm pullups/ not work at 1M? 
    LPC_IOCON->PIO0_11 &= ~(0x03<<8);
    LPC_IOCON->PIO0_11 |= (0x02<<8);
    LPC_IOCON->PIO0_10 &= ~(0x03<<8);
    LPC_IOCON->PIO0_10 |= (0x02<<8);
//    LPC_I2C0->CLKDIV &= 0xFFFFFF00;
//    LPC_I2C0->CLKDIV |= 0x05;
//    LPC_I2C0->MSTTIME &= 0xFFFFFF00;
//    LPC_I2C0->MSTTIME |= 0x00;
#ifdef QUAD_I2C
    dev2.frequency(400000);//400k
    dev3.frequency(400000);//400k
    dev4.frequency(400000);//400k
#else
    DigitalInOut* gpio1[]={
        &_GPIO10,
        &_GPIO11,
        &_GPIO12,
        &_GPIO13,
        &_GPIO14,
        &_GPIO15,
        &_GPIO16,
        &_GPIO17,
    };
    for(int k=0; k<8; k++){
        gpio1[k]->input();
        gpio1[k]->mode(PullDown);
    }
#endif
    DigitalInOut* gpio0[]={
        &_GPIO00,
        &_GPIO01,
        &_GPIO02,
        &_GPIO03,
        &_GPIO04,
        &_GPIO05,
        &_GPIO06,
        &_GPIO07,
    };
    for(int k=0; k<8; k++){
        gpio0[k]->input();
        gpio0[k]->mode(PullDown);
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
        GPIO0_STAT = '1',
        GPIO1_STAT = '2',
        GPIO0_CONF = '3',
        GPIO1_CONF = '4',
        REG5,
        REG6,
        REG7,
        REG8,
        REG9,
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
        0xDD,
        0xEE,
        REG5,
        REG6,
        REG7,
        REG8,
        REG9,
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
#ifdef QUAD_I2C
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
#endif
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

                        if(address & 0x01) { //read
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
                    if(length < 1){
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
                                    break;
                                }
                                case GPIO0_STAT:
                                {
                                    for(int k=0; k<8; k++){
                                        _data = gpio0[k]->read();
                                        data |= (_data << k);
                                    }
                                    registers[GPIO0_STAT-'0'] = data;
                                    break;
                                }
                                case GPIO0_CONF:
                                {
                                    data = registers[GPIO0_CONF-'0'];
                                    break;
                                }
#ifndef QUAD_I2C
                                case GPIO1_STAT:
                                {
                                    for(int k=0; k<8; k++){
                                        _data = gpio1[k]->read();
                                        data |= (_data << k);
                                    }
                                    registers[GPIO1_STAT-'0'] = data;
                                    break;
                                }
                                case GPIO1_CONF:
                                {
                                    data = registers[GPIO1_CONF-'0'];
                                    break;
                                }
#endif
                                default:
                                {
                                    data = 0xAA;
                                    break;
                                }
                            }
                            send[j] = (char)data;
                            data=0;
                        }
                        i += (length+1);
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
                            _data = 0;
                            switch(address){
                                case CHIP_ID:
                                {
                                    //READ ONLY: do nothing
                                    data = registers[CHIP_ID-'0'];
                                    break;
                                }
                                case GPIO0_STAT:
                                {
                                    _data = registers[GPIO0_CONF-'0'];
                                    for(int k=0; k<8; k++){
                                        if(_data&0x01){ // output
                                            gpio0[k]->write((data>>k)&0x01);
                                        }else{ // input
                                            ; // do nothing
                                        }
                                        _data >>= 1;
                                    }
                                    break;
                                }
                                case GPIO0_CONF:
                                {
                                    registers[GPIO0_CONF-'0'] = data;
                                    for(int k=0; k<8; k++){
                                        if(data&0x01){//output
                                            gpio0[k]->output();
                                        }else{//input
                                            gpio0[k]->input();
                                            gpio0[k]->mode(PullUp);
                                        }
                                        data >>= 1;
                                    }
                                    data = registers[GPIO0_CONF-'0'];
                                    break;
                                }
#ifndef QUAD_I2C
                                case GPIO1_STAT:
                                {
                                    _data = registers[GPIO1_CONF-'0'];
                                    for(int k=0; k<8; k++){
                                        if(_data&0x01){ // output
                                            gpio1[k]->write((data>>k)&0x01);
                                        }else{ // input
                                            ; // do nothing
                                        }
                                        _data >>= 1;
                                    }
                                    break;
                                }
                                case GPIO1_CONF:
                                {
                                    registers[GPIO1_CONF-'0'] = data;
                                    for(int k=0; k<6; k++){
                                        if(data&0x01){//output
                                            gpio1[k]->output();
                                        }else{//input
                                            gpio1[k]->input();
                                            gpio1[k]->mode(PullUp);
                                        }
                                        data >>= 1;
                                    }
                                    data = registers[GPIO1_CONF-'0'];
                                    break;
                                }
#endif
                                default:
                                {
                                    break;
                                }
                            }
                            send[j/3] = data;
                        }
                        i += (length+1);
                        length /= 3;
                    }
                    break;
                }
                case CMD_I:
                {
                    length = plength - 2;
                    if(length < 1){
                        pc.printf("bad packet! %d\n\r",length);
                        i = plength + 1;
                        length = 0;
                    }else{
                        for(int j=0; j<length; j++){
                            address = recieve[i+1+j];
                            _data=0;
                            switch(address){
                                case GPIO0_STAT:
                                {
                                    for(int k=0; k<8; k++){
                                        _data = gpio0[k]->read();
                                        data |= (_data << k);
                                    }
                                    registers[GPIO0_STAT-'0'] = data;
                                    break;
                                }
#ifndef QUAD_I2C
                                case GPIO1_STAT:
                                {
                                    for(int k=0; k<8; k++){
                                        _data = gpio1[k]->read();
                                        data |= (_data << k);
                                    }
                                    registers[GPIO1_STAT-'0'] = data;
                                    break;
                                }
#endif
                                default:
                                {
                                    data = 0xAA;
                                    break;
                                }
                            }
                            send[j] = (char)data;
                            data = 0;
                        }
                        i += (length+1);
                    }
                    break;
                }
                case CMD_O:
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
                                case GPIO0_STAT:
                                {
                                    _data = registers[GPIO0_CONF-'0'];
                                    for(int k=0; k<8; k++){
                                        if(_data&0x01){ // output
                                            gpio0[k]->write(data&0x01);
                                        }else{ // input
                                            ; // do nothing
                                        }
                                        data >>= 1;
                                        _data >>= 1;
                                    }
                                    break;
                                }
#ifndef QUAD_I2C
                                case GPIO1_STAT:
                                {
                                    _data = registers[GPIO1_CONF-'0'];
                                    for(int k=0; k<8; k++){
                                        if(_data&0x01){ // output
                                            gpio1[k]->write(data&0x01);
                                        }else{ // input
                                            ; // do nothing
                                        }
                                        data >>= 1;
                                        _data >>= 1;
                                    }
                                    break;
                                }
#endif
                                default:
                                {
                                    break;
                                }
                            }
                            send[j/3] = data;
                        }
                    }
                    i += (length+1);
                    length /= 3;
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
