from django import template  
from cryptography.fernet import Fernet
register = template.Library()  

@register.filter('decrypt')
def decrypt(password, key):
    fernet = Fernet(key)
    return fernet.decrypt(password).decode()