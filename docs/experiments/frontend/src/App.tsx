import React, { useCallback, useEffect, useState } from "react";
import { Layout } from "./components/Layout";
import { RunView } from "./components/RunView";
import { Sidebar } from "./components/Sidebar";
import type { Experiment, RunDetail, RunListItem } from "./types";

export const App: React.FC = () => {
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [activeExperiment, setActiveExperiment] = useState<string | null>(null);
  const [runs, setRuns] = useState<RunListItem[]>([]);
  const [activeRun, setActiveRun] = useState<string | null>(null);
  const [runDetail, setRunDetail] = useState<RunDetail | null>(null);
  const [loadingExperiments, setLoadingExperiments] = useState(false);
  const [loadingRuns, setLoadingRuns] = useState(false);
  const [loadingRun, setLoadingRun] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [failuresOnly, setFailuresOnly] = useState(false);
  const [lastUpdatedAt, setLastUpdatedAt] = useState<number | null>(null);

  const loadExperiments = useCallback(async (background = false) => {
    try {
      if (!background) setLoadingExperiments(true);
      const res = await fetch(`/api/experiments?ts=${Date.now()}`);
      if (!res.ok) throw new Error(`Failed to load experiments (${res.status})`);
      const data = (await res.json()) as { experiments: Experiment[] };
      const next = data.experiments ?? [];
      setExperiments(next);
      setLastUpdatedAt(Date.now());
      setActiveExperiment((prev) => {
        if (prev && next.some((e) => e.id === prev)) return prev;
        return next[0]?.id ?? null;
      });
    } catch (e) {
      setError((e as Error).message);
    } finally {
      if (!background) setLoadingExperiments(false);
    }
  }, []);

  const loadRuns = useCallback(
    async (expId: string, background = false) => {
      try {
        if (!background) setLoadingRuns(true);
        const res = await fetch(
          `/api/experiments/${encodeURIComponent(expId)}/runs?ts=${Date.now()}`
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
    },
    []
  );

  useEffect(() => {
    void loadExperiments(false);
    const interval = window.setInterval(() => void loadExperiments(true), 5000);
    return () => window.clearInterval(interval);
  }, [loadExperiments]);

  useEffect(() => {
    if (!activeExperiment) {
      setRuns([]);
      setActiveRun(null);
      return;
    }
    void loadRuns(activeExperiment, false);
    const interval = window.setInterval(
      () => void loadRuns(activeExperiment, true),
      5000
    );
    return () => window.clearInterval(interval);
  }, [activeExperiment, loadRuns]);

  useEffect(() => {
    if (!activeExperiment || !activeRun) {
      setRunDetail(null);
      return;
    }

    let cancelled = false;
    const loadRun = async (background = false) => {
      try {
        if (!background) setLoadingRun(true);
        const res = await fetch(
          `/api/experiments/${encodeURIComponent(activeExperiment)}/runs/${encodeURIComponent(activeRun)}?ts=${Date.now()}`
        );
        if (!res.ok) throw new Error(`Failed to load run (${res.status})`);
        const data = (await res.json()) as RunDetail;
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
  }, [activeExperiment, activeRun]);

  const sidebar = (
    <Sidebar
      experiments={experiments}
      loadingExperiments={loadingExperiments}
      activeExperiment={activeExperiment}
      onExperimentChange={(id) => {
        setActiveExperiment(id);
        setActiveRun(null);
        setRunDetail(null);
      }}
      runs={runs}
      loadingRuns={loadingRuns}
      activeRun={activeRun}
      onRunChange={setActiveRun}
    />
  );

  const experimentLabel =
    experiments.find((e) => e.id === activeExperiment)?.label ?? "Corpus";

  const main = (
    <div className="main">
      <header className="main-header">
        <h1>{experimentLabel} Run Viewer</h1>
        <p>
          Inspect pipeline runs: pred vs gold on disposition, exemption engagement,
          public-interest balance, and per-atom grounding — with the model&apos;s own
          reasoning on failures.
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

      {runDetail?.kind === "eval" ? (
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

      <RunView run={runDetail} failuresOnly={failuresOnly} />
    </div>
  );

  return <Layout sidebar={sidebar} main={main} />;
};
