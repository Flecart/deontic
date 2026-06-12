export interface Source {
  id: string;
  label: string;
  type: "corpus" | "modal" | "casebank";
  run_count: number;
}

export interface RunListItem {
  name: string;
  mtime: number;
  kind: "eval" | "label" | "modal" | "casebank" | "expa_eval" | "other";
  model?: string;
  arms?: string[];
  case_count: number;
}

export interface CaseItem {
  atom: string;
  id: string;
  phrase: string;
  polarity: boolean;
}

export interface CaseGold {
  share_status: "obligatory" | "permitted" | "forbidden";
  violation: boolean;
  notify_required: boolean;
}

export interface ExpACase {
  case_id: string;
  tier: number;
  variant: number;
  acted: boolean;
  assignment: Record<string, boolean>;
  items: CaseItem[];
  gold: CaseGold;
  narrative: string;
  leak_flags: string[];
}

export interface CaseBankDetail {
  name: string;
  mtime: number;
  source: "expA";
  experiment: string;
  kind: "casebank";
  meta: Record<string, unknown> & { llm_arms?: string[] };
  summary: {
    case_count: number;
    acted_count: number;
    pending_count: number;
    leaky_count: number;
    assignment_count: number;
    by_tier: Record<string, number>;
    by_share_status: Record<string, number>;
  };
  cases: ExpACase[];
}

export interface AtomFailure {
  atom: string;
  kind: "missed" | "extra";
  where: string;
  reasoning: string;
  call_ts?: string;
}

export interface LlmCall {
  ts?: string;
  type?: "llm_call";
  case?: string;
  slug?: string;
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
  proof_trace?: string;
  parse_error?: string | null;
}

export interface ArmScores {
  cases: number;
  scores: Record<string, string | null>;
  failure_cases: number;
}

export interface CaseResult {
  id: string;
  arm: string;
  kind: "eval" | "label" | "modal" | "expa_eval";
  tier?: number;
  acted?: boolean;
  model?: string;
  tokens?: number;
  secs?: number;
  pred_assignment?: Record<string, boolean> | null;
  gold_assignment?: Record<string, boolean>;
  question_type?: string;
  story?: string[];
  question?: string;
  expected?: string;
  predicted?: string;
  correct?: boolean;
  parse_error?: string | null;
  label?: Record<string, unknown> | null;
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
  source: "corpus" | "modal" | "expA";
  experiment: string;
  kind: "eval" | "label" | "modal" | "expa_eval";
  meta: Record<string, unknown>;
  summary: {
    llm_calls: number;
    arm_results: number;
    prompt_tokens: number;
    completion_tokens: number;
    seconds: number;
    scores: Record<string, string | null>;
    failure_cases: number;
    by_arm?: Record<string, ArmScores>;
    by_question_type?: Record<string, { cot?: number; kb?: number; n?: number }>;
    kb_parse_success?: number;
  };
  cases: CaseResult[];
}

export type ExpARunDetail = RunDetail & { kind: "expa_eval"; source: "expA" };
