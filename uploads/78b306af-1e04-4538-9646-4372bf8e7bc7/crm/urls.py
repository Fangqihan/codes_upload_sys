from django.conf.urls import url,include
from crm import views

urlpatterns = [
    url(r'^$', views.dashboard,name='crm_home'),
    url(r'^login/$', views.user_login, name='crm_login'),
    url(r'^register/$', views.user_register, name='crm_register'),
    url(r'^logout/$', views.user_logout, name='crm_logout'),

    url(r'^enroll/$', views.add_student, name='add_student'),  # 第一步：报名信息录入
    url(r'^enroll/(\d+)/$', views.student_enroll, name='student_enroll'),  # 第二步：学生完善信息

    url(r'^audit_list/$', views.audit_list, name='audit_list'),  # 第三步：销售审核列表页
    url(r'^audit_list/(\d+)/$', views.audit, name='audit'),  # 第四步：销售审核学员

    url(r'^get_classes/(\d+)/$', views.get_classes, name='get_classes'), # 获取对应校区的所有班级

    url(r'^enroll/(\d+)/file_upload/$', views.enroll_file_upload, name='enroll_file_upload'),
    url(r'^enroll/file_delete/(\d+)/([\w|\.]+)/$', views.enroll_file_delete, name='enroll_file_delete'),
]
