# Codice Penale — altri delitti contro la persona (578, 580, 591, 593, 600, 609-bis, 614).
# ===========================================================================
# Infanticidio, istigazione al suicidio, abbandono, omissione di soccorso,
# riduzione in schiavitù, violenza sessuale, violazione di domicilio.
from definizioni.ddl import *

facts:

atom MadreNeonato:        the agent is the mother and the victim is her own newborn, killed immediately after birth (art. 578) | quote: La madre che cagiona la morte del proprio neonato immediatamente dopo il parto | uri: examples/codice_penale/sources/codice_penale_full.md#L7768-L7775
atom AbbandonoMaterialeMorale: the killing was determined by conditions of material and moral abandonment connected with the birth (mitigating circumstance, art. 578) | quote: quando il fatto è determinato da condizioni di abbandono materiale e morale connesse al parto | uri: examples/codice_penale/sources/codice_penale_full.md#L7768-L7775
atom DeterminaAlSuicidio: the agent causes another to commit suicide, reinforces their resolve, or facilitates its execution (art. 580) | quote: determina altrui al suicidio o rafforza l'altrui proposito di suicidio, ovvero ne agevola … l'esecuzione | uri: examples/codice_penale/sources/codice_penale_full.md#L7802-L7809
atom SuicidioAvviene:     the suicide actually occurs (event condition, art. 580) | quote: se il suicidio avviene | uri: examples/codice_penale/sources/codice_penale_full.md#L7802-L7809
atom AbbandonaIncapace:   the agent abandons a person under 14, or one unable to care for themselves through mental/bodily illness or age, whom they have a duty to keep or care for (art. 591) | quote: abbandona una persona minore degli anni quattordici, ovvero una persona incapace … di provvedere a se stessa | uri: examples/codice_penale/sources/codice_penale_full.md#L8053-L8061
atom OmetteSoccorso:      finding a child under 10 or an incapable person abandoned/lost, the agent fails to give the necessary assistance or to notify the authority (art. 593) | quote: trovando abbandonato o smarrito un fanciullo minore degli anni dieci … omette di prestare l'assistenza occorrente | uri: examples/codice_penale/sources/codice_penale_full.md#L8086-L8094
atom EsercitaPoteriProprieta: the agent exercises over a person powers corresponding to ownership, or keeps them in continuous subjection (art. 600) | quote: esercita su una persona poteri corrispondenti a quelli del diritto di proprietà ovvero … riduce o mantiene una persona in uno stato di soggezione continuativa | uri: examples/codice_penale/sources/codice_penale_full.md#L8248-L8256
atom AttiSessualiCostretti: the agent compels someone to perform or undergo sexual acts (the result of art. 609-bis) | quote: costringe taluno a compiere o subire atti sessuali | uri: examples/codice_penale/sources/codice_penale_full.md#L8502-L8509
atom IntroduceDomicilio:  the agent enters another's dwelling or private place against the express or tacit will of who has the right to exclude them (art. 614) | quote: s'introduce nell'abitazione altrui … contro la volontà espressa o tacita di chi ha il diritto di escluderlo | uri: examples/codice_penale/sources/codice_penale_full.md#L8784-L8792
atom AbusoAutorita:       the coercion was achieved through abuse of authority (a third modality of art. 609-bis, alongside violence and threat) | quote: con violenza o minaccia o mediante abuso di autorità | uri: examples/codice_penale/sources/codice_penale_full.md#L8502-L8509
atom ReclusioneInfanticidio:  penalty: reclusion 4-12 years (art. 578) | quote: è punita con la reclusione da quattro a dodici anni | uri: examples/codice_penale/sources/codice_penale_full.md#L7768-L7780
atom ReclusioneIstigSuicidio: penalty: reclusion 5-12 years (art. 580) | quote: con la reclusione da cinque a dodici anni | uri: examples/codice_penale/sources/codice_penale_full.md#L7802-L7809
atom ReclusioneAbbandono:     penalty: reclusion 6 months-5 years (art. 591) | quote: è punito con la reclusione da sei mesi a cinque anni | uri: examples/codice_penale/sources/codice_penale_full.md#L8053-L8061
atom ReclusioneOmissioneSoccorso: penalty: reclusion up to 1 year or fine (art. 593) | quote: è punito con la reclusione fino a un anno o con la multa | uri: examples/codice_penale/sources/codice_penale_full.md#L8086-L8094
atom ReclusioneSchiavitu:     penalty: reclusion 8-20 years (art. 600) | quote: è punito con la reclusione da otto a venti anni | uri: examples/codice_penale/sources/codice_penale_full.md#L8248-L8256
atom ReclusioneViolenzaSessuale: penalty: reclusion 5-10 years (art. 609-bis) | quote: è punito con la reclusione da cinque a dieci anni | uri: examples/codice_penale/sources/codice_penale_full.md#L8502-L8509
atom ReclusioneViolazioneDomicilio: penalty: reclusion up to 3 years (art. 614) | quote: è punito con la reclusione fino a tre anni | uri: examples/codice_penale/sources/codice_penale_full.md#L8784-L8792

precetto_580: =>O@Chiunque ~DeterminaAlSuicidio
precetto_591: =>O@Chiunque ~AbbandonaIncapace
precetto_593: =>O@Chiunque ~OmetteSoccorso
precetto_600: =>O@Chiunque ~EsercitaPoteriProprieta
precetto_609: =>O@Chiunque ~AttiSessualiCostretti
precetto_614: =>O@Chiunque ~IntroduceDomicilio

# Infanticidio (578): la madre cagiona la morte del neonato in abbandono.
MadreNeonato, CagionaMorte, AbbandonoMaterialeMorale, Dolo {
  tipico_578: =>O@Giudice FattoTipico
  pena_578:   O(Sanziona) =>O@Giudice ReclusioneInfanticidio
}

# Istigazione/aiuto al suicidio (580): punibile SE il suicidio avviene.
DeterminaAlSuicidio, SuicidioAvviene, Dolo {
  tipico_580: =>O@Giudice FattoTipico
  pena_580:   O(Sanziona) =>O@Giudice ReclusioneIstigSuicidio
}

# Abbandono di incapaci (591).
AbbandonaIncapace, Dolo {
  tipico_591: =>O@Giudice FattoTipico
  pena_591:   O(Sanziona) =>O@Giudice ReclusioneAbbandono
}

# Omissione di soccorso (593): reato omissivo.
OmetteSoccorso, Dolo {
  tipico_593: =>O@Giudice FattoTipico
  pena_593:   O(Sanziona) =>O@Giudice ReclusioneOmissioneSoccorso
}

# Riduzione in schiavitù (600).
EsercitaPoteriProprieta, Dolo {
  tipico_600: =>O@Giudice FattoTipico
  pena_600:   O(Sanziona) =>O@Giudice ReclusioneSchiavitu
}

# Violenza sessuale (609-bis): costrizione ad atti sessuali mediante violenza,
# minaccia o abuso di autorità (riusa Violenza/Minaccia).
AttiSessualiCostretti, oneof[Violenza, Minaccia, AbusoAutorita], Dolo {
  tipico_609: =>O@Giudice FattoTipico
  pena_609:   O(Sanziona) =>O@Giudice ReclusioneViolenzaSessuale
}

# Violazione di domicilio (614).
IntroduceDomicilio, Dolo {
  tipico_614: =>O@Giudice FattoTipico
  pena_614:   O(Sanziona) =>O@Giudice ReclusioneViolazioneDomicilio
}
