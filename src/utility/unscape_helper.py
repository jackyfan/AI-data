from functools import wraps
import re


def access_control(permission_required,get_permission_func):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user_permission = get_permission_func()
            if permission_required in current_user_permission:
                return func(*args, **kwargs)
            else:
                raise PermissionError(f'Access denied.Required permission:{permission_required}')
        return wrapper
    return decorator

def contains_escaped_unicode(s):
    """
    匹配\u后面跟着4个十六进制数字的模式
    """
    pattern = re.compile(r'\\u[0-9a-fA-F]{4}')
    match = pattern.search(s)
    return match is not None
def unescape_unicode(s):
    if contains_escaped_unicode(s):
        try:
            new_text =s.replace('\\\\u', '\\u')
            return replace_escaped_unicode(new_text)
        except(UnicodeDecodeError,UnicodeEncodeError):
            return s
    return s
def replace_escaped_unicode(s):
    def replace_match(match):
        return match.group(0).encode().decode('unicode_escape')
    pattern = re.compile(r'\\u[0-9a-fA-F]{4}')
    return pattern.sub(replace_match, s)