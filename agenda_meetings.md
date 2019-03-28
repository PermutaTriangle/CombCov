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
it's `n` first elements. What Gurobi then does is finding a (binary) linear combinatin of strings that is a mix of
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
