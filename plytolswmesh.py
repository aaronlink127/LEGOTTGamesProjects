# LEGO Star Wars PLY Model Importer Version r1.0
# Notes:
# Python 3.6 recommended, any 3.x version should work however
# Requires PYFFI, which needs to be installed via PIP
# Install PIP, then use "python -m pip install pyffi" in command line
# Models are flipped before import, as the game reflips when loading models, so keep this in mind when using other lego game assets
# Some material editing may be required for this to work, specifically 0x1BB after the beginning of the material should be "02"
# When exporting from Blender, export as a PLY with "-Z Forward" and "Y Up"
import struct, sys, pyffi, math
from pyffi.utils import tristrip
verts = []
uvs = []
norms = []
faces = []
vertcolors = []
if len(sys.argv) < 2:
    import tkinter, tkinter.filedialog
    tkinter.Tk().withdraw()
    modelname = tkinter.filedialog.askopenfilename(title = "Select a ply file")
    if not modelname:
        sys.exit()
else:
    modelname = sys.argv[1]
with open(modelname) as modelfile:
    lines = [x[:-1] for x in modelfile.readlines()]
    propcountervert = 0
    proporder = {}
    section = ""
    while True:
        curline = lines.pop(0)
        if curline == "end_header": break
        headerarg = curline.split()
        headercmd = headerarg.pop(0)
        if headercmd == "element":
            section = headerarg[0]
            if section == "vertex":numberVertex = int(headerarg[1])
            if section == "face": numberFace = int(headerarg[1])
        if headercmd == "property" and section == "vertex":
            proporder[headerarg[1]] = propcountervert
            propcountervert += 1
    for i in range(0,numberVertex):
        vertex = lines.pop(0).split()
        verts.append([
            float(vertex[proporder["x"]]),
            -float(vertex[proporder["y"]]),
            float(vertex[proporder["z"]])])
        norms.append([
            int((float(vertex[proporder["nx"]]) + 1) * 127.5),
            255 - int((float(vertex[proporder["ny"]]) + 1) * 127.5),
            int((float(vertex[proporder["nz"]]) + 1) * 127.5)])
        uvs.append([float(vertex[proporder["s"]]),1 - float(vertex[proporder["t"]])])
    for i in range(0,numberFace):
        face = lines.pop(0).split()
        face.reverse()
        face.pop()
        faces.append([int(x) for x in face])
stripfaces = tristrip.stripify(faces, stitchstrips=True)[0]
sizeVertex = 0
with open(modelname[:-4] + "_vertexList.dat","wb") as ws:
    ws.write(b"\0\0\0\0")
    for i in range(0,len(verts)):
        ws.write(struct.pack("fff", *verts[i]))
        ws.write(struct.pack("BBBB", *norms[i], 255))
        ws.write(b"\0"*4)
        ws.write(b"\x7F"*4)
        ws.write(b"".join([struct.pack("f",x) for x in uvs[i]]))
        if not sizeVertex:
            sizeVertex = ws.tell() - 4
    sizeVertexList = ws.tell() - 4
    ws.seek(0)
    ws.write(struct.pack("i",sizeVertexList))
with open(modelname[:-4] + "_indexList.dat","wb") as ws:
    ws.write(struct.pack("i",len(stripfaces) * 2))
    for i in stripfaces: ws.write(struct.pack("h",i))
    sizeIndexList = ws.tell() - 4
with open(modelname[:-4] + "_partData.dat","wb") as ws:
    ws.write(b"\6\0\0\0")
    ws.write(struct.pack("i",len(stripfaces) - 2))
    ws.write(struct.pack("h",sizeVertex))
    ws.write(b"\xff"*8)
    ws.write(b"\0"*6)
    ws.write(struct.pack("i",len(verts)))
    ws.write(b"\0"*4)
    ws.write(b"xxxxxxxx")
    ws.write(b"\0"*16)