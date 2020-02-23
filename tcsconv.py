#Shoddy TCS Converter by aaronlink127
#Converts LB1/LIJ1 models to TCS format, except badly. Some meshes may not render, or it may be unstable!
import tkinter, tkinter.simpledialog, tkinter.filedialog, sys, os, struct, msvcrt
tkinter.Tk().withdraw()
openfile = tkinter.filedialog.askopenfilename(title = "Select a model to convert", filetypes = (("GHG Files","*.ghg"), ("GSC Files","*.gsc")))
if not openfile:
    sys.exit()
def readInt(): return struct.unpack("i", bs.read(4))[0]
def printPos(identifier): print("%s @ 0x%x" % (identifier,bs.tell()))
bs = open(openfile, "rb")
bs.seek(0x18)
absOffsetPNTR = bs.tell() + readInt() - 4
bs.seek(readInt()+0x20) #GSNH
absOffsetGSNH = bs.tell()
printPos("GSNH")
numberImages = readInt()
print("numberImages %i" % numberImages)
bs.seek(readInt()-4,1)
printPos("imageMetas")

imageMetas = []
numberRealImages = 0
for i in range(0, numberImages):
    tmp = bs.tell()
    bs.seek(readInt() - 4,1)
    imageMeta = {}
    imageMeta["width"] = readInt()
    imageMeta["height"] = readInt()
    bs.seek(0x30,1)
    imageMeta["unknownBytes"] = bs.read(0xC)
    imageMeta["size"] = readInt()
    if (imageMeta["size"] != 0): numberRealImages += 1
    imageMetas.append(imageMeta)
    bs.seek(tmp+4)
print("numberRealImages %i" % numberRealImages)
bs.seek(absOffsetPNTR)
printPos("hi")
bs.seek(readInt()-4,1)
DDSOffset = bs.tell()

savefile = tkinter.filedialog.asksaveasfilename(title = "Save model as...", filetypes = (("GHG Files","*.ghg"), ("GSC Files","*.gsc")))
ws = open(savefile, "wb")
ws.write(b'....')
ws.write(struct.pack("h",numberImages))
for i in range(0, numberRealImages):
    ws.write(struct.pack("i",imageMetas[i]["width"]))
    ws.write(struct.pack("i",imageMetas[i]["height"]))
    ws.write(imageMetas[i]["unknownBytes"])
    ws.write(struct.pack("i",imageMetas[i]["size"]))
    ws.write(bs.read(imageMetas[i]["size"]))
ws.write(bs.read())
NU20offset = ws.tell() - 4
ws.seek(0)
ws.write(struct.pack("i",NU20offset))
ws.seek(0,2)
bs.seek(0)
ws.write(bs.read(8))
ws.write(b'\x02\x00\x00\x00\x00\x00\x00\x00')
# bs.seek(0x10)
# ws.write(bs.read(0x10))
# bs.seek(4,1)
# tmp = readInt()
# print(tmp)
# bs.seek(-8,1)
# ws.write(bs.read(tmp))
# ws.write(bs.read(0x10))
# bs.seek(4,1)
# tmp = readInt()
# bs.seek(-8,1)
# print("%x"%(ws.tell()+tmp))
# ws.write(bs.read(tmp))
# ws.write(bs.read(0x142))
# bs.read(1)
# ws.write(b"\xC8")
# ws.write(bs.read(0x13C))
# bs.read(1)
# ws.write(b"\0")
ws.write(bs.read(DDSOffset - bs.tell()))