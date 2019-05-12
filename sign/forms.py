from django import forms

class RegistForm(forms.Form):
    no = forms.CharField(max_length=20,required=True,error_messages={'max_length':'学号或教师号不得超过20个字符','required':'学号或教师号不为空'})
    name = forms.CharField(max_length=20,required=True,error_messages={'max_length':'姓名不得超过20个字符','required':'姓名不为空'})
    password = forms.CharField(max_length=100,required=True,error_messages={'max_length':'密码不得超过20个字符','required':'密码不为空'})

class LoginForm(forms.Form):
    no_or_name = forms.CharField(max_length=20,required=True,error_messages={'max_length':'学号或教师号或姓名不得超过20个字符','required':'学号或教师号或姓名不得为空'})
    password = forms.CharField(max_length=100,required=True,error_messages={'max_length':'密码不得超过20个字符','required':'密码不为空'})

class CourseForm(forms.Form):
    no = forms.CharField(max_length=8)
    course_name = forms.CharField(max_length=40)

class PhotographForm(forms.Form):
    image = forms.ImageField()