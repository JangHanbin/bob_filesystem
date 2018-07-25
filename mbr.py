import struct

#
# class MBR():
#     boot_code=bytearray(446)
#     PTE = bytearray(64)
#     BR_signature = bytearray(2)
#
#     # def __init__(self):

MBR_SIZE = 512
BOOTCODE_SIZE = 446
PTE_SIZE = 64
SIGNATURE_SIZE = 2
EBR_UNUSE_SIZE = 446
EBR_SIZE = 512


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

    file = input("Input File Path : ")
    drive = open(file, "rb")
    drive.seek(0)  # move to file pointer 0

    mbr = drive.read(512)

    drive.seek(0) # reset file reader pointer
    bootcode = drive.read(BOOTCODE_SIZE)
    PTE = drive.read(PTE_SIZE)
    signature = drive.read(SIGNATURE_SIZE)

    print("=====================================MBR Hex Code=====================================")
    printByHex(mbr, MBR_SIZE)
    print("=====================================MBR Hex Code=====================================")

    print('')

    fp = 0

    print("=====================================BOOT CODE Hex Code=====================================")
    printByHex(bootcode, BOOTCODE_SIZE)
    print("=====================================BOOT CODE Hex Code=====================================")

    print('')
    print("=====================================PTE Hex Code=====================================")
    printByHex(PTE, PTE_SIZE)
    print("=====================================PTE Hex Code=====================================")

    print("=====================================PTE Info Hex Code=====================================")
    shifter = 0
    count = 1
    while True:

        LBA_start = struct.unpack('<I', PTE[8+shifter:12+shifter])
        LBA_size = struct.unpack('<I', PTE[12+shifter:16+shifter])

        if int.from_bytes(PTE[4 + shifter:5 + shifter], 'little') != 7 and int.from_bytes(PTE[4 + shifter:5 + shifter], 'little') != 5: break

        print("LBA%d Address of the start : " % count + "%08X" % LBA_start)
        print("LBA%d Num of sectors partition size : " % count  + "%08X" % LBA_size)
        print("LBA{0} type : {1} ".format(count,int.from_bytes(PTE[4+shifter:5+shifter],'little')))
        count = count + 1

        if int.from_bytes(PTE[4+shifter:5+shifter], 'little') == 5:
            drive.seek(LBA_start[0]*512+EBR_UNUSE_SIZE)
            PTE = drive.read(EBR_SIZE-EBR_UNUSE_SIZE)
            shifter = -16

        shifter = shifter + 16





    print("=====================================PTE Info Hex Code=====================================")

    drive.close()



