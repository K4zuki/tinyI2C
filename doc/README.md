+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|     Macro      |   Board   |  Function\ |            |          |          |          |            |                   |                   |
+================+===========+============+============+==========+==========+==========+============+===================+===================+
|                |           | **always**\| **always**\|          |          |          | **always**\|    **always**\    |                   |
|                |           |  **UART**  |  **I2C0**  | **I2C1** | **I2C2** | **I2C3** |  **SPI**   | **GPIO0[7\.\.0]** | **GPIO1[7\.\.0]** |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
| **#QUAD_I2C**  | LPC824MAX |   USBTX    |  I2C_SDA   |   P0_6   |  P0_23   |  P0_21   |   P0_26    |   P0_27           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |   USBRX    |  I2C_SCL   |  P0_14   |  P0_22   |  P0_20   |   P0_25    |   P0_13           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |   P0_24    |   P0_17           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |   P0_15    |   P0_16           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |            |   P0_28           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |            |   P0_18           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |            |   P0_12           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |            |   P0_19           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
| **#QUAD_I2C**\ |  TINYI2C  |    P0_4    |  I2C_SDA   |  P0_16   |  P0_26   |  P0_24   |    P0_6    |   P0_14           |                   |
| **+ #TINYI2C** |           |            |            |          |          |          |            |                   |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
| **+ #TINYI2C** |  SSCI824  |    P0_0    |  I2C_SCL   |  P0_27   |  P0_25   |  P0_15   |    P0_7    |   P0_23           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |   P0_13    |   P0_22           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |    P0_1    |   P0_21           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |            |   P0_20           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |            |   P0_19           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |            |   P0_18           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |            |   P0_17           |                   |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|  **#TINYI2C**  |  TINYI2C  |    P0_4    |  I2C_SDA   |          |          |          |    P0_6    |   P0_14           |   P0_12           |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |  SSCI824  |    P0_0    |  I2C_SCL   |          |          |          |    P0_7    |   P0_23           |   P0_28           |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |   P0_13    |   P0_22           |   P0_16           |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |    P0_1    |   P0_21           |   P0_27           |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |            |   P0_20           |   P0_26           |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |            |   P0_19           |   P0_25           |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |            |   P0_18           |   P0_24           |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
|                |           |            |            |          |          |          |            |   P0_17           |   P0_15           |
+----------------+-----------+------------+------------+----------+----------+----------+------------+-------------------+-------------------+
