from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from account.models import Profile
import os
from PIL import Image
import numpy as np
import cv2
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
def index(request):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'My Face Data'
        return render(request, 'face/index.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def create_dataset(request, pk):
    if(request.method == 'POST'):
        profile = Profile.objects.get(pk = pk)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cam = cv2.VideoCapture(0)
        createFolder('./media/dataset/'+str(profile.id)+'/')
        FaceCount = 1
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
            for(x, y, w, h) in faces:
                FaceCount = FaceCount+1
                print(FaceCount)
                path = './media/dataset/'+str(profile.id)+'/'
                cv2.imwrite(os.path.join(path, str(pk)+"_" +
                            str(FaceCount)+".jpg"), gray[y:y+h, x:x+w])
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 10)
                #cv2.waitKey(100000)
            cv2.imshow("Face", img)
            #cv2.destroyAllWindows()
            if(FaceCount > 100):
                break
            else:
                continue
        cam.release()
        cv2.destroyAllWindows()
        # face_train(pk)
        face_train(request)
        messages.success(request, f'Dataset of {profile.name} created.')
        return HttpResponseRedirect(reverse('su-face-index'))


def face_train(request):
    image_dir = str(BASE_DIR) + '/media/dataset/'
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Train dataset with OpenCv's Principal Component Analysis (PCA) component LBPHFaceRecognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids = {}
    y_labels = []
    x_train = []
    ids = []
    for root, dirs, files in os.walk(image_dir):
        New = 0
        for file in files:
            if file.endswith("png") or file.endswith("JPEG") or file.endswith("JPG") or file.endswith("jpeg") or file.endswith("jpg") or file.endswith("PNG"):
                path = os.path.join(root, file)
                label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
                # label = profile.name

                #Give ID:
                if label in label_ids:
                    pass
                else:
                    label_ids[label] = current_id
                    current_id += 1

                # id_ = label_ids[label]
                id_ = int(label)
                print('ID: ' + str(id_))
                print('Label: ' + label)

                if New == 0:
                    New = 1
                else:
                    pass

                ids.append(id_)

                pil_image = Image.open(path).convert("L")
                size = (550, 550)
                final_image = pil_image.resize(size, Image.ANTIALIAS)
                # Every pixels into numpy array
                image_array = np.array(final_image, "uint8")

                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

                for (x, y, w, h) in faces:
                    roi = image_array[y:y+h, x:x+w]
                    x_train.append(roi)
                    y_labels.append(id_)

    recognizer.train(x_train, np.array(y_labels))
    recognizer.save(str(BASE_DIR) + '/trainer.yml')
    return 1
    # messages.success(request, 'Dataset created and faces are trained.')
    # return HttpResponseRedirect(reverse('su-face-index'))


def test(request):
    if(request.method == 'POST'):
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(str(BASE_DIR) + '/trainer.yml')
        cap = cv2.VideoCapture(0)
        while True:
            ret, FaceDetect = cap.read()
            gray = cv2.cvtColor(FaceDetect, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.5, minNeighbors=5)
            for(x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                id_, conf = recognizer.predict(roi_gray)
                print('ID is ' + str(id_))
                if conf >= 40 and conf <= 70:
                    cv2.rectangle(FaceDetect, (x, y),
                                  (x+w, y+h), (255, 0, 0), 2)
                    face_profile = Profile.objects.get(pk=id_)

                    name = face_profile.name
                    print(name)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    color = (255, 255, 255)
                    stroke = 2
                    cv2.putText(FaceDetect, name, (x, y), font,
                                1, color, stroke, cv2.LINE_AA)
                else:
                    pass

            cv2.imshow('Face', FaceDetect);
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
