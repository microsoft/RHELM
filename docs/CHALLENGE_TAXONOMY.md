# RHELM Challenge Taxonomy

This document provides a comprehensive taxonomy of challenging memory questions in **RHELM**. The taxonomy outlines seven major categories (*Fact*, *Temporal*, *Hallucination*, *Aggregation*, *Misleading*, *External Source*, *Mixed*) and their corresponding complex characteristics requiring advanced reasoning capabilities.

## Overview

RHELM features a comprehensive taxonomy of challenging memory questions across three major QA domains:

- **I. Dialogue History QA** - Questions based on conversation history
- **II. External Source QA** - Questions requiring information from attachments and emails
- **III. Hybrid Context QA** - Questions combining multiple information sources

---

## I. Dialogue History QA

### Fact Questions

| Challenge Characteristic | Description |
|-------------------------|-------------|
| Multi-Hop Traversal | Requires retrieving answers via intermediate links |
| Entity Disambiguation | Distinguishing between entities with similar attributes |
| State-Dependent Attribute | Identifying dynamic properties at a referenced state |
| Negative Constraints | Filtering candidates based on exclusion criteria |

### Temporal Questions

| Challenge Characteristic | Description |
|-------------------------|-------------|
| Indirect Identification | Identify specific events via indirect markers |
| Sequence Comprehension | Reason about events based on relative ordering relationship |
| Long-Horizon Synthesis | Synthesizing distinct temporal facts spanning long periods |
| Implicit Temporal Lookup | Deducing specific time of an event described by context or features |

### Hallucination Questions

| Challenge Characteristic | Description |
|-------------------------|-------------|
| Misattribution | Disentangling details linked to incorrect entities, times, or locations |
| Fabrication | Addressing queries regarding facts absent from memory ground truth |
| Preference Conflict | Resolving requests that violate established user constraints or dislikes |
| Contextual Contradiction | Detecting queries logically incompatible with the user's current state |

### Aggregation Questions

| Challenge Characteristic | Description |
|-------------------------|-------------|
| Conditional Counting | Counting items that meet specific, non-trivial filtering criteria |
| Trend Analysis | Comparing quantitative metrics across different contexts |
| Extreme Value | Identifying the most or least under specific conditions |
| Absence Detection | Identifying items or events that did not occur within a defined scope |

### Misleading Questions

| Challenge Characteristic | Description |
|-------------------------|-------------|
| Implicit State Conflict | Proposing requests that implicitly contradict the user's evolved state |
| Proactive Response | Proactively identifying conflict, refuse the request, and propose a safe, constraint-compliant alternative |

---

## II. External Source QA

### Attachment Questions

| Challenge Characteristic | Description |
|-------------------------|-------------|
| Fact Retrieval | Extracts key facts embedded in attachments or tables |
| Table Reasoning | Performs multi-step and cross column reasoning on tables |
| Structural Navigation | Locates information based on headers or document organization |
| Table Aggregation | Performing aggregation operations with conditional filtering |

### Email Questions

| Challenge Characteristic | Description |
|-------------------------|-------------|
| Cross-time Count/Localization | Analyzes count, locates senders/recipients within a specific period |

---

## III. Hybrid Context QA

### Mixed Questions

| Challenge Characteristic | Description |
|-------------------------|-------------|
| Relative Location Positioning | Identifying the topic content and locate its neighbors or substructure |
| Contextual Retrieval | Retrieving context from a different, untouched section |
| Post-Modification Analysis | Analyzes the quantitative state of a document resulting from modifications |

---

## Summary Statistics

| QA Domain | Categories | Challenge Characteristics |
|-----------|------------|--------------------------|
| Dialogue History QA | 5 (Fact, Temporal, Hallucination, Aggregation, Misleading) | 18 |
| External Source QA | 2 (Attachment, Email) | 5 |
| Hybrid Context QA | 1 (Mixed) | 3 |
| **Total** | **8** | **26** |

---

[← Back to README](../README.md)
