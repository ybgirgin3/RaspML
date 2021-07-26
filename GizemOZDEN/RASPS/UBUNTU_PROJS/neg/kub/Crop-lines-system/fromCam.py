import cv2
import os


def get_image():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if success:
            cv2.imshow('camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('c'):
                img_name = 'opencvimage.png'
                cv2.imwrite(img_name, frame)
                cv2.destroyAllWindows()
                return str(img_name)
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

#print(get_image())
