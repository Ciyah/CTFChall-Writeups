from trace import traceable

P256_PRIME = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
P256_MASK = (1 << 256) - 1

@traceable("add", "a")
def add(a, b):
    return a + b

@traceable("sub", "s")
def sub(a, b):
    return a - b

@traceable("neg", "n")
def neg(a):
    return -a

@traceable("mul", "m")
def mul(a, b):
    return a * b

@traceable("square", "q")
def square(value):
    return mul(value, value)

@traceable("double", "b")
def double(value):
    return add(value, value)

@traceable("triple", "t")
def triple(value):
    return add(double(value), value)

@traceable("octuple", "o")
def octuple(value):
    return double(double(double(value)))

@traceable("half", "h")
def half(value):
    return value // 2

@traceable("mod", "r")
def mod(value, modulus):
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    if modulus == P256_PRIME:
        return _p256_quasi_reduce(value)
    return value % modulus

@traceable("p256_quasi_reduce", "p")
def _p256_quasi_reduce(value):
    if value < 0:
        reduced = _p256_quasi_reduce(sub(0, value))
        return 0 if reduced == 0 else sub(P256_PRIME, reduced)

    while value.bit_length() > 256:
        high = value >> 256
        low = value & P256_MASK
        value = add(low, high)
        value = add(value, high << 224)
        value = sub(value, high << 192)
        value = sub(value, high << 96)

    while value >= P256_PRIME:
        value = sub(value, P256_PRIME)
    return value

@traceable("binary_division_odd_modulus", "y")
def _binary_division_odd_modulus(a, b, modulus):
    u = b
    v = modulus
    x1 = a
    x2 = 0

    while u != 1 and v != 1:
        while (u & 1) == 0:
            u = half(u)
            if (x1 & 1) == 0:
                x1 = half(x1)
            else:
                x1 = half(add(x1, modulus))

        while (v & 1) == 0:
            v = half(v)
            if (x2 & 1) == 0:
                x2 = half(x2)
            else:
                x2 = half(add(x2, modulus))

        if u >= v:
            u = sub(u, v)
            x1 = sub(x1, x2)
        else:
            v = sub(v, u)
            x2 = sub(x2, x1)

    if u == 1:
        return mod(x1, modulus)
    return mod(x2, modulus)

@traceable("inv", "i")
def inv(a, modulus):
    a = mod(a, modulus)
    return _binary_division_odd_modulus(1, a, modulus)

@traceable("div", "v")
def div(a, b, modulus):
    a = mod(a, modulus)
    return _binary_division_odd_modulus(a, b, modulus)
