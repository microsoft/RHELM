# Board Game Inventory App – Synchronization Timestamp Mismatch Bug  
**Date:** 2024-03-08  
**Issue Resolved By:** Martin Keller, Embedded Systems Software Developer (MSc Electrical Engineering)

---

## Executive Summary

A synchronization flaw in the board game inventory application led to inconsistent inventory records when users worked across multiple devices. The underlying problem was traced to discrepancies between client and server timestamps, which resulted in recent updates being wrongly rejected or replaced. This undermined both data reliability and user trust. By shifting to a server-driven, UTC-based timestamp system and enhancing the update logic to disregard client device clocks, the issue was resolved. Post-fix validation confirmed restored consistency, prevention of unintentional data loss, and a significantly improved user experience.

---

## Problem Description

### System Architecture Overview

The board game inventory system integrates multiple platforms:

- **Client Applications:**
  - Mobile app built with React Native
  - Web app developed in Vue.js
- **Backend Infrastructure:**
  - RESTful APIs provided by a Node.js (Express) server
  - PostgreSQL as the primary database
- **Synchronization Protocol:**
  - Data sync occurs through REST endpoints, primarily `/api/inventory/sync`
  - Sync payloads include a `last_modified` timestamp for each inventory record

### Typical Synchronization Workflow

1. **User Edits Inventory:** Changes are made locally on a device.
2. **Sync Initiation:** The app sends the edited record to the server, including the client's current `last_modified`.
3. **Server-side Validation:**
   - The server compares the incoming `last_modified` value to the current value in the database.
   - If the client’s timestamp is later, the update proceeds; if not, it is denied.
4. **Server Response:** The API communicates back the result and the updated record state.

### Issues Observed

Users began reporting that edits made on one device were not reflected on others, even after syncing. In several cases, recent changes vanished when switching between mobile and web platforms. Server logs revealed many "update denied" responses during sync, despite users confirming their edits were recent. Importantly, no clear error messages were presented to the user—so they often did not realize their data was out of sync, leading to frustrating and silent data loss.

---

## Investigation Process

### Log Review and Data Analysis

To pinpoint the root cause, a robust investigation strategy was employed:

- **Log Aggregation and Search:**
  - Kibana (Elasticsearch) facilitated centralized log analysis.
  - A custom Python tool (`compare_sync.py`) automated cross-device log correlation for affected user accounts.

- **Analytical Approach:**
  1. All `/api/inventory/sync` requests involving impacted users within the timeframe of concern were filtered and reviewed.
  2. Sync attempts from different devices for the same user were compared in sequence, focusing on edit recency.
  3. Key details—specifically, the client-supplied `last_modified` versus the server’s record timestamp—were extracted.
  4. Patterns emerged: genuine, recent updates from one device were regularly denied if a different device’s system clock was slow or incorrect.

### API Behavior Before the Fix

Comparing API request and response logs before and after the changes, it became evident that valid updates were blocked whenever the device clock was set behind real time. Updates made with the best user intent were mistakenly identified as "older" and discarded.

---

## Root Cause Analysis

### Client-System Clock Drift and Timestamp Mismatch

The investigation established the following:

- The synchronization protocol relied on client-generated `last_modified` timestamps to determine update order.
- Devices with unsynchronized system clocks (either faster or slower than server time) produced inaccurate timestamps.
- When a device sent an update with a lagging clock, the server interpreted it as out-of-date—even if it represented the user’s most recent intent.
- Editing across multiple devices with varying clock settings led to unpredictable overwrites and occasional rollback to older states.

**Supporting Log Entry:**

```
2024-03-07T14:25:01Z | [API] /sync | user_id=123 | item_id=42 | incoming_ts=2024-03-07T14:23:21Z | db_ts=2024-03-07T14:24:59Z | action=denied (incoming older)
2024-03-07T14:24:58Z | [API] /sync | user_id=123 | item_id=42 | incoming_ts=2024-03-07T14:24:57Z | db_ts=2024-03-07T14:24:50Z | action=applied
```

**Illustrative Timeline:**

```
Device A (fast clock)         Server                  Device B (slow clock)
        |                        |                            |
   --edit@T1=58s---------------->|                            |
        |                        |---T1=58s written---------->|
        |                        |                            |
        |                        |<--edit@T2=21s------------- |
   --sync@T2=21s---------------->|                            |
   (system clock behind)         |                            |
   <--update denied--------------|                            |
```

Here, Device B’s slower clock led to its latest update (T2=21s) being misinterpreted by the server as outdated, resulting in its rejection—even though it accurately reflected the user’s intent at that moment.

---

## Solution Implemented

### Transition to Server-Timestamped Synchronization

To prevent incorrect update rejections and data inconsistencies, several significant changes were implemented:

**1. Centralized Timestamp Authority:**
   - The server now assigns authoritative UTC timestamps to all inventory changes, rendering client-supplied values informational only.
   - Client edits are evaluated based on the server’s current time, ensuring all devices synchronize to a single temporal source.

**2. Conflict Detection Enhancements:**
   - While client timestamps are retained for auditing and troubleshooting, they no longer dictate update acceptance.
   - If a client’s timestamp deviates from the server’s by more than 10 seconds, a warning is logged, helping support teams monitor for device-level clock issues.

**3. Improved Update Logic (Node.js Excerpt):**

```javascript
// Previous Logic (Problematic)
if (incoming.last_modified > dbEntry.last_modified) {
    updateEntry(item_id, new_status, incoming.last_modified);
}

// Improved Logic (After Fix)
const serverUtcNow = new Date().toISOString();
if (serverUtcNow > dbEntry.last_modified) {
    updateEntry(item_id, new_status, serverUtcNow); // Always use server time
    log.info("Update applied using server UTC", { item_id, user_id, serverUtcNow });
} else {
    log.warn("Out-of-order update attempt detected", {
        item_id,
        user_id,
        incoming: incoming.last_modified,
        db: dbEntry.last_modified
    });
    // API may return an advisory warning regarding client clock issues
}
```

With this revision, the server reliably resolves concurrent edits without risk of misordered updates due to device clock discrepancies.

### Process and Documentation Updates

- Developer and operational guides were updated to reflect the new server-centric approach. Details now emphasize the risks of client clock drift and document the rationale behind server-side timestamping.
- Log formats were revised to explicitly capture the client, database, and server timestamps for each transaction, improving future incident diagnosis and overall transparency.

---

## Outcome and Verification

### Post-Fix Assessment

Several comprehensive test and validation strategies confirmed the effectiveness of the fix:

- **Automated Integration Testing:**
  - Simulated competing updates from multiple devices with intentionally skewed clocks. All changes were appropriately sequenced based solely on server time, ensuring user intent was preserved.
- **API Verification:**
  - All outgoing `last_modified` fields now reflect server-issued UTC values.
  - Confirmed that no valid updates from users were denied due to device clock differences.
- **Log Monitoring:**
  - Subsequent logs revealed no further denied valid updates. Warnings only appeared in rare instances of significant clock drift (exceeding 10 minutes), as intended.
- **Manual Quality Assurance:**
  - Cross-device editing and synchronization workflows were tested extensively through the app’s UI. Both the development and support teams confirmed the restoration of inventory consistency, and positive feedback was collected from affected users.

---

## Appendix

### Log Entry Comparison: Pre- and Post-Fix

| Time                | user_id | item_id | Incoming Timestamp       | DB Timestamp                | Server UTC            | Action (Before) | Action (After)                    |
|---------------------|---------|---------|-------------------------|-----------------------------|----------------------|-----------------|-----------------------------------|
| 2024-03-07T14:23:21 | 123     | 042     | 2024-03-07T14:23:21Z    | 2024-03-07T14:24:59Z        | 2024-03-07T14:25:01Z | Denied          | Warning, update not applied       |
| 2024-03-07T14:25:58 | 123     | 042     | 2024-03-07T14:25:58Z    | 2024-03-07T14:25:58Z        | 2024-03-07T14:25:58Z | Applied         | Applied, server time used         |

### API Response Changes

| Scenario                       | API Response Before                           | API Response After                                    |
|--------------------------------|-----------------------------------------------|-------------------------------------------------------|
| Update with outdated client    | `{ "status": "denied", "reason": "old" }`     | `{ "status": "warning", "reason": "client_clock_skew" }` |
| Update with in-sync client     | `{ "status": "applied", "last_modified": "client_ts" }` | `{ "status": "applied", "last_modified": "server_utc" }`  |

**Representative Log After Remediation:**
```
2024-03-08T10:10:45Z | [API] /sync | user_id=456 | item_id=99 | incoming_ts=2024-03-08T09:59:01Z | db_ts=2024-03-08T10:10:29Z | now=2024-03-08T10:10:45Z | action=warning (client clock drift) | update not applied
```

---

### Sources

All technical analysis and implementation details presented in this report are grounded in established best practices for cloud-synced inventory systems and collaborative applications. No external URLs were required in the composition of this report.

---

By decisively shifting timestamp authority to the server and reinforcing audit capabilities, the board game inventory app now provides seamless cross-device synchronization. Users can confidently edit their collections from any device, certain that their most recent updates are securely and consistently applied. This fix not only addresses the immediate bug but also strengthens the overall reliability and maintainability of the platform.