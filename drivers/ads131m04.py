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
DATA_PAD_READ = [0x0, 96]
DATA_PAD_WRITE = [0x0, 72]
DATA_PAD_WRITE2 = [0x0, 48]
NULL_FRAME = [0x0, 120]

def getChunks(frame_width, word_size):
    loop_length = frame_width / word_size
    out_list =  [None] * loop_length
    count = 0
    for i in range(0, loop_length):




class ADS131M0x:

    def __init__(self, spi, frame_size, samples, channels):
        self.spi = spi
        self.frame_size_diff = frame_size - 16
        self.samples = samples
        self.channels = channels

    def readSingleReg(self, REG_BYTE):
        parse_list = [[0x5, 3], [REG_BYTE, 6], [0x0, 7], [0x0, self.frame_size_diff], DATA_PAD]
        out_list = GenerateSPIFrame(parse_list, 2)
        sendSPI(out_list)
        return sendSPI(NULL)

    def readMultipleReg(self, REG_BYTE, NUM_BYTE):
        parse_list = [[0x5, 3], [REG_BYTE, 6], [NUM_BYTE, 5], [0x0, self.frame_size_diff], DATA_PAD]
        out_list = GenerateSPIFrame(parse_list, 2)
        sendSPI(out_list)
        return sendSPI(NULL)

    def writeSingle(self, REG_BYTE, WRITE_FRAME):
        parse_list = [[0x3, 3], [REG_BYTE, 6], [0x0, 7], [0x0, self.frame_size_diff], [WRITE_FRAME, 16], [0x0, self.frame_size], DATA_PAD]
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
        parse_list = [[0x3, 3], [REG_BYTE, 6], [0x0, 7], [0x0, self.frame_size_diff], [phase_delay, 10], [0x0, 3], [filter, 1], [mux, 2], [0x0, self.frame_size_diff]]
        out_list = GenerateSPIFrame(parse_list, 2)
        return sendSPI(out_list)

    def configureGainCalibration(self, channel, gcal_val1, gcal_val2):
        REG_BYTE = 0x0
        REG_BYTE2 = 0x0
        if channel == 0:
            REG_BYTE = CH0_GCAL_MSB
            #REG2_BYTE = CH0_GCAL_LSB
        elif channel == 1:
            REG_BYTE = CH1_GCAL_MSB
            #REG2_BYTE = CH1_GCAL_LSB
        elif channel == 2:
            REG_BYTE = CH2_GCAL_MSB
            #REG2_BYTE = CH2_GCAL_LSB
        elif channel == 3:
            REG_BYTE = CH3_GCAL_MSB
            #REG2_BYTE = CH3_GCAL_LSB
        parse_list = [[0x3, 3], [REG_BYTE, 6], [0x0, 7], [0x0, self.frame_size_diff], [gcal_val1, 16], [0x0, self.frame_size_diff], [gcal_val2, 16], [0x0, self.frame_size_diff], DATA_PAD_WRITE2]
        out_list = GenerateSPIFrame(parse_list, 2)
        sendSPI(out_list)
        return sendSPI(NULL)

    def configureClockReg(self, ch0, ch1, ch2, ch3, osr, pm):
        parse_list = [[0x3, 3], [0x3, 6], [0x0, 7], [0x0, self.frame_size_diff], [0x0, 4], [ch0, 1], [ch1, 1], [ch2, 1], [ch3, 1], [0x0, 2], [0x0, 1], [osr, 3], [pm, 2], [0x0, self.frame_size_diff], DATA_PAD_WRITE]
        sendSPI(GenerateSPIFrame(parse_list))
        return sendSPI(GenerateSPIFrame(NULL_FRAME))

    def readStatusReg(self):
        parse_list = [[0x5, 3], [0x1, 6], [0x0, 7], [0x0, self.frame_size_diff], DATA_PAD]
        sendSPI(GenerateSPIFrame(parse_list))
        return sendSPI(GenerateSPIFrame(NULL_FRAME))

    def configureModeReg(self, reg_crc, crc_en, crc_t, wlength, timeout, drdy_sel, reset):
        parse_list = [[0x3, 3], [0x2, 6], [0x0, 7], [0x0, self.frame_size_diff], [0x0, 2], [reg_crc, 1], [crc_en, 1], [crc_t, 1], [reset, 1], [wlength, 2], [0x0, 3], [timeout, 1], [drdy_sel, 2], [0x0, 1], [0x0, 1], [0x0, self.frame_size_diff], DATA_PAD_WRITE]
        sendSPI(GenerateSPIFrame(parse_list))
        return sendSPI(GenerateSPIFrame(NULL_FRAME))

    def configureGain1Reg(self, gain0, gain1, gain2, gain3):
        parse_list = [[0x3, 3], [0x4, 6], [0x0, 7], [0x0, self.frame_size_diff], [0x0, 1], [gain3, 3], [0x0, 1], [gain2, 3], [0x0, 1], [gain1, 3], [0x0, 1], [gain0, 3], DATA_PAD_WRITE]
        sendSPI(GenerateSPIFrame(parse_list))
        return sendSPI(GenerateSPIFrame(NULL_FRAME))






























