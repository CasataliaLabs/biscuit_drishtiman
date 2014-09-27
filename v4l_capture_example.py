import Image
import select
import v4l2capture
import numpy
import pylab

import time

# Open the video device.
#~ video = v4l2capture.Video_device("/dev/video0")
video = v4l2capture.Video_device("http://admin:@192.168.1.105/snapshot.cgi?.mjpeg")
# Suggest an image size to the device. The device may choose and
# return another size if it doesn't support the suggested one.
size_x, size_y = video.set_format(800, 448)

# Create a buffer to store image data in. This must be done before
# calling 'start' if v4l2capture is compiled with libv4l2. Otherwise
# raises IOError.
video.create_buffers(1)

# Send the buffer to the device. Some devices require this to be done
# before calling 'start'.
video.queue_all_buffers()

# Start the device. This lights the LED if it's a camera that has one.
video.start()

# Wait for the device to fill the buffer.
select.select((video,), (), ())

# The rest is easy :-)
image_data = video.read()
video.close()
#~ image = Image.fromstring("L", (size_x, size_y), image_data)
image = Image.fromstring("RGB", (size_x, size_y), image_data)
imageNumpy = numpy.asarray(image)
pylab.imshow(imageNumpy)
pylab.show()
#~ a = input('test')
#time.sleep(4)
#image.save("image.jpg")
#print "Saved image.jpg (Size: " + str(size_x) + " x " + str(size_y) + ")"

