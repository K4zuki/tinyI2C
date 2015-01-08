/** I2C_FmPlus library
 *
 *  @class   I2C_FmPlus
 *  @author  tedd
 *  @version 1.0
 *  @date    02-Dec-2014
 */

#ifndef     MBED_I2C_FMPLUS
#define     MBED_I2C_FMPLUS

#include    "mbed.h"

class I2C_FmPlus : public I2C {
public:
    /** Create an I2C Master interface, connected to the specified pins
     *
     *  @param sda I2C data line pin
     *  @param scl I2C clock line pin
     */
    I2C_FmPlus( PinName sda, PinName scl );

    /** Set the frequency of the I2C interface
     *
     *  @param hz The bus frequency in hertz
     */
    void frequency( float hz );

    /** Set the duty ratio of SCL
     *
     *  @param ratio Ratio of High/(High+Low) of SCL signal
     */
    void duty_ratio( float ratio );
    
//    void scl_setting( char sclh, char scll );
private:
    float   _frequency;
    float   _ratio;
}
;

#endif  //  MBED_I2C_FMPLUS
