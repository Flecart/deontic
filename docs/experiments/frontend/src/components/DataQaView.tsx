import React, { useEffect, useMemo, useState } from "react";
import { Card } from "./Card";
import { MarkdownView } from "./MarkdownView";
import type {
  QaCaseDetail,
  QaCasesResponse,
  QaDescriptions,
  QaStatute,
  QaValidationResponse,
} from "../types";

export interface DataQaViewProps {
  statute: QaStatute | null;
}

type QaTab = "cases" | "validation";

function shareClass(status: unknown): string {
  if (status === "obligatory") return "share-obligatory";
  if (status === "permitted") return "share-permitted";
  if (status === "forbidden") return "share-forbidden";
  return "";
}

function fmtVerdictValue(value: unknown): string {
  if (value === true) return "true";
  if (value === false) return "false";
  if (value == null) return "—";
  return String(value);
}

export const DataQaView: React.FC<DataQaViewProps> = ({ statute }) => {
  const [tab, setTab] = useState<QaTab>("cases");
  const [tier, setTier] = useState<string>("all");
  const [verdict, setVerdict] = useState<string>("all");
  const [leakyOnly, setLeakyOnly] = useState(false);
  const [disagreeOnly, setDisagreeOnly] = useState(false);
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [casesResp, setCasesResp] = useState<QaCasesResponse | null>(null);
  const [casesLoading, setCasesLoading] = useState(false);
  const [activeCaseId, setActiveCaseId] = useState<string | null>(null);
  const [detail, setDetail] = useState<QaCaseDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [descriptions, setDescriptions] = useState<QaDescriptions | null>(null);
  const [validation, setValidation] = useState<QaValidationResponse | null>(null);
  const [validationLoading, setValidationLoading] = useState(false);
  const [votesDisagreeOnly, setVotesDisagreeOnly] = useState(true);

  // Reset per-statute state when the statute changes.
  useEffect(() => {
    setTier("all");
    setVerdict("all");
    setLeakyOnly(false);
    setDisagreeOnly(false);
    setQuery("");
    setDebouncedQuery("");
    setActiveCaseId(null);
    setDetail(null);
    setCasesResp(null);
    setDescriptions(null);
    setValidation(null);
  }, [statute?.id]);

  useEffect(() => {
    const handle = window.setTimeout(() => setDebouncedQuery(query), 300);
    return () => window.clearTimeout(handle);
  }, [query]);

  useEffect(() => {
    if (!statute) return;
    let cancelled = false;
    const load = async () => {
      try {
        const res = await fetch(`/api/qa/${encodeURIComponent(statute.id)}/descriptions`);
        if (!res.ok) throw new Error(`descriptions fetch failed (${res.status})`);
        const data = (await res.json()) as QaDescriptions;
        if (!cancelled) setDescriptions(data);
      } catch {
        if (!cancelled) setDescriptions(null);
      }
    };
    void load();
    return () => {
      cancelled = true;
    };
  }, [statute?.id]);

  useEffect(() => {
    if (!statute) {
      setCasesResp(null);
      return;
    }
    let cancelled = false;
    const load = async () => {
      setCasesLoading(true);
      try {
        const params = new URLSearchParams({ limit: "1000" });
        if (tier !== "all") params.set("tier", tier);
        if (verdict !== "all") params.set("verdict", verdict);
        if (leakyOnly) params.set("leaky", "1");
        if (disagreeOnly) params.set("disagree", "1");
        if (debouncedQuery.trim()) params.set("q", debouncedQuery.trim());
        const res = await fetch(
          `/api/qa/${encodeURIComponent(statute.id)}/cases?${params}`
        );
        if (!res.ok) throw new Error(`cases fetch failed (${res.status})`);
        const data = (await res.json()) as QaCasesResponse;
        if (!cancelled) setCasesResp(data);
      } catch {
        if (!cancelled) setCasesResp(null);
      } finally {
        if (!cancelled) setCasesLoading(false);
      }
    };
    void load();
    return () => {
      cancelled = true;
    };
  }, [statute?.id, tier, verdict, leakyOnly, disagreeOnly, debouncedQuery]);

  const visibleCases = useMemo(() => casesResp?.cases ?? [], [casesResp]);

  useEffect(() => {
    if (!visibleCases.length) {
      setActiveCaseId(null);
      return;
    }
    if (!activeCaseId || !visibleCases.some((c) => c.case_id === activeCaseId)) {
      setActiveCaseId(visibleCases[0].case_id);
    }
  }, [visibleCases, activeCaseId]);

  useEffect(() => {
    if (!statute || !activeCaseId) {
      setDetail(null);
      return;
    }
    let cancelled = false;
    const load = async () => {
      setDetailLoading(true);
      try {
        const res = await fetch(
          `/api/qa/${encodeURIComponent(statute.id)}/cases/${encodeURIComponent(activeCaseId)}`
        );
        if (!res.ok) throw new Error(`case fetch failed (${res.status})`);
        const data = (await res.json()) as QaCaseDetail;
        if (!cancelled) setDetail(data);
      } catch {
        if (!cancelled) setDetail(null);
      } finally {
        if (!cancelled) setDetailLoading(false);
      }
    };
    void load();
    return () => {
      cancelled = true;
    };
  }, [statute?.id, activeCaseId]);

  useEffect(() => {
    if (!statute || tab !== "validation" || validation) return;
    let cancelled = false;
    const load = async () => {
      setValidationLoading(true);
      try {
        const res = await fetch(`/api/qa/${encodeURIComponent(statute.id)}/validation`);
        if (!res.ok) throw new Error(`validation fetch failed (${res.status})`);
        const data = (await res.json()) as QaValidationResponse;
        if (!cancelled) setValidation(data);
      } catch {
        if (!cancelled) setValidation(null);
      } finally {
        if (!cancelled) setValidationLoading(false);
      }
    };
    void load();
    return () => {
      cancelled = true;
    };
  }, [statute?.id, tab, validation]);

  const statusKey = casesResp?.status_key ?? statute?.status_key ?? null;
  const goldKeys = useMemo(
    () => (detail ? Object.keys(detail.case.gold) : []),
    [detail]
  );
  const atomCols = useMemo(() => {
    if (statute?.atoms.length) return statute.atoms;
    if (detail) return Object.keys(detail.case.assignment).sort();
    return [];
  }, [statute, detail]);

  if (!statute) {
    return (
      <Card>
        <Card.Header>
          <h1>Data QA</h1>
        </Card.Header>
        <Card.Body>
          <p>Select a statute (A–F) from the sidebar to audit its generated cases.</p>
        </Card.Body>
      </Card>
    );
  }

  const visibleInstances = (validation?.instances ?? []).filter(
    (inst) => !votesDisagreeOnly || inst.disagree
  );

  return (
    <div className="run-view">
      <Card className="run-view-section run-view-hero">
        <Card.Header>
          <div className="hero-header">
            <div>
              <h1>{statute.label}</h1>
              <p>
                Case bank <code>{statute.case_bank}</code> scored against{" "}
                <code>{statute.results_file}</code>.
              </p>
            </div>
            <div className="metric-strip">
              <div className="metric-pill">
                <span className="metric-label">Cases</span>
                <strong>{statute.case_count}</strong>
              </div>
              <div className="metric-pill">
                <span className="metric-label">Result rows</span>
                <strong>{statute.result_rows}</strong>
              </div>
              <div className="metric-pill">
                <span className="metric-label">Models</span>
                <strong>{statute.models.length}</strong>
              </div>
              <div className="metric-pill">
                <span className="metric-label">Atoms</span>
                <strong>{statute.atoms.length}</strong>
              </div>
            </div>
          </div>
        </Card.Header>
        <Card.Body>
          <div className="tabs-row">
            <button
              type="button"
              className={"tab" + (tab === "cases" ? " tab--active" : " tab--inactive")}
              onClick={() => setTab("cases")}
            >
              Cases
            </button>
            <button
              type="button"
              className={"tab" + (tab === "validation" ? " tab--active" : " tab--inactive")}
              onClick={() => setTab("validation")}
              disabled={!statute.has_validation}
              title={statute.has_validation ? undefined : "No bank_validation.jsonl for this statute"}
            >
              Bank validation
            </button>
          </div>
        </Card.Body>
      </Card>

      {tab === "cases" ? (
        <>
          <Card className="run-view-section">
            <Card.Header>
              <h2>Filters</h2>
            </Card.Header>
            <Card.Body>
              <div className="controls-row">
                <label>
                  Tier
                  <select value={tier} onChange={(e) => setTier(e.target.value)}>
                    <option value="all">All tiers</option>
                    <option value="0">Tier 0 (closed bank)</option>
                    <option value="1">Tier 1 (near variants)</option>
                    <option value="2">Tier 2 (world shift)</option>
                  </select>
                </label>
                <label>
                  Gold verdict
                  <select value={verdict} onChange={(e) => setVerdict(e.target.value)}>
                    <option value="all">All verdicts</option>
                    {statute.verdicts.map((v) => (
                      <option key={v} value={v}>
                        {v}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={leakyOnly}
                    onChange={(e) => setLeakyOnly(e.target.checked)}
                  />
                  Leak-flagged only
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={disagreeOnly}
                    onChange={(e) => setDisagreeOnly(e.target.checked)}
                  />
                  With disagreements only
                </label>
                <label>
                  Search
                  <input
                    type="search"
                    className="qa-search"
                    placeholder="free text over the narration…"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                  />
                </label>
              </div>
              <p className="main-subtle">
                Showing {visibleCases.length} of {statute.case_count} cases
                {casesLoading ? " (loading…)" : ""}
              </p>
            </Card.Body>
          </Card>

          <div className="run-view-grid">
            <Card className="run-view-section">
              <Card.Header>
                <h2>Cases</h2>
              </Card.Header>
              <Card.Body>
                {visibleCases.length ? (
                  <div className="case-list case-list--tall">
                    {visibleCases.map((c) => (
                      <button
                        key={c.case_id}
                        type="button"
                        className={
                          "case-row case-row--bank" +
                          (c.case_id === activeCaseId ? " case-row--active" : "") +
                          (c.leak_flags.length ? " case-row--leaky" : "")
                        }
                        onClick={() => setActiveCaseId(c.case_id)}
                      >
                        <span className="case-row-name">{c.case_id}</span>
                        <span
                          className={`case-row-share ${shareClass(
                            statusKey ? c.gold[statusKey] : null
                          )}`}
                        >
                          {fmtVerdictValue(statusKey ? c.gold[statusKey] : null)}
                        </span>
                        <span className="case-row-disp">
                          t{c.tier}
                          {c.variant != null ? ` · v${c.variant}` : ""}
                          {" · "}
                          <span className={c.wrong_rows ? "qa-wrong-count" : "qa-clean-count"}>
                            {c.wrong_rows}/{c.total_rows} wrong
                          </span>
                          {c.leak_flags.length ? ` · leak: ${c.leak_flags.join(",")}` : ""}
                        </span>
                      </button>
                    ))}
                  </div>
                ) : (
                  <p>No cases match the current filters.</p>
                )}
              </Card.Body>
            </Card>

            <Card className="run-view-section run-view-span-2">
              <Card.Header>
                <h2>{detail ? detail.case.case_id : "Case detail"}</h2>
              </Card.Header>
              <Card.Body>
                {detailLoading ? <p className="main-subtle">Loading case…</p> : null}
                {!detailLoading && detail ? (
                  <>
                    <div className="case-meta-strip">
                      <span className="case-meta-pill">
                        Tier <strong>{detail.case.tier}</strong>
                      </span>
                      {detail.case.variant != null ? (
                        <span className="case-meta-pill">
                          Variant <strong>{detail.case.variant}</strong>
                        </span>
                      ) : null}
                      {detail.case.acted != null ? (
                        <span className="case-meta-pill">
                          {detail.case.acted ? "Hand-off acted" : "Pending hand-off"}
                        </span>
                      ) : null}
                      {goldKeys.map((k) => (
                        <span
                          key={k}
                          className={`case-meta-pill ${
                            k === statusKey ? shareClass(detail.case.gold[k]) : ""
                          }`}
                        >
                          {k}: <strong>{fmtVerdictValue(detail.case.gold[k])}</strong>
                        </span>
                      ))}
                      {detail.case.leak_flags.length ? (
                        <span className="case-meta-pill meta-bad">
                          leaky: <strong>{detail.case.leak_flags.join(", ")}</strong>
                        </span>
                      ) : null}
                    </div>

                    <div className="facts-block narrative-block">
                      <div className="section-kicker">Narration</div>
                      <div className="narrative-panel">
                        <MarkdownView content={detail.case.narrative} />
                      </div>
                    </div>

                    <div className="facts-block">
                      <div className="section-kicker">
                        Gold atom assignment + descriptions
                      </div>
                      <div className="qa-atom-list">
                        {atomCols.map((atom) => (
                          <details key={atom} className="qa-atom-desc">
                            <summary>
                              <span
                                className={
                                  "atom-chip " +
                                  (detail.case.assignment[atom]
                                    ? "atom-chip--true"
                                    : "atom-chip--false")
                                }
                              >
                                {atom}:{" "}
                                {detail.case.assignment[atom] ? "true" : "false"}
                              </span>
                            </summary>
                            <div className="qa-atom-desc-body">
                              <p>
                                <strong>Open (intension):</strong>{" "}
                                {descriptions?.atoms[atom]?.open ?? "(no descriptions.py entry)"}
                              </p>
                              <p>
                                <strong>Closed (enumeration):</strong>{" "}
                                {descriptions?.atoms[atom]?.closed ?? "(no descriptions.py entry)"}
                              </p>
                            </div>
                          </details>
                        ))}
                      </div>
                    </div>

                    <div className="facts-block">
                      <div className="section-kicker">
                        Model × arm predictions ({detail.results.length} rows —
                        mismatches vs gold highlighted)
                      </div>
                      <div className="qa-table-wrap">
                        <table className="qa-table">
                          <thead>
                            <tr>
                              <th>Model</th>
                              <th>Arm</th>
                              {goldKeys.map((k) => (
                                <th key={k}>{k}</th>
                              ))}
                              {atomCols.map((a) => (
                                <th key={a} className="qa-th-atom">
                                  {a}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            <tr className="qa-row--gold">
                              <td colSpan={2}>gold</td>
                              {goldKeys.map((k) => (
                                <td key={k}>{fmtVerdictValue(detail.case.gold[k])}</td>
                              ))}
                              {atomCols.map((a) => (
                                <td key={a}>{detail.case.assignment[a] ? "T" : "F"}</td>
                              ))}
                            </tr>
                            {detail.results.map((r, idx) => (
                              <tr
                                key={`${r.model}-${r.arm}-${idx}`}
                                className={r.verdict_wrong ? "qa-row--wrong" : ""}
                              >
                                <td>{r.model && r.model !== "-" ? r.model : "—"}</td>
                                <td>{r.arm}</td>
                                {goldKeys.map((k) => (
                                  <td
                                    key={k}
                                    className={r.wrong_fields.includes(k) ? "qa-cell--bad" : ""}
                                  >
                                    {fmtVerdictValue(r.pred_verdict[k])}
                                  </td>
                                ))}
                                {atomCols.map((a) => (
                                  <td
                                    key={a}
                                    className={r.wrong_atoms.includes(a) ? "qa-cell--bad" : ""}
                                  >
                                    {r.pred_assignment == null
                                      ? "—"
                                      : r.pred_assignment[a]
                                        ? "T"
                                        : "F"}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </>
                ) : null}
                {!detailLoading && !detail ? (
                  <p>Select a case to inspect narration, gold labels, and predictions.</p>
                ) : null}
              </Card.Body>
            </Card>
          </div>
        </>
      ) : (
        <Card className="run-view-section">
          <Card.Header>
            <div className="inspector-header">
              <div>
                <h2>Bank validation</h2>
                <p className="main-subtle">
                  Dual-model annotator votes per bank instance (
                  {validation ? `${validation.disagreements} of ${validation.total}` : "…"}{" "}
                  instances have at least one vote against gold).
                </p>
              </div>
              <label className="controls-row-inline">
                <input
                  type="checkbox"
                  checked={votesDisagreeOnly}
                  onChange={(e) => setVotesDisagreeOnly(e.target.checked)}
                />
                Disagreements only
              </label>
            </div>
          </Card.Header>
          <Card.Body>
            {validationLoading ? <p className="main-subtle">Loading votes…</p> : null}
            {!validationLoading && validation ? (
              visibleInstances.length ? (
                <div className="qa-validation-list">
                  {visibleInstances.map((inst) => (
                    <div
                      key={`${inst.atom}-${inst.bank}-${inst.id}`}
                      className={"qa-vote-card" + (inst.disagree ? " qa-vote-card--bad" : "")}
                    >
                      <div className="failure-card-head">
                        <span className="items-atom">{inst.atom}</span>
                        <span className="items-id">
                          {inst.bank} / {inst.id}
                        </span>
                        <span
                          className={
                            "badge " + (inst.gold_member ? "badge--member" : "badge--nonmember")
                          }
                        >
                          gold: {inst.gold_member ? "member" : "non-member"}
                        </span>
                      </div>
                      {Object.entries(inst.votes).map(([model, vote]) => (
                        <div key={model} className="qa-vote-row">
                          <span
                            className={
                              vote.annot_member === inst.gold_member ? "hit-ok" : "hit-miss"
                            }
                          >
                            {vote.annot_member ? "member" : "non-member"}
                          </span>
                          <span className="qa-vote-model">{model}</span>
                          <span className="qa-vote-reason">
                            {vote.reason || "(no reason logged)"}
                          </span>
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              ) : (
                <p>
                  {votesDisagreeOnly
                    ? "No annotator disagreements with gold for this statute."
                    : "No bank validation rows for this statute."}
                </p>
              )
            ) : null}
            {!validationLoading && !validation ? (
              <p>No bank validation data for this statute.</p>
            ) : null}
          </Card.Body>
        </Card>
      )}
    </div>
  );
};
