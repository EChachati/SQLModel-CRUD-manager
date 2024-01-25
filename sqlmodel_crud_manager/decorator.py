from fastapi import HTTPException


def raise_as_http_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if e.__class__.__name__ == "HTTPException":
                raise e

            else:
                raise HTTPException(status_code=500, detail=str(e)) from e

    return wrapper


def raise_404_if_none(func, detail="Not Found"):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise HTTPException(status_code=404, detail=detail)
        return result

    return wrapper


def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:  # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate
