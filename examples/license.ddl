# Example 1 / Section 4 (Governatori 2018): product-evaluation licence.
# Try:  ddl run examples/license.ddl --facts "license. publish. remove. comment."
#       (drop `comment` -> compliant; add `approval.` -> compliant again)

r0:  =>O -use                   # use is forbidden by default
r1:  license ~>O use            # a licence permits use (defeats r0)
r2:  =>O -publish (x) remove    # publishing forbidden; removing compensates
r2e: approval ~>O publish       # approval permits publishing
r3:  =>O -comment               # commenting forbidden
r3e: P publish ~>O comment      # if publishing is permitted, so is commenting
r4:  commission =>O publish     # if commissioned, must publish
r4x: commission =>O use         # if commissioned, must use
r5:  bottom =>O -use            # a non-compensable violation forbids use

r0 < r1
r0 < r4x
r1 < r5
r4x < r2e
r2 < r2e
r3 < r3e
