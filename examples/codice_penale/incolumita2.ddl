# Codice Penale — incolumita2 (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom CagionaInondazioneFrana: causes a flood, a landslide, or the fall of an avalanche (art. 426) | quote: Inondazione, frana o valanga | uri: examples/codice_penale/sources/codice_penale_full.md#L5823-L5828
atom ReclusioneInondazione: reclusion 5-12 years (art. 426) | quote: Inondazione, frana o valanga | uri: examples/codice_penale/sources/codice_penale_full.md#L5823-L5828
precetto_426: =>O@Chiunque ~CagionaInondazioneFrana
CagionaInondazioneFrana, Dolo {
  tipico_426: =>O@Giudice FattoTipico
  pena_426:   O(Sanziona) =>O@Giudice ReclusioneInondazione
}

atom CagionaNaufragio: causes the shipwreck or sinking of another's vessel, or the fall of an aircraft (art. 428) | quote: Naufragio, sommersione o disastro aviatorio | uri: examples/codice_penale/sources/codice_penale_full.md#L5840-L5848
atom ReclusioneNaufragio: reclusion 5-12 years (art. 428) | quote: Naufragio, sommersione o disastro aviatorio | uri: examples/codice_penale/sources/codice_penale_full.md#L5840-L5848
precetto_428: =>O@Chiunque ~CagionaNaufragio
CagionaNaufragio, Dolo {
  tipico_428: =>O@Giudice FattoTipico
  pena_428:   O(Sanziona) =>O@Giudice ReclusioneNaufragio
}

atom FattoCrolloDisastro: commits a fact apt to cause the collapse of a construction or another disaster (art. 434) | quote: Crollo di costruzioni o altri disastri dolosi | uri: examples/codice_penale/sources/codice_penale_full.md#L5910-L5918
atom ReclusioneCrollo: reclusion 1-5 years for the mere attempt (art. 434) | quote: Crollo di costruzioni o altri disastri dolosi | uri: examples/codice_penale/sources/codice_penale_full.md#L5910-L5918
precetto_434: =>O@Chiunque ~FattoCrolloDisastro
FattoCrolloDisastro, Dolo {
  tipico_434: =>O@Giudice FattoTipico
  pena_434:   O(Sanziona) =>O@Giudice ReclusioneCrollo
}

atom AdulteraSostanzeAlimentari: corrupts or adulterates water or substances destined for food, before they are drawn or distributed, making them dangerous to public health (art. 440) | quote: Adulterazione e contraffazione di sostanze alimentari | uri: examples/codice_penale/sources/codice_penale_full.md#L5973-L5981
atom ReclusioneAdulterazione: reclusion 3-10 years (art. 440) | quote: Adulterazione e contraffazione di sostanze alimentari | uri: examples/codice_penale/sources/codice_penale_full.md#L5973-L5981
precetto_440: =>O@Chiunque ~AdulteraSostanzeAlimentari
AdulteraSostanzeAlimentari, Dolo {
  tipico_440: =>O@Giudice FattoTipico
  pena_440:   O(Sanziona) =>O@Giudice ReclusioneAdulterazione
}

atom CagionaIncendioBoschivo: causes a fire on woods, forests or forest nurseries (art. 423-bis) | quote: Incendio boschivo | uri: examples/codice_penale/sources/codice_penale_full.md#L5776-L5784
atom ReclusioneIncendioBoschivo: reclusion 4-10 years (art. 423-bis) | quote: Incendio boschivo | uri: examples/codice_penale/sources/codice_penale_full.md#L5776-L5784
precetto_423bis: =>O@Chiunque ~CagionaIncendioBoschivo
CagionaIncendioBoschivo, Dolo {
  tipico_423bis: =>O@Giudice FattoTipico
  pena_423bis:   O(Sanziona) =>O@Giudice ReclusioneIncendioBoschivo
}

atom CagionaDisastroFerroviario: causes a railway disaster (art. 430) | quote: Disastro ferroviario | uri: examples/codice_penale/sources/codice_penale_full.md#L5865-L5869
atom ReclusioneDisastroFerroviario: reclusion 5-15 years (art. 430) | quote: Disastro ferroviario | uri: examples/codice_penale/sources/codice_penale_full.md#L5865-L5869
precetto_430: =>O@Chiunque ~CagionaDisastroFerroviario
CagionaDisastroFerroviario, Dolo {
  tipico_430: =>O@Giudice FattoTipico
  pena_430:   O(Sanziona) =>O@Giudice ReclusioneDisastroFerroviario
}

atom AttentaSicurezzaTrasporti: endangers the safety of public transport (art. 432) | quote: Attentati alla sicurezza dei trasporti | uri: examples/codice_penale/sources/codice_penale_full.md#L5884-L5892
atom ReclusioneAttentatoTrasporti: reclusion 1-5 years (art. 432) | quote: Attentati alla sicurezza dei trasporti | uri: examples/codice_penale/sources/codice_penale_full.md#L5884-L5892
precetto_432: =>O@Chiunque ~AttentaSicurezzaTrasporti
AttentaSicurezzaTrasporti, Dolo {
  tipico_432: =>O@Giudice FattoTipico
  pena_432:   O(Sanziona) =>O@Giudice ReclusioneAttentatoTrasporti
}

atom AttentaImpiantiEnergia: endangers the safety of electricity/gas installations or public communications (art. 433) | quote: Attentati alla sicurezza degli impianti di energia elettrica e del gas ovvero delle pubbliche comunicazioni | uri: examples/codice_penale/sources/codice_penale_full.md#L5896-L5904
atom ReclusioneAttentatoEnergia: reclusion 1-5 years (art. 433) | quote: Attentati alla sicurezza degli impianti di energia elettrica e del gas ovvero delle pubbliche comunicazioni | uri: examples/codice_penale/sources/codice_penale_full.md#L5896-L5904
precetto_433: =>O@Chiunque ~AttentaImpiantiEnergia
AttentaImpiantiEnergia, Dolo {
  tipico_433: =>O@Giudice FattoTipico
  pena_433:   O(Sanziona) =>O@Giudice ReclusioneAttentatoEnergia
}

atom FabbricaEsplodentiAttentato: to attack public safety, fabricates, holds or transports explosive or asphyxiating materials (art. 435) | quote: Fabbricazione o detenzione di materie esplodenti | uri: examples/codice_penale/sources/codice_penale_full.md#L5923-L5930
atom ReclusioneEsplodentiAttentato: reclusion 1-5 years (art. 435) | quote: Fabbricazione o detenzione di materie esplodenti | uri: examples/codice_penale/sources/codice_penale_full.md#L5923-L5930
precetto_435: =>O@Chiunque ~FabbricaEsplodentiAttentato
FabbricaEsplodentiAttentato, Dolo {
  tipico_435: =>O@Giudice FattoTipico
  pena_435:   O(Sanziona) =>O@Giudice ReclusioneEsplodentiAttentato
}

atom OmetteCauteleInfortuni: omits to place plants, apparatus or signs destined to prevent disasters or accidents at work, or removes/damages them (art. 437) | quote: Rimozione od omissione dolosa di cautele contro infortuni sul lavoro | uri: examples/codice_penale/sources/codice_penale_full.md#L5941-L5949
atom ReclusioneCauteleInfortuni: reclusion 6 months-5 years (art. 437) | quote: Rimozione od omissione dolosa di cautele contro infortuni sul lavoro | uri: examples/codice_penale/sources/codice_penale_full.md#L5941-L5949
precetto_437: =>O@Chiunque ~OmetteCauteleInfortuni
OmetteCauteleInfortuni, Dolo {
  tipico_437: =>O@Giudice FattoTipico
  pena_437:   O(Sanziona) =>O@Giudice ReclusioneCauteleInfortuni
}

atom AvvelenaAcque: poisons water or substances destined for food, before they are drawn or distributed (art. 439) | quote: Avvelenamento di acque o di sostanze alimentari | uri: examples/codice_penale/sources/codice_penale_full.md#L5961-L5969
atom ReclusioneAvvelenamento: reclusion not less than 15 years (art. 439) | quote: Avvelenamento di acque o di sostanze alimentari | uri: examples/codice_penale/sources/codice_penale_full.md#L5961-L5969
precetto_439: =>O@Chiunque ~AvvelenaAcque
AvvelenaAcque, Dolo {
  tipico_439: =>O@Giudice FattoTipico
  pena_439:   O(Sanziona) =>O@Giudice ReclusioneAvvelenamento
}

atom AdulteraCoseSalute: adulterates or counterfeits, dangerously to public health, things other than food destined for trade (art. 441) | quote: Adulterazione o contraffazione di altre cose in danno della pubblica salute | uri: examples/codice_penale/sources/codice_penale_full.md#L5985-L5991
atom ReclusioneAdulterazioneCose: reclusion 1-5 years or fine (art. 441) | quote: Adulterazione o contraffazione di altre cose in danno della pubblica salute | uri: examples/codice_penale/sources/codice_penale_full.md#L5985-L5991
precetto_441: =>O@Chiunque ~AdulteraCoseSalute
AdulteraCoseSalute, Dolo {
  tipico_441: =>O@Giudice FattoTipico
  pena_441:   O(Sanziona) =>O@Giudice ReclusioneAdulterazioneCose
}

atom CommercioAlimentiAdulterati: not having taken part in the forgery, holds for trade or markets adulterated/counterfeit food substances (art. 442) | quote: Commercio di sostanze alimentari contraffatte o adulterate | uri: examples/codice_penale/sources/codice_penale_full.md#L5992-L5999
atom ReclusioneCommercioAdulterati: the penalties of artt. 440-441 (art. 442) | quote: Commercio di sostanze alimentari contraffatte o adulterate | uri: examples/codice_penale/sources/codice_penale_full.md#L5992-L5999
precetto_442: =>O@Chiunque ~CommercioAlimentiAdulterati
CommercioAlimentiAdulterati, Dolo {
  tipico_442: =>O@Giudice FattoTipico
  pena_442:   O(Sanziona) =>O@Giudice ReclusioneCommercioAdulterati
}

atom CommercioMedicinaliGuasti: holds for trade, markets or administers spoiled medicines, dangerous to health (art. 443) | quote: Commercio o somministrazione di medicinali guasti | uri: examples/codice_penale/sources/codice_penale_full.md#L6000-L6006
atom ReclusioneMedicinaliGuasti: reclusion 6 months-3 years (art. 443) | quote: Commercio o somministrazione di medicinali guasti | uri: examples/codice_penale/sources/codice_penale_full.md#L6000-L6006
precetto_443: =>O@Chiunque ~CommercioMedicinaliGuasti
CommercioMedicinaliGuasti, Dolo {
  tipico_443: =>O@Giudice FattoTipico
  pena_443:   O(Sanziona) =>O@Giudice ReclusioneMedicinaliGuasti
}

atom CommercioAlimentiNocivi: holds for trade or distributes food substances dangerous to public health (art. 444) | quote: Commercio di sostanze alimentari nocive | uri: examples/codice_penale/sources/codice_penale_full.md#L6007-L6015
atom ReclusioneAlimentiNocivi: reclusion 6 months-3 years (art. 444) | quote: Commercio di sostanze alimentari nocive | uri: examples/codice_penale/sources/codice_penale_full.md#L6007-L6015
precetto_444: =>O@Chiunque ~CommercioAlimentiNocivi
CommercioAlimentiNocivi, Dolo {
  tipico_444: =>O@Giudice FattoTipico
  pena_444:   O(Sanziona) =>O@Giudice ReclusioneAlimentiNocivi
}

atom CagionaDisastroColposo: by negligence, causes a fire or another disaster against public safety (art. 449) | quote: Delitti colposi di danno | uri: examples/codice_penale/sources/codice_penale_full.md#L6059-L6067
atom ReclusioneDisastroColposo: reclusion 1-5 years (art. 449) | quote: Delitti colposi di danno | uri: examples/codice_penale/sources/codice_penale_full.md#L6059-L6067
precetto_449: =>O@Chiunque ~CagionaDisastroColposo
CagionaDisastroColposo, Colpa {
  tipico_449: =>O@Giudice FattoTipico
  pena_449:   O(Sanziona) =>O@Giudice ReclusioneDisastroColposo
}

atom OmetteCauteleColposo: by negligence, omits to place, or removes, apparatus/signs against disasters or accidents at work (art. 451) | quote: Omissione colposa di cautele o difese contro disastri o infortuni sul lavoro | uri: examples/codice_penale/sources/codice_penale_full.md#L6084-L6091
atom ReclusioneCauteleColposo: reclusion up to 1 year or fine (art. 451) | quote: Omissione colposa di cautele o difese contro disastri o infortuni sul lavoro | uri: examples/codice_penale/sources/codice_penale_full.md#L6084-L6091
precetto_451: =>O@Chiunque ~OmetteCauteleColposo
OmetteCauteleColposo, Colpa {
  tipico_451: =>O@Giudice FattoTipico
  pena_451:   O(Sanziona) =>O@Giudice ReclusioneCauteleColposo
}

atom DanneggiamentoSeguitoIncendio: to damage another's thing, sets fire to it, causing danger of fire (art. 424) | quote: Danneggiamento seguito da incendio | uri: examples/codice_penale/sources/codice_penale_full.md#L5791-L5799
atom ReclusioneDanneggiamentoIncendio: reclusion 6 months-2 years (art. 424) | quote: Danneggiamento seguito da incendio | uri: examples/codice_penale/sources/codice_penale_full.md#L5791-L5799
precetto_424: =>O@Chiunque ~DanneggiamentoSeguitoIncendio
DanneggiamentoSeguitoIncendio, Dolo {
  tipico_424: =>O@Giudice FattoTipico
  pena_424:   O(Sanziona) =>O@Giudice ReclusioneDanneggiamentoIncendio
}

atom DanneggiamentoSeguitoInondazione: to damage another's thing, breaks or deteriorates works causing danger of flood, landslide or avalanche (art. 427) | quote: Danneggiamento seguito da inondazione, frana o valanga | uri: examples/codice_penale/sources/codice_penale_full.md#L5829-L5837
atom ReclusioneDanneggiamentoInondazione: reclusion 1-5 years (art. 427) | quote: Danneggiamento seguito da inondazione, frana o valanga | uri: examples/codice_penale/sources/codice_penale_full.md#L5829-L5837
precetto_427: =>O@Chiunque ~DanneggiamentoSeguitoInondazione
DanneggiamentoSeguitoInondazione, Dolo {
  tipico_427: =>O@Giudice FattoTipico
  pena_427:   O(Sanziona) =>O@Giudice ReclusioneDanneggiamentoInondazione
}

atom PericoloDisastroFerroviario: to damage a railway, causes danger of a railway disaster (art. 431) | quote: Pericolo di disastro ferroviario causato da danneggiamento | uri: examples/codice_penale/sources/codice_penale_full.md#L5870-L5878
atom ReclusionePericoloFerroviario: reclusion 1-5 years (art. 431) | quote: Pericolo di disastro ferroviario causato da danneggiamento | uri: examples/codice_penale/sources/codice_penale_full.md#L5870-L5878
precetto_431: =>O@Chiunque ~PericoloDisastroFerroviario
PericoloDisastroFerroviario, Dolo {
  tipico_431: =>O@Giudice FattoTipico
  pena_431:   O(Sanziona) =>O@Giudice ReclusionePericoloFerroviario
}

atom SomministraMedicinaliPericolosi: exercising, even abusively, the sale of medicines, administers them in a way dangerous to public health (art. 445) | quote: Somministrazione di medicinali in modo pericoloso per la salute pubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L6017-L6024
atom ReclusioneMedicinaliPericolosi: reclusion 6 months-2 years (art. 445) | quote: Somministrazione di medicinali in modo pericoloso per la salute pubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L6017-L6024
precetto_445: =>O@Chiunque ~SomministraMedicinaliPericolosi
SomministraMedicinaliPericolosi, Dolo {
  tipico_445: =>O@Giudice FattoTipico
  pena_445:   O(Sanziona) =>O@Giudice ReclusioneMedicinaliPericolosi
}

atom PericoloDisastroColposo: by negligent act or omission, gives rise to or maintains the danger of a fire or other disaster (art. 450) | quote: Delitti colposi di pericolo | uri: examples/codice_penale/sources/codice_penale_full.md#L6074-L6082
atom ReclusionePericoloColposo: reclusion up to 2 years (art. 450) | quote: Delitti colposi di pericolo | uri: examples/codice_penale/sources/codice_penale_full.md#L6074-L6082
precetto_450: =>O@Chiunque ~PericoloDisastroColposo
PericoloDisastroColposo, Colpa {
  tipico_450: =>O@Giudice FattoTipico
  pena_450:   O(Sanziona) =>O@Giudice ReclusionePericoloColposo
}

atom DanneggiamentoSeguitoNaufragio: to damage a ship or aircraft, causes danger of shipwreck or air disaster (art. 429) | quote: Danneggiamento seguito da naufragio | uri: examples/codice_penale/sources/codice_penale_full.md#L5855-L5863
atom ReclusioneDanneggiamentoNaufragio: reclusion 1-5 years (art. 429) | quote: Danneggiamento seguito da naufragio | uri: examples/codice_penale/sources/codice_penale_full.md#L5855-L5863
precetto_429: =>O@Chiunque ~DanneggiamentoSeguitoNaufragio
DanneggiamentoSeguitoNaufragio, Dolo {
  tipico_429: =>O@Giudice FattoTipico
  pena_429:   O(Sanziona) =>O@Giudice ReclusioneDanneggiamentoNaufragio
}

atom SottraeApparecchiDifesa: on the occasion of a fire/disaster, subtracts, conceals or damages apparatus for public defence against accidents (art. 436) | quote: Sottrazione, occultamento o guasto di apparecchi a pubblica difesa da infortuni | uri: examples/codice_penale/sources/codice_penale_full.md#L5931-L5939
atom ReclusioneSottrazioneApparecchi: reclusion 1-5 years (art. 436) | quote: Sottrazione, occultamento o guasto di apparecchi a pubblica difesa da infortuni | uri: examples/codice_penale/sources/codice_penale_full.md#L5931-L5939
precetto_436: =>O@Chiunque ~SottraeApparecchiDifesa
SottraeApparecchiDifesa, Dolo {
  tipico_436: =>O@Giudice FattoTipico
  pena_436:   O(Sanziona) =>O@Giudice ReclusioneSottrazioneApparecchi
}

atom DelittiColposiSalute: by negligence, commits one of the facts against public health of artt. 439-444 (art. 452) | quote: Delitti colposi contro la salute pubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L6092-L6100
atom ReclusioneColposiSalute: reclusion, negligent crimes against public health (art. 452) | quote: Delitti colposi contro la salute pubblica | uri: examples/codice_penale/sources/codice_penale_full.md#L6092-L6100
precetto_452: =>O@Chiunque ~DelittiColposiSalute
DelittiColposiSalute, Colpa {
  tipico_452: =>O@Giudice FattoTipico
  pena_452:   O(Sanziona) =>O@Giudice ReclusioneColposiSalute
}
