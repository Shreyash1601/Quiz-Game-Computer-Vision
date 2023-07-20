import cv2
import csv
import cvzone
import time
from cvzone.HandTrackingModule import HandDetector
cap=cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)
detector=HandDetector(detectionCon=0.8,maxHands=1)
class MCQ:
    def __init__(self,data):
        self.Q=data[0]
        self.C1=data[1]
        self.C2=data[2]
        self.C3=data[3]
        self.C4=data[4]
        self.ans=int(data[5])
        self.userAns=None
    
    def update(self,cursor,bboxs):
        for x,bbox in enumerate(bboxs):
            x1,y1,x2,y2=bbox
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.userAns=x+1
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,255),cv2.FILLED)





file="Mcqs.csv"
with open(file,newline='\n') as f:
    reader=csv.reader(f)
    dataAll=list(reader)[1:]
qNo=0
qLen=len(dataAll)
mcqList=[]
for q in dataAll:
    mcqList.append(MCQ(q))


while True:
    succ,img=cap.read()
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)
    
    if qNo<qLen:
            mcq=mcqList[qNo]
            img,bbox=cvzone.putTextRect(img,mcq.Q,[100,100],3,3,colorR=(0,140,255),border=3,colorB=(43,75,238))
            img,bbox1=cvzone.putTextRect(img,mcq.C1,[100,200],3,3,colorR=(66,84,245),border=2,colorB=(0,140,255))
            img,bbox2=cvzone.putTextRect(img,mcq.C2,[800,200],3,3,colorR=(66,84,245),border=2,colorB=(0,140,255))
            img,bbox3=cvzone.putTextRect(img,mcq.C3,[100,400],3,3,colorR=(66,84,245),border=2,colorB=(0,140,255))
            img,bbox4=cvzone.putTextRect(img,mcq.C4,[800,400],3,3,colorR=(66,84,245),border=2,colorB=(0,140,255))
    else:
        score=0
        for mcq in mcqList:
            if mcq.ans==mcq.userAns:
                score+=1
        print(score)
        img,_=cvzone.putTextRect(img,f'Score:{(score*100)/float(qLen)}',[400,300],5,2,offset=50,colorR=(252,186,3),border=4)

    if hands:
        lmList=hands[0]['lmList']
        cursor=lmList[8]
        length,info,img=detector.findDistance(lmList[8],lmList[12],img)

        if length<60:
            mcq.update(cursor,[bbox1,bbox2,bbox3,bbox4])
            print(mcq.userAns)
            if mcq.userAns is not None:
              time.sleep(0.3)
              qNo+=1

    barValue=150+int((950//10)*qNo)
    cv2.rectangle(img,(150,600),(barValue,650),(0,255,255),cv2.FILLED)
    cv2.rectangle(img,(150,600),(1100,650),(0,255,0),5)
    img,_=cvzone.putTextRect(img,f'{(qNo/qLen)*100}',[1150,630],2,2,offset=20,colorR=(252,186,3),border=4)

    cv2.namedWindow("img",cv2.WND_PROP_FULLSCREEN)
    cv2.imshow("img",img)
    cv2.waitKey(1)