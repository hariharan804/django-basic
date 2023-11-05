from django import template

register = template.Library()


@register.filter(name='get_attribute_with_underscore')
def get_attribute_with_underscore(value, attribute_name):
    # Your filter logic here
    return value.get(attribute_name, None)

