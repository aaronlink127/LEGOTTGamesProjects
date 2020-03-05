# TCS Converter by aaronlink127
# Converts LB1/LIJ1 models to TCS format, but may be unstable!
import tkinter, tkinter.simpledialog, tkinter.filedialog, sys, os, struct, msvcrt
tkinter.Tk().withdraw()
openfile = tkinter.filedialog.askopenfilename(title = "Select a model to convert", filetypes = (("TT Games Model Files","*.ghg"), ("TT Games Model Files","*.gsc")))
if not openfile:
    sys.exit()
savefile = tkinter.filedialog.asksaveasfilename(title = "Save model as...", filetypes = (("TT Games Model Files","*.ghg"), ("TT Games Model Files","*.gsc")))
if not savefile:
    sys.exit()
def readInt(): return struct.unpack("i", bs.read(4))[0]
if openfile == savefile:
    from io import BytesIO
    with open(openfile,"rb") as modelfile:
        fileconts = modelfile.read()
        bs = BytesIO(fileconts)
else:
    bs = open(openfile, "rb")
bs.seek(0x18)
absOffsetPNTR = bs.tell() + readInt() - 4
bs.seek(readInt()+0x20) #GSNH
absOffsetGSNH = bs.tell()
numberImages = readInt()
bs.seek(readInt()-4,1)

imageMetas = []
for i in range(0, numberImages):
    tmp = bs.tell()
    bs.seek(readInt() - 4,1)
    imageMeta = {}
    imageMeta["width"] = readInt()
    imageMeta["height"] = readInt()
    bs.seek(0x30,1)
    imageMeta["unknownBytes"] = bs.read(0xC)
    imageMeta["size"] = readInt()
    imageMetas.append(imageMeta)
    bs.seek(tmp+4)
bs.seek(absOffsetPNTR)
bs.seek(readInt()-4,1)
DDSOffset = bs.tell()

ws = open(savefile, "wb")
ws.write(b'....')
ws.write(struct.pack("h",numberImages))
for imageMeta in imageMetas:
    ws.write(struct.pack("i",imageMeta["width"]))
    ws.write(struct.pack("i",imageMeta["height"]))
    ws.write(imageMeta["unknownBytes"])
    ws.write(struct.pack("i",imageMeta["size"]))
    ws.write(bs.read(imageMeta["size"]))
ws.write(bs.read())
NU20offset = ws.tell() - 4
ws.seek(0)
ws.write(struct.pack("i",NU20offset))
ws.seek(0,2)
bs.seek(0)
ws.write(bs.read(8))
ws.write(b'\x02\x00\x00\x00\x00\x00\x00\x00')
bs.seek(0x10)
ws.write(bs.read(DDSOffset - bs.tell()))