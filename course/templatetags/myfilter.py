
from django import template


register = template.Library()

@register.filter(name='times') 
def times(number):
    return range(number)


@register.filter(name='totle') 
def totl(t=None):
    return t;