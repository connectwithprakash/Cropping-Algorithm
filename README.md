<h3>The algorithm accepts image and then with the given center co-ordinates and aspects ratio finds the image segment and crops the image.</h3>

**Contents**

1. *window_method.py* contains the actual algorithm to find the best crop.
2. *test_window_method.py* contains sample code for direct usage.
3. *crop_with_face_centered.py* contains sample code for indirect usage with MTCNN as face detector.


**Application**

1. Use to crop image of desired aspect ratio from center of image
2. Use it along with face detection model to crop image with person in center

**Usage**

1. Direct usage: Call function by passing image array, center co-ordinates and desired aspect ratio.
    >`image = plt.imread(image_file_path)`</br>
    >`output = crop(image, (h,k), aspect_ratio)`</br>
    >`plt.imshow(output)` | `plt.imsave(output_file_name, output)`

2. Indirect usage: Use face detection model to get center of face.
    >*Use face detection model like cv2 or MTCNN*</br>
