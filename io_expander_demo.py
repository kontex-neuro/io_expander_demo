"""
This is a example script to demonstrate the usage of XDAQ Expander.
There are few sections in this script:
- XDAQ Expander Detection : Check if XDAQ Expander is detected
- Basic data acquisition : Basic data acquisition with 16 channels digital I/O
- 32 channels digital I/O data acquisition : Data acquisition with 32 channels digital I/O
- Digital output : Set digital output channel 16 and 31 to high manually and check the result
"""
#%%
from pyxdaq.board import OkBoard
from enum import Enum
import time

dev = OkBoard()
dev.config_fpga('bitfiles/xr7310a75.bit')

#%% ------------------- XDAQ Expander Detection -------------------


class EP(Enum):
    config = 0x00
    max_frames = 0x01

    multi_use = 0x1f
    data_count = 0x20
    status = 0x22
    expander = 0x35

    trig_config = 0x40
    start = 0x41

    enable32bit_rhd = 0x12
    enable32bit_rhs = 0x0b
    ttl_out16 = 0x15
    ttl_out32 = 0x10

    data_out = 0xA0


# Waiting for MCU
while (dev.GetWireOutValue(EP.status) & 4) == 4:
    time.sleep(0.1)

# reset board
dev.SetWireInValue(EP.config, 1, 1)
dev.SetWireInValue(EP.config, 0, 1)

# usb3 configuration
dev.SendTrig(EP.trig_config, 9, EP.multi_use, 1024 // 4)
dev.SendTrig(EP.trig_config, 10, EP.multi_use, 32)

# check expander
expander_detected = dev.GetWireOutValue(EP.expander) == 0x18180606
if expander_detected:
    print("Expander detected")
else:
    print("Expander not detected")

#%% ------------------- Basic data acquisition -------------------
print('=' * 60)
print('Basic data acquisition')
print('=' * 60)
num_frames = 128

dev.SetWireInValue(EP.config, 0, 2)  # continuous mode off
dev.SetWireInValue(EP.max_frames, num_frames)  # 128 frames
dev.ActivateTriggerIn(EP.start, 0)  # start

while (dev.GetWireOutValue(EP.status) & 1) == 1:
    print('waiting for data')

buffered_data_in_bytes = dev.GetWireOutValue(EP.data_count) * 2
print(f'Buffered data: {buffered_data_in_bytes} bytes')


def frame_size_bytes(dio32, num_streams) -> int:
    frame_size = (
        4 +  # magic number
        2 +  # time stamp
        (num_streams *
         (32 + 3)) +  # Headstage data, 32 amp channels + 3 aux commands
        ((num_streams + 2 * dio32) % 4) +  # padding for alignment
        8 +  # ADCs
        1 +  # Digital input, 16 bits = 1 words
        1 * dio32 +  # Expander digital input when enabled
        1 +  # Digital output, 16 bits = 1 words
        1 * dio32  # Expander digital output when enabled
    )
    return frame_size * 2


# Check data length
frame_size = frame_size_bytes(False, 0)
print(f'Frame size = {frame_size}')
data_size = num_frames * frame_size
print(f'Expected data size: {data_size} bytes')
buffer = bytearray(((data_size + 1023) // 1024) * 1024)
res = dev.ReadFromBlockPipeOut(EP.data_out, 1024, buffer)
print(f'Read {res} bytes from pipe out')
buffered_data_in_bytes = dev.GetWireOutValue(EP.data_count) * 2
print(f'Buffered data: {buffered_data_in_bytes} bytes (After read)')


def simple_frame_unpack(data: bytearray, dio32: bool, num_streams: int):
    magic = int.from_bytes(data[0:8], byteorder='little')
    print(f'Magic: {magic:016X}')
    timestamp = int.from_bytes(data[8:12], byteorder='little')
    print(f'Timestamp: {timestamp}')
    len_headstage = 35 * 2 * num_streams
    headstage = data[12:12 + len_headstage]
    padding = ((num_streams + 2 * dio32) % 4) * 2

    io_offset = 12 + len_headstage + padding
    print('Analog in ch 1-8 : ', end=' ')
    for i in range(8):
        analog_in = int.from_bytes(data[io_offset + i * 2:io_offset + i * 2 +
                                        2],
                                   byteorder='little')
        print(f'{analog_in}', end=' ')
    print()
    if not dio32:
        digital_in = int.from_bytes(data[io_offset + 16:io_offset + 18],
                                    byteorder='little')
        digital_out = int.from_bytes(data[io_offset + 18:io_offset + 20],
                                     byteorder='little')
        print(f'Digital in : {digital_in:016b}')
        print(f'Digital out: {digital_out:016b}')
    else:
        digital_in = int.from_bytes(data[io_offset + 16:io_offset + 20],
                                    byteorder='little')
        digital_out = int.from_bytes(data[io_offset + 20:io_offset + 24],
                                     byteorder='little')
        print(f'Digital in : {digital_in:032b}')
        print(f'Digital out: {digital_out:032b}')


for i in range(2):
    print('-' * 60)
    simple_frame_unpack(buffer[frame_size * i:frame_size * (i + 1)], False, 0)

#%% ------------------- 32 channels digital I/O data acquisition -------------------
print()
print('=' * 60)
print('32 channels digital I/O data acquisition')
print('=' * 60)

# Enable 32 channels digital I/O
dev.SetWireInValue(EP.enable32bit_rhd, 4, 4)

# Start acquisition
dev.ActivateTriggerIn(EP.start, 0)  # start

while (dev.GetWireOutValue(EP.status) & 1) == 1:
    time.sleep(0.01)

buffered_data_in_bytes = dev.GetWireOutValue(EP.data_count) * 2
print(f'Buffered data: {buffered_data_in_bytes} bytes')

frame_size = frame_size_bytes(True, 0)
print(f'Frame size = {frame_size}')
data_size = num_frames * frame_size
print(f'Expected data size: {data_size} bytes')

buffer = bytearray(((data_size + 1023) // 1024) * 1024)
res = dev.ReadFromBlockPipeOut(EP.data_out, 1024, buffer)
print(f'Read {res} bytes from pipe out')

for i in range(2):
    print('-' * 60)
    simple_frame_unpack(buffer[frame_size * i:frame_size * (i + 1)], True, 0)

#%% ------------------- Digital output -------------------
print()
print('=' * 60)
print('Digital output')
print('=' * 60)
# set digital output channel 16 (bit 15) to high
dev.SetWireInValue(EP.ttl_out16, 1 << 15, 1 << 15)
# set digital output channel 31 (bit 31-16-1 = 14) to high
dev.SetWireInValue(EP.ttl_out32, 1 << 14, 1 << 14)

dev.ActivateTriggerIn(EP.start, 0)  # start

while (dev.GetWireOutValue(EP.status) & 1) == 1:
    time.sleep(0.01)

buffered_data_in_bytes = dev.GetWireOutValue(EP.data_count) * 2
print(f'Buffered data: {buffered_data_in_bytes} bytes')

frame_size = frame_size_bytes(True, 0)
print(f'Frame size = {frame_size}')
data_size = num_frames * frame_size
print(f'Expected data size: {data_size} bytes')

buffer = bytearray(((data_size + 1023) // 1024) * 1024)
res = dev.ReadFromBlockPipeOut(EP.data_out, 1024, buffer)
print(f'Read {res} bytes from pipe out')

for i in range(3):
    print('-' * 60)
    simple_frame_unpack(buffer[frame_size * i:frame_size * (i + 1)], True, 0)
