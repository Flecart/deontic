import React from "react";
import type { Experiment, RunListItem } from "../types";

interface SidebarProps {
  experiments: Experiment[];
  loadingExperiments: boolean;
  activeExperiment: string | null;
  onExperimentChange: (id: string) => void;
  runs: RunListItem[];
  loadingRuns: boolean;
  activeRun: string | null;
  onRunChange: (name: string) => void;
}

function formatRunLabel(run: RunListItem): string {
  const stamp = run.name.replace(/^run_/, "").replace(/\.jsonl$/, "");
  if (run.kind === "label") {
    return stamp;
  }
  const arms = run.arms?.join("+") ?? "?";
  return `${stamp} (${arms})`;
}

export const Sidebar: React.FC<SidebarProps> = ({
  experiments,
  loadingExperiments,
  activeExperiment,
  onExperimentChange,
  runs,
  loadingRuns,
  activeRun,
  onRunChange
}) => {
  return (
    <div className="sidebar">
      <section>
        <h2 className="sidebar-title">
          Experiment
          {loadingExperiments ? (
            <span className="inline-loader" aria-label="Loading experiments" />
          ) : null}
        </h2>
        <ul className="sidebar-list">
          {experiments.map((exp) => (
            <li key={exp.id}>
              <button
                type="button"
                className={
                  "sidebar-item" +
                  (exp.id === activeExperiment ? " sidebar-item--active" : "")
                }
                onClick={() => onExperimentChange(exp.id)}
              >
                <span className="sidebar-run-label">{exp.label}</span>
                <span className="sidebar-run-meta">{exp.run_count} runs</span>
              </button>
            </li>
          ))}
          {!loadingExperiments && experiments.length === 0 ? (
            <li className="sidebar-empty">No *_corpus experiments found</li>
          ) : null}
        </ul>
      </section>

      <section>
        <h2 className="sidebar-title">
          Pipeline runs
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
                  {run.kind === "label" ? "label" : run.model ?? "—"} ·{" "}
                  {run.case_count} {run.kind === "label" ? "labels" : "cases"}
                </span>
              </button>
            </li>
          ))}
          {!loadingRuns && runs.length === 0 && activeExperiment ? (
            <li className="sidebar-empty">No runs in runs/</li>
          ) : null}
        </ul>
      </section>
    </div>
  );
};
