# DECISIONS (8–10 lines)

- How I map facts to boolean conditions / numeric comparisons:
  I use an LLM (Phi model via Ollama) to interpret facts in natural language, which handles both boolean conditions (e.g., "has internet device") and numeric comparisons (e.g., "frog > dog+lion") without explicit parsing.

- How I parse rules (`R#:`) and detect antecedents/consequents:
  Rules are passed directly to the LLM in their natural language form. The model understands the if-then structure and can identify antecedents and consequents without explicit parsing.

- How I represent preferences (e.g., `{'R2': priority 2, 'R1': priority 1}`) and break ties:
  Preferences are included in the prompt as natural language, letting the LLM reason about rule priorities. No explicit data structure is needed since the model handles the logic.

- When I output `Proved` vs `Disproved` vs `Unknown`:
  - Proved: When a supporting rule applies and no higher-priority rule contradicts it
  - Disproved: When a blocking rule applies and no higher-priority rule contradicts it
  - Unknown: When no rules apply or there are unresolvable conflicts

- Known weaknesses (string brittleness, limited comparators, negation handling):
  - LLM responses may be non-deterministic even with low temperature
  - Model might struggle with complex numeric comparisons
  - Fallback heuristics are very simplistic
  - No explicit handling of double negations or complex logical structures

- Next steps (normalization, symbolic parser, use LLM for rule grounding, unit tests):
  - Overall accuracy is poor. Explore improvements on these dimensions: data preprocessing, prompt engineering, llm swapping
  - Add prompt templates to improve consistency
  - Implement explicit numeric parsing for better accuracy
  - Add unit tests for edge cases
  - Create a hybrid system combining symbolic reasoning with LLM insights
  - Cache common reasoning patterns

- How this scales to bigger datasets (schema, error handling, logging):
  - Add batch processing for multiple queries
  - Implement request rate limiting for API calls
  - Add detailed logging of LLM responses and reasoning steps
  - Create a schema validator for input data
  - Add error recovery and retries for API failures

- Guardrails or safety checks I would add (bounds, missing fields, noisy input):
  - Validate input fields are non-empty and well-formed
  - Add timeouts for API calls
  - Normalize text input (trim whitespace, standardize separators)
  - Sanitize numeric values and check for reasonable bounds
  - Verify rule syntax follows expected patterns
