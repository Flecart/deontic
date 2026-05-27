"""Defeasible Deontic Logic (DDL) inference engine.

Reference implementation of Governatori (2018), "Practical Normative Reasoning
with Defeasible Deontic Logic".
"""

from .api import Reasoner, Verdict, parse_query, reason
from .engine import Engine, Extension, extension
from .json_io import theory_from_json, theory_to_json
from .parser import ParseError, parse, parse_file
from .proof import Conclusion, Justification
from .render import describe_conclusion, describe_rule, describe_theory
from .syntax import (
    BOTTOM,
    Literal,
    ModalLiteral,
    Rule,
    Theory,
    lit,
)

__all__ = [
    "Reasoner",
    "Verdict",
    "parse_query",
    "reason",
    "Engine",
    "Extension",
    "extension",
    "theory_from_json",
    "theory_to_json",
    "parse",
    "parse_file",
    "ParseError",
    "Conclusion",
    "Justification",
    "describe_conclusion",
    "describe_rule",
    "describe_theory",
    "BOTTOM",
    "Literal",
    "ModalLiteral",
    "Rule",
    "Theory",
    "lit",
]
