2019-04-11
==========

- [x] Decide next meeting time (because of Easter and Bjarni's 3-week course in May).
- [x] What licence is appropriate for the GitHub repo?
- [x] CombCov comes up with rules such as 'a'*Av(b,ab) and 'b'*Av(b,bb). How do we filter them out?
- [x] Discuss how we would like other people such as Rögnvaldur Möller use and interact with this library.
      Aspects ranging from practical stuff (like installation) to programming paradigms (such as class interfaces).
- [ ] (From previously) Discuss deploying a new version of Permuta to Pypi.

### Summary

First discussed the nonsense rules that CombCov currently comes up with and how to avoid that by doing some kind of 
`init` for the avoiding set of strings: Sort them by length and check containment "upwards".

Bjarni will not be in Iceland next week so next meeting is scheduled tomorrow, Fri 12 Apr 2019, at 11:00.

Permuta is licenced under "BSD-3-Clause" but Émile suggested GPL licence (v3) for CombCov as it enforces others that 
use the library to keep their code open source. We'll probably go with GPL then.

Discussed some refactoring of the code which makes it clearer what Rögnvaldur Möller needs to implement to use this 
library. After that refactoring is done Christian will try to use CombCov with tilings.

Enforcing Gurobi as a requirement to run CombCov is not user friendly so we need a fallback linear solver that works
without the need to install anything (besides the `pip install CombCov`). [PuLP](https://github.com/coin-or/pulp) seems 
to support solving linear equations without the need for 3rd party libraries, but also support using Gurobi if it's 
installed. I will look into this and evaluate whether it's shiny promises are true.



2019-04-04
==========

- [x] Review the current status of the repo and run various `StringSet` examples.
- [ ] What licence is appropriate for the GitHub repo?
- [ ] Discuss how we would like other people such as Rögnvaldur Möller use and interact with this library.
      Aspects ranging from practical stuff (like installation) to programming paradigms (such as class interfaces).
- [x] What examples to use in the REM paper?
- [ ] (From previously) Discuss deploying a new version of Permuta to Pypi.

### Summary

Ran some examples with `CombCov` over the alphabet `{a, b}`. Some examples were solved fine like `Av{'aa'}` but others
not, like `Av('aa', 'bb'}`. Our current method of generating rules on the form `prefix + Av(ss)` where ss is a subset
of `{'aa', 'bb'}` simply cannot handle the set of strings with alternating `a`'s and `b`'s.

We fixed the `StringSet.get_all_avoiding_subsets` function. E.g. for the avoiding set `{'aa', 'bb'}` it naively 
generated `[ {'aa', 'bb'}, {'aa', 'b'}, {'a', 'bb'} ]` but now it (correctly) also generates `{'a', 'b'}`.

Discussed avoiding non-consecutive substrings as well as consecutive as we do now. Then we'd need to implement 
`StringSet.contains` method differently, something along the lines of
 1. Set `S` of strings avoiding non-consecutive `'aba'`
 2. String `s` is _not_ in `S` if there exist a index set `I = {i_1, i_2, i_3}` with `i_1 < i_2 < i_3` such that
    `s[i_1] == a` and `s[i_2] == b` and `s[i_3] == a`



2019-03-28
==========

- [x] Explain to me again the concept of rules and rule generators in PermStruct, and how that maps on to CombCov.
- [x] Help me go from `StringSet` generator (all strings in the set, or of specific length) to bitstrings.
- [ ] (From last week) Discuss deploying new version of Permuta to Pypi.

### Summary

We discussed the Rules and RuleGenerators in PermStruct and how that maps on to CombCov, and specifically in context
with the `StringSet` class that I'll be focusing on for now.

In PermStruct terminology, our "root object" will be the `StringSet` class itself and this is what CombCov will be 
trying to find a cover for. The root object is represented as a string of `n` 1's, simply meaning that it contains 
it's `n` first elements. What Gurobi then does is finding a (binary) linear combination of strings that is a mix of
0's and 1's that cover the 11...1 string.

When running CombCov for `StringSet` (easily generalized for other combinatorial object) the user specifies a
`max_elmt_size` variable (default value might be 9 for now) which will result in the `StringSet` class generating 
all valid strings of length up to (and including) this number. Let the total number of these strings be `n`.

Then we need a RuleGenerator of string sets. Each Rule will be on the form `prefix + StringSet`. We'll be picking
prefixes from the root object and string sets as subsets of the root object (meaning the avoiding condition is 
stricter, i.e. now avoiding substring(s) of the avoiding string(s)). For each Rule we'll generate all strings in it 
of length `<= max_elmt_size` and only accept the Rule if all these strings are in the root object. Then we'll 
convert the Rule into a binary string for which the i'th position (from right) is 1 if the root's i'th string is in 
the Rule, else 0.

We'll use all possible prefixes up to a specific (but user overridable) length (e.g. 3). Note that the `n` is the
same as `validcnt` in PermStruct, and `max_elmt_size` corresponds to `perm_bound`.

For the last agenda item, Christan will sort out the correct import logic and then we'll deploy a new version of
Permuta.



2019-03-21
==========

- [x] Pick apart `StructSettings` object (in PermStruct/permstruct/settings.py)
- [x] What is the `sinput`?
- [x] How to calculate `settings.sinput.validcnt` without using the object above?
- [x] Is `permuta==0.1.1` broken?
- [x] Creating binary string from perm (PermStruct/permstruct/rule_set.py)
- [ ] Discuss deploying new version of Permuta to Pypi

### Summary:

`validcnt` explained: In the context finding the cover of Av(231), set `perm_bound = 3`, generate all patterns up to
(and including) length 3, discard those that are not avoiding 231, and the number of these patterns is `validcnt`. 
(These numbers are almost the same for Av(21) which confused me.)

`sinput` (of type `AvoiderInput`) turned out to be the avoidance perm generator (creator of rules) which is what I
need to calculate `validcnt` in previous point. 

The `StructSettings` object turned out to contain a lot of permutation specific stuff and some unused variables. The 
necessary variables were identified and explained to me so I can port them over to CombCov.

Current version of permuta on Pypi is definitely broken. We wan't to build and publish a new version by merging 
`version2` branch to `master` in the repo and make Travis push it to Pypi. However, there is some problem with circular 
imports in the repo which Christian wants to look into first. Will discuss again next week.



2019-03-14
==========

- [x] Run Struct
- [x] Look at connection from Struct to Gurobi
- [x] Discuss how to take it apart
- [x] Discuss test cases

### Summary:

Struct worked OK, we looked at the format of Gurobi input/output files and discussed whether we could use a Python
library instead of writing temp files and calling Gurobi as a subprocess. Decided to continue doing that for now
as there's problem installing the Python library.

Decided to start coding CombCov module by imitating Struct's `exact_cover` and build upon that by mocking a generator 
function for permutation rules for Av(21) and solve that case (unittest?).
