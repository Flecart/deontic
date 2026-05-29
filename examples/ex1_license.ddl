# Example 1: License contract (§4 of Governatori 2018)
facts: license, commission, use

# Atom descriptions are mandatory; this synthetic example cites the paper.
atom license:    the licensee holds a valid licence | Governatori 2018 §4, license example
atom commission: the work was produced under commission | Governatori 2018 §4
atom use:        the licensee uses the licensed material | Governatori 2018 §4
atom publish:    the licensee publishes results | Governatori 2018 §4
atom remove:     the licensee removes the published results (remedy) | Governatori 2018 §4
atom approval:   prior approval to publish was obtained | Governatori 2018 §4
atom comment:    the licensee comments publicly | Governatori 2018 §4
atom bot:        the licensee is (or acts as) an automated agent | Governatori 2018 §4

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
# Without e.g. r4 > r2, commission+use yields an unresolved publish conflict (judge must add ≺)
superiority: r1 > r0, r4x > r0, r5 > r1, r5 > r4x, r2e > r2, r3e > r3
