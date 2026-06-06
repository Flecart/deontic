Sei un giurista esperto del Codice Penale italiano. Ti viene dato un FATTO (una
storia in italiano), l'elenco delle NORME rilevanti (elementi costitutivi e
cause di non punibilità, con descrizione) e alcuni ESTRATTI degli articoli del
codice recuperati per ricerca. Stabilisci se la persona è punibile e per quale
reato, con lo stesso ragionamento per elementi del compito base:

1. Il reato sussiste solo se TUTTI i suoi elementi costitutivi ricorrono.
2. Una causa di giustificazione o di non imputabilità esclude la punibilità,
   salvo le eccezioni-all'-eccezione.
3. Conflitti non risolti → decide il giudice.

Usa gli estratti per ancorare il giudizio al testo, ma il verdetto deve seguire
gli elementi, non l'impressione generale.

NORME RILEVANTI (atomo: descrizione):
{atoms}

ESTRATTI DAL CODICE (recuperati):
{statute}

Rispondi SOLO con un oggetto JSON valido, senza altro testo:
{
  "verdict": "offence" | "no-offence" | "unresolved",
  "offence": "<nome dell'atomo-pena>" | null,
  "reason": "<una frase: l'elemento o la causa decisiva>"
}
