from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password

# Create your models here.

class Student(models.Model):
    no = models.CharField('学号',max_length=20,primary_key=True)
    name = models.CharField('姓名',max_length=20)
    password_hash = models.CharField(max_length=100)
    create_time = models.DateTimeField('注册时间',auto_now_add=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash = make_password(password)
    def verify_password(self,password):
        return check_password(password,self.password_hash)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = verbose_name
        ordering = ['no']
    def __str__(self):
        return self.name

class Teacher(models.Model):
    no = models.CharField('教师号',max_length=8,primary_key=True)
    name = models.CharField('姓名',max_length=20)
    password_hash = models.CharField(max_length=100)
    create_time = models.DateTimeField('注册时间', auto_now_add=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash = make_password(password)
    def verify_password(self,password):
        return check_password(password,self.password_hash)
    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name
        ordering = ['no']
    def __str__(self):
        return self.name

class Course(models.Model):
    no = models.CharField('课程号',max_length=8,primary_key=True)
    course_name = models.CharField('课程名',max_length=40)
    teacher = models.ForeignKey("Teacher",verbose_name='授课教师',related_name='courses',on_delete=models.CASCADE)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        ordering = ['create_time']
    def __str__(self):
        return self.course_name


class SignSheet(models.Model):
    id = models.AutoField('ID',primary_key=True)
    student = models.ForeignKey("Student",models.CASCADE,verbose_name='学号',related_name='signsheets')
    course = models.ForeignKey("Course",models.CASCADE,verbose_name='课程号',related_name='signsheets')
    sign_time = models.DateTimeField('最新时间',auto_now=True)
    count = models.IntegerField('签到次数')

    class Meta:
        unique_together = ('student','course')#联合主键
        verbose_name = '签到表'
        verbose_name_plural = verbose_name
        ordering = ['-sign_time']



class FacePath(models.Model):
    id = models.AutoField('ID',primary_key=True)
    path = models.CharField('图片路径',max_length=200)
    student = models.ForeignKey("Student", related_name="faces",on_delete=models.CASCADE,verbose_name='所属学生')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    class Meta:
        verbose_name = '照片路径'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']