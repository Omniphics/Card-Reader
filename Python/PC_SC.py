from smartcard.System import readers
from smartcard.util import toHexString

# find readers
r=readers()
print(r)

# connect to reader
connection = r[0].createConnection()
connection.connect()

# APDU Commands
CmdSelectAppJPN = [0x00, 0xA4, 0x04, 0x00, 0x0A, 0x0A0, 0x00, 0x00, 0x00, 0x74, 0x4A, 0x50, 0x4E, 0x00, 0x10]
CmdAppResponse = [0x00, 0xC0, 0x00, 0x00, 0x05]
CmdSetLength = [0xC8, 0x32, 0x00, 0x00, 0x05, 0x08, 0x00, 0x00]
CmdSelectFile = [0xCC, 0x00, 0x00, 0x00, 0x08]

#which file
fileOne = [0x01, 0x00, 0x01, 0x00]
fileTwo = [0x02, 0x00, 0x01, 0x00]
fileThree = [0x03, 0x00, 0x01, 0x00]
fileFour = [0x04, 0x00, 0x01, 0x00]
fileFive = [0x05, 0x00, 0x01, 0x00]
fileSix = [0x06, 0x00, 0x01, 0x00]

CmdGetData = [0xCC, 0x06, 0x00, 0x00]

# for JPN
fileLengths = [0,459,4011,1227,171,43,43,0]

# select the application: JPN, JPJ, IMM
data, sw1, sw2 = connection.transmit(CmdSelectAppJPN)

# check for response - not required
data, sw1, sw2 = connection.transmit(CmdAppResponse)
    
    
# loop for data
for FileNum in range(1, 7):
    split_offset = 0
    split_length = 252
    while split_offset < fileLengths[FileNum]:
        if split_offset + split_length > fileLengths[FileNum]:
            split_length = fileLengths[FileNum] - split_offset

        setLength = []
        for x in CmdSetLength:
            setLength.append(x)
        setLength.append(split_length);
        setLength.append(0x00);
        data, sw1, sw2 = connection.transmit(setLength)

        selectFile = []
        for x in CmdSelectFile:
            selectFile.append(x)
        selectFile.append(FileNum);
        selectFile.append(0x00);
        selectFile.append(1);
        selectFile.append(0x00);
        selectFile.append(split_offset)
        selectFile.append(0x00)
        selectFile.append(split_length)
        selectFile.append(0x00)
        data, sw1, sw2 = connection.transmit(selectFile)

        getData = []
        for x in CmdGetData:
            getData.append(x)
        getData.append(split_length)
        data, sw1, sw2 = connection.transmit(getData)
        
        if FileNum == 1:
            if split_offset == 0:
                text = []
                for x in range(0x00003,0x00003+0x28):
                    text.append(data[x])
                print("Name: " + bytearray.fromhex(toHexString(text)).decode())
            elif split_offset == 252:
                text = []
                for x in range(0x111 - 252,0x111 - 252 + 0x0D):
                    text.append(data[x])

                print("IC: " + bytearray.fromhex(toHexString(text)).decode())
                
                text = []
                for x in range( 0x11F - 252, 0x11F - 252 + 0x08):
                    text.append(data[x])

                print("Old IC: " + bytearray.fromhex(toHexString(text)).decode())

                text = []
                for x in range(  0x127 - 252,  0x127 - 252 + 0x04):
                    text.append("{:02x}".format(data[x]))
                
                value = ""
                for i in range(0,4):
                    value += text[i]

                    if i == 1 or i == 2: 
                        value += "-"
                print("DOB: " + value)


                text = []
                for x in range(  0x12B - 252,  0x12B - 252 + 0x19):
                    text.append(data[x])
                print("State of Birth: " + bytearray.fromhex(toHexString(text)).decode())


                text = []
                for x in range(  0x144 - 252,  0x144 - 252 + 0x04):
                    text.append("{:02x}".format(data[x]))

                value = ""
                for i in range(0,4):
                    value += text[i]

                    if i == 1 or i == 2: 
                        value += "-"
                print("Validity Date: " + value)

                text = []
                for x in range(   0x148 - 252,   0x148 - 252 + 0x12):
                    text.append(data[x])
                print("Nationality: " + bytearray.fromhex(toHexString(text)).decode())
                
                text = []
                for x in range(   0x15A - 252,   0x15A - 252 + 0x19):
                    text.append(data[x])
                print("Ethnic/Race: " + bytearray.fromhex(toHexString(text)).decode())

                text = []
                for x in range(   0x173 - 252,   0x173 - 252 + 0x0B):
                    text.append(data[x])
                print("Religion: " + bytearray.fromhex(toHexString(text)).decode())
        if FileNum == 4:
            if split_offset == 0:
                print("\nAddress:")
                text = []
                for x in range( 0x03, 0x03+0x1E):
                    text.append(data[x])
                print(bytearray.fromhex(toHexString(text)).decode())
                
                text = []
                for x in range( 0x21, 0x21+0x1E):
                    text.append(data[x])
                print(bytearray.fromhex(toHexString(text)).decode())

                text = []
                for x in range( 0x3F, 0x3F+0x1E):
                    text.append(data[x])
                print(bytearray.fromhex(toHexString(text)).decode())
                
                text = []
                for x in range(  0x5D,  0x5D + 0x03):
                    text.append("{:02x}".format(data[x]))
                value = ""
                for i in range(0,3):
                    if(i == 2 and text[i] == "00"):
                        value += "0"
                    else:    
                        value += text[i]
                print(value)

                text = []
                for x in range( 0x60, 0x60+0x19):
                    text.append(data[x])
                print(bytearray.fromhex(toHexString(text)).decode())

                text = []
                for x in range( 0x79, 0x79+0x1E):
                    text.append(data[x])
                print(bytearray.fromhex(toHexString(text)).decode())
        split_offset += split_length


connection.disconnect()
