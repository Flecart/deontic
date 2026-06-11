import React, { useCallback, useEffect, useState } from "react";
import { Layout } from "./components/Layout";
import { RunView } from "./components/RunView";
import { Sidebar } from "./components/Sidebar";
import type { RunDetail, RunListItem } from "./types";

export const App: React.FC = () => {
  const [runs, setRuns] = useState<RunListItem[]>([]);
  const [activeRun, setActiveRun] = useState<string | null>(null);
  const [runDetail, setRunDetail] = useState<RunDetail | null>(null);
  const [loadingList, setLoadingList] = useState(false);
  const [loadingRun, setLoadingRun] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [failuresOnly, setFailuresOnly] = useState(false);
  const [lastUpdatedAt, setLastUpdatedAt] = useState<number | null>(null);

  const loadRuns = useCallback(async (background = false) => {
    try {
      if (!background) setLoadingList(true);
      const res = await fetch(`/api/runs?ts=${Date.now()}`);
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
      if (!background) setLoadingList(false);
    }
  }, []);

  useEffect(() => {
    void loadRuns(false);
    const interval = window.setInterval(() => void loadRuns(true), 5000);
    return () => window.clearInterval(interval);
  }, [loadRuns]);

  useEffect(() => {
    if (!activeRun) {
      setRunDetail(null);
      return;
    }

    let cancelled = false;
    const loadRun = async (background = false) => {
      try {
        if (!background) setLoadingRun(true);
        const res = await fetch(`/api/runs/${encodeURIComponent(activeRun)}?ts=${Date.now()}`);
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
  }, [activeRun]);

  const sidebar = (
    <Sidebar
      runs={runs}
      loading={loadingList}
      activeRun={activeRun}
      onRunChange={setActiveRun}
    />
  );

  const main = (
    <div className="main">
      <header className="main-header">
        <h1>FOIA Corpus Run Viewer</h1>
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

      <RunView run={runDetail} failuresOnly={failuresOnly} />
    </div>
  );

  return <Layout sidebar={sidebar} main={main} />;
};
