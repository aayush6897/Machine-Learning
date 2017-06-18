import numpy as np
import cv2

cam=cv2.VideoCapture(0)
facec=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
font=cv2.FONT_HERSHEY_PLAIN

f1=np.load('aayush.npy').reshape((20,-1))
f2=np.load('anju.npy').reshape((20,-1))
f3=np.load('ashwani.npy').reshape((20,-1))

data=np.concatenate((f1,f2,f3))


labels=np.zeros((data.shape[0],))
labels[20:40]=1.0
labels[40:]=2.0

names={
    0:'aayush',
    1:'anju',
    2:'ashwani'
}

def dist(x1,x2):
    d=np.sqrt(((x1-x2)**2).sum())
    return d
def knn(xtrain,ytrain,xt,k=5):
    vals=[]
    for ix in range(xtrain.shape[0]):
        d=dist(xtrain[ix],xt)
        vals.append([d,ytrain[ix]])
    sorted_labels=sorted(vals,key=lambda z:z[0])
    neigh=np.asarray(sorted_labels)[:k,-1]

    freq=np.unique(neigh,return_counts=True)

    return(freq[0][freq[1].argmax()])

while(True):
    ret, fr=cam.read()
    if ret==True:
        gray=cv2.cvtColor(fr,cv2.COLOR_BGR2GRAY)
        faces=facec.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            fc=fr[y:y+h,x:x+w,:]
            r=cv2.resize(fc,(50,50)).flatten()
            text=names[int(knn(data,labels,r))]
            cv2.putText(fr,text,(x,y),font,1,(255,0,0),2)

            cv2.rectangle(fr,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.imshow('fr',fr)
        if cv2.waitKey(1)==27:
            break
    else:
        print('error')
        break
cv2.destroyAllWindows()
