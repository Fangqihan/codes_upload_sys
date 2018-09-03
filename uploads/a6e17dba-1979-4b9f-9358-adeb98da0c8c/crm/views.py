from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import UserProfile


@login_required
def dashboard(request):
    return render(request, 'crm/dashboard.html')


def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if username and password1 and password2 and password1 == password2:
            print('注册成功')
            user = UserProfile(username=username, password=make_password(password1))
            user.save()
            return redirect('/crm/login/')

    return render(request, 'crm/register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            print('验证通过', user)
            login(request, user)
            return redirect('/crm/')

    return render(request, 'crm/login.html')


def user_logout(request):
    logout(request)
    return redirect('/crm/login/')


from crm import models


@login_required
def add_student(request):
    """销售添加学生"""
    customers = models.CustomerInfo.objects.all()
    branches = models.Branch.objects.all()

    # 找到所有人员信息中找出角色是销售的人员
    consultants = models.UserProfile.objects.filter(role__title='销售').exclude(id=1)

    if request.method == 'POST':
        customerid = request.POST.get('customer')
        class_gradeid = request.POST.get('class_grade')
        consultantid = request.POST.get('consultant')

        from crm.models import StudentEnrollment
        if consultantid and class_gradeid and consultantid:
            student_enroll = StudentEnrollment.objects.create(
                customer_id=customerid,
                class_grade_id=class_gradeid,
                consultant_id=consultantid
            )
            print('学生创建成功')
            enroll_links = 'http://127.0.0.1:8008/crm/enroll/%s/' % student_enroll.id
            print(enroll_links)

    return render(request, 'crm/student_enroll.html', locals())


from crm.forms import CustomerInfoForm
from crm.models import StudentEnrollment, CustomerInfo


def student_enroll(request, id):
    """学生完善个人信息"""
    student_enroll = StudentEnrollment.objects.filter(id=int(id)).first()
    customer_obj = student_enroll.customer
    price = student_enroll.class_grade.course.price
    class_grade = student_enroll.class_grade
    course = class_grade.course

    if request.method == 'GET':
        customer_form = CustomerInfoForm(instance=customer_obj)
        upload_files = []
        from django import conf
        import os
        enrollment_upload_dir = os.path.join(conf.settings.ORM_PATH_DIR,id)
        if os.path.isdir(enrollment_upload_dir):
            upload_files=os.listdir(enrollment_upload_dir)
            pass

    elif request.method == 'POST':
        customer_form = CustomerInfoForm(instance=customer_obj, data=request.POST)
        errors = customer_form.errors
        #  自定制errors错误信息
        if not request.POST.get('contract_agreed', ''):
            errors['contract_agreed'] = '必须勾选阅读'
        if not request.POST.get('id_num', ''):
            errors['id_num'] = '身份证号码必填'
        if not request.POST.get('contact_info', ''):
            errors['contact_info'] = '联系电话必填'
        if not request.POST.get('emergency_contact', ''):
            errors['emergency_contact'] = '紧急联系电话必填'

        if customer_form.is_valid():  # 表单填写无错误
            if student_enroll.contract_agreed:  # 排除重复填写此表单
               return HttpResponse('您的相关信息已提交至审核')

            student_enroll.contract_agreed = True
            import datetime
            student_enroll.contract_signed_time = datetime.datetime.now()
            print(datetime.datetime.now())
            student_enroll.save()

            customer_form.save()
            return HttpResponse('待审批....')

        print(errors)

    return render(request, 'crm/complete_info.html', locals())


from crm.models import Branch, ClassList
import json


def get_classes(request, id):
    branch = Branch.objects.filter(id=int(id)).first()
    classes = list(ClassList.objects.filter(branch=branch).values(
        'id', 'branch__name', 'course__name', 'semester'))
    return HttpResponse(json.dumps(classes), content_type="application/json")


import os
from django import conf


def enroll_file_upload(request, enrollment_id):
    # 保存文件，对应的文件夹存在则保存至文件夹内，不存在则先创建文件夹
    enrollment_upload_dir = os.path.join(conf.settings.ORM_PATH_DIR, enrollment_id)
    if not os.path.isdir(enrollment_upload_dir):
        os.mkdir(enrollment_upload_dir)

    file_obj = request.FILES.get('file')
    # 限定上传文件的最大数量
    if len(os.listdir(enrollment_upload_dir)) >= 10:
        return HttpResponse(json.dumps({'status': False, 'err_msg': '最多上传两份文件'}))

    with open(os.path.join(enrollment_upload_dir, file_obj.name), "wb") as f:
        for chunks in file_obj.chunks():
            f.write(chunks)

    return HttpResponse(json.dumps({'status': True, }))


@login_required
def audit_list(request):
    """待审核学员列表页面"""
    audit_stu_list = StudentEnrollment.objects.filter(contract_agreed=1,contract_approved=0)
    return render(request,'crm/audit_list.html',locals())


import datetime


@login_required
def audit(request,id):
    """审核学员"""
    student_enroll = StudentEnrollment.objects.filter(id=int(id)).first()
    customer_obj = student_enroll.customer
    from .forms import StudentEnrollForm
    student_enroll_form = StudentEnrollForm(instance=student_enroll)

    if request.method=='POST':
        student_enroll_form = StudentEnrollForm(instance=student_enroll,data=request.POST)
        if student_enroll.contract_approved:
           return HttpResponse('该学员已经通过审核')
        if student_enroll_form.data.get('contract_approved',''):
            student_enroll.contract_approved=True
            student_enroll.contract_approved_time=datetime.datetime.now()
            customer_obj.status=1
            customer_obj.save()
            student_enroll.save()
            return redirect('/crm/audit_list/')

    return render(request,'crm/audit_student_enroll.html',locals())


import os


@login_required
def enroll_file_delete(request,stu_id,file_name):
    """文件删除功能，根据学生id和文件名确定要删除的文件路径"""
    file_path = os.path.join(conf.settings.ORM_PATH_DIR,stu_id,file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        if request.is_ajax():
            return HttpResponse(json.dumps({'status':True,'file_id':str(file_name).replace('.','_')}))
        return

    else:
        print('no such file:%s' % file_path)
        return HttpResponse(json.dumps({'status':False,'error_msg':'没有找到此文件'}))












