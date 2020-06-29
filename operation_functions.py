def add(a, b):
    "Same as a + b."
    return a + b

def sub(a, b):
    "Same as a - b."
    return a - b

def mul(a, b):
    "Same as a * b."
    return a * b

def div(a, b):
    "Same as a // b + 'and' + a % b + 'remaining'."
    if a % b == 0:
        return str(a // b)
    else:
        return str(a // b) + " and " + str(a % b) + " remaining"

