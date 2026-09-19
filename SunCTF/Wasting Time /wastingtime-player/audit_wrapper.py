import functools
import dis
import random
import re
import runpy
import sys
import time


def wrap(mod, name):
    original = getattr(mod, name)

    @functools.wraps(original)
    def logged(*args, **kwargs):
        result = original(*args, **kwargs)
        print(f"CALL {mod.__name__}.{name} args={args!r} kwargs={kwargs!r} -> {result!r}", file=sys.stderr)
        return result

    setattr(mod, name, logged)


for module, names in (
    (re, ("search", "match", "fullmatch", "findall", "finditer", "sub")),
    (random, ("random", "randint", "randrange", "choice", "choices", "getrandbits")),
    (time, ("time", "monotonic", "perf_counter", "sleep")),
):
    for function in names:
        wrap(module, function)


def hook(event, args):
    if event.startswith("subprocess") or (
        event == "open"
        and isinstance(args[0], str)
        and not args[0].endswith((".pyc", "challenge.py"))
    ):
        print("AUDIT", event, repr(args), file=sys.stderr)


sys.addaudithook(hook)


seen = set()
def profile(frame, event, arg):
    code = frame.f_code
    if event == "call" and code not in seen and "challenge" in code.co_filename:
        seen.add(code)
        print(
            f"FRAME name={code.co_name!r} file={code.co_filename!r} "
            f"names={code.co_names!r} vars={code.co_varnames!r} consts={code.co_consts!r}",
            file=sys.stderr,
        )
        if code.co_name in {"main", "make_program", "orbit_vm"}:
            dis.dis(code, file=sys.stderr)
    if event == "return" and code.co_name in {"random_orbit", "make_program", "orbit_vm"}:
        print(f"RETURN {code.co_name} locals={frame.f_locals!r} -> {arg!r}", file=sys.stderr)


sys.setprofile(profile)
module = runpy.run_path("challenge.py", run_name="challmodule")
print("GLOBALS", sorted(module), file=sys.stderr)
module["main"]()
