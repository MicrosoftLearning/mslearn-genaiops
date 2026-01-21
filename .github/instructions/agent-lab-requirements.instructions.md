---
applyTo: '**'
---

# Lab Design Requirements and Structure

## Core Principles

All labs in this repository must adhere to two fundamental requirements:

1. **1–3 clear, testable outcomes** — Observable, verifiable results that participants must achieve
2. **A mandatory post-workshop artifact** — Tangible evidence of learning and decision-making

These requirements naturally support a **short → deep-dive lab structure** that works across all topics (tracing, security, cost, reliability, AI, etc.).

---

## Lab Structure: Outcome-Driven, Short + Deep-Dive Model

### 0. Lab Framing (5–10 minutes — non-negotiable)

**This is part of the lab, not prep.**

Every lab must explicitly start here.

#### Required Components

**A. 1–3 Testable Outcomes (Required)**

These must be observable by the end of the lab.

Examples:
- ✅ Tracing is successfully enabled and producing spans
- ✅ Tracing data is used to identify a bottleneck
- ✅ A concrete next action is chosen based on evidence

> **Rule:**  
> If you can't answer "How do we know this outcome happened?" the outcome is invalid.

**B. Post-Workshop Artifact (Required)**

Define it up front, not at the end.

Examples:
- Architecture diagram with tracing points annotated
- Screenshot + short written finding
- Decision record ("We will / will not change X because Y")
- Comparison table across apps or agents

> **Rule:**  
> No artifact = lab is incomplete, even if all steps were run.

**C. Lab Paths Explained**

Clearly explain:
- **Core Path** → minimum viable outcome
- **Stretch Path(s)** → deeper analysis or comparison

This explicitly signals:
> "You can stop after Core and still succeed."

---

## 1. Core Lab: Short Outcome (Hands-On, 20–40 minutes)

This is the **non-optional foundation**.

### Purpose of the Core Lab

The Core Lab exists to:
- Prove the system works
- Build confidence
- Enable a *single, concrete outcome*
- Be completable by **every customer**

It is **not** where insight depth lives.

### Core Lab Design Rules

✅ Scenario-based (not step-based)  
✅ Minimal configuration  
✅ Clear success criteria  
✅ Finishes with an artifact

### Core Lab Structure

**A. Scenario Context**

Give a realistic, concrete starting point.

> "You're operating a service with intermittent latency complaints. You need end-to-end visibility to understand where time is spent."

**B. Minimal Setup**

Only what is required to achieve outcome #1.

For tracing example:
- Enable tracing on *one* app
- Validate spans appear
- Visualize a trace

**C. Verification Checkpoint**

Participants must **prove** success.

Examples:
- "Show at least one trace with service-to-service spans"
- "Identify the slowest span in a trace"

**D. Core Outcome Artifact (MANDATORY)**

Customers produce something durable.

Examples:
- Screenshot annotated with where latency occurs
- Simple architecture diagram with trace points
- One-sentence finding: "Most latency occurs in service X → DB call."

> This artifact is the **hard requirement** that enforces learning transfer.

---

## 2. Deep-Dive / Stretch Lab(s): Insight & Decision (Optional)

These are **explicit extensions**, not "more steps."

### Purpose of Deep-Dive Labs

Stretch labs exist to:
- Drive analysis, judgment, and comparison
- Enable **decision-making**, not configuration
- Adapt to advanced audiences
- Reward curiosity

They should feel investigative, not procedural.

### Deep-Dive Lab Design Rules

✅ Optional, clearly marked  
✅ Multiple paths possible  
✅ Fewer instructions, more prompts  
✅ Ends with a decision or recommendation

### Deep-Dive Structure (Repeatable Pattern)

Each deep dive follows this loop:

**Observe → Compare → Decide**

### Example: Tracing Deep-Dive

#### Stretch 1: Multi-App Comparison

- Enable tracing on a second app or service
- Observe differences in span structure, latency, or completeness

**Prompt:**
> "Which app provides more actionable signal? Why?"

**Artifact:**  
Side-by-side comparison (table or diagram)

#### Stretch 2: Agent or Configuration Comparison

- Compare two agents, sampling rates, or configurations

**Prompt:**
> "What trade-off do you observe between overhead and visibility?"

**Artifact:**  
Decision note:
- Keep current setup ✅
- Change configuration ❌
- Run further test 🟡

#### Stretch 3: Action Planning

- Use trace data to decide on a next optimization or fix

**Prompt:**
> "Based on evidence, what would you do next?"

**Artifact:**  
Concrete next action:
- Refactor service X
- Add DB index
- Adjust retry policy
- Increase sampling temporarily

---

## 3. Lab Close: Explicit Outcome Validation (5 minutes)

This step is mandatory and often skipped—**don't skip it**.

### Required Close-Out Questions

Facilitator explicitly asks:

1. **Which outcomes did we achieve?**
2. **What artifact did you produce?**
3. **What would you do next in your environment?**

### Optional (But Powerful)

Have participants **share artifacts**, not opinions.

---

## Canonical Lab Template (Reusable)

Use this template when creating new labs:

```markdown
# [Lab Title]

**Audience / Prerequisites:** [Define who this is for and what they need]

## Outcomes (1–3, testable)

✅ Outcome 1: [Observable, verifiable result]
✅ Outcome 2: [Observable, verifiable result]
✅ Outcome 3: [Observable, verifiable result]

## Post-Workshop Artifact

[Specify what participants will create/deliver]

---

## Core Lab (Required)

### Scenario
[Realistic, concrete starting point]

### Minimal Setup
[Only what's required for outcome #1]

### Verification
[How participants prove success]

### Artifact Creation
[What they must produce]

---

## Stretch Lab A (Optional)

### Investigation Goal
[What deeper question to explore]

### Prompts
[Questions to guide investigation]

### Artifact
[What to produce]

---

## Stretch Lab B (Optional)

### Comparison / Decision
[What to compare or decide]

### Artifact
[What to produce]

---

## Close-Out

- Verify outcomes achieved
- Capture decisions / next actions
```

---

## Why This Structure Works

- Enforces **outcomes over completion**
- Supports **short + deep-dive naturally**
- Scales from beginner to advanced audiences
- Makes workshops measurable and repeatable
- Turns labs into **decision engines**, not tutorials

---

## Validation Checklist

Before publishing any lab, verify:

- [ ] Lab has 1–3 testable outcomes clearly stated
- [ ] Post-workshop artifact is defined up front
- [ ] Core lab is completable in 20–40 minutes
- [ ] Core lab has clear success criteria
- [ ] Stretch labs are explicitly marked as optional
- [ ] Stretch labs focus on decision-making, not just configuration
- [ ] Close-out questions are included
- [ ] Lab follows scenario-based (not step-based) approach
