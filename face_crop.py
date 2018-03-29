import cv2

facedata = "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(facedata)


def facechop(image):  

    global facedata, cascade
    img = image

    minisize = (img.shape[1],img.shape[0])
    miniframe = cv2.resize(img, minisize)

    faces = cascade.detectMultiScale(miniframe)

    if len(faces) == 0:
        print "No faces found"
        return ''
    
    elif len(faces) > 1:
        old_face_height = 0
        current_face_height = 0
        current_face = -1
        chosed_face = 0
        
        for face in faces:
            current_face += 1
            x, y, w, h = [ v for v in face ]
            current_face_height = y+h
            if current_face_height > old_face_height:
                old_face_height = current_face_height
                chosed_face = current_face


        face = faces[chosed_face]
        x, y, w, h = [ v for v in face ]

        if y < 130 or h < 130: #Either wrong face is detected or they are too far
            print "Please come closer"
            return ''            
        

    else:
        face = faces[0]
        x, y, w, h = [ v for v in face ]

        if h < 170: #Either wrong face is detected or they are too far
            print "Please come closer"
            return None            

        elif h > 220: #Either wrong face is detected or they are too far
            print "Please move a little farther"
            return None            


    x, y, w, h = [ v for v in face ]
    cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))

    sub_face = img[y:y+h, x:x+w]
    face_file_name = "faces/face_" + str(y) + ".jpg"


    cv2.imwrite(face_file_name, sub_face)
    print "Face recorded"

    return


if __name__ == '__main__':  

    cv2.namedWindow("Record faces")
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("Record faces", frame)
        rval, frame = vc.read()
        
        key = cv2.waitKey(33)

        if key == 1048586: #Save face on pressing enter key
            facechop(frame)
            
        elif key == 1048603: # exit on ESC
            cv2.destroyAllWindows()
            exit(0)

    cv2.destroyWindow("Record faces")
