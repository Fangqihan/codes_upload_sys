from django.template import Library

register = Library()

@register.simple_tag
def replace_str(s):
    return str(s).replace('.','_')


@register.simple_tag
def is_active(menu_path,path):
    if menu_path in path:
        return True
    return False



