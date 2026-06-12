import React, { useEffect, useMemo, useState } from "react";
import { Card } from "./Card";
import { MarkdownView } from "./MarkdownView";
import { ModelIoView } from "./ModelIoView";
import type { CaseBankDetail, ExpACase, LlmCall } from "../types";

export interface CaseBankViewProps {
  bank: CaseBankDetail | null;
}

type FilterAll = "all";

function assignmentOf(c: ExpACase): string {
  return c.case_id.split("_")[0] ?? c.case_id;
}

function shareClass(status: string): string {
  if (status === "obligatory") return "share-obligatory";
  if (status === "permitted") return "share-permitted";
  if (status === "forbidden") return "share-forbidden";
  return "";
}

function polarityLabel(polarity: boolean): string {
  return polarity ? "present" : "absent";
}

export const CaseBankView: React.FC<CaseBankViewProps> = ({ bank }) => {
  const [tier, setTier] = useState<number | FilterAll>("all");
  const [variant, setVariant] = useState<number | FilterAll>("all");
  const [acted, setActed] = useState<"all" | "acted" | "pending">("all");
  const [shareStatus, setShareStatus] = useState<string>("all");
  const [assignment, setAssignment] = useState<string>("all");
  const [leaky, setLeaky] = useState<"all" | "clean" | "leaky">("all");
  const [activeCaseId, setActiveCaseId] = useState<string | null>(null);
  const [promptArm, setPromptArm] = useState("ground_open");
  const [promptCalls, setPromptCalls] = useState<LlmCall[]>([]);
  const [promptLoading, setPromptLoading] = useState(false);
  const [activeCallIdx, setActiveCallIdx] = useState(0);

  const llmArms = bank?.meta.llm_arms ?? [
    "ground_closed",
    "ground_open",
    "holistic",
    "staged_open",
    "staged_closed",
  ];

  const assignments = useMemo(() => {
    if (!bank) return [];
    return [...new Set(bank.cases.map(assignmentOf))].sort();
  }, [bank]);

  const visibleCases = useMemo(() => {
    if (!bank) return [];
    return bank.cases.filter((c) => {
      if (tier !== "all" && c.tier !== tier) return false;
      if (variant !== "all" && c.variant !== variant) return false;
      if (acted === "acted" && !c.acted) return false;
      if (acted === "pending" && c.acted) return false;
      if (shareStatus !== "all" && c.gold.share_status !== shareStatus) return false;
      if (assignment !== "all" && assignmentOf(c) !== assignment) return false;
      if (leaky === "leaky" && !c.leak_flags.length) return false;
      if (leaky === "clean" && c.leak_flags.length) return false;
      return true;
    });
  }, [bank, tier, variant, acted, shareStatus, assignment, leaky]);

  useEffect(() => {
    if (!visibleCases.length) {
      setActiveCaseId(null);
      return;
    }
    if (!activeCaseId || !visibleCases.some((c) => c.case_id === activeCaseId)) {
      setActiveCaseId(visibleCases[0].case_id);
    }
  }, [visibleCases, activeCaseId]);

  const selected = useMemo(
    () => visibleCases.find((c) => c.case_id === activeCaseId) ?? null,
    [visibleCases, activeCaseId]
  );

  useEffect(() => {
    if (!llmArms.includes(promptArm)) {
      setPromptArm(llmArms[0] ?? "ground_open");
    }
  }, [llmArms, promptArm]);

  useEffect(() => {
    setActiveCallIdx(0);
  }, [activeCaseId, promptArm]);

  useEffect(() => {
    if (!bank || !selected) {
      setPromptCalls([]);
      return;
    }
    let cancelled = false;
    const load = async () => {
      setPromptLoading(true);
      try {
        const params = new URLSearchParams({
          bank: bank.name,
          case: selected.case_id,
          arm: promptArm,
        });
        const res = await fetch(`/api/sources/expA/prompts?${params}`);
        if (!res.ok) throw new Error(`prompt fetch failed (${res.status})`);
        const data = (await res.json()) as { calls: LlmCall[] };
        if (!cancelled) setPromptCalls(data.calls ?? []);
      } catch {
        if (!cancelled) setPromptCalls([]);
      } finally {
        if (!cancelled) setPromptLoading(false);
      }
    };
    void load();
    return () => {
      cancelled = true;
    };
  }, [bank, selected, promptArm]);

  const selectedCall = promptCalls[activeCallIdx] ?? null;

  if (!bank) {
    return (
      <Card>
        <Card.Header>
          <h1>Case bank</h1>
        </Card.Header>
        <Card.Body>
          <p>Select a case bank from the sidebar to browse generated Experiment A cases.</p>
        </Card.Body>
      </Card>
    );
  }

  const summary = bank.summary;

  return (
    <div className="run-view">
      <Card className="run-view-section run-view-hero">
        <Card.Header>
          <div className="hero-header">
            <div>
              <h1>{bank.name.replace(/\.jsonl$/, "")}</h1>
              <p>
                Experiment A generated cases — latent assignment, bank instantiation,
                engine gold, and narrative memo.
              </p>
            </div>
            <div className="metric-strip">
              <div className="metric-pill">
                <span className="metric-label">Cases</span>
                <strong>{summary.case_count}</strong>
              </div>
              <div className="metric-pill">
                <span className="metric-label">Assignments</span>
                <strong>{summary.assignment_count}</strong>
              </div>
              <div className="metric-pill">
                <span className="metric-label">Acted</span>
                <strong>{summary.acted_count}</strong>
              </div>
              <div className="metric-pill">
                <span className="metric-label">Leaky</span>
                <strong>{summary.leaky_count}</strong>
              </div>
            </div>
          </div>
        </Card.Header>
        <Card.Body>
          <div className="hero-grid">
            <div className="hero-panel">
              <div className="section-kicker">By tier</div>
              <ul className="summary-facts">
                {Object.entries(summary.by_tier).map(([t, n]) => (
                  <li key={t}>
                    <span>Tier {t}</span> <strong>{n}</strong>
                  </li>
                ))}
              </ul>
            </div>
            <div className="hero-panel">
              <div className="section-kicker">Share status (gold)</div>
              <ul className="summary-facts">
                {Object.entries(summary.by_share_status).map(([s, n]) => (
                  <li key={s}>
                    <span>{s}</span> <strong>{n}</strong>
                  </li>
                ))}
              </ul>
            </div>
            <div className="hero-panel">
              <div className="section-kicker">Acted split</div>
              <ul className="summary-facts">
                <li>
                  <span>Pending hand-off</span> <strong>{summary.pending_count}</strong>
                </li>
                <li>
                  <span>Already acted</span> <strong>{summary.acted_count}</strong>
                </li>
              </ul>
            </div>
          </div>
        </Card.Body>
      </Card>

      <Card className="run-view-section">
        <Card.Header>
          <h2>Filters</h2>
        </Card.Header>
        <Card.Body>
          <div className="controls-row">
            <label>
              Tier
              <select value={String(tier)} onChange={(e) => setTier(e.target.value === "all" ? "all" : Number(e.target.value))}>
                <option value="all">All tiers</option>
                <option value="0">Tier 0 (closed bank)</option>
                <option value="1">Tier 1 (near variants)</option>
                <option value="2">Tier 2 (world shift)</option>
              </select>
            </label>
            <label>
              Variant
              <select value={String(variant)} onChange={(e) => setVariant(e.target.value === "all" ? "all" : Number(e.target.value))}>
                <option value="all">All variants</option>
                <option value="0">Variant 0</option>
                <option value="1">Variant 1</option>
              </select>
            </label>
            <label>
              Hand-off
              <select value={acted} onChange={(e) => setActed(e.target.value as typeof acted)}>
                <option value="all">All</option>
                <option value="pending">Pending (not acted)</option>
                <option value="acted">Acted</option>
              </select>
            </label>
            <label>
              Share status
              <select value={shareStatus} onChange={(e) => setShareStatus(e.target.value)}>
                <option value="all">All</option>
                <option value="obligatory">Obligatory</option>
                <option value="permitted">Permitted</option>
                <option value="forbidden">Forbidden</option>
              </select>
            </label>
            <label>
              Assignment
              <select value={assignment} onChange={(e) => setAssignment(e.target.value)}>
                <option value="all">All assignments</option>
                {assignments.map((a) => (
                  <option key={a} value={a}>
                    {a}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Leak check
              <select value={leaky} onChange={(e) => setLeaky(e.target.value as typeof leaky)}>
                <option value="all">All</option>
                <option value="clean">Clean only</option>
                <option value="leaky">Leaky only</option>
              </select>
            </label>
          </div>
          <p className="main-subtle">
            Showing {visibleCases.length} of {bank.cases.length} cases
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
                    <span className={`case-row-share ${shareClass(c.gold.share_status)}`}>
                      {c.gold.share_status}
                    </span>
                    <span className="case-row-disp">
                      t{c.tier} · v{c.variant} · {c.acted ? "acted" : "pending"}
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
            <h2>{selected ? selected.case_id : "Case detail"}</h2>
          </Card.Header>
          <Card.Body>
            {selected ? (
              <>
                <div className="case-meta-strip">
                  <span className="case-meta-pill">
                    Tier <strong>{selected.tier}</strong>
                  </span>
                  <span className="case-meta-pill">
                    Variant <strong>{selected.variant}</strong>
                  </span>
                  <span className="case-meta-pill">
                    {selected.acted ? "Hand-off acted" : "Pending hand-off"}
                  </span>
                  <span className={`case-meta-pill ${shareClass(selected.gold.share_status)}`}>
                    share: <strong>{selected.gold.share_status}</strong>
                  </span>
                  {selected.acted ? (
                    <>
                      <span className={`case-meta-pill ${selected.gold.violation ? "meta-bad" : "meta-ok"}`}>
                        violation: <strong>{String(selected.gold.violation)}</strong>
                      </span>
                      <span className={`case-meta-pill ${selected.gold.notify_required ? "meta-warn" : "meta-ok"}`}>
                        notify: <strong>{String(selected.gold.notify_required)}</strong>
                      </span>
                    </>
                  ) : null}
                  {selected.leak_flags.length ? (
                    <span className="case-meta-pill meta-bad">
                      leaky: <strong>{selected.leak_flags.join(", ")}</strong>
                    </span>
                  ) : null}
                </div>

                <div className="facts-block">
                  <div className="section-kicker">Latent assignment (ground truth)</div>
                  <div className="assignment-grid">
                    {Object.entries(selected.assignment)
                      .sort(([a], [b]) => a.localeCompare(b))
                      .map(([atom, val]) => (
                        <span
                          key={atom}
                          className={"atom-chip " + (val ? "atom-chip--true" : "atom-chip--false")}
                        >
                          {atom}: {val ? "true" : "false"}
                        </span>
                      ))}
                  </div>
                </div>

                <div className="facts-block">
                  <div className="section-kicker">Bank items ({selected.items.length})</div>
                  <div className="items-table">
                    <div className="items-table-header">
                      <span>Atom</span>
                      <span>Instance</span>
                      <span>Polarity</span>
                      <span>Phrase</span>
                    </div>
                    {selected.items.map((item) => (
                      <div key={`${item.atom}-${item.id}`} className="items-table-row">
                        <span className="items-atom">{item.atom}</span>
                        <span className="items-id">{item.id}</span>
                        <span className={item.polarity ? "polarity-present" : "polarity-absent"}>
                          {polarityLabel(item.polarity)}
                        </span>
                        <span className="items-phrase">{item.phrase}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="facts-block narrative-block">
                  <div className="section-kicker">Narrative memo</div>
                  <div className="narrative-panel">
                    <MarkdownView content={selected.narrative} />
                  </div>
                </div>
              </>
            ) : (
              <p>Select a case to inspect assignment, items, gold labels, and narrative.</p>
            )}
          </Card.Body>
        </Card>
      </div>

      <Card className="run-view-section model-io-card">
        <Card.Header>
          <div className="inspector-header">
            <div>
              <h2>LLM prompt preview</h2>
              <p className="main-subtle">
                Exact user message(s) reconstructed from <code>arms.py</code> for the
                selected case and arm.
              </p>
            </div>
            <label className="inspector-call-select">
              Arm
              <select value={promptArm} onChange={(e) => setPromptArm(e.target.value)}>
                {llmArms.map((arm) => (
                  <option key={arm} value={arm}>
                    {arm}
                  </option>
                ))}
              </select>
            </label>
            {promptCalls.length > 1 ? (
              <label className="inspector-call-select">
                LLM call
                <select
                  value={activeCallIdx}
                  onChange={(e) => setActiveCallIdx(Number(e.target.value))}
                >
                  {promptCalls.map((call, idx) => (
                    <option key={idx} value={idx}>
                      Call {idx + 1}
                      {call.atom ? ` · ${call.atom}` : ""}
                    </option>
                  ))}
                </select>
              </label>
            ) : null}
          </div>
        </Card.Header>
        <Card.Body>
          {promptLoading ? <p className="main-subtle">Loading prompt…</p> : null}
          {!promptLoading && selectedCall ? (
            <ModelIoView call={selectedCall} />
          ) : null}
          {!promptLoading && selected && !promptCalls.length ? (
            <p>
              Arm <strong>{promptArm}</strong> does not call the model (oracle/program).
            </p>
          ) : null}
          {!selected ? <p>Select a case to preview its LLM prompts.</p> : null}
        </Card.Body>
      </Card>
    </div>
  );
};
