export interface RunListItem {
  name: string;
  mtime: number;
  model?: string;
  arms?: string[];
  cases?: string[];
  case_count: number;
}

export interface AtomFailure {
  atom: string;
  kind: "missed" | "extra";
  where: string;
  reasoning: string;
  call_ts?: string;
}

export interface LlmCall {
  ts: string;
  type: "llm_call";
  case: string;
  arm: string;
  batch?: number;
  batches?: number;
  batch_atoms?: string[];
  model?: string;
  system?: string;
  user?: string;
  reply?: string;
  seconds?: number;
  prompt_tokens?: number;
  completion_tokens?: number;
}

export interface CaseResult {
  id: string;
  arm: string;
  pred: Record<string, unknown>;
  gold: Record<string, unknown>;
  hits: Record<string, boolean | null>;
  facts_agreement?: [number, number, string[], string[]] | null;
  atom_failures: AtomFailure[];
  calls: LlmCall[];
}

export interface RunDetail {
  name: string;
  mtime: number;
  meta: Record<string, unknown>;
  summary: {
    llm_calls: number;
    arm_results: number;
    prompt_tokens: number;
    completion_tokens: number;
    seconds: number;
    scores: {
      disposition: string | null;
      engaged: string | null;
      pi: string | null;
      facts: string | null;
    };
    failure_cases: number;
  };
  cases: CaseResult[];
}
