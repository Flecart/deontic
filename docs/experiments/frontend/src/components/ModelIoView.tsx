import React from "react";
import type { LlmCall } from "../types";

export interface ModelIoViewProps {
  call: LlmCall;
}

function charCount(text: string | undefined): number {
  return text?.length ?? 0;
}

function ExactBlock({
  label,
  role,
  content,
}: {
  label: string;
  role?: string;
  content: string | undefined;
}) {
  const text = content ?? "";
  const empty = !text.trim();

  return (
    <div className="model-io-block">
      <div className="model-io-block-head">
        <h4>
          {label}
          {role ? <span className="model-io-role">{role}</span> : null}
        </h4>
        <span className="model-io-meta">
          {empty ? "empty" : `${charCount(text).toLocaleString()} chars`}
        </span>
      </div>
      <pre className="model-io-pre">{empty ? "(empty)" : text}</pre>
    </div>
  );
}

export const ModelIoView: React.FC<ModelIoViewProps> = ({ call }) => {
  const inputChars =
    charCount(call.system) + charCount(call.user);
  const outputChars = charCount(call.reply);

  return (
    <div className="model-io">
      <div className="model-io-summary">
        <span>
          Model <strong>{call.model ?? "—"}</strong>
        </span>
        <span>
          Input <strong>{inputChars.toLocaleString()}</strong> chars
          {call.prompt_tokens != null ? (
            <> · <strong>{call.prompt_tokens.toLocaleString()}</strong> prompt tokens</>
          ) : null}
        </span>
        <span>
          Output <strong>{outputChars.toLocaleString()}</strong> chars
          {call.completion_tokens != null ? (
            <> · <strong>{call.completion_tokens.toLocaleString()}</strong> completion tokens</>
          ) : null}
        </span>
        {call.seconds != null ? (
          <span>
            Latency <strong>{call.seconds.toFixed(2)}s</strong>
          </span>
        ) : null}
        {call.batch != null && call.batches != null ? (
          <span>
            Batch <strong>{call.batch}/{call.batches}</strong>
          </span>
        ) : null}
      </div>

      <div className="model-io-columns">
        <section className="model-io-column model-io-column--in">
          <h3>Input to model</h3>
          <ExactBlock label="System message" role="system" content={call.system} />
          <ExactBlock label="User message" role="user" content={call.user} />
        </section>

        <section className="model-io-column model-io-column--out">
          <h3>Output from model</h3>
          <ExactBlock label="Assistant reply" role="assistant" content={call.reply} />
          {call.proof_trace ? (
            <ExactBlock label="Proof trace" content={call.proof_trace} />
          ) : null}
          {call.parse_error ? (
            <ExactBlock label="Parse error" content={call.parse_error} />
          ) : null}
        </section>
      </div>

      <details className="model-io-raw">
        <summary>Full call record (JSON)</summary>
        <pre className="summary-raw-json">{JSON.stringify(call, null, 2)}</pre>
      </details>
    </div>
  );
};
