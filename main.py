import cv2
import numpy as np
import serial


ser = serial.Serial('COM7', 9600)
ser.timeout = 0.1


def detect_blue_object(frame):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Create a binary mask to isolate blue pixels
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find contours in the binary image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        for contour in contours:
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

        # Get the area of the largest contour (assuming the blue object is the largest)
        contour_area = max(cv2.contourArea(contour) for contour in contours)
        
        # Calculate the area of the ROI
        roi_area = frame.shape[0] * frame.shape[1]
        
        # Check if the blue object occupies at least 20% of the small frame
        if contour_area >= 0.2 * roi_area:
            print("Blue Object Detected")
            ser.write(b'1')  # Send '1' to Arduino to turn on the green LED
        else:
            ser.write(b'0') # send '0' to turn red LED on 

    return frame

def instructionsFrame():
    width, height = 640, 480
    canvas = 255 * np.ones((height, width, 3), dtype=np.uint8)

    # Define the instructions text and font settings
    instructions_text = "Place a Blue object in the square"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (0, 0, 0)  # Black color (in BGR format)

    # Calculate the text size to center the text on the canvas
    (text_width, text_height), _ = cv2.getTextSize(instructions_text, font, font_scale, font_thickness)
    text_x = int((width - text_width) / 2)
    text_y = int((height + text_height) / 2)

    # Draw the instructions text on the canvas
    cv2.putText(canvas, instructions_text, (text_x, text_y), font, font_scale, font_color, font_thickness)
    
    return cv2.imshow('Instructions', canvas)


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()


    if ret:
        # Specify the region of interest (ROI) coordinates (x, y, width, height)
        roi_width = 200
        roi_height = 200
        roi_x = 400
        roi_y = 0


        # Crop the frame to the ROI
        roi_frame = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]


        # Perform blue object detection only on the ROI
        blue_detected_roi = detect_blue_object(roi_frame)


        # Replace the ROI in the original frame with the detected ROI
        frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width] = blue_detected_roi


        # Draw lines around the small frame to show it on the screen at all times
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (255, 0, 0), 2)


        cv2.imshow('Blue Detection', frame)
        instructionsFrame()

    # Press q or x button to close window
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Blue Detection', cv2.WND_PROP_VISIBLE) < 1:
        break


cap.release()
cv2.destroyAllWindows()