import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture('Video.mp4')

detector = PoseDetector()
posList = []
while True:
    success, img = cap.read()
    print(img.shape)
    if success:
        img = detector.findPose(img)
        lmList, bboxInfo = detector.findPosition(img)

        if bboxInfo:
            lmString = ''
            for lm in lmList:
                # print(lm)
                lmString += f'{lm[0]},{lm[1]},{lm[2]},'
            posList.append(lmString)

        print(len(posList))

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        # if key == ord('s'):
        continue
    with open("AnimationFile.txt", 'w') as f:
        f.writelines(["%s\n" % item for item in posList])
        break
