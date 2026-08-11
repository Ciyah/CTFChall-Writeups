#!/usr/bin/env python3
import json
import socket
from z3 import BitVec, BitVecVal, If, Int, LShR, Or, Solver, SolverFor, UGE, UGT, ULT

HOST, PORT = "154.57.164.82", 30390


def request(sock, payload):
    sock.sendall(json.dumps(payload).encode() + b"\n")
    data = bytearray()
    while not data.endswith(b"\n"):
        chunk = sock.recv(65536)
        if not chunk:
            raise EOFError("server disconnected")
        data.extend(chunk)
    return json.loads(data)


def main():
    sample = json.load(open("sample.json"))
    recover(sample)


def parse_blocks(trace):
    start = max(i for i, op in enumerate(trace) if op == "v")
    ops = trace[start + 2:]  # skip div (v) and its binary-division call (y)
    blocks, block, i = [], [], 0
    while i < len(ops):
        if ops[i:i + 2] == ["s", "s"]:
            blocks.append(block); block = []; i += 2
        elif ops[i:i + 2] == ["h", "h"]:
            block.append(0); i += 2       # x was even
        elif ops[i:i + 3] == ["h", "a", "h"]:
            block.append(1); i += 3       # x was odd
        else:
            raise ValueError((i, ops[i:i + 10]))
    blocks.append(block)
    return blocks


def recover(sample):
    n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
    sig_s = int(sample["s"], 0)
    blocks = parse_blocks(sample["trace"])
    print("binary-GCD rounds:", len(blocks) - 1)
    product = recover_boolector(blocks, n, sig_s)
    if product is not None:
        print("denominator product:", hex(product))
        finish(sample, product, n)
        return
    product = recover_bv(blocks, n, sig_s)
    if product is not None:
        print("denominator product:", hex(product))
        finish(sample, product, n)
        return
    products = reverse_paths(blocks, n)
    print("path candidates:", len(products))
    if products:
        print("denominator product:", hex(products[0]))
        return

    denominator = Int("denominator")
    numerator = Int("numerator")
    quotient = Int("quotient")
    u, v = denominator, n
    x1, x2 = numerator, 0
    solver = SolverFor("QF_LIA")
    solver.set("threads", 8)
    # Product of two independently uniform 256-bit scalars; this overwhelmingly
    # lies in the top part of the 512-bit range and fixes the long initial path.
    solver.add(denominator >= 1 << 500, denominator < n * n)
    solver.add(numerator >= 0, numerator < n)
    solver.add(sig_s * denominator == quotient * n + numerator)
    serial = 0

    def fresh(prefix, expression):
        nonlocal serial
        serial += 1
        value = Int(f"{prefix}_{serial}")
        solver.add(value == expression)
        return value

    def exact_half(prefix, expression):
        nonlocal serial
        serial += 1
        value = Int(f"{prefix}_{serial}")
        solver.add(2 * value == expression)
        return value

    selected_u = True
    cumulative_initial_shifts = 0
    for round_no, parity_bits in enumerate(blocks):
        cumulative_initial_shifts += len(parity_bits)
        for parity in parity_bits:
            selected_x = x1 if selected_u is True else x2 if selected_u is False else If(selected_u, x1, x2)
            selected_val = u if selected_u is True else v if selected_u is False else If(selected_u, u, v)
            solver.add(selected_val % 2 == 0, selected_x % 2 == parity)
            half_val = exact_half("halfval", selected_val)
            new_x = exact_half("halfx", selected_x + parity * n)
            if selected_u is True:
                u, x1 = half_val, new_x
            elif selected_u is False:
                v, x2 = half_val, new_x
            else:
                u, v = fresh("u", If(selected_u, half_val, u)), fresh("v", If(selected_u, v, half_val))
                x1, x2 = fresh("x1", If(selected_u, new_x, x1)), fresh("x2", If(selected_u, x2, new_x))
        if round_no == len(blocks) - 1:
            break
        solver.add(u % 2 == 1, v % 2 == 1)
        forced_u = cumulative_initial_shifts <= 242
        take_u = True if forced_u else u >= v
        old_u, old_v, old_x1, old_x2 = u, v, x1, x2
        if take_u is True:
            solver.add(old_u >= old_v)
            u, v = fresh("u", old_u - old_v), old_v
            x1, x2 = fresh("x1", old_x1 - old_x2), old_x2
        else:
            u = fresh("u", If(take_u, old_u - old_v, old_u))
            v = fresh("v", If(take_u, old_v, old_v - old_u))
            x1 = fresh("x1", If(take_u, old_x1 - old_x2, old_x1))
            x2 = fresh("x2", If(take_u, old_x2, old_x2 - old_x1))
        selected_u = take_u
    solver.add(Or(u == 1, v == 1))
    print(solver.check())
    model = solver.model()
    product = model[denominator].as_long()
    print("denominator product:", hex(product))


def recover_boolector(blocks, n, sig_s):
    from pyboolector import Boolector, BtorOption, BtorSolverResult
    btor = Boolector()
    btor.Set_opt(BtorOption.BTOR_OPT_MODEL_GEN, 1)
    width = 600
    sort = btor.BitVecSort(width)
    const = lambda value: btor.Const(value, width)
    denominator = btor.Var(sort, "denominator")
    numerator = btor.Var(sort, "numerator")
    quotient = btor.Var(sort, "quotient")
    bn, one, zero = const(n), const(1), const(0)
    btor.Assert(btor.Ugte(denominator, const(1 << 508)))
    btor.Assert(btor.Ult(denominator, const(n * n)))
    use_coefficients = True
    btor.Assert(btor.Ult(numerator, bn))
    u, v, x1, x2 = denominator, bn, numerator, zero
    selected = True
    cumulative = 0
    shift_one = const(1)
    for round_no, parity_bits in enumerate(blocks):
        cumulative += len(parity_bits)
        for parity in parity_bits:
            val = u if selected is True else v if selected is False else btor.Cond(selected, u, v)
            x = x1 if selected is True else x2 if selected is False else btor.Cond(selected, x1, x2)
            btor.Assert((val & one) == zero)
            if use_coefficients:
                btor.Assert((x & one) == (one if parity else zero))
            hv = btor.Srl(val, shift_one)
            hx = btor.Sra(x + (bn if parity else zero), shift_one) if use_coefficients else x
            if selected is True:
                u, x1 = hv, hx
            elif selected is False:
                v, x2 = hv, hx
            else:
                u, v = btor.Cond(selected, hv, u), btor.Cond(selected, v, hv)
                x1, x2 = btor.Cond(selected, hx, x1), btor.Cond(selected, x2, hx)
        if round_no == len(blocks) - 1:
            break
        btor.Assert((u & one) == one)
        btor.Assert((v & one) == one)
        take_u = True if cumulative <= 248 else btor.Ugte(u, v)
        ou, ov, ox1, ox2 = u, v, x1, x2
        if take_u is True:
            btor.Assert(btor.Ugte(ou, ov))
            u, x1 = ou - ov, ox1 - ox2
        else:
            u, v = btor.Cond(take_u, ou - ov, ou), btor.Cond(take_u, ov, ov - ou)
            x1, x2 = btor.Cond(take_u, ox1 - ox2, ox1), btor.Cond(take_u, ox2, ox2 - ox1)
        selected = take_u
    # The routine returns x1 mod N when u == 1, otherwise x2 mod N.  Express
    # that terminal congruence with a bounded signed multiple of N, avoiding
    # the much larger initial s*denominator multiplication.
    q1p, q1n = btor.Var(sort, "q1p"), btor.Var(sort, "q1n")
    q2p, q2n = btor.Var(sort, "q2p"), btor.Var(sort, "q2n")
    qbound = const(1 << 300)
    for q in (q1p, q1n, q2p, q2n):
        btor.Assert(btor.Ult(q, qbound))
    bs = const(sig_s)
    x1_ok = (x1 == bs + q1p * bn) | (x1 == bs - q1n * bn)
    x2_ok = (x2 == bs + q2p * bn) | (x2 == bs - q2n * bn)
    btor.Assert(((u == one) & x1_ok) | ((v == one) & x2_ok))
    result = btor.Sat()
    print("boolector solve:", result)
    if result != BtorSolverResult.BTOR_RESULT_SAT:
        return None
    return int(denominator.assignment, 2)


def recover_bv(blocks, n, sig_s):
    width = 768
    bv_n = BitVecVal(n, width)
    denominator = BitVec("bv_denominator", width)
    numerator = BitVec("bv_numerator", width)
    quotient = BitVec("bv_quotient", width)
    solver = Solver()
    solver.set("threads", 8)
    serial = 0

    def fresh(prefix, expression):
        nonlocal serial
        serial += 1
        value = BitVec(f"{prefix}_{serial}", width)
        solver.add(value == expression)
        return value
    solver.add(UGE(denominator, BitVecVal(1 << 508, width)))
    solver.add(ULT(denominator, BitVecVal(n * n, width)))
    solver.add(ULT(numerator, bv_n))
    solver.add(BitVecVal(sig_s, width) * denominator == quotient * bv_n + numerator)

    u, v, x1, x2 = denominator, bv_n, numerator, BitVecVal(0, width)
    selected_u = True
    cumulative_shifts = 0
    for round_no, parity_bits in enumerate(blocks):
        cumulative_shifts += len(parity_bits)
        for parity in parity_bits:
            selected_val = u if selected_u is True else v if selected_u is False else If(selected_u, u, v)
            selected_x = x1 if selected_u is True else x2 if selected_u is False else If(selected_u, x1, x2)
            solver.add((selected_val & 1) == 0, (selected_x & 1) == parity)
            half_val = LShR(selected_val, 1)
            half_x = (selected_x + (bv_n if parity else 0)) >> 1
            if selected_u is True:
                u, x1 = fresh("u", half_val), fresh("x1", half_x)
            elif selected_u is False:
                v, x2 = fresh("v", half_val), fresh("x2", half_x)
            else:
                u, v = fresh("u", If(selected_u, half_val, u)), fresh("v", If(selected_u, v, half_val))
                x1, x2 = fresh("x1", If(selected_u, half_x, x1)), fresh("x2", If(selected_u, x2, half_x))
        if round_no == len(blocks) - 1:
            break
        solver.add((u & 1) == 1, (v & 1) == 1)
        take_u = True if cumulative_shifts <= 248 else UGE(u, v)
        old_u, old_v, old_x1, old_x2 = u, v, x1, x2
        if take_u is True:
            solver.add(UGE(old_u, old_v))
            u, v = fresh("u", old_u - old_v), old_v
            x1, x2 = fresh("x1", old_x1 - old_x2), old_x2
        else:
            u, v = fresh("u", If(take_u, old_u - old_v, old_u)), fresh("v", If(take_u, old_v, old_v - old_u))
            x1, x2 = fresh("x1", If(take_u, old_x1 - old_x2, old_x1)), fresh("x2", If(take_u, old_x2, old_x2 - old_x1))
        selected_u = take_u
    solver.add(Or(u == 1, v == 1))
    print("bit-vector solve:", solver.check())
    if str(solver.check()) != "sat":
        return None
    return solver.model()[denominator].as_long()


def finish(sample, product, n):
    import sympy
    factors = sympy.factorint(product)
    print("factors:", factors)
    h, r, s = (int(sample[k], 0) for k in ("hash", "r", "s"))
    from importlib import import_module
    import sys
    sys.path.insert(0, "Surprise Factor/crypto_surprise_factor")
    ec = import_module("ec")
    public = (int(sample["public_key"]["x"], 0), int(sample["public_key"]["y"], 0))
    for factor in factors:
        for k in (factor, product // factor):
            if not 1 <= k < n:
                continue
            if ec.to_affine(ec.scalar_mul(k, ec.G))[0] % n != r:
                continue
            private = ((s * k - h) * pow(r, -1, n)) % n
            if ec.to_affine(ec.scalar_mul(private, ec.G)) == public:
                print("private key:", hex(private))
                submit(private)
                return
    raise ValueError("no factor produced the signature nonce")


def submit(private):
    with socket.create_connection((HOST, PORT)) as sock:
        print(request(sock, {"action": "submit", "d": hex(private)}))


def reverse_paths(blocks, n):
    """Invert the binary-GCD value path; affine pairs represent a*w+b."""
    answers = []
    nodes = 0

    def rec(i, u, v):
        nonlocal nodes
        nodes += 1
        # Backward steps only increase coordinates.  Initial v is exactly N.
        if v[0] + v[1] > n:
            return
        if i < 0:
            a, b = v
            if a == 0:
                return
            rem = n - b
            if rem <= 0 or rem % a:
                return
            w = rem // a
            if w <= 0 or w % 2 == 0:
                return
            u0 = u[0] * w + u[1]
            answers.append(u0 << len(blocks[0]))
            return
        shift = len(blocks[i + 1])
        scale = 1 << shift
        choices = (True,) if sum(map(len, blocks[:i + 1])) <= 242 else (True, False)
        for took_u in choices:
            if took_u:
                # U_i = 2^t U_{i+1} + V_{i+1}
                rec(i - 1, (scale * u[0] + v[0], scale * u[1] + v[1]), v)
            else:
                rec(i - 1, u, (scale * v[0] + u[0], scale * v[1] + u[1]))

    # At loop exit either coordinate is one; the other is an unknown odd w.
    rec(len(blocks) - 2, (0, 1), (1, 0))
    rec(len(blocks) - 2, (1, 0), (0, 1))
    print("reverse nodes:", nodes)
    return answers


if __name__ == "__main__":
    main()
