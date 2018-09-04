from django.db import models
from django.contrib.auth.models import AbstractUser, User


class UserProfile(AbstractUser):
    """用户信息"""
    # 一个角色可以对应多个用户，一个用户可以有多个角色
    role = models.ManyToManyField('Role', blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        db_table = '用户信息'


class Role(models.Model):
    """角色,可以包括学生，讲师等"""
    title = models.CharField(max_length=64, unique=True)
    menu = models.ManyToManyField('Menu')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        db_table = '角色'


class CustomerInfo(models.Model):
    """客户信息表"""
    name = models.CharField(max_length=64, default=None, verbose_name='姓名')
    gender = models.IntegerField(choices=((0, '男'), (1, '女')), null=True, blank=True, verbose_name='性别')
    age = models.IntegerField(blank=True, null=True, verbose_name='年龄')
    id_num = models.CharField(max_length=32, blank=True, null=True, verbose_name='身份证号码')
    contact_type_choices = ((0, 'QQ'), (1, '微信'), (2, '手机'))
    contact_type = models.IntegerField(choices=contact_type_choices, default=0, verbose_name='联系方式')
    contact_info = models.CharField(max_length=64, unique=True, verbose_name='联系电话')
    emergency_contact = models.CharField(max_length=20, null=True, blank=True, verbose_name='紧急电话')
    consult_course = models.ManyToManyField('Course', verbose_name='咨询课程')
    consult_content = models.TextField(verbose_name='咨询大致内容')
    consultant = models.ForeignKey('UserProfile', verbose_name='课程顾问')
    status_choice = ((0, '未报名'), (1, '已报名'), (2, '已退学'))
    status = models.SmallIntegerField(choices=status_choice, default=0, verbose_name='状态')
    source_choices = ((0, 'QQ群'), (1, '51CTO'), (2, '知乎'), (3, '转介绍'), (4, '百度推广'), (5, '其他'))
    source = models.SmallIntegerField(choices=source_choices, verbose_name='来源')
    referral_from = models.ForeignKey('self', blank=True, null=True, verbose_name='转介绍人')
    date = models.DateField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '客户信息'
        verbose_name_plural = verbose_name
        db_table = '客户信息'


class CustomerFollowUp(models.Model):
    """客户跟踪记录表"""
    customer = models.ForeignKey('CustomerInfo')
    content = models.TextField(verbose_name='跟踪内容')
    user = models.ForeignKey('UserProfile', verbose_name='跟踪人')
    status_choice = ((0, '近期无报名计划'), (1, '2周内报名'), (2, '一个月内报名'), (3, '已报名'))
    status = models.SmallIntegerField(choices=status_choice)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer.name

    class Meta:
        verbose_name = '客户跟踪记录'
        verbose_name_plural = verbose_name
        db_table = '客户跟踪记录'


class Course(models.Model):
    """课程"""
    name = models.CharField(verbose_name='课程名称', max_length=64, unique=True)
    price = models.PositiveSmallIntegerField(verbose_name='价格')
    outline = models.TextField(verbose_name='大纲')
    period = models.SmallIntegerField(verbose_name="课程周期（月）")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        db_table = '课程'


class ClassList(models.Model):
    """班级列表"""
    branch = models.ForeignKey('Branch', verbose_name='校区')
    course = models.ForeignKey('Course')
    semester = models.SmallIntegerField(verbose_name='学期')
    teacher = models.ForeignKey('UserProfile',null=True,blank=True)
    start_date = models.DateField(verbose_name='开班日期', auto_now_add=True)
    contract_tempalte = models.ForeignKey('ContractTemplate', blank=True, null=True, verbose_name='关联合同模板')
    graduate_date = models.DateField(verbose_name='毕业日期', blank=True, null=True)
    class_type_choices = (
        (0, '脱产'),
        (1, '周末'),
        (2, '网络班'),
    )
    class_type = models.SmallIntegerField(choices=class_type_choices, default=0)

    def __str__(self):
        return "%s(%s)期" % (self.course.name, self.semester)

    class Meta:
        verbose_name = '班'
        verbose_name_plural = verbose_name
        db_table = '班'
        unique_together = ('course', 'semester', 'branch', 'class_type')


class CourseRecord(models.Model):
    """课程记录"""
    class_grade = models.ForeignKey('ClassList', verbose_name='上课班级')
    day_num = models.SmallIntegerField(verbose_name='课程节次')
    teacher = models.ForeignKey('UserProfile', verbose_name='讲师')
    title = models.CharField(verbose_name='本节主题', max_length=64)
    content = models.TextField(verbose_name='本节内容')
    has_homework = models.BooleanField(verbose_name='是否有作业', default=True)
    homework = models.TextField(verbose_name='作业需求', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s第（%s）节" % (self.class_grade, self.day_num)

    class Meta:
        unique_together = ('day_num', 'class_grade')
        verbose_name = '课程记录'
        verbose_name_plural = verbose_name
        db_table = '课程记录'

class Branch(models.Model):
    """校区"""
    name = models.CharField(max_length=64, unique=True)
    address = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '校区'
        verbose_name_plural = verbose_name
        db_table = '校区'


class Menu(models.Model):
    """动态菜单"""
    name = models.CharField(max_length=64)
    url_type_choices = (
        (0, 'absolute'),
        (1, 'dynamic'),  # 带参数的url
    )
    url_type = models.SmallIntegerField(choices=url_type_choices)
    url_name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'url_name')
        db_table = '菜单'
        verbose_name = '菜单'
        verbose_name_plural = verbose_name


class ContractTemplate(models.Model):
    """合同"""
    name = models.CharField(max_length=32)
    content = models.TextField()
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = '合同'


class StudentEnrollment(models.Model):
    """学员报名"""
    customer = models.ForeignKey('CustomerInfo')
    consultant = models.ForeignKey('UserProfile')
    class_grade = models.ForeignKey('ClassList')
    contract_agreed = models.BooleanField(default=False, verbose_name='同意条款')
    contract_signed_time = models.DateTimeField(blank=True, null=True, verbose_name='合同签订时间')
    contract_approved = models.BooleanField(default=False, verbose_name='审核通过')
    contract_approved_time = models.DateTimeField(blank=True, null=True, verbose_name='合同审核时间')

    def __str__(self):
        return '%s' % self.customer.name

    class Meta:
        unique_together = ['customer', 'class_grade']
        db_table = '学生报名'


class PaymentRecord(models.Model):
    """学员缴费记录"""
    enrollment = models.ForeignKey('StudentEnrollment')
    pay_amount = models.IntegerField(default=500)
    consultant = models.ForeignKey('CustomerInfo')
    payment_type_choices = ((0, '报名费'), (1, '学费'), (2, '退费'))
    payment_type = models.IntegerField(choices=payment_type_choices)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.enrollment

    class Meta:
        db_table = '缴费记录'


class Student(models.Model):
    """学生"""
    student = models.OneToOneField('StudentEnrollment')  #　只有走完报名流程才会成为正式学员
    user_account = models.OneToOneField('UserProfile')  # 创建用户

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = verbose_name
        db_table = '学生'

    def __str__(self):
        return self.student.customer.name


class StudyRecord(models.Model):
    """学习记录表"""
    course_record = models.ForeignKey('CourseRecord')
    student = models.ForeignKey('Student')
    score_choices = (
        (100, 'A+'),
        (90, 'A'),
        (85, 'B+'),
        (80, 'B'),
        (75, 'B-'),
        (70, 'C+'),
        (60, 'C'),
        (40, 'C-'),
        (-50, 'D'),
        (0, 'N/A'),
        (-100, 'COPY'),
    )
    score = models.SmallIntegerField(choices=score_choices, default=0,
                                     verbose_name='成绩')

    show_choices = (
        (0, '缺勤'),
        (1, '已签到'),
        (0, '迟到'),
        (0, '早退'),
    )
    show_status = models.SmallIntegerField(choices=show_choices, default=1,
                                           verbose_name='考勤状态')
    note = models.TextField(verbose_name='成绩备注', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" % (self.course_record, self.student, self.score)

    class Meta:
        verbose_name = '学习记录'
        verbose_name_plural = verbose_name
        db_table = '学习记录'


