from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import View
from django.db.models import Q

import os
import base64
import json
from datetime import datetime,timedelta
import face_recognition

from django.conf import settings
from .forms import *
from .models import *
from . authentication import login_require
# Create your views here.



# @require_http_methods(["GET"])
def index(request):
    name = request.session.get('name')
    is_teacher = request.session.get('teacher')
    return render(request, 'index.html',context={'name':name,'is_teacher':is_teacher})

class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            no_or_name = form.cleaned_data.get('no_or_name')
            password = form.cleaned_data.get('password')
            try:
                user1 = Student.objects.get(Q(no=no_or_name)|Q(name=no_or_name))
            except:
                user1 = None
            try:
                user2 = Teacher.objects.get(Q(no=no_or_name) | Q(name=no_or_name))
            except:
                user2 = None
            if user1 and user2:
                if user1.verify_password(password):
                    request.session['name'] = user1.name
                    return redirect(reverse('student'))
                elif user2.verify_password(password):
                    request.session['name'] = user2.name
                    request.session['teacher'] = True
                    return redirect(reverse('teacher'))
            elif user1:
                if user1.verify_password(password):
                    request.session['name'] = user1.name
                    return redirect(reverse('student'))
            elif user2:
                if user2.verify_password(password):
                    request.session['name'] = user2.name
                    request.session['teacher'] = True
                    return redirect(reverse('teacher'))
        else:
            print(form.errors.get_json_data())
        return render(request, 'login.html')

class RegistView(View):
    def get(self,request):
        return render(request, 'regist.html')
    def post(self,request):
        form = RegistForm(request.POST)
        if form.is_valid():
            no = form.cleaned_data.get('no')
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            if request.POST.get('key') == settings.TEACHER_REGIST_KEY:
                teacher = Teacher(no=no,name=name,password=password)
                teacher.save()
                request.session['teacher'] = True
                request.session['name'] = name
                return redirect(reverse('teacher'))
            elif request.POST.get('key') == '':
                student = Student(no=no,name=name,password=password)
                student.save()
                request.session['name'] = name
                return redirect(reverse('student'))
        return render(request, 'regist.html')

class LogoutView(View):
    def get(self,request):
        del request.session['name']
        if request.session.get('teacher'):
            del request.session['teacher']
        return redirect(reverse('login'))

class TeacherView(View):
    @login_require
    def get(self,request):
        name = request.session.get('name')
        is_teacher = request.session.get('teacher')
        teacher = Teacher.objects.filter(name=name).first()
        courses = Course.objects.filter(teacher=teacher)
        return render(request,'teacher.html',context={'courses':courses,'name':name,'is_teacher':is_teacher})
    def post(self,request):
        form = CourseForm(request.POST)
        if form.is_valid():
            no = form.cleaned_data.get('no')
            course_name = form.cleaned_data.get('course_name')
            name = request.session.get('name')
            teacher = Teacher.objects.get(name=name)
            course = Course(no=no,course_name=course_name,teacher=teacher)
            course.save()
        else:
            print(form.errors.get_json_data())
        return redirect(reverse('teacher'))

class StudentView(View):
    @login_require
    def get(self,request):
        name = request.session.get('name')
        student = Student.objects.filter(name=name).first()
        signsheets = SignSheet.objects.filter(student=student)
        return render(request,'student.html',context={'signsheets':signsheets,'name':name})
    def post(self,request):

        value = request.POST.get('value')
        student = Student.objects.get(name=request.session.get('name'))
        course = Course.objects.get(Q(no=value)|Q(course_name=value))
        signsheet = SignSheet(student=student,course=course,count=0)
        signsheet.save()
        return redirect(reverse('student'))


class StudentUploadFace(View):
    @login_require
    def get(self,request):
        name = request.session.get('name')
        return render(request, 'student_face.html', context={'name': name})
    def post(self,request):
        image_base64 = request.POST.get('image')
        image_file = request.FILES.get('image')
        create_time = datetime.now().strftime('%Y%m%d%H%M%S')
        imgpath = settings.MEDIA_ROOT + '/' + create_time + '.jpg'
        if image_file or image_base64:
            if image_base64:
                imgdata = base64.b64decode(image_base64)
                with open(imgpath, 'wb') as f:
                    f.write(imgdata)
            elif image_file:
                with open(imgpath, 'wb') as f:
                    for fimg in image_file.chunks():
                        f.write(fimg)
            student = Student.objects.get(name=request.session.get('name'))
            face_path = FacePath(path=imgpath, student=student)
            face_path.save()
        else:
            pass
        return redirect(reverse('uploadface'))

class StudentListView(View):
    @login_require
    def get(self,request,course_id):
        name = request.session.get('name')
        course = Course.objects.get(no=course_id)
        signsheets = course.signsheets.all()
        return render(request,'student_list.html',context={'name':name,'signsheets':signsheets})
    def post(self,rquest,course_id):
        pass

class StudentFaceSign(View):
    @login_require
    def get(self,request,course_id):
        name = request.session.get('name')
        return render(request, 'student_face_sign.html', context={'name': name,'course_id':course_id})
    def post(self,request,course_id):
        image_base64 = request.POST.get('image')
        imgdata = base64.b64decode(image_base64)
        create_time = datetime.now().strftime('%Y%m%d%H%M%S')
        imgpath = settings.MEDIA_ROOT + '/scaning_faces/' + create_time + '.jpg'
        with open(imgpath, 'wb') as f:
            f.write(imgdata)

        course = Course.objects.get(no=course_id)
        signsheets = course.signsheets.all()
        for signsheet in signsheets:
            faces = signsheet.student.faces.all()
            for face in faces:
                strange_image = face_recognition.load_image_file(imgpath)
                known_image = face_recognition.load_image_file(face.path)
                try:
                    known_image_encoding = face_recognition.face_encodings(known_image)[0]
                    strange_image_encoding = face_recognition.face_encodings(strange_image)[0]
                    results = face_recognition.compare_faces([known_image_encoding], strange_image_encoding,tolerance=0.4)
                except:
                    print('there is not face here...')
                    continue
                if results[0] == True:
                    d = {'no':face.student.no,'name': face.student.name,'repeat':True}
                    course = Course.objects.get(no=course_id)
                    signsheet = SignSheet.objects.get(student=face.student, course=course)
                    sign_time = signsheet.sign_time.replace(tzinfo=None)+ timedelta(hours=8)
                    time_hold = (datetime.now()-sign_time).seconds
                    if time_hold > (60*30) or signsheet.count==0:
                        signsheet.count = signsheet.count + 1
                        signsheet.save()
                        d['repeat'] = False
                    if os.path.exists(imgpath):
                        os.remove(imgpath)
                    return HttpResponse(json.dumps(d))
        return HttpResponse(json.dumps({'name':None}))