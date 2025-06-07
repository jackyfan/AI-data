from functools import wraps

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