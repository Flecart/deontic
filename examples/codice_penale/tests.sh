#!/usr/bin/env bash
# Testcases for the element-level Codice Penale formalization.
# Run from the repo root:  bash examples/codice_penale/tests.sh
# Each offence is the CONJUNCTION of its elements: a positive case (all elements
# -> O(pena)), negatives where ONE element is missing (-> no offence), and a
# justification case (-> non punibile, inherited from the parte generale).
set -u
cd "$(dirname "$0")/../.." || exit 2
DEO=./.lake/build/bin/deontic
OMI=examples/codice_penale/omicidio.ddl
FUR=examples/codice_penale/furto.ddl
RAP=examples/codice_penale/rapina.ddl
PAT=examples/codice_penale/patrimonio.ddl
LES=examples/codice_penale/lesioni.ddl
LIB=examples/codice_penale/liberta.ddl
PA=examples/codice_penale/pubblica_amministrazione.ddl
GIU=examples/codice_penale/giustizia.ddl
FED=examples/codice_penale/fede_pubblica.ddl
OP=examples/codice_penale/ordine_pubblico.ddl
IP=examples/codice_penale/incolumita_pubblica.ddl
PEX=examples/codice_penale/persona_extra.ddl
FAM=examples/codice_penale/famiglia.ddl
PA2=examples/codice_penale/patrimonio2.ddl
STA=examples/codice_penale/stato.ddl
ORD=examples/codice_penale/ordine_autorita.ddl
PER2=examples/codice_penale/persona2.ddl
ONO=examples/codice_penale/onore.ddl
PA3=examples/codice_penale/pa2.ddl
IC2=examples/codice_penale/incolumita2.ddl
MOR=examples/codice_penale/moralita.ddl
FA2=examples/codice_penale/famiglia2.ddl
[ -x "$DEO" ] || { echo "build first: lake build deontic"; exit 2; }
pass=0; fail=0

expect_status() {  # FILE ATOM ASSUME EXPECTED DESC
  local out got
  out=$("$DEO" query "$1" "$2" --assume "$3" 2>/dev/null)
  got=$(printf '%s\n' "$out" | grep -E "^[[:space:]]*$2 : " | sed -E 's/.* : //; s/\(.*//')
  if [ "$got" = "$4" ]; then pass=$((pass+1)); printf 'ok   %-54s %s(%s)\n' "$5" "$4" "$2"
  else fail=$((fail+1)); printf 'FAIL %-54s want %s got %s  [%s]\n' "$5" "$4" "${got:-none}" "$2"; fi
}
expect_judge() {  # FILE ASSUME DESC
  if "$DEO" check "$1" --assume "$2" 2>/dev/null | grep -qi 'unresolved obligation conflict'; then
    pass=$((pass+1)); printf 'ok   %-54s [JUDGE]\n' "$3"
  else fail=$((fail+1)); printf 'FAIL %-54s expected [JUDGE]\n' "$3"; fi
}

# Base = all constitutive elements of the offence present.
BO="CagionaMorte,Dolo"
BF="Impossessamento,CosaMobileAltrui,Sottrazione,FineDiProfitto"

echo "== OMICIDIO (artt. 575-577): evento + dolo =="
expect_status "$OMI" CagionaMorte  "$BO"                              F "uccidere è vietato (precetto)"
expect_status "$OMI" Sanziona      "$BO"                              O "morte + dolo: omicidio punibile"
expect_status "$OMI" Reclusione575 "$BO"                              O "pena base: reclusione >= 21 anni"
expect_status "$OMI" Sanziona      "CagionaMorte"                     P "morte SENZA dolo: non è omicidio doloso"
expect_status "$OMI" Ergastolo     "$BO,Premeditazione"               O "art.576/577 premeditazione: ergastolo"
expect_status "$OMI" Reclusione575 "$BO,Premeditazione"               P "ergastolo scavalca (overrides) la reclusione base"
expect_status "$OMI" Ergastolo     "$BO,ControAscendenteDiscendente"  O "art.577 contro ascendente: ergastolo (atomo condiviso)"
expect_status "$OMI" Sanziona      "$BO,PericoloAttuale,DifesaProporzionata" F "art.52 legittima difesa: non punibile"
expect_status "$OMI" Sanziona      "$BO,PericoloAttuale"              O "art.52 senza proporzione: punibile"
expect_status "$OMI" Sanziona      "$BO,VizioTotaleMente"             F "art.88 vizio totale: non punibile"
expect_status "$OMI" Sanziona      "$BO,VizioTotaleMente,Preordinato" O "art.87 actio libera in causa: punibile"
expect_status "$OMI" Sanziona      "$BO,StatoNecessita"               F "art.54 stato di necessità: non punibile"
expect_status "$OMI" Sanziona      "$BO,StatoNecessita,DovereEsporsi" O "art.54 c.2 dovere di esporsi: punibile"
expect_status "$OMI" Sanziona      "$BO,MinoreAnni14"                 F "art.97 minore di 14: non punibile"

echo "== FURTO (art. 624-625): impossessamento+altruità+sottrazione+profitto =="
expect_status "$FUR" Sottrazione      "$BF,Querela"                   F "sottrarre la cosa altrui è vietato (precetto)"
expect_status "$FUR" Sanziona         "$BF,Querela"                   O "tutti gli elementi + querela: furto punibile"
expect_status "$FUR" ReclusioneFurto  "$BF,Querela"                   O "pena base del furto"
expect_status "$FUR" Sanziona "Impossessamento,CosaMobileAltrui,Sottrazione,Querela" P "manca il FINE DI PROFITTO: niente furto"
expect_status "$FUR" Sanziona "CosaMobileAltrui,Sottrazione,FineDiProfitto,Querela"  P "manca l'IMPOSSESSAMENTO: niente furto"
expect_status "$FUR" Sanziona         "$BF"                           P "manca la querela e non aggravato: improcedibile"
expect_status "$FUR" Sanziona         "$BF,ViolenzaSulleCose"         O "art.625 violenza sulle cose: d'ufficio"
expect_status "$FUR" ReclusioneFurtoAggravata "$BF,Destrezza"         O "art.625 destrezza: pena aggravata"
expect_status "$FUR" ReclusioneFurto  "$BF,Destrezza"                 P "aggravante scavalca (overrides) la pena base"
expect_status "$FUR" Sanziona         "$BF,Querela,StatoNecessita"    F "scriminante ereditata anche nel furto"

echo "== RAPINA (art. 628): furto (elementi condivisi) + violenza/minaccia =="
expect_status "$RAP" ReclusioneRapina "$BF,Violenza"                  O "furto + violenza = rapina (d'ufficio)"
expect_status "$RAP" ReclusioneRapina "$BF,Minaccia"                  O "furto + minaccia = rapina"
expect_status "$RAP" Sanziona         "$BF"                           P "stessi elementi SENZA violenza: NON è rapina"
expect_status "$RAP" Sanziona         "$BF,Violenza,StatoNecessita"   F "scriminante ereditata anche nella rapina"
# stesso insieme di fatti -> furto vs rapina secondo la presenza della violenza:
expect_status "$FUR" ReclusioneFurto  "$BF,Querela"                   O "  (controprova: gli stessi 4 elementi + querela sono furto)"

echo "== LESIONI (artt. 581-590): gradazione per elementi =="
expect_status "$LES" ReclusionePercosse      "Percuote,Dolo,Querela"                          O "percosse (581), a querela"
expect_status "$LES" ReclusioneLesione       "CagionaLesione,MalattiaCorpoMente,Dolo,Querela" O "lesione (582): la malattia eleva a lesione"
expect_status "$LES" ReclusionePercosse      "Percuote,CagionaLesione,MalattiaCorpoMente,Dolo,Querela" P "la lesione scavalca le percosse (581 c.1)"
expect_status "$LES" ReclusioneLesioneGrave  "CagionaLesione,MalattiaCorpoMente,Dolo,LesioneGrave" O "lesione grave (583), d'ufficio"
expect_status "$LES" ReclusionePreterint     "AttiDirettiLesione,CagionaMorte"                O "omicidio preterintenzionale (584)"
expect_status "$LES" ReclusioneLesioneColposa "CagionaLesione,Colpa"                          O "lesioni colpose (590): colpa, non dolo"
expect_status "$LES" Sanziona                "CagionaLesione,MalattiaCorpoMente,Dolo,Querela,StatoNecessita" F "scriminante ereditata"

echo "== LIBERTÀ INDIVIDUALE (artt. 605, 610, 612) =="
expect_status "$LIB" ReclusioneSequestro      "PrivaLibertaPersonale,Dolo"           O "sequestro di persona (605)"
expect_status "$LIB" ReclusioneViolPrivata    "Costringe,Violenza,Dolo"              O "violenza privata (610) con violenza"
expect_status "$LIB" ReclusioneViolPrivata    "Costringe,Minaccia,Dolo"              O "violenza privata (610) con minaccia (oneof)"
expect_status "$LIB" Sanziona                 "Costringe,Dolo"                       P "costrizione senza violenza né minaccia: niente reato"
expect_status "$LIB" MultaMinaccia            "MinacciaIngiustoDanno,Dolo,Querela"   O "minaccia semplice (612 c.1), a querela"
expect_status "$LIB" ReclusioneMinacciaGrave  "MinacciaIngiustoDanno,Dolo,MinacciaGrave" O "minaccia grave (612 c.2), d'ufficio"
expect_status "$LIB" MultaMinaccia            "MinacciaIngiustoDanno,Dolo,MinacciaGrave" P "minaccia grave scavalca la multa base"

echo "== PATRIMONIO oltre furto/rapina (artt. 629-648) =="
expect_status "$PAT" ReclusioneEstorsione "Costringe,Minaccia,IngiustoProfittoAltruiDanno,Dolo" O "estorsione (629) = violenza privata + profitto"
expect_status "$PAT" ReclusioneDanneggiamento "Distrugge,Dolo,Querela"                          O "danneggiamento (635), a querela"
expect_status "$PAT" ReclusioneDanneggiamentoViolento "Distrugge,Dolo,Violenza"                 O "danneggiamento violento (635 c.2), d'ufficio"
expect_status "$PAT" ReclusioneDanneggiamento "Distrugge,Dolo,Violenza"                          P "  e scavalca (overrides) il danneggiamento base"
expect_status "$PAT" ReclusioneTruffa     "ArtifiziRaggiri,IngiustoProfittoAltruiDanno,Dolo"    O "truffa (640)"
expect_status "$PAT" ReclusioneAppropriazione "SiAppropria,FineDiProfitto,Dolo,Querela"          O "appropriazione indebita (646)"
expect_status "$PAT" ReclusioneRicettazione "AcquistaRiceveOcculta,ProvenienzaDelitto,FineDiProfitto,Dolo" O "ricettazione (648)"
expect_status "$PAT" Sanziona "AcquistaRiceveOcculta,FineDiProfitto,Dolo"                        P "ricettazione senza provenienza delittuosa: niente reato"

echo "== PUBBLICA AMMINISTRAZIONE (artt. 314-337) =="
expect_status "$PA" ReclusionePeculato      "QualificaPubblica,PossessoPerUfficio,SiAppropria,Dolo" O "peculato (314)"
expect_status "$PA" Sanziona                "PossessoPerUfficio,SiAppropria,Dolo"                P "peculato senza qualifica pubblica: niente reato"
expect_status "$PA" ReclusioneCorruzione318 "QualificaPubblica,RiceveUtilitaNonDovuta,PerAttoUfficio,Dolo"        O "corruzione per atto d'ufficio (318)"
expect_status "$PA" ReclusioneCorruzione319 "QualificaPubblica,RiceveUtilitaNonDovuta,PerAttoContrarioDoveri,Dolo" O "corruzione per atto contrario (319)"
expect_status "$PA" ReclusioneAbuso         "QualificaPubblica,ViolazioneNorme,IngiustoVantaggioODanno,Dolo"     O "abuso d'ufficio (323)"
expect_status "$PA" ReclusioneViolenzaPU    "Violenza,ControPubblicoUfficiale,PerCostringereAtto,Dolo"           O "violenza a pubblico ufficiale (336)"
expect_status "$PA" ReclusioneResistenza    "Minaccia,ControPubblicoUfficiale,PerOpporsiAtto,Dolo"               O "resistenza a pubblico ufficiale (337, minaccia)"

echo "== AMMINISTRAZIONE DELLA GIUSTIZIA (artt. 368, 372, 378) =="
expect_status "$GIU" ReclusioneCalunnia           "IncolpaInnocente,Dolo"                              O "calunnia (368)"
expect_status "$GIU" ReclusioneFalsaTestimonianza "TestimoneAutorita,AffermaFalsoNegaVero,Dolo"        O "falsa testimonianza (372)"
expect_status "$GIU" ReclusioneFavoreggiamento    "DelittoAltruiCommesso,AiutaEludereIndagini,FuoriConcorso,Dolo" O "favoreggiamento personale (378)"
expect_status "$GIU" Sanziona                     "DelittoAltruiCommesso,AiutaEludereIndagini,Dolo"   P "favoreggiamento ma concorrente nel reato: niente 378"

echo "== FEDE PUBBLICA (artt. 479, 481, 485, 494) =="
expect_status "$FED" ReclusioneFalsoIdeologico  "QualificaPubblica,AttoNelleFunzioni,AttestaFalso,Dolo"  O "falsità ideologica del PU (479)"
expect_status "$FED" ReclusioneFalsoCertificato "ServizioPubblicaNecessita,AttestaFalsoCertificato,Dolo" O "falsità in certificati (481)"
expect_status "$FED" ReclusioneFalsoScrittura   "FormaScritturaFalsa,NeFaUso,FineVantaggioODanno,Dolo"   O "falsità in scrittura privata (485)"
expect_status "$FED" Sanziona                   "FormaScritturaFalsa,FineVantaggioODanno,Dolo"           P "scrittura falsa ma non usata: niente 485"
expect_status "$FED" ReclusioneSostituzione     "SostituiscePersona,FineVantaggioODanno,Dolo"            O "sostituzione di persona (494)"

echo "== ORDINE PUBBLICO (artt. 414, 416) =="
expect_status "$OP" ReclusioneIstigazione "IstigaPubblicamente,Dolo"                       O "istigazione a delinquere (414)"
expect_status "$OP" ReclusioneAssociazione "TrePiuPersoneAssociate,PromuoveOrganizza,Dolo" O "associazione per delinquere (416)"

echo "== INCOLUMITÀ PUBBLICA (artt. 422, 423, 438) — ergastolo condiviso =="
expect_status "$IP" Ergastolo          "AttiPericoloIncolumita,FineDiUccidere,MorteDiPiuPersone,Dolo" O "strage (422) -> ergastolo"
expect_status "$IP" Sanziona           "AttiPericoloIncolumita,FineDiUccidere,Dolo"          P "strage senza morte di più persone: niente reato"
expect_status "$IP" ReclusioneIncendio "CagionaIncendio,Dolo"                                O "incendio (423)"
expect_status "$IP" Ergastolo          "CagionaEpidemia,Dolo"                                O "epidemia (438) -> ergastolo (stesso atomo)"

echo "== ALTRI CONTRO LA PERSONA (578, 580, 591, 593, 600, 609-bis, 614) =="
expect_status "$PEX" ReclusioneInfanticidio   "MadreNeonato,CagionaMorte,AbbandonoMaterialeMorale,Dolo" O "infanticidio (578)"
expect_status "$PEX" Sanziona                 "DeterminaAlSuicidio,Dolo"                          P "istigazione al suicidio ma il suicidio non avviene: niente 580"
expect_status "$PEX" ReclusioneIstigSuicidio  "DeterminaAlSuicidio,SuicidioAvviene,Dolo"          O "istigazione al suicidio (580), se avviene"
expect_status "$PEX" ReclusioneViolenzaSessuale "AttiSessualiCostretti,AbusoAutorita,Dolo"         O "violenza sessuale (609-bis) per abuso di autorità"
expect_status "$PEX" ReclusioneSchiavitu      "EsercitaPoteriProprieta,Dolo"                      O "riduzione in schiavitù (600)"
expect_status "$PEX" ReclusioneViolazioneDomicilio "IntroduceDomicilio,Dolo"                      O "violazione di domicilio (614)"

echo "== FAMIGLIA (570, 572, 574) + usura (644) =="
expect_status "$FAM" ReclusioneMaltrattamenti "Maltratta,Dolo"                                    O "maltrattamenti in famiglia (572)"
expect_status "$FAM" ReclusioneSottrazioneMinore "SottraeMinore,Dolo"                             O "sottrazione di persone incapaci (574)"
expect_status "$PAT" ReclusioneUsura          "FaDarePromettereInteressiUsurari,Dolo"             O "usura (644)"

echo "== ALTRO PATRIMONIO (626, 630, 633, 634, 642, 643, 647) =="
expect_status "$PA2" ReclusioneSequestroEstorsione "SequestraPersona,ScopoPrezzoLiberazione,Dolo" O "sequestro a scopo di estorsione (630)"
expect_status "$PA2" Ergastolo          "SequestraPersona,ScopoPrezzoLiberazione,MorteSequestrato,Dolo" O "  con morte del sequestrato -> ergastolo"
expect_status "$PA2" ReclusioneSequestroEstorsione "SequestraPersona,ScopoPrezzoLiberazione,MorteSequestrato,Dolo" P "  e la pena base è scavalcata"
expect_status "$PA2" ReclusioneTurbativa "TurbaPossesso,Minaccia,Dolo"                       O "turbativa violenta del possesso (634)"
expect_status "$PA2" ReclusioneCirconvenzione "AbusaInfermitaBisogni,FineDiProfitto,Dolo"    O "circonvenzione di incapaci (643)"

echo "== PERSONALITÀ DELLO STATO (270, 283, 284, 285, 289) =="
expect_status "$STA" ReclusioneAttentatoCost "AttoViolentoMutareCostituzione,Dolo"            O "attentato contro la costituzione (283)"
expect_status "$STA" Ergastolo          "PromuoveInsurrezioneArmata,Dolo"                     O "insurrezione armata (284) -> ergastolo condiviso"
expect_status "$STA" Ergastolo          "FattoDevastazioneStrage,ScopoSicurezzaStato,Dolo"    O "devastazione/saccheggio/strage (285) -> ergastolo"

echo "== GENERATI da spec hand-decomposte (589, 595, 328, 426, 440, 527, 556, ...) =="
expect_status "$PER2" ReclusioneOmicidioColposo "CagionaMorte,Colpa"                          O "omicidio colposo (589): colpa"
expect_status "$ONO"  ReclusioneDiffamazione "ComunicaPiuPersone,OffendeReputazione,Dolo,Querela" O "diffamazione (595), a querela"
expect_status "$ONO"  Sanziona              "ComunicaPiuPersone,OffendeReputazione,Dolo"      P "diffamazione senza querela: improcedibile"
expect_status "$PA3"  ReclusioneRifiutoAtti "QualificaPubblica,RifiutaAttoUfficio,Dolo"       O "rifiuto di atti d'ufficio (328)"
expect_status "$IC2"  ReclusioneInondazione "CagionaInondazioneFrana,Dolo"                    O "inondazione/frana/valanga (426)"
expect_status "$IC2"  ReclusioneAdulterazione "AdulteraSostanzeAlimentari,Dolo"               O "adulterazione di alimenti (440)"
expect_status "$MOR"  ReclusioneAttiOsceni  "LuogoPubblico,CompieAttiOsceni,Dolo"             O "atti osceni (527)"
expect_status "$FA2"  ReclusioneBigamia     "GiaSposato,ContraeAltroMatrimonio,Dolo"          O "bigamia (556)"
expect_status examples/codice_penale/pa3.ddl ReclusioneConcussione "QualificaPubblica,AbusaQualitaPoteri,CostringeDareUtilita,Dolo" O "concussione (317)"
expect_status examples/codice_penale/pa3.ddl ReclusioneMalversazione "OttenutoContributiPubblici,DistraeDallaFinalita,Dolo" O "malversazione (316-bis, label senza trattino)"
expect_status examples/codice_penale/giustizia2.ddl ReclusioneFalsaPerizia "PeritoInterprete,ParereMendace,Dolo" O "falsa perizia (373)"
# tutti i file generati da spec caricano senza errori
gfail=0; gn=0
for f in $(python3 - <<'PY'
import re
seen=[]
for l in open("examples/codice_penale/tools/specs.txt"):
    m=re.match(r"@\S+\s+(\S+)",l)
    if m and m.group(1) not in seen: seen.append(m.group(1))
print(" ".join("examples/codice_penale/%s.ddl"%s for s in seen for s in [s]))
PY
); do gn=$((gn+1)); err=$("$DEO" check "$f" 2>&1 >/dev/null | grep -i '^Error'); [ -z "$err" ] || { gfail=$((gfail+1)); echo "  LOAD FAIL $(basename "$f"): $err"; }; done
if [ "$gfail" -eq 0 ]; then pass=$((pass+1)); printf 'ok   %-54s %d file\n' "tutti i file generati da spec caricano" "$gn"; else fail=$((fail+1)); printf 'FAIL %d file generati non caricano\n' "$gfail"; fi

echo "== ORDINE DELLA PUBBLICA AUTORITÀ (art. 51 c.3-4) =="
expect_status "$ORD" Sanziona "$BO,OrdineEseguito"                    O "esegue l'ordine, nessun errore: risponde"
expect_judge  "$ORD" "$BO,OrdineEseguito,ErroreSullOrdine"           "esegue + errore sulla legittimità: il giudice decide"

echo
echo "passed: $pass   failed: $fail"
[ "$fail" -eq 0 ]
