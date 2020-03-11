# TCS Converter by aaronlink127
# Converts LB1/LIJ1 models to TCS format, but may be unstable!

class ImageMeta(object):
    def __init__(self, width, height, miscBytes, size):
        self.width = width
        self.height = height
        self.miscBytes = miscBytes
        self.size = size
import tkinter, tkinter.simpledialog, tkinter.filedialog, sys, os, struct, msvcrt
tkinter.Tk().withdraw()
openfile = tkinter.filedialog.askopenfilename(title = "Select a model to convert", filetypes = (("TT Games Model Files","*.ghg"), ("TT Games Model Files","*.gsc")))
if not openfile:
    sys.exit()
savefile = tkinter.filedialog.asksaveasfilename(title = "Save model as...", filetypes = (("TT Games Model Files","*.ghg"), ("TT Games Model Files","*.gsc")))
if not savefile:
    sys.exit()
if openfile == savefile:
    from io import BytesIO
    with open(openfile,"rb") as modelfile:
        fileconts = modelfile.read()
        bs = BytesIO(fileconts)
else:
    bs = open(openfile, "rb")
bs.seek(0x18)
absOffsetPNTR = bs.tell() + struct.unpack("i", bs.read(4))[0] - 4
bs.seek(struct.unpack("i", bs.read(4))[0]+0x20) #GSNH
absOffsetGSNH = bs.tell()
numberImages = struct.unpack("i", bs.read(4))[0]
print(numberImages)
bs.seek(struct.unpack("i", bs.read(4))[0]-4,1)
isLevel = openfile.lower().endswith("gsc")
imageMetas = []
for i in range(0, numberImages):
    tmp = bs.tell()
    bs.seek(struct.unpack("i", bs.read(4))[0] - 4,1)
    width = struct.unpack("i", bs.read(4))[0]
    height = struct.unpack("i", bs.read(4))[0]
    bs.seek(0x30,1)
    miscBytes = bs.read(0xC)
    size = struct.unpack("i", bs.read(4))[0]
    print("Image{0}: width = {1:4d}; height = {2:4d}; size = {3:8d}".format(i, width, height, size))
    if size > 0:
        imageMetas.append(ImageMeta(width,height,miscBytes,size))
    elif isLevel:
        imageMetas.append(ImageMeta(0,0,b"\0"*0xC,0))
    bs.seek(tmp+4)
bs.seek(absOffsetPNTR)
bs.seek(struct.unpack("i", bs.read(4))[0]-4,1)
DDSOffset = bs.tell()

ws = open(savefile, "wb")
ws.write(b'....')
ws.write(struct.pack("h",len(imageMetas)))
for imageMeta in imageMetas:
    ws.write(struct.pack("i",imageMeta.width))
    ws.write(struct.pack("i",imageMeta.height))
    ws.write(imageMeta.miscBytes)
    ws.write(struct.pack("i",imageMeta.size))
    ws.write(bs.read(imageMeta.size))
ws.write(bs.read())
NU20offset = ws.tell() - 4
ws.seek(0)
ws.write(struct.pack("i",NU20offset))
ws.seek(0,2)
bs.seek(0)
ws.write(bs.read(8))
ws.write(b'\x02\x00\x00\x00\x00\x00\x00\x00')
bs.seek(0x10)
ws.write(bs.read(absOffsetGSNH - bs.tell()))
ws.write(struct.pack("i",len(imageMetas)))
bs.seek(4,1)
ws.write(bs.read(DDSOffset - bs.tell()))