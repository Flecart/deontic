import React, { useCallback, useEffect, useState } from "react";
import { CaseBankView } from "./components/CaseBankView";
import { Layout } from "./components/Layout";
import { RunView } from "./components/RunView";
import { Sidebar } from "./components/Sidebar";
import type { CaseBankDetail, RunDetail, RunListItem, Source } from "./types";

export const App: React.FC = () => {
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
  const isCaseBank = activeSourceMeta?.type === "casebank";

  const sidebar = (
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
  );

  const main = (
    <div className="main">
      <header className="main-header">
        <h1>{sourceLabel} {isCaseBank ? "Case Viewer" : "Run Viewer"}</h1>
        <p>
          {isCaseBank
            ? "Browse generated case banks: filters, gold labels, bank items, and narrative memos."
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

      {!isCaseBank && runDetail && runDetail.kind !== "label" ? (
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
      ) : (
        <RunView run={runDetail?.kind === "casebank" ? null : runDetail} failuresOnly={failuresOnly} />
      )}
    </div>
  );

  return <Layout sidebar={sidebar} main={main} />;
};
