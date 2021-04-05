from django.template.defaulttags import register
from datetime import date
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@property
def is_past(self):
    print(self.date, date.today())
    return date.today() > self.date