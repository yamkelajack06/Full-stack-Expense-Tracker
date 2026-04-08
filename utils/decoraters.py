import functools
import time
from datetime import datetime as dt


def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Function '{func.__name__}' was called")
        result = func(*args, **kwargs)
        return result
    return wrapper


def validate_input(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Validate positional args
        for i, arg in enumerate(args):
            if arg is None:
                print(f"Error: Argument {i + 1} cannot be None.")
                return None
            if isinstance(arg, str) and not arg.strip():
                print(f"Error: Argument {i + 1} cannot be an empty string.")
                return None
            if isinstance(arg, (int, float)) and arg <= 0:
                print(f"Error: Argument {i + 1} must be a positive number.")
                return None

        # Validate keyword args
        for key, value in kwargs.items():
            if value is None:
                print(f"Error: '{key}' cannot be None.")
                return None
            if isinstance(value, str) and not value.strip():
                print(f"Error: '{key}' cannot be an empty string.")
                return None
            if isinstance(value, (int, float)) and value <= 0:
                print(f"Error: '{key}' must be a positive number.")
                return None

        result = func(*args, **kwargs)
        return result
    return wrapper


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Function '{func.__name__}' took {end - start:.4f} seconds to run")
        return result
    return wrapper