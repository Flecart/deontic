# Same NDA norm, but the role definitions are imported UNDER A NAMESPACE.
# Imported atoms/labels are prefixed `roles.` and referred to qualified.
import definitions.ddl as roles

atom Disclose:   holds when Confidential Information is disclosed to the person
atom NeedToKnow: holds when the person has a need to know the information

no_disclosure:  =>O  ~Disclose
rep_disclosure: roles.Representative, NeedToKnow  ~>O  Disclose
superiority: rep_disclosure > no_disclosure

# Try it:
#   deontic atoms  examples/imports/nda_namespaced.ddl
#     → roles.Director, roles.Representative, ... alongside Disclose, NeedToKnow
#   deontic abduce examples/imports/nda_namespaced.ddl 'P(Disclose)' --all
#     → { roles.Representative, NeedToKnow }
