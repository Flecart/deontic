"""Experiment C atom material: "no vehicles in the park" (S-3).

Same schema as expA/expB. Two groundable atoms; the smallest statute in the
dataset and the paper's concept-figure example. The famous hard negative
(the powered wheelchair) is in the vehicle negative bank: it satisfies a
literal "conveyance" reading and the purposive intension excludes it.
"""

GROUNDABLE = ["vehicle", "emergency"]

ATOMS = {
  "vehicle": {
    "open": ("the item is a conveyance for moving people or goods about, of "
             "a kind whose use would bring the hazards of traffic into the "
             "park; an aid that merely substitutes for a person's own walking "
             "is not of that kind"),
    "closed": ("the item is one of: a car; a truck; a motorcycle; a bicycle"),
    "closed_items": [
      ("car",        "a sedan to be driven along the main path to the bandstand"),
      ("truck",      "a pickup hauling sound equipment across the great lawn"),
      ("motorcycle", "a motorbike ridden in through the east gate"),
      ("bicycle",    "a bicycle ridden around the gravel loop"),
    ],
    "tier1": [
      ("moped",   "a moped ridden along the flower-bed path"),
      ("e_bike",  "an electric-assist two-wheeler ridden along the lakeside path"),
    ],
    "tier2": [
      ("e_scooter",      "a stand-up electric scooter ridden at speed down the promenade"),
      ("delivery_robot", "a knee-high autonomous delivery cart rolling across the park to the kiosk with parcels"),
      ("hoverboard",     "a self-balancing powered board weaving between the flowerbeds"),
      ("segway",         "a two-wheeled standing personal transporter gliding along the jogging route"),
    ],
    "negative": [
      ("powered_wheelchair", "a powered wheelchair a visitor uses to get around the grounds instead of walking"),
      ("stroller",           "a baby stroller pushed along the path"),
      ("toy_rc_car",         "a child's remote-controlled toy car carried in under one arm"),
    ],
  },

  "emergency": {
    "open": ("bringing the item into the park is necessary to prevent "
             "imminent and serious harm to a person's life, health or "
             "safety, and the harm cannot reasonably be averted otherwise"),
    "closed": ("one of: an ambulance answering a call inside the park; a "
               "police response crossing the grounds; a fire engine reaching "
               "a fire on park premises"),
    "closed_items": [
      ("ambulance",   "an ambulance answering a collapse at the fountain"),
      ("police_resp", "a police response cutting through to a reported assault by the boathouse"),
      ("fire_engine", "a fire engine heading for a smoking food kiosk"),
    ],
    "tier1": [
      ("medic_cart",  "the park medics' response cart speeding to a cardiac arrest at the bandstand"),
    ],
    "tier2": [
      ("organ_courier", "a courier's motorbike crossing the park as the only route fast enough to deliver a transplant organ before it expires"),
      ("defib_robot",   "an automated defibrillator unit summoned across the lawns to a collapsed jogger, minutes ahead of any crew on foot"),
    ],
    "negative": [
      ("icecream_rush", "an ice-cream van hurrying through to beat the lunch crowd to the south gate"),
      ("late_commuter", "a commuter cutting across the grounds to catch a morning meeting"),
    ],
  },
}

FILLER = [
    "the visit takes place on a clear weekday morning",
    "the south gate attendant logged the arrival as usual",
    "the park is moderately busy with walkers",
]

BANNED_STEMS = [
    "vehicle", "conveyance", "traffic", "emergency", "necessary",
    "statute", "obligat", "prohibit", "permitted", "forbidden", "violat",
]

CLOSED_CATEGORIES = {
  "vehicle":   ["a car", "a truck", "a motorcycle", "a bicycle"],
  "emergency": ["an ambulance answering a call inside the park",
                "a police response crossing the grounds",
                "a fire engine reaching a fire on park premises"],
}
CLOSED_INTROS = {"vehicle": "the item is one of: ", "emergency": "one of: "}


def build_closed(atom: str, k: int) -> str:
    cats = CLOSED_CATEGORIES[atom][: max(1, k)]
    return CLOSED_INTROS[atom] + "; ".join(cats)


def english_statute(regime: str) -> str:
    d = {a: ATOMS[a][regime] for a in GROUNDABLE}
    return f"""PARK ENTRY ORDINANCE

Definitions (each condition holds exactly when its definition is met):
- BARREDKIND: {d['vehicle']}.
- URGENT: {d['emergency']}.

Sections (a later-listed "notwithstanding" clause states which section prevails):
S0. Entering the park with one's effects is permitted by default.
S1. If BARREDKIND, bringing the item in is forbidden, notwithstanding S0.
S2. If URGENT, bringing the item in is obligatory, notwithstanding S1.
"""
