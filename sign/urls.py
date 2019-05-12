
from django.urls import path,re_path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('regist/',views.RegistView.as_view(),name='regist'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('teacher/',views.TeacherView.as_view(),name='teacher'),
    path('student/',views.StudentView.as_view(),name='student'),
    path('student/list/<course_id>/',views.StudentListView.as_view(),name='studentlist'),
    path('uploadface/',views.StudentUploadFace.as_view(),name='uploadface'),
    path('studentfacesign/<course_id>/',views.StudentFaceSign.as_view(),name='studentfacesign'),
]

# 尝试了一下re_path也是接收位置参数url的用法，还没有找到如何接收关键字参数url的接收办法