print('执行kingadmin.py文件...')

from king_admin.sites import site
from crm import models
from king_admin.base_king_admin import BaseKingAdmin


class CustomerInfoAdmin(BaseKingAdmin):
    def __init__(self):
        self.actions.extend(self.default_actions)

    # 显示的表字段
    list_display = ['name','contact_type', 'status', 'source','consultant','date']
    # 过滤字段
    list_filter = ['contact_type','consultant','status','source','date']
    # 搜索字段
    search_fields = ['name','consultant__username']
    # readonly_fields = ['name']
    filter_horizontal = ['consult_course']


class UserprofileInfoAdmin(BaseKingAdmin):
    list_display = ['username','role']


# Registers the given model(s) with the given admin class.
# 根据CustomerInfoAdmin自定义的字段来注册table
site.register(models.CustomerInfo, CustomerInfoAdmin)
site.register(models.Role)
site.register(models.UserProfile)
site.register(models.Course)
site.register(models.CourseRecord)
site.register(models.Student)
site.register(models.ClassList)
site.register(models.StudyRecord)
site.register(models.Branch)
site.register(models.StudentEnrollment)
site.register(models.ContractTemplate)
site.register(models.Menu)
site.register(models.CustomerFollowUp)
print('注册结束')



