from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from account.models import Roles, Profile
from django.db.models import Q
from django.contrib import messages
import os
from PIL import Image
import numpy as np
import cv2
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Create roles on first run
def insertRoles():
    roles = Roles.objects.count()
    if (roles < 1):
        role = Roles()
        role.name = 'Admin'
        role.save()

# Create an admin on first run
def insertAdmin():
    profiles = Profile.objects.count()
    if (profiles < 1):
        profile = Profile()
        profile.name = 'Admin'
        profile.username = 'admin'
        profile.password = 'admin'
        profile.role = Roles.objects.get(pk=1)
        profile.save()


def login(request):
    content = {}
    insertRoles()
    insertAdmin()
    content['title'] = 'Login'
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        # select * from profiles where username = admin and password = admin@123 limit 1
        profile = Profile.objects.filter(username=username, password=password).first()
        if (profile):
            request.session['account_name'] = profile.name
            request.session['account_id'] = profile.id
            request.session['account_role'] = profile.role_id
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, "Credentials provided does not matched in our records.")
    return render(request, 'account/login.html', content)


def logout(request):
    del request.session['account_name']
    del request.session['account_role']
    del request.session['account_id']
    messages.success(request, "You are logged out!.")
    return HttpResponseRedirect(reverse('login'))

def face_login(request):
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
                    if (face_profile):
                        request.session['account_name'] = face_profile.name
                        request.session['account_id'] = face_profile.id
                        request.session['account_role'] = face_profile.role_id

                        cap.release()
                        cv2.destroyAllWindows()
                        return HttpResponseRedirect(reverse('index'))

                    # name = face_profile.name
                    # print(name)
                    # font = cv2.FONT_HERSHEY_SIMPLEX
                    # color = (255, 255, 255)
                    # stroke = 2
                    # cv2.putText(FaceDetect, name, (x, y), font,
                    #             1, color, stroke, cv2.LINE_AA)
                else:
                    pass

            cv2.imshow('Face', FaceDetect)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
