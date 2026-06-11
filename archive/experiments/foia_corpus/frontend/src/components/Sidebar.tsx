import React from "react";
import type { RunListItem } from "../types";

interface SidebarProps {
  runs: RunListItem[];
  loading: boolean;
  activeRun: string | null;
  onRunChange: (name: string) => void;
}

function formatRunLabel(run: RunListItem): string {
  const stamp = run.name.replace(/^run_/, "").replace(/\.jsonl$/, "");
  const arms = run.arms?.join("+") ?? "?";
  return `${stamp} (${arms})`;
}

export const Sidebar: React.FC<SidebarProps> = ({
  runs,
  loading,
  activeRun,
  onRunChange
}) => {
  return (
    <div className="sidebar">
      <section>
        <h2 className="sidebar-title">
          Pipeline runs
          {loading ? <span className="inline-loader" aria-label="Loading runs" /> : null}
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
                  {run.model ?? "—"} · {run.case_count} cases
                </span>
              </button>
            </li>
          ))}
          {!loading && runs.length === 0 ? (
            <li className="sidebar-empty">No runs in runs/</li>
          ) : null}
        </ul>
      </section>
    </div>
  );
};
