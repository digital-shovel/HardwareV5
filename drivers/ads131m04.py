"""
ADS131MO4 Python Raspberry Pi Driver
By: Benjamin de Vos
Digital Shovel
"""
import math.binary
import numpy as math
# ----------------------------------------------------------------------------------------------------------------------
# Registers
ID = 0x00
STATUS = 0x01
MODE = 0x02
CLOCK = 0x03
GAIN = 0x04
CFG = 0x06
THRSHLD_MSB = 0x07
THRSHLD_LSB = 0x08
REGMAP_CRC = 0x3e
RESERVED = 0x3f
# Ch0
CH0_CFG = 0x09
CH0_OCAL_MSB = 0x0a
CH0_OCAL_LSB = 0x0b
CH0_GCAL_MSB = 0x0c
CH0_GCAL_LSB = 0x0d
# Ch1
CH1_CFG = 0x0e
CH1_OCAL_MSB = 0x0f
CH1_OCAL_LSB = 0x10
CH1_GCAL_MSB = 0x11
CH1_GCAL_LSB = 0x12
# Ch2
CH2_CFG = 0x13
CH2_OCAL_MSB = 0x14
CH2_OCAL_LSB = 0x15
CH2_GCAL_MSB = 0x16
CH2_GCAL_LSB = 0x17
# Ch3
CH3_CFG = 0x18
CH3_OCAL_MSB = 0x19
CH3_OCAL_LSB = 0x1a
CH3_GCAL_MSB = 0x1b
CH3_GCAL_LSB = 0x1c
# ------------------------------------------------------------------------------------------------------------
# Commands
BYTE_PAD = [0x0]
NULL = [0x0, 0x0, 0x0, 0x0]
RESET = [0x0, 0x0, 0x1, 0x1]
STANDBY = [0x0, 0x0, 0x2, 0x2]
WAKEUP = [0x0, 0x0, 0x3, 0x3]
LOCK = [0x0, 0x5, 0x5, 0x5]
UNLOCK = [0x0, 0x6, 0x5, 0x5]

class ADS131M0x:

    def __init__(self, spi, frame_size, samples, channels):
        self.spi = spi
        self.frame_size = frame_size - 16
        self.samples = samples
        self.channels = channels

    def readSingleReg(self, REG_BYTE):
        parse_list = [[0x5, 3], [REG_BYTE, 6], [0x0, 7], [0x0, self.frame_size]]
        out_list = GenerateSPIFrame(parse_list, 2)
        return sendSPI(out_list)

    def readMultipleReg(self, REG_BYTE, NUM_BYTE):
        parse_list = [[0x5, 3], [REG_BYTE, 6], [NUM_BYTE, 5], [0x0, self.frame_size]]
        out_list = GenerateSPIFrame(parse_list, 2)
        return sendSPI(out_list)

    def writeSingle(self, REG_BYTE, WRITE_FRAME):
        parse_list = [[0x3, 3], [REG_BYTE, 6], [0x0, 7], [0x0, self.frame_size], [WRITE_FRAME, 16], [0x0, self.frame_size]]
        out_list = GenerateSPIFrame(parse_list, 2)
        return sendSPI(out_list)

    def configureChannel(self, mux, filter, phase_delay, channel):
        REG_BYTE = 0x0
        if channel == 0:
            REG_BYTE = CH0_CFG
        elif channel == 1:
            REG_BYTE = CH1_CFG
        elif channel == 2:
            REG_BYTE = CH2_CFG
        elif channel == 3:
            REG_BYTE = CH3_CFG
        parse_list = [[0x3, 3], [REG_BYTE, 6], [0x0, 7], [phase_delay, 10], [0x0, 3], [filter, 1], [mux, 2], [0x0, self.frame_size]]
        out_list = GenerateSPIFrame(parse_list, 2)
        return sendSPI(out_list)

    def configureGainCalibration(self, channel, gcal_val):
        REG_BYTE = 0x0
        if channel == 0:
            REG_BYTE = CH0_CFG
        elif channel == 1:
            REG_BYTE = CH1_CFG
        elif channel == 2:
            REG_BYTE = CH2_CFG
        elif channel == 3:
            REG_BYTE = CH3_CFG























