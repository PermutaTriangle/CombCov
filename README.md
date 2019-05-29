# CombCov

[![Build Status](https://img.shields.io/travis/PermutaTriangle/CombCov.svg?label=Linux%20CI&logo=travis&logoColor=white)](https://travis-ci.org/PermutaTriangle/CombCov)
[![Coverage Status](https://img.shields.io/coveralls/github/PermutaTriangle/CombCov.svg)](https://coveralls.io/github/PermutaTriangle/CombCov)
[![Licence](https://img.shields.io/github/license/PermutaTriangle/CombCov.svg)](https://raw.githubusercontent.com/PermutaTriangle/CombCov/master/LICENSE)

[![PyPi Version](https://img.shields.io/pypi/v/CombCov.svg)](https://pypi.org/project/CombCov/)
[![PyPi Downloads](https://img.shields.io/pypi/dm/CombCov.svg)](https://pypi.org/project/CombCov/)
[![Python Implementation](https://img.shields.io/pypi/implementation/CombCov.svg)](https://pypi.org/project/CombCov/)
[![Python Versions](https://img.shields.io/pypi/pyversions/CombCov.svg)](https://pypi.org/project/CombCov/)

A generalization of the permutation-specific algorithm [Struct](https://github.com/PermutaTriangle/PermStruct) -- 
extended for other types of combinatorial objects.


## Demo

Take a look at `demo/string_set.py` as an example on how to use `CombCov` with
your own combinatorial object. It finds a _String Set_ cover for the set of
string over the alphabet `{a,b}` that avoids the substring `aa` (meaning no
string in the set contains `aa` as a substring).

```bash
python -m demo.string_set
```

It prints out the following:

```text
Trying to find a cover for ''*Av(aa) over ∑={a,b} using elements up to size 7.
(Enumeration: [1, 2, 3, 5, 8, 13, 21, 34])
Solution nr. 1:
 - ''*Av(a,b) over ∑={a,b}
 - 'a'*Av(a,b) over ∑={a,b}
 - 'b'*Av(aa) over ∑={a,b}
 - 'ab'*Av(aa) over ∑={a,b}
```


## Development

Run unittests (with coverage for the `demo` module as well):

```bash
python setup.py test --addopts --cov=demo
```
