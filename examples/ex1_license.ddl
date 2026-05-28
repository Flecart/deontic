# Example 1: License contract (§4 of Governatori 2018)
# Scenario A: licensee has license, published results, then removed them
facts: license, publish, remove

r0:  =>O  ~use
r1:  license  ~>O  use
r2:  =>O  ~publish * remove
r2e: approval  ~>O  publish
r3:  =>O  ~comment
r3e: P(publish)  ~>O  comment
r4:  commission  =>O  publish
r4x: commission  =>O  use
r5:  bot  =>O  ~use

# r ≺ s means r defeats s (r wins when both conflict)
# More specific/exception rules defeat more general ones
superiority: r1 > r0, r4x > r0, r5 > r1, r5 > r4x, r2e > r2, r3e > r3
