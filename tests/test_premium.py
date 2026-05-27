"""Example 2 (Governatori 2018): provision of goods and services.

Covers the *constitutive* fragment (clauses 3.1 and 3.2): the counts-as
definition of a Premium Customer and the special-order surcharge with the
premium-customer exemption as an exception (superiority). The obligation /
entitlement clauses (5.2, 5.3) need the deontic layer and are tested in M2.

    c31:  highSpend      => premiumCustomer       # 3.1 "Premium Customer"
    c32a: specialOrder   => surcharge             # 3.2 5% surcharge
    c32b: premiumCustomer => -surcharge           # 3.2 premium exemption
    c32a < c32b                                   # exemption is superior
"""

from ddl import lit, parse
from ddl.engine import extension

THEORY = """
    c31:  highSpend       => premiumCustomer
    c32a: specialOrder    => surcharge
    c32b: premiumCustomer => -surcharge
    c32a < c32b
"""


def test_premium_customer_is_exempt_from_surcharge():
    e = extension(parse(THEORY + "\nspecialOrder. highSpend."))
    assert e.provable(lit("premiumCustomer"))
    assert e.provable(lit("surcharge", True))  # exempt: -surcharge
    assert e.refuted(lit("surcharge"))


def test_non_premium_customer_pays_surcharge():
    e = extension(parse(THEORY + "\nspecialOrder."))
    assert e.refuted(lit("premiumCustomer"))
    assert e.provable(lit("surcharge"))
    assert e.refuted(lit("surcharge", True))
