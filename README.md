# CombCov

[![Build Status](https://img.shields.io/travis/PermutaTriangle/CombCov.svg?label=Linux%20CI&logo=travis&logoColor=white)](https://travis-ci.org/PermutaTriangle/CombCov)
[![Coverage Status](https://img.shields.io/coveralls/github/PermutaTriangle/CombCov.svg)](https://coveralls.io/github/PermutaTriangle/CombCov)
[![Requirements Status](https://img.shields.io/requires/github/PermutaTriangle/CombCov.svg)](https://requires.io/github/PermutaTriangle/CombCov/requirements)
[![Licence](https://img.shields.io/github/license/PermutaTriangle/CombCov.svg)](https://raw.githubusercontent.com/PermutaTriangle/CombCov/master/LICENSE)

[![PyPi Version](https://img.shields.io/pypi/v/CombCov.svg)](https://pypi.org/project/CombCov/)
[![PyPi Downloads](https://img.shields.io/pypi/dm/CombCov.svg)](https://pypi.org/project/CombCov/)
[![Python Implementation](https://img.shields.io/pypi/implementation/CombCov.svg)](https://pypi.org/project/CombCov/)
[![Python Versions](https://img.shields.io/pypi/pyversions/CombCov.svg)](https://pypi.org/project/CombCov/)

A generalization of the permutation-specific algorithm [Struct](https://github.com/PermutaTriangle/PermStruct) -- 
extended for other types of combinatorial objects.


## Demos

Take a look at the `demo/` folder in this repo to see examples on how to use
`CombCov` with your own combinatorial object. On example finds a _String Set_
cover for the set of string over the alphabet `{a,b}` that avoids the substring
`aa` (meaning no string in the set contains `aa` as a substring).

```bash
$ python -m demo.string_set
[INFO] (CombCov) Enumerating all elements of size up to 7...
[INFO] (CombCov) ...DONE enumerating elements! (Running time: 0.00 sec)
[INFO] (CombCov) Total of 87 elements.
[INFO] (CombCov) Enumeration: [1, 2, 3, 5, 8, 13, 21, 34]
[INFO] (CombCov) Creating binary strings from rules...
[INFO] (CombCov) Bitstring to cover: 154742504910672534362390527 
[INFO] (StringSet) Generated 16 subrules
[INFO] (CombCov) ...DONE creating binary strings! (Running time: 0.00 sec)
[INFO] (CombCov) Total of 14 valid rules with 14 distinct binary strings.
[INFO] (CombCov) Searching for a cover for ''*Av(aa) over ∑={a,b}...
[INFO] (CombCov) Gurobi installed on system and set as solver
[INFO] (CombCov) ...DONE searching for a cover! (Running time: 0.02 sec)
Solution found!
 - Rule #1: ''*Av(a,b) over ∑={a,b} with bitstring 1
 - Rule #2: 'a'*Av(a,b) over ∑={a,b} with bitstring 2
 - Rule #3: 'b'*Av(aa) over ∑={a,b} with bitstring 154742431132702343545997108
 - Rule #4: 'ab'*Av(aa) over ∑={a,b} with bitstring 73777970190816393416
```


## Development

Run unittests (with coverage for the `demo` module as well):

```bash
./setup.py test --addopts --cov=demo
```
