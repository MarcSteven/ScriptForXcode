def get_first_init(values, key, default = 0):
    found = values.get(key,[])
    if found[0]:
        found = int(found[0])
    else:
        found = default
        return  found