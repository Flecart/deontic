import React, { useEffect, useMemo, useState } from "react";
import { Card } from "./Card";
import { ModelIoView } from "./ModelIoView";
import type { CaseResult, ExpARunDetail, LlmCall } from "../types";

export interface ExpARunViewProps {
  run: ExpARunDetail | null;
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
  return c.hits.share_status === false || c.hits.assignment === false;
}

function callLabel(call: LlmCall, index: number): string {
  const batch =
    call.batch != null && call.batches != null
      ? `batch ${call.batch}/${call.batches}`
      : "single call";
  const atom = call.atom ? ` · ${call.atom}` : "";
  return `Call ${index + 1} · ${batch}${atom}`;
}

export const ExpARunView: React.FC<ExpARunViewProps> = ({ run, failuresOnly }) => {
  const [activeKey, setActiveKey] = useState<string | null>(null);
  const [activeCallIdx, setActiveCallIdx] = useState(0);

  const visibleCases = useMemo(() => {
    if (!run) return [];
    return failuresOnly ? run.cases.filter(caseHasFailure) : run.cases;
  }, [run, failuresOnly]);

  useEffect(() => {
    if (!visibleCases.length) {
      setActiveKey(null);
      return;
    }
    const keys = visibleCases.map((c) => `${c.id}::${c.arm}::${c.model ?? ""}`);
    if (!activeKey || !keys.includes(activeKey)) {
      setActiveKey(keys[0]);
    }
  }, [visibleCases, activeKey]);

  const selectedCase = useMemo(() => {
    if (!activeKey) return null;
    const [id, arm, model] = activeKey.split("::");
    return (
      visibleCases.find(
        (c) => c.id === id && c.arm === arm && (c.model ?? "") === model
      ) ?? null
    );
  }, [visibleCases, activeKey]);

  useEffect(() => {
    setActiveCallIdx(0);
  }, [activeKey]);

  const selectedCall = selectedCase?.calls[activeCallIdx] ?? null;

  if (!run) {
    return (
      <Card>
        <Card.Header>
          <h1>Experiment A results</h1>
        </Card.Header>
        <Card.Body>
          <p>Select a results run from the sidebar to inspect verdicts and LLM prompts.</p>
        </Card.Body>
      </Card>
    );
  }

  const scores = run.summary.scores;
  const meta = run.meta;

  return (
    <div className="run-view">
      <Card className="run-view-section run-view-hero">
        <Card.Header>
          <div className="hero-header">
            <div>
              <h1>{run.name.replace(/\.jsonl$/, "")}</h1>
              <p>
                Experiment A arm sweep — share-status verdict and atom assignment vs gold,
                with reconstructed LLM prompts and logged replies.
              </p>
            </div>
            <div className="metric-strip">
              <div className="metric-pill">
                <span className="metric-label">Share status</span>
                <strong>{scores.share_status ?? "—"}</strong>
              </div>
              <div className="metric-pill">
                <span className="metric-label">Assignment</span>
                <strong>{scores.assignment ?? "—"}</strong>
              </div>
              <div className="metric-pill">
                <span className="metric-label">Failures</span>
                <strong>{run.summary.failure_cases}</strong>
              </div>
              <div className="metric-pill">
                <span className="metric-label">LLM calls</span>
                <strong>{run.summary.llm_calls}</strong>
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
                  <span>Arms</span>{" "}
                  <strong>
                    {Array.isArray(meta.arms) ? meta.arms.join(", ") : "—"}
                  </strong>
                </li>
                <li>
                  <span>Models</span>{" "}
                  <strong>
                    {Array.isArray(meta.models) ? meta.models.join(", ") : "—"}
                  </strong>
                </li>
                <li>
                  <span>Rows</span> <strong>{run.summary.arm_results}</strong>
                </li>
              </ul>
            </div>
            <div className="hero-panel">
              <div className="section-kicker">Latency</div>
              <ul className="summary-facts">
                <li>
                  <span>Total seconds</span> <strong>{run.summary.seconds}s</strong>
                </li>
              </ul>
            </div>
          </div>
        </Card.Body>
      </Card>

      <div className="run-view-grid">
        <Card className="run-view-section">
          <Card.Header>
            <h2>Results {failuresOnly ? "(failures only)" : ""}</h2>
          </Card.Header>
          <Card.Body>
            {visibleCases.length ? (
              <div className="case-list case-list--tall">
                {visibleCases.map((c) => {
                  const key = `${c.id}::${c.arm}::${c.model ?? ""}`;
                  const failed = caseHasFailure(c);
                  return (
                    <button
                      key={key}
                      type="button"
                      className={
                        "case-row" +
                        (key === activeKey ? " case-row--active" : "") +
                        (failed ? " case-row--fail" : " case-row--pass")
                      }
                      onClick={() => setActiveKey(key)}
                    >
                      <span className="case-row-name">{c.id}</span>
                      <span className="case-row-arm">{c.arm}</span>
                      <span className="case-row-disp">
                        {String(c.pred.share_status ?? "?")} /{" "}
                        {String(c.gold.share_status ?? "?")}
                      </span>
                    </button>
                  );
                })}
              </div>
            ) : (
              <p>{failuresOnly ? "No failing rows." : "No results."}</p>
            )}
          </Card.Body>
        </Card>

        <Card className="run-view-section run-view-span-2">
          <Card.Header>
            <h2>{selectedCase ? `${selectedCase.id} · ${selectedCase.arm}` : "Row detail"}</h2>
          </Card.Header>
          <Card.Body>
            {selectedCase ? (
              <>
                <div className="case-meta-strip">
                  {selectedCase.model ? (
                    <span className="case-meta-pill">
                      model <strong>{selectedCase.model}</strong>
                    </span>
                  ) : null}
                  {selectedCase.tier != null ? (
                    <span className="case-meta-pill">
                      tier <strong>{selectedCase.tier}</strong>
                    </span>
                  ) : null}
                  {selectedCase.tokens != null ? (
                    <span className="case-meta-pill">
                      tokens <strong>{selectedCase.tokens}</strong>
                    </span>
                  ) : null}
                </div>

                <div className="execution-table">
                  <div className="execution-table-header">
                    <span>Field</span>
                    <span>Pred</span>
                    <span>Gold</span>
                    <span>Hit</span>
                  </div>
                  {(["share_status", "violation", "notify_required"] as const).map((dim) => {
                    const mark = hitMark(
                      dim === "share_status" ? selectedCase.hits.share_status : null
                    );
                    return (
                      <div key={dim} className="execution-table-row">
                        <span>{dim}</span>
                        <span>{String(selectedCase.pred[dim] ?? "—")}</span>
                        <span>{String(selectedCase.gold[dim] ?? "—")}</span>
                        <span className={mark.className}>{mark.label}</span>
                      </div>
                    );
                  })}
                  <div className="execution-table-row">
                    <span>assignment</span>
                    <span>{selectedCase.hits.assignment === null ? "—" : "all atoms"}</span>
                    <span>gold</span>
                    <span className={hitMark(selectedCase.hits.assignment).className}>
                      {hitMark(selectedCase.hits.assignment).label}
                    </span>
                  </div>
                </div>
              </>
            ) : (
              <p>Select a row to inspect verdicts and prompts.</p>
            )}
          </Card.Body>
        </Card>
      </div>

      <Card className="run-view-section model-io-card">
        <Card.Header>
          <div className="inspector-header">
            <div>
              <h2>Exact model I/O</h2>
              <p className="main-subtle">
                Prompt reconstructed from <code>arms.py</code> templates; reply from the
                results log.
              </p>
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
              <ModelIoView call={selectedCall} />
            ) : null
          ) : selectedCase ? (
            <p>No LLM calls for arm <strong>{selectedCase.arm}</strong> (oracle/program).</p>
          ) : (
            <p>Select a row with an LLM arm to inspect prompts.</p>
          )}
        </Card.Body>
      </Card>
    </div>
  );
};
