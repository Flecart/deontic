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

function parseReplyFacts(reply: string): string[] {
  const m = reply.match(/\{[\s\S]*\}/);
  if (!m) return [];
  try {
    const parsed = JSON.parse(m[0]) as { facts?: unknown };
    return Array.isArray(parsed.facts) ? parsed.facts.map(String) : [];
  } catch {
    return [];
  }
}

function parseReplyReasoning(reply: string): string {
  const m = reply.match(/\{[\s\S]*\}/);
  if (!m) return reply.slice(0, 400);
  try {
    const parsed = JSON.parse(m[0]) as { reasoning?: unknown };
    return typeof parsed.reasoning === "string" ? parsed.reasoning : "";
  } catch {
    return reply.slice(0, 400);
  }
}

function callLabel(call: LlmCall, index: number): string {
  const batch =
    call.batch != null && call.batches != null
      ? `batch ${call.batch}/${call.batches}`
      : "single call";
  return `Call ${index + 1} · ${batch} · ${call.seconds?.toFixed(1) ?? "?"}s`;
}

export const RunView: React.FC<RunViewProps> = ({ run, failuresOnly }) => {
  const [activeCase, setActiveCase] = useState<string | null>(null);
  const [activeCallIdx, setActiveCallIdx] = useState(0);

  const visibleCases = useMemo(() => {
    if (!run) return [];
    return failuresOnly ? run.cases.filter(caseHasFailure) : run.cases;
  }, [run, failuresOnly]);

  useEffect(() => {
    if (!visibleCases.length) {
      setActiveCase(null);
      return;
    }
    if (!activeCase || !visibleCases.some((c) => c.id === activeCase)) {
      setActiveCase(visibleCases[0].id);
    }
  }, [visibleCases, activeCase]);

  const selectedCase = useMemo(
    () => visibleCases.find((c) => c.id === activeCase) ?? null,
    [visibleCases, activeCase]
  );

  useEffect(() => {
    setActiveCallIdx(0);
  }, [activeCase]);

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

  return (
    <div className="run-view">
      <Card className="run-view-section run-view-hero">
        <Card.Header>
          <div className="hero-header">
            <div>
              <h1>{run.name.replace(/\.jsonl$/, "")}</h1>
              <p>
                FOIA Phase-0 eval — oracle / ground / llm arms scored on disposition,
                exemption engagement, PI direction, and per-atom facts.
              </p>
            </div>
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

      <div className="run-view-grid">
        <Card className="run-view-section">
          <Card.Header>
            <h2>Cases {failuresOnly ? "(failures only)" : ""}</h2>
          </Card.Header>
          <Card.Body>
            {visibleCases.length ? (
              <div className="case-list">
                {visibleCases.map((c) => {
                  const failed = caseHasFailure(c);
                  return (
                    <button
                      key={`${c.id}-${c.arm}`}
                      type="button"
                      className={
                        "case-row" +
                        (c.id === activeCase ? " case-row--active" : "") +
                        (failed ? " case-row--fail" : " case-row--pass")
                      }
                      onClick={() => setActiveCase(c.id)}
                    >
                      <span className="case-row-name">{c.id}</span>
                      <span className="case-row-arm">{c.arm}</span>
                      <span className="case-row-disp">
                        {String(c.pred.disposition ?? "?")} / {String(c.gold.disposition ?? "?")}
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
                    const fmt = (v: unknown) =>
                      Array.isArray(v) ? v.join(", ") : String(v ?? "—");
                    return (
                      <div key={dim} className="execution-table-row">
                        <span>{dim}</span>
                        <span>{fmt(pred)}</span>
                        <span>{fmt(gold)}</span>
                        <span className={mark.className}>{mark.label}</span>
                      </div>
                    );
                  })}
                </div>

                {selectedCase.facts_agreement ? (
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

                {selectedCase.atom_failures.length > 0 && (
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
            <p>No LLM calls logged for the selected case.</p>
          )}
        </Card.Body>
      </Card>
    </div>
  );
};
