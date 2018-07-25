import struct

#
# class MBR():
#     boot_code=bytearray(446)
#     PTE = bytearray(64)
#     BR_signature = bytearray(2)
#
#     # def __init__(self):

MBR_SIZE = 512
GPT_SIZE = 92
GPT_PE_SIZE = 128
PTE_SIZE = 64
SIGNATURE_SIZE = 2


def isascii(i):
    return (32 < i) & (i < 126)


def printByHex(bytes, size):
    fp = 0
    while fp < size:
        line = bytes[:16]
        bytes = bytes[16:]
        fp = fp + 16

        # print by hex
        for l in line:
            print("%02X" % l, end=' ')
            if hex(l).isalpha():
                print()

        # correct space
        if len(line) < 16:
            tmp = 16 - len(line)
            while tmp>0:
                print("  ", end=' ')
                tmp = tmp -1
        print(end='\t\t')

        # print ASCII
        for l in line:
            if isascii(l):
                print("%c" % l, end=' ')
            else:
                print('.', end=' ')
        print('')


if __name__ == "__main__":

    file = input("Input File path : ")
    drive = open(file, "rb")
    drive.seek(0)  # move to file pointer 0

    mbr = drive.read(512)
    gptheader = drive.read(GPT_SIZE)
    drive.seek(2 * 512)
    GPT_PE = drive.read(GPT_PE_SIZE) # GPT Section - MBR Size) * section

    print("=====================================MBR Hex Code=====================================")
    printByHex(mbr, MBR_SIZE)
    print("=====================================MBR Hex Code=====================================")

    print('')

    fp = 0

    print("=====================================GPT Hex Code=====================================")
    printByHex(gptheader, GPT_SIZE)
    print("=====================================GPT Hex Code=====================================")

    #
    print("First usable LBA : "+"%016X" % struct.unpack('<Q', gptheader[40:40+8]))
    print("Last usable LBA : " + "%016X" % struct.unpack('<Q', gptheader[48:48+8]))
    print("Size of partion entry : "+"%08X" % struct.unpack('<L', gptheader[84:84+4]))
    numOfPartion = struct.unpack('<L', gptheader[80:80 + 4])
    print("Num of Partion Entry : " + "%08X" % numOfPartion)
    print()



    print("=====================================GPT PE Hex Code=====================================")

    count = 0
    while numOfPartion[0] > count:
        printByHex(GPT_PE,GPT_PE_SIZE)
        if struct.unpack('<Q', GPT_PE[32:32+8])[0] ==0: break
        print("First LBA : " + "%016X" % struct.unpack('<Q', GPT_PE[32:32+8]))
        print("Last LBA : " + "%016X" % struct.unpack('<Q', GPT_PE[40:40 + 8]))
        size = struct.unpack('<Q', GPT_PE[40:40 + 8])[0] - struct.unpack('<Q', GPT_PE[32:32+8])[0] + 1
        print("Size Of Partion : %08X" % size)
        count = count + 1
        GPT_PE = drive.read(GPT_PE_SIZE)
    print("=====================================GPT PE Hex Code=====================================")
    drive.close()



