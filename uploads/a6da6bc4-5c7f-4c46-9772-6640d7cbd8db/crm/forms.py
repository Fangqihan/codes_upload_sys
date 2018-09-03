from django.forms import ModelForm
from crm.models import CustomerInfo,StudentEnrollment


class CustomerInfoForm(ModelForm):

    def __new__(cls, *args, **kwargs):
        """方法2：在实例化类对象（model_form()）的时候给input框增加样式"""
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs.update({'class': 'form-control'})

            # 设定只读字段disabled属性
            if field_name in cls.Meta.readonly_fields:
                field_obj.widget.attrs.update({'disabled': True})

        return ModelForm.__new__(cls)

    class Meta:
        model = CustomerInfo
        fields = '__all__'
        exclude = ['consult_content', 'contact_type', 'consultant', 'status', 'source','consult_course']
        readonly_fields = []
        error_messages = {
            'name': {
                'required': "名字不能为空",
            },
        }


class StudentEnrollForm(ModelForm):
    """信息完善form"""

    class Meta:
        model = StudentEnrollment
        fields = '__all__'
        readonly_fields = ['customer', 'consultant', 'class_grade', 'contract_agreed', 'contract_signed_time']

    def __new__(cls, *args, **kwargs):
        """方法2：在实例化类对象（model_form()）的时候给input框增加样式"""
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs.update({'class': 'form-control'})

            # 设定只读字段disabled属性
            if field_name in cls.Meta.readonly_fields:
                field_obj.widget.attrs.update({'disabled': True})

        return ModelForm.__new__(cls)

