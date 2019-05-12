from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = '人脸识别签到系统后台'
admin.site.site_title = '后台管理'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('no','name','create_time')
    list_display_links = ('no', 'name')
    search_fields = ('name',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('no','name','create_time')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('no','course_name','teacher','create_time')

@admin.register(SignSheet)
class SignSheetAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'count','sign_time')

@admin.register(FacePath)
class FaceUrlAdmin(admin.ModelAdmin):
    list_display = ('id', 'path', 'student', 'create_time')