# NDA disclosure norm that reuses the shared role definitions by MERGING them
# into this namespace. `Director`, `Representative`, ... are referred to plainly.
from definitions.ddl import *

atom Disclose:   holds when Confidential Information is disclosed to the person
atom NeedToKnow: holds when the person has a need to know the information

# Default: do not disclose. A Representative with a need to know may receive CI.
no_disclosure:       =>O  ~Disclose
rep_disclosure:      Representative, NeedToKnow  ~>O  Disclose
superiority: rep_disclosure > no_disclosure

# Try it:
#   deontic atoms  examples/imports/nda_glob.ddl     (shows merged role + NDA atoms)
#   deontic abduce examples/imports/nda_glob.ddl 'P(Disclose)' --all
#     → { Representative, NeedToKnow }
#   With a fact `Director`, `query` derives `fact(Representative)` via the
#   imported def_director rule (constitutive classification crosses the import).
