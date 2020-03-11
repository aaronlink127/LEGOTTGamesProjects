# All Icons Reinjector by aaronlink127
# Looks for STARWARS_ICONS_ALL_PC.GSC in working directory, so place a copy
# of the icons all in the same folder as the python file
import os, struct, itertools, tkinter, tkinter.filedialog, sys, tkinter.messagebox
tkinter.Tk().withdraw()
def group(n, iterable):
    args = [iter(iterable)] * n
    return list(itertools.zip_longest(*args))
images = {}
for file in os.listdir("."):
    if file.lower().endswith("icon_pc.gsc"):
        with open(file, "rb") as image:
            image.seek(0x1a)
            images[file[:-7].encode()] = image.read(struct.unpack("i",image.read(4))[0])
imagenames = list(images.keys())
bs = open("STARWARS_ICONS_ALL_PC.GSC", "rb")
savefile = tkinter.filedialog.asksaveasfilename(title = "Save icon file as...", filetypes = [("GSC Files","*.gsc")], initialfile="STARWARS_ICONS_ALL_PC.GSC", defaultextension="*.gsc")
if not savefile:
    sys.exit()
ws = open(savefile, "wb")
bs.seek(struct.unpack("i",bs.read(4))[0] + 0x2C)
bonelist = bs.read(struct.unpack("i",bs.read(4))[0]).split(b"\0")[:-3]
bonepairs = group(2,bonelist)
modifiedicons = {}
print(imagenames)
for i in range(0,len(bonepairs)):
    if (len(imagenames) > 0):
        for j in range(0,len(imagenames)):
            if (bonepairs[i][1].lower() == imagenames[j].lower()): # if the names are equal
                imagename = imagenames.pop(j)
                modifiedicons[i] = imagename # store name for later
                break # we've found the image, stop please
if (len(imagenames) > 0): # Run only if there are new icons
    for i in range(0,len(bonepairs)):
        if (len(imagenames) > 0 and i not in modifiedicons):
            for j in range(0,len(imagenames)):
                if (len(bonepairs[i][1]) == len(imagenames[j])): # if the names are of equal length
                    imagename = imagenames.pop(j)
                    bonepairs[i] = [imagename + b"1",imagename] # recreate an icon bone pair
                    modifiedicons[i] = imagename # store name for later
                    break # we've found the image, stop please
if (len(imagenames) > 0): # Help! Not all icons used. This will find any working name, even if its too short
    for i in range(0,len(bonepairs)):
        if (len(imagenames) > 0 and i not in modifiedicons):
            for j in range(0,len(imagenames)):
                print(imagenames[j])
                if (len(bonepairs[i][1]) > len(imagenames[j])): # if the name is shorter than the other
                    imagename = imagenames.pop(j)
                    bonepairs[i] = [(imagename + b"1").ljust(len(bonepairs[i][0]),b"\0"),(imagename).ljust(len(bonepairs[i][1]),b"\0")] # recreate an icon bone pair
                    modifiedicons[i] = imagename # store name for later
                    break # we've found the image, stop please
if (len(imagenames) > 0): # Still not used somehow
    tkinter.messagebox.showinfo("Warning","The following icons were not included:\n" + b"\n".join(imagenames).decode() + "\nTry a shorter name!")
ws.write(b"padd")
bs.seek(0)
NU20offset = struct.unpack("i",bs.read(4))[0] + 4
numberImages = struct.unpack("h",bs.read(2))[0]
bs.seek(4)
ws.write(bs.read(2))
for i in range(0,numberImages):
    if (i in modifiedicons):
        image = images[modifiedicons[i]]
        ws.write(image[0xC:0x14])
        bs.seek(8,1)
        ws.write(bs.read(0xC))
        ws.write(struct.pack("i",len(image)))
        ws.write(image)
        bs.seek(struct.unpack("i",bs.read(4))[0],1)
    else:
        ws.write(bs.read(0x18))
        bs.seek(-4,1)
        ws.write(bs.read(struct.unpack("i",bs.read(4))[0]))
ws.write(bs.read(NU20offset - bs.tell()))
NU20offsetWS = ws.tell()
ws.write(bs.read(0x2C))
startoff = ws.tell()
for pair in bonepairs:
    ws.write(b"\0".join(pair))
    ws.write(b"\0")
bs.seek(bs.tell() + ws.tell() - startoff)
ws.write(bs.read())
ws.seek(0)
ws.write(struct.pack("i",NU20offsetWS - 4))