# Codice Penale — DELITTI CONTRO LA FAMIGLIA (artt. 570, 572, 574).
# ===========================================================================
# Violazione degli obblighi di assistenza, maltrattamenti, sottrazione di
# persone incapaci.
from definizioni.ddl import *

facts:

atom SottraeObblighiAssistenza: by abandoning the family home or keeping a conduct against family order/morals, the agent evades the assistance duties inherent in parental authority or the spouse status (art. 570) | quote: si sottrae agli obblighi di assistenza inerenti alla responsabilità genitoriale o alla qualità di coniuge | uri: examples/codice_penale/sources/codice_penale_full.md#L7601-L7609
atom Maltratta:        the agent mistreats a family member, a person under 14, or a person under their authority or entrusted to them (art. 572) | quote: maltratta una persona della famiglia, o un minore degli anni quattordici, o una persona sottoposta alla sua autorità | uri: examples/codice_penale/sources/codice_penale_full.md#L7648-L7656
atom SottraeMinore:    the agent removes a person under 14, or a mentally infirm person, from the parent exercising authority, the guardian, or whoever has their custody (art. 574) | quote: sottrae un minore degli anni quattordici, o un infermo di mente, al genitore esercente la patria potestà, al tutore | uri: examples/codice_penale/sources/codice_penale_full.md#L7684-L7692
atom ReclusioneViolazAssistenza: penalty: reclusion up to 1 year or fine (art. 570) | quote: con la reclusione fino a un anno o con la multa | uri: examples/codice_penale/sources/codice_penale_full.md#L7601-L7609
atom ReclusioneMaltrattamenti:   penalty: reclusion 3-7 years (art. 572) | quote: è punito con la reclusione da tre a sette anni | uri: examples/codice_penale/sources/codice_penale_full.md#L7648-L7656
atom ReclusioneSottrazioneMinore: penalty: reclusion 1-3 years (art. 574) | quote: è punito … con la reclusione da uno a tre anni | uri: examples/codice_penale/sources/codice_penale_full.md#L7684-L7692

precetto_570: =>O@Chiunque ~SottraeObblighiAssistenza
precetto_572: =>O@Chiunque ~Maltratta
precetto_574: =>O@Chiunque ~SottraeMinore

# Violazione degli obblighi di assistenza familiare (570).
SottraeObblighiAssistenza, Dolo {
  tipico_570: =>O@Giudice FattoTipico
  pena_570:   O(Sanziona) =>O@Giudice ReclusioneViolazAssistenza
}

# Maltrattamenti in famiglia (572): condotta abituale di maltrattamento.
Maltratta, Dolo {
  tipico_572: =>O@Giudice FattoTipico
  pena_572:   O(Sanziona) =>O@Giudice ReclusioneMaltrattamenti
}

# Sottrazione di persone incapaci (574).
SottraeMinore, Dolo {
  tipico_574: =>O@Giudice FattoTipico
  pena_574:   O(Sanziona) =>O@Giudice ReclusioneSottrazioneMinore
}
