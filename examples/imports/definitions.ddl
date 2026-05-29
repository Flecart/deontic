# Shared definitions module: institutional roles (constitutive `=>` rules).
# Reusable across contracts in an agent society. Import it with either
#   from definitions.ddl import *      (merge into the importer's namespace)
#   import definitions.ddl as roles    (namespaced: roles.Director, ...)
#
# This module declares no facts — it only defines what counts as a Representative.

atom Director:       holds when the person has a director role at the party
atom Officer:        holds when the person has an officer role at the party
atom Employee:       holds when the person is an employee of the party
atom Representative: holds when the person counts as a Representative of the party

def_director: Director => Representative
def_officer:  Officer  => Representative
def_employee: Employee => Representative
