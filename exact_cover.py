import os
import shutil
import tempfile
from subprocess import Popen, DEVNULL


def exact_cover(bitstrings, cover_string_length):
    try:
        for res in exact_cover_gurobi(bitstrings, cover_string_length):
            yield res
    except Exception as exc:
        raise RuntimeError(
            "Gurobi may not be installed and there are no alternative solution method at the moment.") from exc


def _call_Popen(inp, outp):
    return Popen('gurobi_cl ResultFile=%s %s' % (outp, inp), shell=True, stdout=DEVNULL)

def exact_cover_gurobi(bitstrings, cover_string_length):
    tdir = None
    used = set()
    anything = False
    try:
        tdir = tempfile.mkdtemp(prefix='combcov_tmp')
        inp = os.path.join(tdir, 'inp.lp')
        outp = os.path.join(tdir, 'out.sol')

        with open(inp, 'w') as lp:
            lp.write('Minimize %s\n' % ' + '.join('x%d' % i for i in range(len(bitstrings))))
            lp.write('Subject To\n')

            for i in range(cover_string_length):
                here = []
                for j in range(len(bitstrings)):
                    if (bitstrings[j] & (1 << i)) != 0:
                        here.append(j)
                lp.write('    %s = 1\n' % ' + '.join('x%d' % x for x in here))

            lp.write('Binary\n')
            lp.write('    %s\n' % ' '.join('x%d' % i for i in range(len(bitstrings))))
            lp.write('End\n')

        p = _call_Popen(inp, outp)
        assert p.wait() == 0

        with open(outp, 'r') as sol:
            while True:
                line = sol.readline()
                if not line:
                    break
                if line.startswith('#') or not line.strip():
                    continue
                anything = True

                # x2 0
                # x3 1
                k, v = line.strip().split()
                if int(v) == 1:
                    used.add(int(k[1:]))
    finally:
        if tdir is not None:
            shutil.rmtree(tdir)

    if anything:
        yield sorted(used)
