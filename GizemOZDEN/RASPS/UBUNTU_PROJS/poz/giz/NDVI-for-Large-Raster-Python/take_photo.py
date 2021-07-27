import cv2

def take():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        if not _:
            break
        else:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
                cv2.imwrite('taken.png', frame)
                cv2.destroyAllWindows()
                return 'taken.png'
                break
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


    cap.release()





