# CombCov

[![Build Status](https://travis-ci.org/PermutaTriangle/CombCov.svg?branch=master)](https://travis-ci.org/PermutaTriangle/CombCov)


A generalization of the permutation-specific algorithm [Struct](https://github.com/PermutaTriangle/PermStruct) -- 
extended for other types of combinatorial objects.

## Example usage

Below is an example where CombCov finds a _String Set_ cover for the set of string over the alphabet `{a,b}` that
avoids the substring `aa` (meaning no string in the set contains `aa` as a substring).

```python
from string_set import StringSet
from comb_cov import CombCov

alphabet = ['a', 'b']
avoid = ['aa']
string_set = StringSet(alphabet, avoid)

max_elmnt_size = 7
comb_cov = CombCov(string_set, max_elmnt_size)
```

It prints out the following:

```text
Trying to find a cover for 'Av(aa) over ∑={a,b}' up to size 7 using 27 self-generated rules.
(Enumeration: [1, 2, 3, 5, 8, 13, 21, 34])
SUCCESS! Found 1 solution(s).
Solution nr. 1:
 - ''*Av(b,a) over ∑={a,b}
 - 'a'*Av(b,a) over ∑={a,b}
 - 'b'*Av(aa) over ∑={a,b}
 - 'ab'*Av(aa) over ∑={a,b}
```
