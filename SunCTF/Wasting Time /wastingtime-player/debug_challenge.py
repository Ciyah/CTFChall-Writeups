import runpy
import subprocess
import sys

m = runpy.run_path("challenge.py", run_name="challmodule")
original_check_output = subprocess.check_output
original_vm = m["orbit_vm"]


def check_output(*args, **kwargs):
    result = original_check_output(*args, **kwargs)
    print("CHILD", len(kwargs["input"]), result, file=sys.stderr)
    return result


def orbit_vm(*args):
    result = original_vm(*args)
    print("VERIFY", len(args[0]), result, repr(args[0][-10:]), file=sys.stderr)
    return result


subprocess.check_output = check_output
m["main"].__globals__["orbit_vm"] = orbit_vm
m["main"]()
