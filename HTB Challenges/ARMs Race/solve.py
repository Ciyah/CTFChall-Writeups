#!/usr/bin/env python3
import re
import socket
import sys

sys.path.append('/usr/lib/python3/dist-packages')
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

HOST, PORT = '154.57.164.83', 31917

def recv_until(sock, marker):
    data = b''
    while marker not in data:
        chunk = sock.recv(65536)
        if not chunk:
            break
        data += chunk
    return data

MASK = 0xffffffff

def emulate(blob):
    regs = {'r0': 0, 'r1': 0, 'r2': 0}
    carry = 0  # The service's fresh CPU context starts with CPSR flags clear.
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for ins in md.disasm(blob, 0):
        op = ins.mnemonic
        args = [x.strip() for x in ins.op_str.split(',')]
        if op in ('mov', 'movw'):
            regs[args[0]] = int(args[1][1:], 0)
        elif op == 'movt':
            regs[args[0]] = (regs[args[0]] & 0xffff) | (int(args[1][1:], 0) << 16)
        elif op in ('add', 'adc', 'sub', 'sbc', 'rsb', 'eor', 'orr', 'and', 'bic', 'mul'):
            dst, left, right = args
            a = regs[left]
            b = int(right[1:], 0) if right.startswith('#') else regs[right]
            if op == 'add': v = a + b
            elif op == 'adc': v = a + b + carry
            elif op == 'sub': v = a - b
            elif op == 'sbc': v = a - b - (1 - carry)
            elif op == 'rsb': v = b - a
            elif op == 'eor': v = a ^ b
            elif op == 'orr': v = a | b
            elif op == 'and': v = a & b
            elif op == 'bic': v = a & ~b
            elif op == 'mul': v = a * b
            regs[dst] = v & MASK
        else:
            raise RuntimeError(f'unsupported instruction: {op} {ins.op_str}')
    return regs['r0']

def main():
    s = socket.create_connection((HOST, PORT))
    transcript = b''
    for expected in range(1, 51):
        data = recv_until(s, b'Register r0:')
        transcript += data
        matches = re.findall(rb'Level (\d+)/50: ([0-9a-f]+)', data)
        if not matches:
            print(data.decode(errors='replace'))
            raise RuntimeError(f'no level payload at round {expected}')
        level, raw = matches[-1]
        answer = emulate(bytes.fromhex(raw.decode()))
        print(f'level {int(level):2}: {answer} (0x{answer:08x})', flush=True)
        s.sendall(f'{answer}\n'.encode())
    tail = b''
    while True:
        chunk = s.recv(65536)
        if not chunk: break
        tail += chunk
    print(tail.decode(errors='replace'))

if __name__ == '__main__':
    main()
