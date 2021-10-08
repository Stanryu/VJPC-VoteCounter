# -*- coding: utf8 -*-
import cv2
import sys
import numpy as np
from marker import Marker

#Read the original Imagem
img_o = cv2.imread(sys.argv[1], 1)

#Grayscale img
img_g = cv2.imread(sys.argv[1], 0)

#Binary img
blur = cv2.GaussianBlur(img_g,(5,5),0)
ret, img_b = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

cut_width = int(img_o.shape[0] * 0.81)
cut_height = int(img_o.shape[1] * 0.46)

#print cut_width, cut_height

#erode and dilate kernel
kernel = np.ones((3,3), np.uint8)
kernel[0][0] = 0;
kernel[0][2] = 0;
kernel[2][0] = 0;
kernel[2][2] = 0;

#erode
img_e = cv2.erode(img_b, kernel, iterations=6)
#
# #dilate
# img_e = cv2.dilate(img_e, kernel, iterations=2)
#
# #erode
# img_e = cv2.erode(img_e, kernel, iterations=1)

#roi = img[row:row+height,column:column+width]
img_croped = img_e[cut_height : cut_height + img_o.shape[1], 0 : cut_width]

#get all objects contours
cnts = cv2.findContours(img_croped.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[1]

markers_list = []

for c in cnts:
	x,y,w,h = cv2.boundingRect(c)
	# cv2.rectangle(img_o, (x, (y + cut_height)), (x + w, (y + cut_height) + h), (0,255,0),2)
	markers_list.append(Marker(x,y,w,h,0))

marker_top_left = markers_list[0]
marker_top_right = markers_list[0]
marker_bottom_left = markers_list[0]


for marker in markers_list:
	#identificar o marcador mais acima e mais a esquerda
	if((marker.x <= marker_top_left.x) and (marker.y <= marker_top_left.y)):
		marker_top_left = marker

	#identificar o marcador mais acima e mais a direita
	if((marker.x >= marker_top_right.x) and (marker.y <= marker_top_right.y)):
		marker_top_right = marker

	#identificar o marcador mais abaixo e mais a esquerda
	if((marker.x <= marker_bottom_left.x) and (marker.y >= marker_bottom_left.y)):
		marker_bottom_left = marker


# print "TL: ", marker_top_left.x, marker_top_left.y
# print "TR: ", marker_top_right.x, marker_top_right.y
# print "BL: ", marker_bottom_left.x, marker_bottom_left.y

cv2.rectangle(img_o, (marker_top_left.x, (marker_top_left.y + cut_height)), (marker_top_left.x + marker_top_left.w, (marker_top_left.y + cut_height) + marker_top_left.h), (0,0,255),2)
cv2.rectangle(img_o, (marker_top_right.x, (marker_top_right.y + cut_height)), (marker_top_right.x + marker_top_right.w, (marker_top_right.y + cut_height) + marker_top_right.h), (255,0,0),2)
cv2.rectangle(img_o, (marker_bottom_left.x, (marker_bottom_left.y + cut_height)), (marker_bottom_left.x + marker_bottom_left.w, (marker_bottom_left.y + cut_height) +marker_bottom_left.h), (0,255,0),2)

markers_line = []
for marker in markers_list:
	if((marker.y == marker_top_left.y) and (marker.y == marker_top_right.y) and marker != marker_top_left):
		markers_line.append(marker)
		cv2.rectangle(img_o, (marker.x, (marker.y + cut_height)), (marker.x + marker.w, (marker.y + cut_height) + marker.h), (255,0,255),2)

markers_line.sort(key=lambda marker: marker.y, reverse=True)
for i, marker in enumerate(markers_line):
	marker.value = 9 - i
	#print (marker.x, marker.y, marker.value)

markers_column = []
for marker in markers_list:
	if((marker.x == marker_top_left.x) and (marker.x == marker_bottom_left.x) and (marker != marker_top_left and marker != marker_bottom_left)):
		markers_line.append(marker)
		cv2.rectangle(img_o, (marker.x, (marker.y + cut_height)), (marker.x + marker.w, (marker.y + cut_height) + marker.h), (0,255,255),2)

markers_rest = []
for marker in markers_list:
	if ((marker not in markers_line) and (marker not in markers_column) and (marker != marker_top_left and marker != marker_top_right and marker != marker_bottom_left)):
		markers_rest.append(marker)
		cv2.rectangle(img_o, (marker.x, (marker.y + cut_height)), (marker.x + marker.w, (marker.y + cut_height) + marker.h), (255,255,0),2)

for marker in markers_rest:
	for lmarker in markers_line:
		if((marker.x >= (lmarker.x - (lmarker.w / 2))) and (marker.x <= (lmarker.x + (lmarker.w / 2)))):
			marker.value = lmarker.value

markers_rest.sort(key=lambda marker: marker.y, reverse=False)

pres = str(markers_rest[0].value) + str(markers_rest[1].value)
senad = str(markers_rest[2].value) + str(markers_rest[3].value) + str(markers_rest[4].value) + str(markers_rest[5].value) + str(markers_rest[6].value)

print "Presidente: ", pres
print "Senador: ", senad

cv2.imshow("IMG", img_o)
cv2.waitKey(0)
