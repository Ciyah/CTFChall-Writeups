import secrets
from bignum import add, double, inv, mod, mul, octuple, square, sub, triple
from trace import traceable

P = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
A = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
GX = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
GY = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
H = 1

INFINITY = (1, 1, 0)
G_AFFINE = (GX, GY)
G = (GX, GY, 1)

@traceable("is_infinity", "I")
def is_infinity(point):
    return point[2] == 0

@traceable("to_jacobian", "J")
def to_jacobian(point):
    if point is None:
        return INFINITY
    return (mod(point[0], P), mod(point[1], P), 1)

@traceable("to_affine", "F")
def to_affine(point):
    if is_infinity(point):
        return None

    x, y, z = point
    z_inv = inv(mod(z, P), P)
    z_inv_sq = mod(square(z_inv), P)
    z_inv_cu = mod(mul(z_inv_sq, z_inv), P)
    affine_x = mod(mul(x, z_inv_sq), P)
    affine_y = mod(mul(y, z_inv_cu), P)
    return (affine_x, affine_y)

@traceable("randomize_coordinates", "R")
def randomize_coordinates(point):
    if is_infinity(point):
        return None

    mask = secrets.randbelow(P)
    mask2 = mul(mask, mask)
    mask3 = mul(mask2, mask)

    x, y, z = point
    X = mod(mul(x, mask2), P)
    Y = mod(mul(y, mask3), P)
    Z = mod(mul(z, mask), P)

    return (X, Y, Z)

@traceable("is_on_curve_affine", "C")
def is_on_curve_affine(point):
    if point is None:
        return True

    x, y = point
    left = mod(square(y), P)
    right = mod(add(add(mul(x, square(x)), mul(A, x)), B), P)
    return left == right

def _select_coordinate(on_one, on_zero, bit):
    mask = -int(bit == "1")
    return (on_one & mask) | (on_zero & ~mask)

def _select_point(on_one, on_zero, bit):
    return (
        _select_coordinate(on_one[0], on_zero[0], bit),
        _select_coordinate(on_one[1], on_zero[1], bit),
        _select_coordinate(on_one[2], on_zero[2], bit),
    )

@traceable("point_double", "D")
def point_double(point):
    if is_infinity(point):
        return INFINITY

    x1, y1, z1 = point
    if mod(y1, P) == 0:
        return INFINITY

    delta = mod(square(z1), P)
    gamma = mod(square(y1), P)
    beta = mod(mul(x1, gamma), P)

    x1_minus_delta = mod(sub(x1, delta), P)
    x1_plus_delta = mod(add(x1, delta), P)
    alpha = mod(triple(mul(x1_minus_delta, x1_plus_delta)), P)

    x3 = mod(sub(square(alpha), octuple(beta)), P)

    yz_sum = add(y1, z1)
    z3 = mod(sub(sub(square(yz_sum), gamma), delta), P)

    gamma_sq = mod(square(gamma), P)
    four_beta = double(double(beta))
    y3 = mod(sub(mul(alpha, mod(sub(four_beta, x3), P)), octuple(gamma_sq)), P)
    return (x3, y3, z3)

@traceable("point_add", "A")
def point_add(point_p, point_q):
    if is_infinity(point_p):
        return point_q
    if is_infinity(point_q):
        return point_p

    x1, y1, z1 = point_p
    x2, y2, z2 = point_q

    # Jacobian addition intermediates: U1/U2 are normalized X coordinates,
    # S1/S2 are normalized Y coordinates.
    z1z1 = mod(square(z1), P)
    z2z2 = mod(square(z2), P)
    u1 = mod(mul(x1, z2z2), P)
    u2 = mod(mul(x2, z1z1), P)
    s1 = mod(mul(y1, mul(z2, z2z2)), P)
    s2 = mod(mul(y2, mul(z1, z1z1)), P)

    if u1 == u2:
        if s1 != s2:
            return INFINITY
        return point_double(point_p)

    # H = U2 - U1, r = 2 * (S2 - S1), and the derived products used below.
    h = mod(sub(u2, u1), P)
    doubled_h = mod(double(h), P)
    i = mod(square(doubled_h), P)
    j = mod(mul(h, i), P)
    r = mod(double(sub(s2, s1)), P)
    v = mod(mul(u1, i), P)

    # X3 = r^2 - J - 2 * V.
    x3 = mod(sub(sub(square(r), j), double(v)), P)

    # Y3 = r * (V - X3) - 2 * S1 * J.
    y3 = mod(sub(mul(r, mod(sub(v, x3), P)), double(mul(s1, j))), P)

    # Z3 = ((Z1 + Z2)^2 - Z1^2 - Z2^2) * H.
    z1_plus_z2 = add(z1, z2)
    z1_plus_z2_sq = mod(square(z1_plus_z2), P)
    z3 = mod(mul(mod(sub(sub(z1_plus_z2_sq, z1z1), z2z2), P), h), P)
    return (x3, y3, z3)


@traceable("scalar_mul", "M")
def scalar_mul(k, point):
    if k == 0 or is_infinity(point):
        return INFINITY

    # Left-to-right binary double-and-add with constant-time point selection.
    result = point
    for bit in bin(k)[3:]:
        result = point_double(result)
        added  = point_add(result, point)
        result = _select_point(added, result, bit)
    return result
