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
