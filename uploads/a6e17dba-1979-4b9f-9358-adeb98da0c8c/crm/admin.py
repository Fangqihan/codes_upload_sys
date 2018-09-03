from django.contrib import admin
from crm import models


class CustomerInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_type', 'consultant', 'status', 'source', 'date','contact_info']
    list_filter = ['contact_type', 'consult_course', 'consultant', 'status', 'source']
    search_fields = ['name', 'consultant__username']
    filter_horizontal = ['consult_course']
    actions = ['change_status']

    def change_status(self,request,query_set):
        """
        :param request: 请求
        :param query_set: 选中的所有对象
        :return: 可以直接对选中的对象进行操作
        """
        query_set.update(status=0)  # 更新对象的属性

admin.site.register(models.CustomerInfo, CustomerInfoAdmin)

admin.site.register(models.UserProfile)
admin.site.register(models.Role)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Course)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord)
# admin.site.register(models.Student)
admin.site.register(models.StudyRecord)
admin.site.register(models.Branch)
admin.site.register(models.Menu)
