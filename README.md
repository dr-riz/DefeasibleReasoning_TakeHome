# Take‑Home: Defeasible Reasoning from Evidence (30 minutes, CPU‑only)

You will implement a tiny reasoner that decides whether a hypothesis is **Proved**, **Disproved**, or **Unknown** from short **facts**, **rules**, and **preferences** (rule priorities). This task is inspired by *BoardgameQA* (defeasible reasoning with conflicting rules).

## Files in this package
- `defeasible_tasks.csv` — 10 toy tasks with columns: `id, facts, rules, preferences, question, label`.
- `solution.py` — starter script **you must complete**.
- `DECISIONS_TEMPLATE.md` — short rationale template.

## Your tasks
### Part A — Code
Edit **`solution.py`** to:
1. Load and parse each row of `defeasible_tasks.csv`.
2. Evaluate which **rules** are triggered by the **facts**.
3. Resolve contradictions using **preferences** (higher‑priority rule wins).
4. Answer the **question** with one of: `Proved`, `Disproved`, `Unknown`.
5. Print per‑row predictions and final accuracy on the gold `label` column.

Constraints:
- Use only Python standard library (e.g., `csv`, `re`).
- Keep everything CPU-only and runnable in seconds on any laptop.
- Decide which **LLM inference engine** would be optimal for this scenario, and justify your choice.
- Decide which **small LLM model** would be optimal for this task, and justify your choice.

### Part B — Rationale (8–10 lines)
Fill out **`DECISIONS_TEMPLATE.md`** with:
- How you detect rule conditions from facts.
- How you represent and apply preferences.
- Weaknesses of the approach and what you’d improve next.

---

## Input format
- **facts**: Semi‑colon separated snippets (e.g., `Frog has $100; Dog has $30; Lion attacks cat`).
- **rules**: Semi‑colon separated natural language rules prefixed by `R#:` (e.g., `R1: if frog > (dog+lion) then builds plant`).
- **preferences**: Comma or `;` separated priorities like `R2>R1, R3>R2` (higher left wins).
- **question**: A yes/no style query mapped to `Proved` (yes), `Disproved` (no), or `Unknown` (insufficient/conflicting evidence).

## What counts as "proved/disproved"?
- If a **supporting rule** fires and is **not overridden** by a higher‑priority **blocking rule**, the answer is **Proved**.
- If a **blocking rule** fires and is **not overridden** by a higher‑priority **supporting rule**, the answer is **Disproved**.
- If no applicable rule fires (or only conflicts remain without clear priority), return **Unknown**.

---

## Examples (Input → Output)

### Example 1
**facts:** `Frog has $100; Dog has $30; Lion has $20; no attacks`  
**rules:** `R1: if frog > (dog+lion) then frog builds plant`  
**preferences:** *(none)*  
**question:** `Does frog build plant?`  
**expected label:** **Proved**  
**why:** `frog(100) > dog+lion(50)` triggers **R1**; no higher‑priority blocker.

### Example 2
**facts:** `Frog has $100; Dog has $30; Lion has $20; frog attacks cat`  
**rules:** `R1: if frog > (dog+lion) then frog builds plant; R2: if frog attacks cat then frog does not build plant`  
**preferences:** `R2>R1`  
**question:** `Does frog build plant?`  
**expected label:** **Disproved**  
**why:** R1 supports build, R2 blocks build, and **R2 outranks R1**.

### Example 3
**facts:** `Seal is older than 2`  
**rules:** `R2: if has internet device then seal reveals secret; R3: if older than 2 then seal reveals secret`  
**preferences:** `R2>R3`  
**question:** `Does seal reveal secret?`  
**expected label:** **Proved**  
**why:** Even though **R2** is preferred, it doesn't apply (no device info). **R3** applies and is unopposed → Proved.

---

## Running
```bash
python3 solution.py
```
Expected style of output:
```
id:1 predicted: Proved (correct)
id:2 predicted: Disproved (correct)
...
Overall Accuracy: 0.80
```

Good luck!
