from django import template
import os

register = template.Library()

@register.simple_tag
def set_url(request, id):
 return request + '/search_qr_set/' + str(id)

@register.simple_tag
def key_url(request, id):
 return request + '/search_qr_key/' + str(id)

@register.simple_tag
def backup_url(request, id):
 return request + '/search_qr_backup/' + str(id)

@register.simple_tag
def guide_url(request, id):
 return request + '/search_qr_guide/' + str(id)

@register.simple_tag
def survey_url(request, id):
 return request + '/search_qr_survey/' + str(id)

@register.filter
def getfilename(value):
    return os.path.basename(value.file.name)

