import streamlit as st

import base64

import cv2

import numpy as np

from PIL import Image

from io import BytesIO


@st.cache
def load_image(image_file):
	imag = Image.open(image_file,'r')

	return imag

def get_image_download_link1(img, image_type):
	"""Generates a link allowing the PIL image to be downloaded
	in:  PIL image
	out: JPEG Image
	"""
	#buffered = BytesIO()
	img.save("Cartoonified.jpg")

	labelled = "Download "+str(image_type)+" image"

	with open("Cartoonified.jpg","rb") as file:
		st.download_button(label=labelled,data=file,file_name="Cartoonified.jpg",mime="image/jpg")

def cartoonify(img):
	img = np.array(img)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.medianBlur(gray,5)

	edges = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)

	color = cv2.bilateralFilter(img,9,250,250)

	cartoon = cv2.bitwise_and(color,color,mask = edges)

	return img, edges, cartoon

def main():
	st.title("Cartoonify Yourself")

	image_file = st.file_uploader("Upload images", type=["jpeg","jpg"])

	if image_file is not None:
		#st.write(type(image_file))

		file_details ={"filename":image_file.name,"filetype":image_file.type,"filesize":image_file.size}

		st.image(load_image(image_file),width=300)

		image, edges, cartoon = cartoonify(load_image(image_file))



		st.subheader("Artified Image")

		st.image(edges, width=300)

		edges_ = Image.fromarray(edges)

		get_image_download_link1(edges_,"Artified")

		st.subheader("Cartoonified Image")

		st.image(cartoon, width=300)

		cartoon_ = Image.fromarray(cartoon)

		get_image_download_link1(cartoon_,"Cartoonified")
		


if __name__ =='__main__':
	main() 