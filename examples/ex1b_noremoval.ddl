# Example 1B: license + publish without removal (non-compensable violation)
facts: license, publish

r0:  =>O  ~use
r1:  license  ~>O  use
r2:  =>O  ~publish * remove
r2e: approval  ~>O  publish
r3:  =>O  ~comment
r3e: P(publish)  ~>O  comment
r4:  commission  =>O  publish
r4x: commission  =>O  use
r5:  bot  =>O  ~use

superiority: r1 > r0, r4x > r0, r5 > r1, r5 > r4x, r2e > r2, r3e > r3
