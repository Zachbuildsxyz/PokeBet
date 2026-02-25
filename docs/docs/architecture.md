# Architecture

Wysper is structured as a safety-first execution pipeline:

Signal -> Risk Gate -> Execution -> Log -> Monitor -> (Kill Switch)

## Components
- **Signal**: proposes actions (paper/live)
- **Risk Gate**: enforces hard limits before any order is allowed
- **Execution**: places/cancels orders (dry-run until ready)
- **Log**: writes decision traces with reason codes
- **Monitor**: watches for abnormal conditions
- **Kill Switch**: halts execution when safety triggers fire

## Design goal
Treat capital like infrastructure: bounded risk, predictable behavior, auditability.
