import os
import runpy
import subprocess

m = runpy.run_path("challenge.py", run_name="challmodule")
source = open("solve.c", "rb").read() + b"\n"
for trial in range(100):
    start, stride = m["random_orbit"](len(source))
    seed = m["random_u64"]()
    program = m["make_program"]()
    pad = os.urandom(len(source))
    header = b"".join(x.to_bytes(8, "little") for x in (start, stride, seed, len(program)))
    encoded_program = b"".join(bytes([op]) + arg.to_bytes(8, "little") for op, arg in program)
    blob = header + encoded_program + pad
    actual = subprocess.check_output(["./solve"], input=blob, timeout=1)
    expected = m["orbit_vm"](source, pad, start, stride, seed, program)
    assert int(actual) == expected, (trial, actual, expected)
print("passed", trial + 1, "random trials")
