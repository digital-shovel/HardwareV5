import numpy as math

def GenerateSPIFrame(byte_list, form):
    seg_count = len(byte_list)
    parse_list = [None] * seg_count
    for i in range(0, seg_count):
        parse_list[i] = math.binary_repr(byte_list[i][0], width=byte_list[i][1])
    print(parse_list)
    if form == 1:
        out = ''.join(parse_list)
        return out
    if form == 2:
        return parse_list


def sendSPI(byte_list, spiobj):
    return spiobj.bb_spi_xfer(byte_list)