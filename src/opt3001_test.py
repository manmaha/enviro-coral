from opt3001 import opt3001
import time

address = 0x45

opt = opt3001.OPT3001(address) 

# Configure to run in Continuous conversions mode
opt.write_config_reg(opt3001.I2C_LS_CONFIG_CONT_FULL_800MS)

while(True):
  print(opt.read_lux_float())
  time.sleep(10)
