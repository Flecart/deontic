import React, { useCallback, useEffect, useState } from "react";
import { CaseBankView } from "./components/CaseBankView";
import { DataQaView } from "./components/DataQaView";
import { ExpARunView } from "./components/ExpARunView";
import { Layout } from "./components/Layout";
import { RunView } from "./components/RunView";
import { Sidebar } from "./components/Sidebar";
import type {
  CaseBankDetail,
  ExpARunDetail,
  QaStatute,
  RunDetail,
  RunListItem,
  Source,
} from "./types";

type ViewMode = "runs" | "qa";

export const App: React.FC = () => {
  const [view, setView] = useState<ViewMode>("runs");
  const [statutes, setStatutes] = useState<QaStatute[]>([]);
  const [activeStatute, setActiveStatute] = useState<string | null>(null);
  const [loadingStatutes, setLoadingStatutes] = useState(false);
  const [sources, setSources] = useState<Source[]>([]);
  const [activeSource, setActiveSource] = useState<string | null>(null);
  const [runs, setRuns] = useState<RunListItem[]>([]);
  const [activeRun, setActiveRun] = useState<string | null>(null);
  const [runDetail, setRunDetail] = useState<RunDetail | CaseBankDetail | null>(null);
  const [loadingSources, setLoadingSources] = useState(false);
  const [loadingRuns, setLoadingRuns] = useState(false);
  const [loadingRun, setLoadingRun] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [failuresOnly, setFailuresOnly] = useState(false);
  const [lastUpdatedAt, setLastUpdatedAt] = useState<number | null>(null);

  const loadSources = useCallback(async (background = false) => {
    try {
      if (!background) setLoadingSources(true);
      const res = await fetch(`/api/sources?ts=${Date.now()}`);
      if (!res.ok) throw new Error(`Failed to load sources (${res.status})`);
      const data = (await res.json()) as { sources: Source[] };
      const next = data.sources ?? [];
      setSources(next);
      setLastUpdatedAt(Date.now());
      setActiveSource((prev) => {
        if (prev && next.some((s) => s.id === prev)) return prev;
        return next[0]?.id ?? null;
      });
    } catch (e) {
      setError((e as Error).message);
    } finally {
      if (!background) setLoadingSources(false);
    }
  }, []);

  const loadRuns = useCallback(async (sourceId: string, background = false) => {
    try {
      if (!background) setLoadingRuns(true);
      const res = await fetch(
        `/api/sources/${encodeURIComponent(sourceId)}/runs?ts=${Date.now()}`
      );
      if (!res.ok) throw new Error(`Failed to load runs (${res.status})`);
      const data = (await res.json()) as { runs: RunListItem[] };
      const next = data.runs ?? [];
      setRuns(next);
      setLastUpdatedAt(Date.now());
      setActiveRun((prev) => {
        if (prev && next.some((r) => r.name === prev)) return prev;
        return next[0]?.name ?? null;
      });
    } catch (e) {
      setError((e as Error).message);
    } finally {
      if (!background) setLoadingRuns(false);
    }
  }, []);

  useEffect(() => {
    void loadSources(false);
    const interval = window.setInterval(() => void loadSources(true), 5000);
    return () => window.clearInterval(interval);
  }, [loadSources]);

  useEffect(() => {
    if (view !== "qa") return;
    let cancelled = false;
    const load = async () => {
      try {
        setLoadingStatutes(true);
        const res = await fetch(`/api/qa/statutes?ts=${Date.now()}`);
        if (!res.ok) throw new Error(`Failed to load statutes (${res.status})`);
        const data = (await res.json()) as { statutes: QaStatute[] };
        if (cancelled) return;
        const next = data.statutes ?? [];
        setStatutes(next);
        setActiveStatute((prev) => {
          if (prev && next.some((s) => s.id === prev)) return prev;
          return next[0]?.id ?? null;
        });
        setError(null);
      } catch (e) {
        if (!cancelled) setError((e as Error).message);
      } finally {
        if (!cancelled) setLoadingStatutes(false);
      }
    };
    void load();
    return () => {
      cancelled = true;
    };
  }, [view]);

  useEffect(() => {
    if (!activeSource) {
      setRuns([]);
      setActiveRun(null);
      return;
    }
    void loadRuns(activeSource, false);
    const interval = window.setInterval(
      () => void loadRuns(activeSource, true),
      5000
    );
    return () => window.clearInterval(interval);
  }, [activeSource, loadRuns]);

  useEffect(() => {
    if (!activeSource || !activeRun) {
      setRunDetail(null);
      return;
    }

    let cancelled = false;
    const loadRun = async (background = false) => {
      try {
        if (!background) setLoadingRun(true);
        const res = await fetch(
          `/api/sources/${encodeURIComponent(activeSource)}/runs/${encodeURIComponent(activeRun)}?ts=${Date.now()}`
        );
        if (!res.ok) throw new Error(`Failed to load run (${res.status})`);
        const data = (await res.json()) as RunDetail | CaseBankDetail;
        if (cancelled) return;
        setRunDetail(data);
        setLastUpdatedAt(Date.now());
        setError(null);
      } catch (e) {
        if (cancelled) return;
        setError((e as Error).message);
      } finally {
        if (!cancelled && !background) setLoadingRun(false);
      }
    };

    void loadRun(false);
    const interval = window.setInterval(() => void loadRun(true), 5000);
    return () => {
      cancelled = true;
      window.clearInterval(interval);
    };
  }, [activeSource, activeRun]);

  const activeSourceMeta = sources.find((s) => s.id === activeSource);
  const sourceLabel = activeSourceMeta?.label ?? "Eval";
  const runKind = runDetail?.kind;
  const isCaseBank = runKind === "casebank";
  const isExpAEval = runKind === "expa_eval";

  const viewSwitch = (
    <div className="view-switch">
      <button
        type="button"
        className={"view-switch-btn" + (view === "runs" ? " view-switch-btn--active" : "")}
        onClick={() => setView("runs")}
      >
        Eval runs
      </button>
      <button
        type="button"
        className={"view-switch-btn" + (view === "qa" ? " view-switch-btn--active" : "")}
        onClick={() => setView("qa")}
      >
        Data QA
      </button>
    </div>
  );

  const sidebar =
    view === "qa" ? (
      <div className="sidebar">
        {viewSwitch}
        <section>
          <h2 className="sidebar-title">
            Statutes
            {loadingStatutes ? (
              <span className="inline-loader" aria-label="Loading statutes" />
            ) : null}
          </h2>
          <ul className="sidebar-list">
            {statutes.map((s) => (
              <li key={s.id}>
                <button
                  type="button"
                  className={
                    "sidebar-item" + (s.id === activeStatute ? " sidebar-item--active" : "")
                  }
                  onClick={() => setActiveStatute(s.id)}
                >
                  <span className="sidebar-run-label">
                    {s.label} ({s.id})
                  </span>
                  <span className="sidebar-run-meta">
                    {s.case_count} cases · {s.result_rows} rows · {s.models.length} models
                  </span>
                </button>
              </li>
            ))}
            {!loadingStatutes && statutes.length === 0 ? (
              <li className="sidebar-empty">No eval statutes found</li>
            ) : null}
          </ul>
        </section>
      </div>
    ) : (
      <>
        {viewSwitch}
        <Sidebar
          sources={sources}
          loadingSources={loadingSources}
          activeSource={activeSource}
          onSourceChange={(id) => {
            setActiveSource(id);
            setActiveRun(null);
            setRunDetail(null);
          }}
          runs={runs}
          loadingRuns={loadingRuns}
          activeRun={activeRun}
          onRunChange={setActiveRun}
        />
      </>
    );

  const activeStatuteMeta = statutes.find((s) => s.id === activeStatute) ?? null;

  const qaMain = (
    <div className="main">
      <header className="main-header">
        <h1>Data QA{activeStatuteMeta ? ` — ${activeStatuteMeta.label}` : ""}</h1>
        <p>
          Audit the generated evaluation data: gold labels, narrations, model × arm
          disagreements, and annotator bank-validation votes.
        </p>
      </header>
      {error ? <div className="alert alert-error">{error}</div> : null}
      <DataQaView statute={activeStatuteMeta} />
    </div>
  );

  const main = (
    <div className="main">
      <header className="main-header">
        <h1>
          {sourceLabel}{" "}
          {isCaseBank ? "Case Viewer" : isExpAEval ? "Results Viewer" : "Run Viewer"}
        </h1>
        <p>
          {isCaseBank
            ? "Browse case banks: gold labels, bank items, narrative memos, and per-arm LLM prompts."
            : isExpAEval
              ? "Inspect arm sweeps: verdict accuracy, failures, and exact LLM prompts plus logged replies."
              : "Inspect eval runs: per-arm accuracy, failures, and logged model outputs."}
        </p>
        {lastUpdatedAt ? (
          <p className="main-subtle">
            Live refresh every 5s. Last update:{" "}
            {new Date(lastUpdatedAt).toLocaleTimeString()}
          </p>
        ) : null}
      </header>

      {error ? <div className="alert alert-error">{error}</div> : null}
      {loadingRun ? (
        <div className="alert alert-info alert-loading">
          <span className="inline-loader" aria-hidden="true" />
          <span>Loading run…</span>
        </div>
      ) : null}

      {!isCaseBank && runDetail && runDetail.kind !== "label" && runDetail.kind !== "casebank" ? (
        <div className="tabs-row">
          <button
            type="button"
            className={"tab" + (!failuresOnly ? " tab--active" : " tab--inactive")}
            onClick={() => setFailuresOnly(false)}
          >
            All cases
          </button>
          <button
            type="button"
            className={"tab" + (failuresOnly ? " tab--active" : " tab--inactive")}
            onClick={() => setFailuresOnly(true)}
          >
            Failures only
          </button>
        </div>
      ) : null}

      {isCaseBank ? (
        <CaseBankView bank={runDetail?.kind === "casebank" ? runDetail : null} />
      ) : isExpAEval ? (
        <ExpARunView
          run={runDetail?.kind === "expa_eval" ? (runDetail as ExpARunDetail) : null}
          failuresOnly={failuresOnly}
        />
      ) : (
        <RunView run={runDetail?.kind === "casebank" ? null : runDetail} failuresOnly={failuresOnly} />
      )}
    </div>
  );

  return <Layout sidebar={sidebar} main={view === "qa" ? qaMain : main} />;
};
