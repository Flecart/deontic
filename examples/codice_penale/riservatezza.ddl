# Codice Penale — riservatezza (generato da spec hand-decomposte, tools/gen.py).
# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).
from definizioni.ddl import *

facts:

atom ProcuraNotizieVitaPrivata: by visual or sound recording instruments, unduly obtains news or images of another's private life in places of private dwelling (art. 615-bis) | quote: Interferenze illecite nella vita privata | uri: examples/codice_penale/sources/codice_penale_full.md#L8818-L8826
atom ReclusioneInterferenze: reclusion 6 months-4 years (art. 615-bis) | quote: Interferenze illecite nella vita privata | uri: examples/codice_penale/sources/codice_penale_full.md#L8818-L8826
precetto_615bis: =>O@Chiunque ~ProcuraNotizieVitaPrivata
ProcuraNotizieVitaPrivata, Dolo {
  proc_615bis:   Querela =>O@Giudice Procedibile
  tipico_615bis: O(Procedibile) =>O@Giudice FattoTipico
  pena_615bis:   O(Sanziona) =>O@Giudice ReclusioneInterferenze
}

atom AccedeAbusivamenteSistema: abusively enters a computer or telematic system protected by security measures, or stays there against the holder's will (art. 615-ter) | quote: Accesso abusivo ad un sistema informatico o telematico | uri: examples/codice_penale/sources/codice_penale_full.md#L8841-L8849
atom ReclusioneAccessoAbusivo: reclusion up to 3 years (art. 615-ter) | quote: Accesso abusivo ad un sistema informatico o telematico | uri: examples/codice_penale/sources/codice_penale_full.md#L8841-L8849
precetto_615ter: =>O@Chiunque ~AccedeAbusivamenteSistema
AccedeAbusivamenteSistema, Dolo {
  tipico_615ter: =>O@Giudice FattoTipico
  pena_615ter:   O(Sanziona) =>O@Giudice ReclusioneAccessoAbusivo
}

atom PrendeCognizioneCorrispondenza: takes cognisance of correspondence not addressed to them, or subtracts/suppresses/diverts it (art. 616) | quote: Violazione, sottrazione e soppressione di corrispondenza | uri: examples/codice_penale/sources/codice_penale_full.md#L8902-L8910
atom ReclusioneViolazioneCorrispondenza: reclusion up to 1 year or fine, a querela (art. 616) | quote: Violazione, sottrazione e soppressione di corrispondenza | uri: examples/codice_penale/sources/codice_penale_full.md#L8902-L8910
precetto_616: =>O@Chiunque ~PrendeCognizioneCorrispondenza
PrendeCognizioneCorrispondenza, Dolo {
  proc_616:   Querela =>O@Giudice Procedibile
  tipico_616: O(Procedibile) =>O@Giudice FattoTipico
  pena_616:   O(Sanziona) =>O@Giudice ReclusioneViolazioneCorrispondenza
}

atom IntercettaComunicazioni: fraudulently takes cognisance of, or interrupts/impedes, telegraphic or telephone communications between others (art. 617) | quote: Cognizione interruzione o impedimento illeciti di comunicazioni o conversazioni telegrafiche o telefoniche | uri: examples/codice_penale/sources/codice_penale_full.md#L8924-L8932
atom ReclusioneIntercettazione: reclusion 6 months-4 years (art. 617) | quote: Cognizione interruzione o impedimento illeciti di comunicazioni o conversazioni telegrafiche o telefoniche | uri: examples/codice_penale/sources/codice_penale_full.md#L8924-L8932
precetto_617: =>O@Chiunque ~IntercettaComunicazioni
IntercettaComunicazioni, Dolo {
  tipico_617: =>O@Giudice FattoTipico
  pena_617:   O(Sanziona) =>O@Giudice ReclusioneIntercettazione
}

atom RivelaCorrispondenza: having abusively learned the content of correspondence, reveals it without just cause, to another's harm (art. 618) | quote: Rivelazione del contenuto di corrispondenza | uri: examples/codice_penale/sources/codice_penale_full.md#L9027-L9035
atom ReclusioneRivelazioneCorrisp: reclusion up to 6 months or fine (art. 618) | quote: Rivelazione del contenuto di corrispondenza | uri: examples/codice_penale/sources/codice_penale_full.md#L9027-L9035
precetto_618: =>O@Chiunque ~RivelaCorrispondenza
RivelaCorrispondenza, Dolo {
  proc_618:   Querela =>O@Giudice Procedibile
  tipico_618: O(Procedibile) =>O@Giudice FattoTipico
  pena_618:   O(Sanziona) =>O@Giudice ReclusioneRivelazioneCorrisp
}

atom RivelaSegretoProfessionale: having learned a secret by reason of their state, office or profession, reveals it without just cause, to another's harm (art. 622) | quote: Rivelazione di segreto professionale | uri: examples/codice_penale/sources/codice_penale_full.md#L9080-L9088
atom ReclusioneSegretoProfessionale: reclusion up to 1 year or fine, a querela (art. 622) | quote: Rivelazione di segreto professionale | uri: examples/codice_penale/sources/codice_penale_full.md#L9080-L9088
precetto_622: =>O@Chiunque ~RivelaSegretoProfessionale
RivelaSegretoProfessionale, Dolo {
  proc_622:   Querela =>O@Giudice Procedibile
  tipico_622: O(Procedibile) =>O@Giudice FattoTipico
  pena_622:   O(Sanziona) =>O@Giudice ReclusioneSegretoProfessionale
}

atom RivelaSegretiIndustriali: having learned, by reason of office, scientific or industrial secrets, reveals them or uses them to another's profit (art. 623) | quote: Rivelazione di segreti scientifici o industriali | uri: examples/codice_penale/sources/codice_penale_full.md#L9094-L9102
atom ReclusioneSegretiIndustriali: reclusion up to 2 years (art. 623) | quote: Rivelazione di segreti scientifici o industriali | uri: examples/codice_penale/sources/codice_penale_full.md#L9094-L9102
precetto_623: =>O@Chiunque ~RivelaSegretiIndustriali
RivelaSegretiIndustriali, Dolo {
  proc_623:   Querela =>O@Giudice Procedibile
  tipico_623: O(Procedibile) =>O@Giudice FattoTipico
  pena_623:   O(Sanziona) =>O@Giudice ReclusioneSegretiIndustriali
}

atom DetieneCodiciAccesso: to profit or harm, abusively procures, holds or diffuses access codes to a protected computer system (art. 615-quater) | quote: Detenzione e diffusione abusiva di codici di accesso a sistemi informatici o telematici | uri: examples/codice_penale/sources/codice_penale_full.md#L8873-L8881
atom ReclusioneCodiciAccesso: reclusion up to 1 year and fine (art. 615-quater) | quote: Detenzione e diffusione abusiva di codici di accesso a sistemi informatici o telematici | uri: examples/codice_penale/sources/codice_penale_full.md#L8873-L8881
precetto_615quater: =>O@Chiunque ~DetieneCodiciAccesso
DetieneCodiciAccesso, Dolo {
  tipico_615quater: =>O@Giudice FattoTipico
  pena_615quater:   O(Sanziona) =>O@Giudice ReclusioneCodiciAccesso
}

atom DiffondeProgrammiDannosi: to damage or interrupt a computer system, diffuses apparatus, devices or programs apt to do so (art. 615-quinquies) | quote: Diffusione di apparecchiature, dispositivi o programmi informatici diretti a danneggiare o interrompere un sistema | uri: examples/codice_penale/sources/codice_penale_full.md#L8886-L8894
atom ReclusioneProgrammiDannosi: reclusion up to 2 years and fine (art. 615-quinquies) | quote: Diffusione di apparecchiature, dispositivi o programmi informatici diretti a danneggiare o interrompere un sistema | uri: examples/codice_penale/sources/codice_penale_full.md#L8886-L8894
precetto_615quinquies: =>O@Chiunque ~DiffondeProgrammiDannosi
DiffondeProgrammiDannosi, Dolo {
  tipico_615quinquies: =>O@Giudice FattoTipico
  pena_615quinquies:   O(Sanziona) =>O@Giudice ReclusioneProgrammiDannosi
}

atom IntercettaComunicazioniInformatiche: fraudulently intercepts, impedes or interrupts computer or telematic communications (art. 617-quater) | quote: Intercettazione, impedimento o interruzione illecita di comunicazioni informatiche o telematiche | uri: examples/codice_penale/sources/codice_penale_full.md#L8978-L8986
atom ReclusioneIntercettInformatica: reclusion 6 months-4 years (art. 617-quater) | quote: Intercettazione, impedimento o interruzione illecita di comunicazioni informatiche o telematiche | uri: examples/codice_penale/sources/codice_penale_full.md#L8978-L8986
precetto_617quater: =>O@Chiunque ~IntercettaComunicazioniInformatiche
IntercettaComunicazioniInformatiche, Dolo {
  tipico_617quater: =>O@Giudice FattoTipico
  pena_617quater:   O(Sanziona) =>O@Giudice ReclusioneIntercettInformatica
}

atom ViolaCorrispondenzaAddetto: a person employed in the postal/telegraph service, abusing their office, takes cognisance of, subtracts or suppresses correspondence (art. 619) | quote: Violazione, sottrazione e soppressione di corrispondenza commesse da persona addetta al servizio delle poste, dei | uri: examples/codice_penale/sources/codice_penale_full.md#L9041-L9049
atom ReclusioneCorrispondenzaAddetto: reclusion 6 months-3 years (art. 619) | quote: Violazione, sottrazione e soppressione di corrispondenza commesse da persona addetta al servizio delle poste, dei | uri: examples/codice_penale/sources/codice_penale_full.md#L9041-L9049
precetto_619: =>O@Chiunque ~ViolaCorrispondenzaAddetto
ViolaCorrispondenzaAddetto, Dolo {
  tipico_619: =>O@Giudice FattoTipico
  pena_619:   O(Sanziona) =>O@Giudice ReclusioneCorrispondenzaAddetto
}

atom RivelaDocumentiSegreti: having abusively learned the content of secret documents, reveals it without just cause, to another's harm (art. 621) | quote: Rivelazione del contenuto di documenti segreti | uri: examples/codice_penale/sources/codice_penale_full.md#L9062-L9070
atom ReclusioneDocumentiSegreti: reclusion up to 3 years or fine (art. 621) | quote: Rivelazione del contenuto di documenti segreti | uri: examples/codice_penale/sources/codice_penale_full.md#L9062-L9070
precetto_621: =>O@Chiunque ~RivelaDocumentiSegreti
RivelaDocumentiSegreti, Dolo {
  proc_621:   Querela =>O@Giudice Procedibile
  tipico_621: O(Procedibile) =>O@Giudice FattoTipico
  pena_621:   O(Sanziona) =>O@Giudice ReclusioneDocumentiSegreti
}

atom InstallaApparecchiIntercettazione: installs apparatus apt to intercept or impede telegraphic or telephone communications between others (art. 617-bis) | quote: Installazione di apparecchiature atte ad intercettare od impedire comunicazioni o conversazioni telegrafiche o | uri: examples/codice_penale/sources/codice_penale_full.md#L8943-L8951
atom ReclusioneInstallazioneIntercett: reclusion 1-4 years (art. 617-bis) | quote: Installazione di apparecchiature atte ad intercettare od impedire comunicazioni o conversazioni telegrafiche o | uri: examples/codice_penale/sources/codice_penale_full.md#L8943-L8951
precetto_617bis: =>O@Chiunque ~InstallaApparecchiIntercettazione
InstallaApparecchiIntercettazione, Dolo {
  tipico_617bis: =>O@Giudice FattoTipico
  pena_617bis:   O(Sanziona) =>O@Giudice ReclusioneInstallazioneIntercett
}

atom FalsificaComunicazioni: forms a false telegraphic/telephone communication, or alters/suppresses the content of a true one (art. 617-ter) | quote: Falsificazione, alterazione o soppressione del contenuto di comunicazioni o conversazioni telegrafiche o telefoniche | uri: examples/codice_penale/sources/codice_penale_full.md#L8961-L8969
atom ReclusioneFalsoComunicazioni: reclusion 1-4 years (art. 617-ter) | quote: Falsificazione, alterazione o soppressione del contenuto di comunicazioni o conversazioni telegrafiche o telefoniche | uri: examples/codice_penale/sources/codice_penale_full.md#L8961-L8969
precetto_617ter: =>O@Chiunque ~FalsificaComunicazioni
FalsificaComunicazioni, Dolo {
  tipico_617ter: =>O@Giudice FattoTipico
  pena_617ter:   O(Sanziona) =>O@Giudice ReclusioneFalsoComunicazioni
}

atom InstallaApparecchiInformatici: installs apparatus apt to intercept, impede or interrupt computer or telematic communications (art. 617-quinquies) | quote: Installazione di apparecchiature atte ad intercettare, impedire o interrompere comunicazioni informatiche o telematiche | uri: examples/codice_penale/sources/codice_penale_full.md#L9004-L9012
atom ReclusioneInstallazioneInformatica: reclusion 1-4 years (art. 617-quinquies) | quote: Installazione di apparecchiature atte ad intercettare, impedire o interrompere comunicazioni informatiche o telematiche | uri: examples/codice_penale/sources/codice_penale_full.md#L9004-L9012
precetto_617quinquies: =>O@Chiunque ~InstallaApparecchiInformatici
InstallaApparecchiInformatici, Dolo {
  tipico_617quinquies: =>O@Giudice FattoTipico
  pena_617quinquies:   O(Sanziona) =>O@Giudice ReclusioneInstallazioneInformatica
}

atom FalsificaComunicazioniInformatiche: to profit or harm, forms a false computer/telematic communication, or alters/suppresses a true one (art. 617-sexies) | quote: Falsificazione, alterazione o soppressione del contenuto di comunicazioni informatiche o telematiche | uri: examples/codice_penale/sources/codice_penale_full.md#L9014-L9022
atom ReclusioneFalsoInformatico: reclusion 1-4 years (art. 617-sexies) | quote: Falsificazione, alterazione o soppressione del contenuto di comunicazioni informatiche o telematiche | uri: examples/codice_penale/sources/codice_penale_full.md#L9014-L9022
precetto_617sexies: =>O@Chiunque ~FalsificaComunicazioniInformatiche
FalsificaComunicazioniInformatiche, Dolo {
  tipico_617sexies: =>O@Giudice FattoTipico
  pena_617sexies:   O(Sanziona) =>O@Giudice ReclusioneFalsoInformatico
}
