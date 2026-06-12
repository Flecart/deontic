import React from "react";
import type { RunListItem, Source } from "../types";

interface SidebarProps {
  sources: Source[];
  loadingSources: boolean;
  activeSource: string | null;
  onSourceChange: (id: string) => void;
  runs: RunListItem[];
  loadingRuns: boolean;
  activeRun: string | null;
  onRunChange: (name: string) => void;
}

function formatRunLabel(run: RunListItem): string {
  const stamp = run.name
    .replace(/^run_/, "")
    .replace(/^cases_/, "")
    .replace(/^results_/, "")
    .replace(/\.jsonl$/, "");
  if (run.kind === "casebank") return `cases: ${stamp}`;
  if (run.kind === "expa_eval") return `results: ${stamp}`;
  if (run.kind === "label") return stamp;
  if (run.kind === "modal") return stamp;
  const arms = run.arms?.join("+") ?? "?";
  return `${stamp} (${arms})`;
}

export const Sidebar: React.FC<SidebarProps> = ({
  sources,
  loadingSources,
  activeSource,
  onSourceChange,
  runs,
  loadingRuns,
  activeRun,
  onRunChange
}) => {
  return (
    <div className="sidebar">
      <section>
        <h2 className="sidebar-title">
          Source
          {loadingSources ? (
            <span className="inline-loader" aria-label="Loading sources" />
          ) : null}
        </h2>
        <ul className="sidebar-list">
          {sources.map((src) => (
            <li key={src.id}>
              <button
                type="button"
                className={
                  "sidebar-item" +
                  (src.id === activeSource ? " sidebar-item--active" : "")
                }
                onClick={() => onSourceChange(src.id)}
              >
                <span className="sidebar-run-label">{src.label}</span>
                <span className="sidebar-run-meta">
                  {src.type} · {src.run_count} runs
                </span>
              </button>
            </li>
          ))}
          {!loadingSources && sources.length === 0 ? (
            <li className="sidebar-empty">No data sources found</li>
          ) : null}
        </ul>
      </section>

      <section>
        <h2 className="sidebar-title">
          Runs
          {loadingRuns ? (
            <span className="inline-loader" aria-label="Loading runs" />
          ) : null}
        </h2>
        <ul className="sidebar-list">
          {runs.map((run) => (
            <li key={run.name}>
              <button
                type="button"
                className={
                  "sidebar-item" +
                  (run.name === activeRun ? " sidebar-item--active" : "")
                }
                onClick={() => onRunChange(run.name)}
              >
                <span className="sidebar-run-label">{formatRunLabel(run)}</span>
                <span className="sidebar-run-meta">
                  {run.model ?? (run.kind === "casebank" ? "case bank" : "—")} ·{" "}
                  {run.case_count}{" "}
                  {run.kind === "modal"
                    ? "problems"
                    : run.kind === "casebank"
                      ? "cases"
                      : run.kind === "expa_eval"
                        ? "rows"
                        : "results"}
                </span>
              </button>
            </li>
          ))}
          {!loadingRuns && runs.length === 0 && activeSource ? (
            <li className="sidebar-empty">No runs</li>
          ) : null}
        </ul>
      </section>
    </div>
  );
};
