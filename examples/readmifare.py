
import binascii
import sys

import Adafruit_PN532 as PN532


# Setup how the PN532 is connected to the Raspbery Pi/BeagleBone Black.
# It is recommended to use a software SPI connection with 4 digital GPIO pins.

# Configuration for a Raspberry Pi:
CS   = 18
MOSI = 23
MISO = 24
SCLK = 25

# Configuration for a BeagleBone Black:
# CS   = 'P8_7'
# MOSI = 'P8_8'
# MISO = 'P8_9'
# SCLK = 'P8_10'

# Create an instance of the PN532 class.
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)

# Call begin to initialize communication with the PN532.  Must be done before
# any other calls to the PN532!
pn532.begin()

# Get the firmware version from the chip and print(it out.)
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards.
pn532.SAM_configuration()

# Main loop to detect cards and read a block.
print('Waiting for MiFare card...')
while True:
    # Check if a card is available to read.
    uid = pn532.read_passive_target()
    # Try again if no card is available.
    if uid is None:
        continue
    print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
    # Authenticate block 4 for reading with default key (0xFFFFFFFFFFFF).
    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                                   [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
        print('Failed to authenticate block 4!')
        continue
    # Read block 4 data.
    data = pn532.mifare_classic_read_block(4)
    if data is None:
        print('Failed to read block 4!')
        continue
    # Note that 16 bytes are returned, so only show the first 4 bytes for the block.
    print('Read block 4: 0x{0}'.format(binascii.hexlify(data[:4])))
