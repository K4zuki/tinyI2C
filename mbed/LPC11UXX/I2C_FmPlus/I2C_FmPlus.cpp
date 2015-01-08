/** I2C_FmPlus library
 *
 *  @class   I2C_FmPlus
 *  @author  tedd
 *  @version 1.0
 *  @date    02-Dec-2014
 */

#include    "mbed.h"
#include    "I2C_FmPlus.h"

#if defined(TARGET_LPC11U24_401) || defined(TARGET_LPC11U35_501) || defined(TARGET_LPC11U35_401)
// do nothing
#else
#error this version only supports mbed-LPC11U24/LPC11U35
#endif

I2C_FmPlus::I2C_FmPlus( PinName sda, PinName scl ) : I2C( sda, scl ), _frequency( 1000 * 1000 ), _ratio( 0.4 )
{
    LPC_IOCON->PIO0_4   &= ~0x300;
    LPC_IOCON->PIO0_4   |=  0x200;
    LPC_IOCON->PIO0_5   &= ~0x300;
    LPC_IOCON->PIO0_5   |=  0x200;
}

void I2C_FmPlus::frequency( float hz ) {
    _frequency  = hz;
    uint32_t pclk = SystemCoreClock;
    float   i2c_scl_period   = (1.0 / hz) - 100e-9; //  for SCLH offset and rise/fall time conpensation;    
    float   scl_period_in_clock = (float)pclk * i2c_scl_period;
    uint32_t   low_period = scl_period_in_clock * (1.0 - _ratio);
    uint32_t   high_period = scl_period_in_clock * _ratio;
    // I2C Rate
    LPC_I2C->SCLL   =  low_period  < 4 ? 4 : low_period;
    LPC_I2C->SCLH   =  high_period < 4 ? 4 : high_period;
}

void I2C_FmPlus::duty_ratio( float ratio ) {
    _ratio  = ratio;
    frequency( _frequency );
}

#if 0
void I2C_FmPlus::scl_setting( char sclh, char scll )
{
    LPC_I2C->SCLH   =  sclh;
    LPC_I2C->SCLL   =  scll;
}
#endif
