import React, { useEffect, useMemo, useState } from "react";
import { Card } from "./Card";
import { MarkdownView } from "./MarkdownView";
import type { CaseResult, LlmCall, RunDetail } from "../types";

export interface RunViewProps {
  run: RunDetail | null;
  failuresOnly: boolean;
}

function hitMark(ok: boolean | null | undefined): { label: string; className: string } {
  if (ok === null || ok === undefined) {
    return { label: "n/a", className: "hit-na" };
  }
  return ok
    ? { label: "OK", className: "hit-ok" }
    : { label: "MISS", className: "hit-miss" };
}

function caseHasFailure(c: CaseResult): boolean {
  const dimMiss = Object.values(c.hits).some((v) => v === false);
  const fa = c.facts_agreement;
  const factMiss = Boolean(fa && (fa[2]?.length || fa[3]?.length));
  return dimMiss || factMiss;
}

function parseReplyJson(reply: string): Record<string, unknown> {
  const m = reply.match(/\{[\s\S]*\}/);
  if (!m) return {};
  try {
    const parsed = JSON.parse(m[0]) as unknown;
    return parsed && typeof parsed === "object" ? (parsed as Record<string, unknown>) : {};
  } catch {
    return {};
  }
}

function parseReplyFacts(reply: string): string[] {
  const parsed = parseReplyJson(reply);
  const facts = parsed.facts ?? parsed.oracle_facts;
  return Array.isArray(facts) ? facts.map(String) : [];
}

function parseReplyReasoning(reply: string): string {
  const parsed = parseReplyJson(reply);
  if (typeof parsed.reasoning === "string") return parsed.reasoning;
  if (typeof parsed.notes === "string") return parsed.notes;
  return reply.slice(0, 400);
}

function fmtValue(v: unknown): string {
  if (Array.isArray(v)) return v.join(", ");
  return String(v ?? "—");
}

function fmtScore(score: string | null | undefined): string {
  if (!score) return "—";
  const m = /^(\d+)\/(\d+)$/.exec(score);
  if (!m) return score;
  const ok = Number(m[1]);
  const total = Number(m[2]);
  if (total === 0) return score;
  const pct = Math.round((ok / total) * 100);
  return `${score} (${pct}%)`;
}

function callLabel(call: LlmCall, index: number): string {
  const batch =
    call.batch != null && call.batches != null
      ? `batch ${call.batch}/${call.batches}`
      : "single call";
  return `Call ${index + 1} · ${batch} · ${call.seconds?.toFixed(1) ?? "?"}s`;
}

function caseKey(c: CaseResult): string {
  return `${c.id}\0${c.arm}`;
}

function defaultCaseKey(cases: CaseResult[]): string | null {
  if (!cases.length) return null;
  const withCalls = cases.find((c) => c.calls.length > 0);
  return caseKey(withCalls ?? cases[0]);
}

export const RunView: React.FC<RunViewProps> = ({ run, failuresOnly }) => {
  const [activeCaseKey, setActiveCaseKey] = useState<string | null>(null);
  const [activeCallIdx, setActiveCallIdx] = useState(0);

  const visibleCases = useMemo(() => {
    if (!run) return [];
    return failuresOnly ? run.cases.filter(caseHasFailure) : run.cases;
  }, [run, failuresOnly]);

  useEffect(() => {
    if (!visibleCases.length) {
      setActiveCaseKey(null);
      return;
    }
    if (!activeCaseKey || !visibleCases.some((c) => caseKey(c) === activeCaseKey)) {
      setActiveCaseKey(defaultCaseKey(visibleCases));
    }
  }, [visibleCases, activeCaseKey]);

  const selectedCase = useMemo(
    () => visibleCases.find((c) => caseKey(c) === activeCaseKey) ?? null,
    [visibleCases, activeCaseKey]
  );

  useEffect(() => {
    setActiveCallIdx(0);
  }, [activeCaseKey]);

  const selectedCall = selectedCase?.calls[activeCallIdx] ?? null;

  if (!run) {
    return (
      <Card>
        <Card.Header>
          <h1>Run details</h1>
        </Card.Header>
        <Card.Body>
          <p>Select a pipeline run from the sidebar to inspect scores, failures, and LLM calls.</p>
        </Card.Body>
      </Card>
    );
  }

  const meta = run.meta;
  const scores = run.summary.scores;
  const byArm = run.summary.by_arm ?? {};
  const armRows = Object.entries(byArm);
  const isLabel = run.kind === "label";

  return (
    <div className="run-view">
      <Card className="run-view-section run-view-hero">
        <Card.Header>
          <div className="hero-header">
            <div>
              <h1>{run.name.replace(/\.jsonl$/, "")}</h1>
              <p>
                {isLabel
                  ? "Gold-label draft — model transcription from withheld tribunal reasoning."
                  : "Eval run — oracle / ground / llm arms scored on disposition, exemption engagement, PI direction, and per-atom facts."}
              </p>
            </div>
            {isLabel ? (
              <div className="metric-strip">
                <div className="metric-pill">
                  <span className="metric-label">Labels</span>
                  <strong>{run.cases.length}</strong>
                </div>
                <div className="metric-pill">
                  <span className="metric-label">LLM calls</span>
                  <strong>{run.summary.llm_calls}</strong>
                </div>
              </div>
            ) : (
              <div className="metric-strip">
                <div className="metric-pill">
                  <span className="metric-label">Disposition</span>
                  <strong>{scores.disposition ?? "—"}</strong>
                </div>
                <div className="metric-pill">
                  <span className="metric-label">Engaged</span>
                  <strong>{scores.engaged ?? "—"}</strong>
                </div>
                <div className="metric-pill">
                  <span className="metric-label">PI balance</span>
                  <strong>{scores.pi ?? "—"}</strong>
                </div>
                <div className="metric-pill">
                  <span className="metric-label">Facts</span>
                  <strong>{scores.facts ?? "—"}</strong>
                </div>
              </div>
            )}
          </div>
        </Card.Header>
        <Card.Body>
          <div className="hero-grid">
            <div className="hero-panel">
              <div className="section-kicker">Run config</div>
              <ul className="summary-facts">
                <li>
                  <span>Model</span> <strong>{String(meta.model ?? "—")}</strong>
                </li>
                <li>
                  <span>Arms</span>{" "}
                  <strong>{Array.isArray(meta.arms) ? meta.arms.join(", ") : "—"}</strong>
                </li>
                <li>
                  <span>Atoms / call</span>{" "}
                  <strong>{String(meta.atoms_per_call ?? "all")}</strong>
                </li>
                <li>
                  <span>Seed</span> <strong>{String(meta.seed ?? "—")}</strong>
                </li>
              </ul>
            </div>
            <div className="hero-panel">
              <div className="section-kicker">API usage</div>
              <ul className="summary-facts">
                <li>
                  <span>LLM calls</span> <strong>{run.summary.llm_calls}</strong>
                </li>
                <li>
                  <span>Prompt tokens</span>{" "}
                  <strong>{run.summary.prompt_tokens.toLocaleString()}</strong>
                </li>
                <li>
                  <span>Completion tokens</span>{" "}
                  <strong>{run.summary.completion_tokens.toLocaleString()}</strong>
                </li>
                <li>
                  <span>Latency</span> <strong>{run.summary.seconds}s</strong>
                </li>
              </ul>
            </div>
          </div>
        </Card.Body>
      </Card>

      {!isLabel && armRows.length > 0 ? (
        <Card className="run-view-section">
          <Card.Header>
            <h2>Scores by arm</h2>
            <p className="main-subtle">
              Per-arm precision — oracle (verified facts → engine), ground (LLM facts →
              engine), llm (holistic, no engine).
            </p>
          </Card.Header>
          <Card.Body>
            <div className="execution-table arm-scores-table">
              <div className="execution-table-header">
                <span>Arm</span>
                <span>Cases</span>
                <span>Disposition</span>
                <span>Engaged</span>
                <span>PI</span>
                <span>Facts</span>
                <span>Failures</span>
              </div>
              {armRows.map(([arm, row]) => (
                <div key={arm} className="execution-table-row">
                  <span className="arm-name">{arm}</span>
                  <span>{row.cases}</span>
                  <span>{fmtScore(row.scores.disposition)}</span>
                  <span>{fmtScore(row.scores.engaged)}</span>
                  <span>{fmtScore(row.scores.pi)}</span>
                  <span>{fmtScore(row.scores.facts)}</span>
                  <span>{row.failure_cases}</span>
                </div>
              ))}
              <div className="execution-table-row execution-table-row--total">
                <span className="arm-name">All</span>
                <span>{run.summary.arm_results}</span>
                <span>{fmtScore(scores.disposition)}</span>
                <span>{fmtScore(scores.engaged)}</span>
                <span>{fmtScore(scores.pi)}</span>
                <span>{fmtScore(scores.facts)}</span>
                <span>{run.summary.failure_cases}</span>
              </div>
            </div>
          </Card.Body>
        </Card>
      ) : null}

      <div className="run-view-grid">
        <Card className="run-view-section">
          <Card.Header>
            <h2>{isLabel ? "Labels" : "Cases"} {failuresOnly ? "(failures only)" : ""}</h2>
          </Card.Header>
          <Card.Body>
            {visibleCases.length ? (
              <div className="case-list">
                {visibleCases.map((c) => {
                  const failed = !isLabel && caseHasFailure(c);
                  const labelGold = c.label?.gold;
                  const key = caseKey(c);
                  return (
                    <button
                      key={key}
                      type="button"
                      className={
                        "case-row" +
                        (key === activeCaseKey ? " case-row--active" : "") +
                        (isLabel ? "" : failed ? " case-row--fail" : " case-row--pass")
                      }
                      onClick={() => setActiveCaseKey(key)}
                    >
                      <span className="case-row-name">{c.id}</span>
                      <span className="case-row-arm">{c.arm}</span>
                      <span className="case-row-disp">
                        {isLabel
                          ? `gold: ${fmtValue(labelGold)}`
                          : `${String(c.pred.disposition ?? "?")} / ${String(c.gold.disposition ?? "?")}`}
                      </span>
                    </button>
                  );
                })}
              </div>
            ) : (
              <p>{failuresOnly ? "No failing cases in this run." : "No case results."}</p>
            )}
          </Card.Body>
        </Card>

        <Card className="run-view-section run-view-span-2">
          <Card.Header>
            <h2>{selectedCase ? selectedCase.id : "Case detail"}</h2>
          </Card.Header>
          <Card.Body>
            {selectedCase ? (
              <>
                {isLabel && selectedCase.label ? (
                  <div className="label-output">
                    <div className="section-kicker">Drafted gold label</div>
                    <ul className="summary-facts">
                      <li>
                        <span>Disposition</span>
                        <strong>{fmtValue(selectedCase.label.gold)}</strong>
                      </li>
                      <li>
                        <span>Engaged</span>
                        <strong>{fmtValue(selectedCase.label.engaged)}</strong>
                      </li>
                      <li>
                        <span>PI</span>
                        <strong>{fmtValue(selectedCase.label.pi)}</strong>
                      </li>
                      <li>
                        <span>Exemptions</span>
                        <strong>{fmtValue(selectedCase.label.exemptions)}</strong>
                      </li>
                    </ul>
                    {Array.isArray(selectedCase.label.oracle_facts) ? (
                      <div className="facts-block">
                        <div className="section-kicker">Oracle facts</div>
                        <div className="reply-facts">
                          {selectedCase.label.oracle_facts.map((atom) => (
                            <span key={String(atom)} className="atom-chip atom-chip--included">
                              {String(atom)}
                            </span>
                          ))}
                        </div>
                      </div>
                    ) : null}
                    {typeof selectedCase.label.notes === "string" ? (
                      <p className="reasoning-text">{selectedCase.label.notes}</p>
                    ) : null}
                  </div>
                ) : (
                  <div className="execution-table">
                    <div className="execution-table-header">
                      <span>Dimension</span>
                      <span>Pred</span>
                      <span>Gold</span>
                      <span>Hit</span>
                    </div>
                    {(["disposition", "engaged", "pi"] as const).map((dim) => {
                      const mark = hitMark(selectedCase.hits[dim]);
                      const pred = selectedCase.pred[dim];
                      const gold = selectedCase.gold[dim];
                      return (
                        <div key={dim} className="execution-table-row">
                          <span>{dim}</span>
                          <span>{fmtValue(pred)}</span>
                          <span>{fmtValue(gold)}</span>
                          <span className={mark.className}>{mark.label}</span>
                        </div>
                      );
                    })}
                  </div>
                )}

                {!isLabel && selectedCase.facts_agreement ? (
                  <div className="facts-block">
                    <div className="section-kicker">Facts agreement</div>
                    <p>
                      <strong>
                        {selectedCase.facts_agreement[0]}/{selectedCase.facts_agreement[1]}
                      </strong>
                      {selectedCase.facts_agreement[2]?.length ? (
                        <> · missed: {selectedCase.facts_agreement[2].join(", ")}</>
                      ) : null}
                      {selectedCase.facts_agreement[3]?.length ? (
                        <> · extra: {selectedCase.facts_agreement[3].join(", ")}</>
                      ) : null}
                    </p>
                  </div>
                ) : null}

                {!isLabel && selectedCase.atom_failures.length > 0 && (
                  <div className="failures-block">
                    <div className="section-kicker">Atom failures + model reasoning</div>
                    {selectedCase.atom_failures.map((f, i) => (
                      <div key={`${f.atom}-${i}`} className="failure-card">
                        <div className="failure-card-head">
                          <span className={`badge badge--${f.kind}`}>{f.kind}</span>
                          <strong>{f.atom}</strong>
                          <span className="failure-where">{f.where}</span>
                        </div>
                        <p className="failure-reasoning">{f.reasoning}</p>
                      </div>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <p>Select a case to inspect dimension scores and grounding failures.</p>
            )}
          </Card.Body>
        </Card>
      </div>

      <Card className="run-view-section inspector-card">
        <Card.Header>
          <div className="inspector-header">
            <div>
              <h2>Prompt inspector</h2>
              {selectedCall ? (
                <p className="main-subtle">
                  {selectedCall.prompt_tokens?.toLocaleString() ?? "?"} prompt tokens ·{" "}
                  {selectedCall.completion_tokens?.toLocaleString() ?? "?"} completion ·{" "}
                  {selectedCall.seconds?.toFixed(1) ?? "?"}s
                </p>
              ) : null}
            </div>
            {selectedCase && selectedCase.calls.length ? (
              <label className="inspector-call-select">
                LLM call
                <select
                  value={activeCallIdx}
                  onChange={(e) => setActiveCallIdx(Number(e.target.value))}
                >
                  {selectedCase.calls.map((call, idx) => (
                    <option key={idx} value={idx}>
                      {callLabel(call, idx)}
                    </option>
                  ))}
                </select>
              </label>
            ) : null}
          </div>
        </Card.Header>
        <Card.Body>
          {selectedCase && selectedCase.calls.length ? (
            selectedCall ? (
              <div className="inspector-layout">
                <section className="inspector-panel inspector-panel--reply">
                  <h3>Reply</h3>
                  <div className="reply-facts">
                    {parseReplyFacts(selectedCall.reply ?? "").map((atom) => (
                      <span key={atom} className="atom-chip atom-chip--included">
                        {atom}
                      </span>
                    ))}
                    {!parseReplyFacts(selectedCall.reply ?? "").length ? (
                      <span className="inspector-empty-note">No atoms included</span>
                    ) : null}
                  </div>
                  <div className="inspector-scroll">
                    <p className="reasoning-text">
                      {parseReplyReasoning(selectedCall.reply ?? "") ||
                        "(no reasoning field)"}
                    </p>
                    <details>
                      <summary>Raw reply JSON</summary>
                      <pre className="summary-raw-json">{selectedCall.reply}</pre>
                    </details>
                  </div>
                </section>

                <section className="inspector-panel inspector-panel--user">
                  <h3>User prompt</h3>
                  <div className="inspector-scroll inspector-scroll--tall">
                    <MarkdownView
                      content={
                        selectedCall.user
                          ? `\`\`\`\n${selectedCall.user}\n\`\`\``
                          : "(empty)"
                      }
                    />
                  </div>
                </section>

                <section className="inspector-panel inspector-panel--system">
                  <h3>System prompt</h3>
                  {selectedCall.batch_atoms?.length ? (
                    <div className="batch-atoms">
                      <span className="section-kicker">Batch atoms</span>
                      <div className="reply-facts">
                        {selectedCall.batch_atoms.map((atom) => (
                          <span key={atom} className="atom-chip atom-chip--batch">
                            {atom}
                          </span>
                        ))}
                      </div>
                    </div>
                  ) : null}
                  <div className="inspector-scroll inspector-scroll--tall">
                    <MarkdownView
                      content={
                        selectedCall.system
                          ? `\`\`\`\n${selectedCall.system}\n\`\`\``
                          : "(empty)"
                      }
                    />
                  </div>
                </section>
              </div>
            ) : null
          ) : (
            <p>
              {selectedCase?.arm === "oracle"
                ? "Oracle arm uses hand-verified facts — no LLM call logged."
                : "No LLM calls logged for the selected case."}
            </p>
          )}
        </Card.Body>
      </Card>
    </div>
  );
};
