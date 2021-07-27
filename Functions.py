import math
import brents
import os #just for showing the progress bar, can remove
from PIL import Image, ImageColor, ImageDraw, ImagePath, ImageFont

def ptx(pixel): #convert from pixels to X value
	return (pixel-SIZE//2)/SF


def ytp(y): #converts from Y value to pixel
	return SIZE-round((y*SF)+SIZE//2)

def pty(pixel): #converts from pixel to Y value (for X intersection)
	return (SIZE//2 - pixel)/SF

#init
SIZE = 10000
BOX = (SIZE, SIZE)
RANGE = 10 #how far will the function show on the positive X axis?
SF = SIZE/(2*RANGE) #scaling factor
RATIO = SIZE//RANGE #Pixel to X ratio
WIDTH = SIZE//400 #make the graph thicker by this constant

#colors
axisColor = ImageColor.getcolor('#0D0106', 'RGB')
gridColor = ImageColor.getcolor('#E5D4ED', 'RGB')
backgroundColor = ImageColor.getcolor('#fff5f9', 'RGB')
asymptoteColor = ImageColor.getcolor('#DC143C', 'RGB')
#graphColor = ImageColor.getcolor('#00BFB2', 'RGB')
graphColor = ImageColor.getcolor('#5941A9', 'RGB') 
intersectColor = ImageColor.getcolor('#2B303A', 'RGB')

#the function
f = lambda x: math.sin(x)

# create drawing context
img = Image.new("RGB", BOX, color=backgroundColor)  # create new Image
dctx = ImageDraw.Draw(img) 
Axisfont = ImageFont.truetype('arial.ttf', SIZE//50)
intersectfont = ImageFont.truetype('arial.ttf', SIZE//75)


#Draw the gridlines
scale=WIDTH//2
for x in range(0, SIZE, RATIO):
	dctx.rectangle([(x-scale//2, 0), (x+scale//2, SIZE)], fill=gridColor)
for y in range(0, SIZE, RATIO):
	dctx.rectangle([(0, y-scale//2), (SIZE, y+scale//2)], fill=gridColor)


#Draw the axis
dctx.rectangle([(0, SIZE//2), (SIZE, SIZE//2 + WIDTH)], fill=axisColor)
dctx.rectangle([(SIZE//2, 0), (SIZE//2 + WIDTH, SIZE)], fill=axisColor)
#the X and Y labels
dctx.text((SIZE-SIZE//50, SIZE//2+5), "X", font=Axisfont, fill=axisColor)
dctx.text((SIZE//2+5, SIZE//100), "Y", font=Axisfont, fill=axisColor)


#draw graph
startfound = False #searching for starting pixel to start rectangle

for pixel in range(0, SIZE):
	#check that there exists a point here
	try:
		nX, nY = pixel, ytp(f(ptx(pixel)))
		print(nX, nY)
	except:
		continue

	#draw graph
	if(startfound):
		if abs(nY-oY)<=2*SIZE: #asymptote
			dctx.rectangle([(oX, oY), (oX+WIDTH, oY+WIDTH)], fill=graphColor) #fill the missing points
			dctx.rectangle([(oX+WIDTH, oY+WIDTH), (nX, nY)], fill=graphColor)
			#test for intersection
			if(f(ptx(oX)) * f(ptx(nX)) <= 0):
				try:
					intersect = brents.search(f, ptx(oX), ptx(nX), roundTo=4)[0]
				except:
					continue
				#print(f"found solution at {intersect}, {brents.search(f, ptx(oX), ptx(nX), roundTo=4)[1]} steps taken!")
				dctx.text((nX, nY), f"{intersect}", font=intersectfont, fill=intersectColor)
		else: #draw line for the asymptote
			dctx.rectangle([(nX-scale//2, 0), (oX+scale//2, SIZE)], fill=asymptoteColor)

	#prepare for next iteration
	startfound=True
	oX, oY = nX, nY
img.save("out.png")