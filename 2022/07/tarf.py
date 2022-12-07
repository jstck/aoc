#!/usr/bin/env python3

import tarfile
import io
import sys

cwd = []

with tarfile.TarFile("elfsys.tar", mode="w") as tarf:
    for line in sys.stdin.readlines():
        line = line.strip()
        if len(line) == 0: continue
        if line[0] == "$":
            cmd = line.split(" ")
            if cmd[1] == "cd":
                p = cmd[2]
                if p == "..": cwd.pop()
                elif p == "/": cwd = []
                else: cwd.append(p)
            elif cmd[1] == "ls":
                pass
            else:
                print(f"UNKNOWN COMMAND: '{line}'")
                assert(false)
        else:
            f = [x.strip() for x in line.split(" ")]
            t = f[0]
            name = f[1]
            if t != "dir":
                if len(cwd) == 0:
                    path = name
                else:
                    path = "/".join(cwd + [name])

                size = int(t)
                print(f"Adding", path, "size", size)

                data = io.BytesIO(b"\0" * size)
                ti = tarfile.TarInfo(path)
                ti.size = size
                tarf.addfile(ti, fileobj=data)
