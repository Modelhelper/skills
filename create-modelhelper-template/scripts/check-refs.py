#!/usr/bin/env python3
"""Report {{ template "x" }} references that resolve to nothing.
Run from the templates repo root: python3 check-refs.py [subdir, default code]
Names mirror the CLI loader: path relative to the root, '/' -> '-', extension dropped, lowercase.
Code templates are rooted at code/, db templates at db/<mssql|postgres>/."""
import os, re, sys

def names(root):
    d = {}
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(('.yaml', '.yml')):
                p = os.path.join(dp, f)
                n = os.path.relpath(p, root).rsplit('.', 1)[0].replace('/', '-').replace(' ', '-').lower()
                d[n] = p
    return d

code = names('code')
db = {k: names('db/' + k) for k in os.listdir('db')}
ref = re.compile(r'template "([^"]+)"')
bad = 0
for dp, _, fs in os.walk(sys.argv[1] if len(sys.argv) > 1 else 'code'):
    for f in sorted(fs):
        p = os.path.join(dp, f)
        for i, l in enumerate(open(p, errors='ignore'), 1):
            for r in ref.findall(l):
                miss = [k for k in db if r not in db[k]]
                if r not in code and miss:
                    bad += 1
                    print(f"{p}:{i}: {r}  missing-in: {', '.join(miss)}")
sys.exit(1 if bad else 0)
