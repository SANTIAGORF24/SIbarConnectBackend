

def fullnamecreate (data):
    fullname = " ".join(filter(None, [
        getattr(data, "first_name_one", None),
        getattr(data, "first_name_two", None),
        getattr(data, "last_name_one", None),
        getattr(data, "last_name_two", None)
    ]))
    
    
    return fullname