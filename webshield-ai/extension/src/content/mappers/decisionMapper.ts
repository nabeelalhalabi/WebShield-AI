import type { ContentDecision } from "../../shared/types/moderation";

export interface DecisionInstruction {
  itemId: string;
  action: ContentDecision["action"];
  explanation: string;
  category?: string | null;
}

export function toDecisionInstructions(decisions: ContentDecision[]): DecisionInstruction[] {
  return decisions.map((decision) => ({
    itemId: decision.item_id,
    action: decision.action,
    explanation: decision.explanation,
    category: decision.primary_category
  }));
}
