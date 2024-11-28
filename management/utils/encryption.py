from django.conf import settings
import hashlib

def md5(data_str):
    # Django automatically generated SECRET_KEY acts as salt in this case
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_str.encode('utf-8'))
    return obj.hexdigest()
    