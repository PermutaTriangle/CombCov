2019-10-03
==========
- [x] Review status of Bjarni's thesis writing and discuss when it's ready for (partial) reviewing
      by Henning and/or Christian
- [x] Discuss dates for Bjarni leaving, thesis submission, MSc presentation etc.
- [ ] Send title and abstract for Icelandic Math Conference talk
- [x] Review results from CombCov runs and what to highlight in the thesis and how to present it
- [ ] Discuss updating https://github.com/PermutaTriangle/permpatts in order to
    + draw mesh patts with highlighted occurrences
    + draw tilings as in Struct paper
    + make rectangle edges around coordinates of shaded squares in mesh patts

### Summary

Bjarni has written most of Chapters 1 (Introduction) and 2 (Methods) while 3 (Results) and 4 (Discussion) are still
left. We discussed the time frame and various dates for reviewing the paper (first version in the next week), Bjarni
leaving (at the end of the month) and thesis defence (last week before Christmas). Henning is talking to people to be
on the committee.

Most of our energy went into going through 318 successful jobs on Garpur, handpicking interesting results to highlight
in the paper. Out of the 1240 started jobs 700 have timed out, 99 exhausted their search space (up to config 5x5x5)
and the last 123 are still running but with high chance of timing out.

Bjarni will continue writing his thesis and highlight the interesting results by showing the cover and discuss them in
words as well. He will also write an abstract for the Icelandic Math Conference talk and get an approval from Henning
before submitting it.

The matter of the LaTeX library was briefly discussed but needs to be updated soon so Bjarni can use it to draw
consistent pictures in the thesis and talk.



2019-09-19
==========
- [x] Look at covers that CombCov has already found and posted on Garpur channel

### Summary

Henning proposes even more papers to run jobs from. The papers are on interval mesh patterns of length 3 and boxed mesh
patterns of length 4. The authords include Woo, Kitaev and Liese. Decided to run all possible variations of BiVincular
mesh patterns of length 3 (excluding symmetries) in addition to the jobs that we've already started from the _Wilf
Classification of Bi-Vincular permutation patterns_ paper.



2019-09-12
==========
- [x] Look at covers that CombCov has already found and posted on Garpur channel

### Summary

Some interesting Fishburn covers. Discussed that it would be interesting to look for covers for the complimentary
containment set `Co(patts)` for every job, in addition to the normal `Av(patts)` search. Bjarni will start containment
jobs for all the Fishburn patterns as well as do that by default when he re-runs WilfShort and Covincular jobs.

Some trivial WilfShort covers where the answer is the same as the input. Turns out to be because input is a `MeshPatt`
with empty shading, but the solution is the underlying pattern as a `Perm` object. Bjarni will make sure that this
won't happen again and re-run the WilfShort jobs.



2019-09-05
==========
- [x] Look at covers that CombCov has already found and posted on Garpur channel

### Summary

The results posted on Garpur are promising and some of the covers are really interesting. Discussed running more jobs
such as these from Anders' first paper (_Generalised Pattern Avoidance_):
```text
          |#| |       | |#|   
         -+-+-2-     -+-+-2-  
          |#| |       | |#|   
    Av(  -+-1-+-  ,  -+-1-+-  )
          |#| |       | |#|   
         -0-+-+-     -0-+-+-  
          |#| |       | |#|   
```
and
```text
          | |#|       |#| |   
         -+-+-2-     -+-2-+-  
          | |#|       |#| |   
    Av(  -+-1-+-  ,  -+-+-1-  )
          | |#|       |#| |   
         -0-+-+-     -0-+-+-  
          | |#|       |#| |   
```
Bjarni will run these as well as everything else from the table(s) in the paper.



2019-08-29
==========
- [x] Review results from Garpur on length 2 mesh patterns (from Wilf paper)
- [x] Discuss skeleton for presentation
       + Stærðfræði á Íslandi (Oct. 12-13) about 30 minutes
       + Thesis defense about 60 minutes
- [x] Discuss skeleton for thesis writing
- [x] Decide on next meeting time as Bjarni will be traveling

### Summary

Much of the time went into debugging why CombCov didn't find the following cover:
```text
    -------------                     ------- 
   |      #|     |        ---        | o | S |
   | Av(  -1-  ) |   =   |   |   U    ---+---+
   |      #|#    |        ---        |   | o |
    -------------                     ------- 
```

where S is the "anything" cell. We found the culprit and fixed the bug. Bjarni will clean up the code a bit and then
push it to GitHub along with unittests to prevent this from happening again. Sufficient regression testing should be
testing that MeshTiling always generates the 1x1 S cell as one of it's subrules.

Following this we wanted CombCov to be able to find the cover for the complementary subset
```text
    -------------         ------- 
   |      #|     |       |   | S |
   | Co(  -1-  ) |   =    ---+---+
   |      #|#    |       | o |   |
    -------------         ------- 
```

This was done in a live session of collaborate coding but proved tricky as the MeshTiling class was written under the
assumption that we'd only be searching for avoidance classes. However, we manage to (drastically) change the class so
that it was able to find the above containment cover _at the cost of_ not being able to find avoidance covers anymore.

Bjarni will now have to refactor the code so that it can do both and preferably find covers for MeshTilings with a mix
of requirements (containment) and obstructions (avoidance) specifications. Plan B is to make the assumption that the
root 1x1 MeshTiling is only allowed to contain requirements _or_ obstructions -- not a mix of both.

We discussed the skeletons for both of the presentations and decided they should look along these lines:

Stærðfræði á Íslandi conference (~30 min):
  * Title will be "Þakningar fléttufræðilegra fyrirbrigða með aðstoð línulegrar bestunnar"
  * Henning/Christian will try to go first with their presentation
    - will define perms and patterns which saves time for Bjarni and Émile
    - definitions should still be included in the slides for future references
  * Explain CombCov with Word Classes
    - Av(aa) with words up to length 3
    - pick selected subrules and calculate their containment strings
    - explain that we use Gurobi (Linear Programming) to solve the set of eqs.
  * Talk about success for MeshTilings without defining it
    - show visual covers (see permuta library for LaTeX code)
    - Wilf length 2 mesh patterns
    - Fishburn length 3 patterns (Catalan numbers)
    - Vincular and Covincular patterns
    - Bi-Vincular patterns

Thesis defence (~60 min):
  * Start same as the other one
  * Define MeshTilings here and go into more detail

Bjarni will be away for travels the next two weeks. Next two meetings will be conducted via Skype.



2019-08-22
==========
- [x] Go over requires.io integration with PermutaTriangle repos
- [x] Discuss results on replicating stuff from Vincular+Covincular paper
- [x] Discuss results on replicating stuff from Fishburn paper
- [ ] Discuss skeleton for presentation
       + Stærðfræði á Íslandi (Oct. 12-13) about 30 minutes
       + Thesis defense about 60 minutes
- [ ] Discuss skeleton for thesis writing

### Summary

We configured default branch in Permuta repo to be 'develop' requires.io makes PRs towards the default branch.

CombCov found covers for 10 combinations of Fishburn + two length 4 patterns using 3x3x3 config (column x row
dimension of MeshTiling x active cells). It did not find covers for the other 266 combinations with 4x4x4 config.
We submitted these jobs again with 4x4x5 config and we'll try 5x5x5 also for those that are unsuccessful. After this
we'll look for covers of Fishburn + three length 4 patterns (2024 combinations).

We went over the results of the Vincular+Covincular patterns as well and rejoiced in the comparative success there.
Many covers needed only 3x3x3 config and some more was found with 4x4x4 config. We'll try config 5x5x5 for the yet
unsuccessful ones.

Henning has asked for 2-3 talking slots at the Icelandic Math Conference in October for Bjarni, Émile and maybe
Christian/Henning to present their work. All of them have registered to participate in the conference.



2019-08-15
==========
- [x] Review EC Python library and Bjarni's homework assignments
- [x] Which results to replicate?
      + Wilf-classification of mesh patterns of short length
      + On pattern-avoiding Fishburn permutations
      + Anything else?
- [ ] Discuss skeleton for presentation
- [ ] Discuss skeleton for thesis writing

### Summary

Henning and Christian were happy with the PyECCArithmetic library and will probably use it for homework assignments
in the Crypto course this fall semester. The owner of the repo hasn't responded to Bjarni's PR that adds support for
the infinity point. We discussed the possibility of releasing another package to PyPi with slightly different name if
the owner won't respond, or instructing students to clone the repo and install via `setup.py`. Bjarni will post his
homework solutions as a private GitHub gist and give Henning and Christian access.

Some results from the Fishburn paper were replicated with CombCov (namely sigma equals to 231, 123, 132 and 213) but
others were unsuccessful (sigma equals 312 and 321 and all of the length 4 patterns). We will try that again on Garpur
with larger search space. We will also try all combinations with two length four patterns. The results from the Wilf
paper that were discussed in last meeting also need to be run on Garpur with larger search space than were tried on
Bjarni's laptop.

Christian came up with yet another paper with results that is interesting to try to replicate, a paper on avoiding
vincular and covincular patterns of length 3. We tried a result from the paper that gives the Motzkin numbers:
```text
         | | |       | | |   
        -+-3-+-     -+-+-3-  
         | | |      #|#|#|#  
   Av(  -+-+-2-  ,  -+-2-+-  )
         | | |       | | |   
        -1-+-+-     -1-+-+-  
         | | |       | | |   
```
At first we were unsuccessful to find a cover for it, but by editing the rule generation function to create more
complicated rules we managed to find a cover for it, albeit slightly different that in the paper. We will try to run
CombCov again with theses changes on previously unsuccessful results from Fishburn and Wilf papers.

We started discussing the layout of Bjarni's thesis but need to follow up on that in the next meeting. Henning
mentioned that it would be smart though to rename `StringSet` to `WordSet` so the elements are called *words* and are
not confused with the underlying *bitstrings*.



2019-06-21
==========
- [x] Prepare Bjarni's reading course in Elliptic Curves so he can study it
      while Henning and Christian are on summer vacation in July
- [x] Implement `MeshTilings.get_elmnts()` method (multiple nested for-loops)

### Summary

Henning prepared reading chapters and exercises for Bjarni solve. Henning wants Bjarni to find a suitable Python
library and solve most of the exercises with it. The idea being that Christian can use it for homework assignments
in his Crypto class this fall.

Together Bjarni and Henning hacked together the `MeshTilings.get_elmnts()` method by porting the multiple nested
for-loops. It was ugly but it worked and we could run it on some short mesh patterns from the Wilf-classification
paper "of mesh patterns of short length". This can be used in Bjarni's thesis as a replication of older work.



2019-06-20
==========
- [ ] Prepare Bjarni's reading course in Elliptic Curves so he can study it
      while Henning and Christian are on summer vacation in July
- [x] Review Bjarni's PR in `permuta` library that adds support for bases of
      mesh patterns and the `for perm in Av(mesh_patts)` syntax
- [ ] Implement `MeshTilings.get_elmnts()` method (multiple nested for-loops)

### Summary

We reviewd the PR in `Permuta` and fixed a regression where `Av(p)` (`p` a single `Perm` object) syntax broke and
added a test for it to README. Christian then approved the PR and merged it to develop branch.

Then we took a look at the multiple nested for-loops in `grids/Tiling.py` repo/file, tried to understand it and started
porting it over to `MeshTiling` class and changing it as needed. Bjarni will keep on with it until the next meeting that
is scheduled for Friday, June 21 at 10:30.



2019-06-13
==========
- [x] Review PR on adding support to `permuta` for `MeshPatt` bases

### Summary

Before the meeting Bjarni had made a PR in the `permuta` repo aiming to add support for looping over permutations
avoiding a set of mesh patterns, i.e. a `for perm in Av(mesh_patts)` syntax. It proposed changing the `Basis` class
to not only accept elements of type `Perm` but the more general `Patt` interface that included `Perm` and `MeshPatt`.

Henning and Christian however raised some concerns over this because in literature a basis generally only refers to
bases of classical permutations and not mesh patterns. Therefore we decided to do some further refactoring along these
lines:
- create a new class called `MeshBasis` accepting `MeshPatt`s and maybe also `Perm`s
- leave `Basis` class intact (only accepting `Perm`s)
- try to avoid code duplication between these two classes by using metaclasses or parent class
- change the `Av` class to behave differently based on whether it's input is `MeshBasis` or `Basis`
- this ensures that `Basis` behaves the way users expect and keeps backwards compatibility



2019-06-06
==========

- [x] CombCov put to the test: Christian finding covers for "polynomial permutation classes"
- [ ] Hack together "Tilings of Mesh patterns" with the goal being able to find a cover for Av(31c2)
      where 31c2 is the mesh pattern
```text
             | |#| 
            -3-+-+-
             | |#| 
            -+-+-2-
             | |#| 
            -+-1-+-
             | |#| 
```

### Summary

Christian was able to use the `Tiling` package to do the heavy lifting of Tiling specific logic such as element
generation, obstructions and requirement conditions. There's no way of getting around implementing the `get_subrules()`
function though, which he did on the projector with neglible help from Bjarni and Henning. The resulting code was
pushed to GitHub and and can be viewed in the resulting [Pull Request #6](https://github.com/PermutaTriangle/CombCov/pull/6/).

Next we want to use`CombCov` with "Mesh Tilings". As in the agenda above, we use _c_ in a pattern to denote a shaded column. 
The first goal is to have `CombCov` find the following cover: 

```text
                                   ------------------------
    ----------         ---        |          | o |         |
   | Av(31c2) |   =   | o |   U   |----------+---+---------|
    ----------         ---        | Av(31c2) |   | Av(1c2) |
                                   ------------------------
```

The things discussed included the difficulties of generating permutations from such a "Tiling" and how we could implement
it. Similar thing has been done in old Grids repo and one option is to [_port those nested for loops_](
https://github.com/PermutaTriangle/grids/blob/master/grids/Tiling.py#L429) over to here. This is far from finished and is
now an ongoing project.
 
Various other small changes to `CombCov` including a request for logging and informative messages were discussed and duly
noted for later implementation.

Regarding Bjarni's missing ECTS units it has been decided that Bjarni does a small reading course on Elliptic Curve cryptography
by reading selected chapters from the book used in Christians cryptography class, solve some related exercises and even write
some Python code.



2019-05-23
==========

- [x] Status of code refactoring before Christian can use it with his _Tilings_
- [ ] Bjarni needs 2 ECTS units of course work. Can he do a reading course in Elliptic Curves?

### Summary

We reviewed the code factoring that had been done so far and then finished it with the aid of Christian. `StringSet`
has been moved into a new `demo` module (where it can serve as an example on how to use CombCov) and `CombCov` was
moved into the new `combcov` module (which will be published to PyPy in due time).

The rough layout is like this: `CombCov` takes in a `Rule` object (such as `StringSet` or `Tiling`) which is an
abstract class that needs to implement the following methods:

- `get_elmnts(of_size)`: return all elements in Rule of specific size
- `get_subrules()`: return all "lesser" Rules (the ones we try to stitch together), but with no requirement at the
    moment that they are all unique or valid
- `__hash__()`: Rule must be hashable
- `__str__()`: Rule must have a string representation

Bjarni will do a little bit of tidying up the code before pushing these changes to GitHub. Then Christian will try to
use it with his _Tilings_ objects.

Discussion of Bjarni's last ECTS credits were postponed to next meeting.



2019-05-02
==========

- [x] Review using `PuLP` to interface with Gurobi as there's a fallback on naive LPS when Gurobi isn't available
- [ ] Decide upon next meeting time.

### Summary

Using `GuLP` to define the optimization problem and calling Gurobi upon works really well as demonstrated in a small
PoC. It is easy to check whether Gurobi is installed on the system or not, and fall back on a "naive" Linear
Programming Solver if it isn't.

We discussed that the next step in the project is to refactor the CombCov code to make it easy to "plug and play" other
combinatorial objects. We want to try _Tilings_, _Permutations_ and _Mesh patterns_ with CombCov. This goes a long way
of constituting the whole thesis work.

Bjarni is currently taking a 3-week course and will thus have little time to work on CombCov in the meantime. Next
meeting time wasn't discussed or decided upon.



2019-04-12
==========

- [x] (From previously) Discuss deploying a new version of Permuta to Pypi.
- [ ] Refactor code with the goal of Christian being able to use CombCov with his Tilings objects.
- [x] Decide upon next meeting time.

### Summary

We discussed what needs to be done in order to deploy a new version of Permuta to Pypi. We edited the Travis CI config
file so it builds and pushes Permuta straight to Pypi on successful builds (passing unittests) on the master branch of
the GitHub repo. Christian was working on refactoring the Permuta code on the version2 branch so we can soon merge it
to master.

Next meeting time is Thu 2 May at 13:00 unless Bjarni will be in class at that time, in which case he contacts Henning
and Christan to reschedule.



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
library. After that refactoring is done Christian will try to use CombCov with Tilings.

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
