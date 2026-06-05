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

# Every duty here is the licensee's — a single-bearer contract. The `@Licensee`
# tag makes that explicit (and, being one bearer, the extension is unchanged from
# the un-tagged form: directing obligations only matters once parties differ).
r0:  =>O@Licensee  ~use
r1:  license  ~>O@Licensee  use
r2:  =>O@Licensee  ~publish * remove
r2e: approval  ~>O@Licensee  publish
r3:  =>O@Licensee  ~comment
r3e: P(publish)  ~>O@Licensee  comment
r4:  commission  =>O@Licensee  publish
r4x: commission  =>O@Licensee  use
r5:  bot  =>O@Licensee  ~use

# r ≺ s means r defeats s (r wins when both conflict)
# More specific/exception rules defeat more general ones
# Without e.g. r4 > r2, commission+use yields an unresolved publish conflict (judge must add ≺)
superiority: r1 > r0, r4x > r0, r5 > r1, r5 > r4x, r2e > r2, r3e > r3
