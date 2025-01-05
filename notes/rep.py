def repeat_decorator(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat_decorator(3)
@repeat_decorator(5)
def say_hi(name):
    print(f"Hi, {name}!")

say_hi("Alice")

