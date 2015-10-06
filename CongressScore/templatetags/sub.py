from django import template

register = template.Library()

@register.filter(name="sub")
def sub(value, arg):
    return int(value - arg) 

@register.filter(name="mul")
def mul(value, arg):
    "Multiplies the arg and the value"
    return int(value * float(arg))

@register.filter(name="div")
def div(value, arg):
    "Divides the value by the arg"
    return int(value / arg)
