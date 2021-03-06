
# import the necessary packages
import numpy as np
import argparse
import cv2
import os


# load our serialized face detector from disk
print("loading face detector...")
protoPath = os.path.sep.join(["face_detector", "deploy.prototxt"])
modelPath = os.path.sep.join(["face_detector",
	"res10_300x300_ssd_iter_140000.caffemodel"])
net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# open a pointer to the video file stream and initialize the total
# number of frames read and saved thus far
videopath='videos'
for files in os.listdir(videopath):
	filename=str(files)
	for video in os.listdir(os.path.join(videopath,files)):
		videoname=str(video)
		
		vs = cv2.VideoCapture(os.path.join(os.path.join(videopath,files),str(video)))
		read = 0
		saved = 0

		# loop over frames from the video file stream
		while True:
			# grab the frame from the file
			(grabbed, frame) = vs.read()

			# if the frame was not grabbed, then we have reached the end
			# of the stream
			if not grabbed:
				break

			# increment the total number of frames read thus far
			read += 1


			# grab the frame dimensions and construct a blob from the frame
			(h, w) = frame.shape[:2]
			blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
				(300, 300), (104.0, 177.0, 123.0))

			# pass the blob through the network and obtain the detections and
			# predictions
			net.setInput(blob)
			detections = net.forward()

			# ensure at least one face was found
			if len(detections) > 0:
				# we're making the assumption that each image has only ONE
				# face, so find the bounding box with the largest probability
				i = np.argmax(detections[0, 0, :, 2])
				confidence = detections[0, 0, i, 2]

				# ensure that the detection with the largest probability also
				# means our minimum probability test (thus helping filter out
				# weak detections)
				if confidence > 0.5:
					# compute the (x, y)-coordinates of the bounding box for
					# the face and extract the face ROI
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					(startX, startY, endX, endY) = box.astype("int")
					face = frame[startY:endY, startX:endX]

					# write the frame to disk
					p = os.path.join('dataset'+'/'+filename,str(videoname)+str(saved)+".png")
					cv2.imwrite(p, face)
					saved += 1
					print("saved {} to disk".format(p))
					# if saved==200:
						# break

		vs.release()
		cv2.destroyAllWindows()