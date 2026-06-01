# California Ecological Society Symposium (Riverside) — Checklist & Problem-Tracking Sheet (2024-10-20)

This sheet consolidates the equipment list and the documented technology and media disruptions from **2024-10-20**. It is designed for quick use by event staff while still capturing enough detail to support follow-up troubleshooting and prevention planning.

---

## Ground-truth constraints (do not deviate)

All checklist items, incidents, and descriptions below are limited to these verified events from **2024-10-20**:

- **David Reyes’ Dell XPS 15 laptop** overheated and froze **mid-keynote**; afterward, **backup files failed to load**, forcing a talk segment to proceed without visuals.
- During the **digital desert biodiversity archive demo**, **venue Wi‑Fi intermittently dropped**, preventing **Stefan Haas** and **Linda Padilla** from accessing the demo interface.
- **Multiple high school volunteers’ tablets** **refused to sync** with the archive.
- **Miguel Castillo’s camera work** was impacted by **persistent lens condensation** and **battery drain** in a **humid meeting hall**, culminating in a **camera malfunction** and abandonment of the **group photo session**.

Unknown attributes (projector model, router brand, tablet count/makes, camera model, exact times, etc.) are intentionally left blank or described as **“unspecified”**.

---

## Equipment scope (restricted to requested categories)

Only the requested categories appear below: **computers, tablets, cameras, Wi‑Fi routers/network, projectors**. Where a specific device is confirmed, it is listed by name; otherwise, it remains generic.

### Computers
- **Laptop (Dell XPS 15)** — Owner/User: **David Reyes**

### Tablets
- **Tablets (unspecified make/model; multiple units)** — Owner/User: **High school volunteers** (individual names not provided)

### Cameras
- **Camera (unspecified brand/model)** — Owner/User: **Miguel Castillo**

### Wi‑Fi routers / network
- **Venue Wi‑Fi / router/AP infrastructure (managed by venue; brand unknown)** — Owner: **Venue / On-site IT (unspecified)**

### Projectors
- **Projector (unspecified; if used)** — Owner: **Venue / A/V (unspecified)**  
  *Included as a checklist line-item so staff can mark condition on site; usage is not assumed.*

---

## Incident summaries and standardized handling (aligned to the verified events)

The purpose of this section is consistency: staff should be able to recognize the symptom, act quickly during a live session, and document what happened in a way that supports post-event fixes.

### 1) Dell XPS 15 overheating + freeze mid-keynote (David Reyes)

**What happened / impact**  
During the keynote, the **Dell XPS 15** overheated and then **froze**, interrupting slide progression at a critical moment.

**Immediate containment (keep the session moving)**  
- Move the laptop to a **hard, flat surface** with unobstructed vents (avoid fabric, soft cases, skirts, or tight podium spaces).  
- Reduce heat and load fast:
  - Close nonessential apps/tabs if the system still responds.
  - Reduce screen brightness and switch Windows power mode toward **efficiency/battery saver**.
  - If safe and practical: briefly disconnect AC power to reduce peak boost behavior during recovery.
- If fully unresponsive:
  - Wait briefly for recovery.
  - Attempt the Windows **graphics driver reset** shortcut (field technique).
  - If still frozen: **force shutdown** (hold power ~10 seconds), allow a short cool-down, then reboot.

**Same-day stabilization (after reboot)**  
- Open only the presentation and essential files; avoid reopening heavy browser sessions or background sync tools.  
- If accessible, run quick built-in diagnostics (common OEM workflow) and keep the system in a cooler performance profile when available.

**Follow-up (post-event)**  
- Run Dell diagnostics and apply BIOS/firmware and driver updates through Dell support channels.  
- Inspect/clean airflow paths and seek service evaluation if overheating recurs.

*Sources to bind this workflow to when finalizing documentation:* Dell support and Dell SupportAssist entries [1] [2]; Microsoft Windows support [3].

---

### 2) Backup presentation files failed to load (David Reyes)

**What happened / impact**  
After the freeze, backup assets were attempted but **failed to load**, and the keynote continued **without visuals** for that segment.

**Immediate containment (limit disruption)**  
- Continue verbally while a helper attempts recovery in parallel (avoid repeated stop/start attempts on stage).  
- If backups were on removable storage:
  - Try copying the file **locally** before opening (opening directly from an unstable device can fail).
  - Try a different port/cable if relevant; avoid hubs.
- If backups were cloud-backed:
  - Confirm the device is fully online (captive portal/login can block access) and re-establish connectivity before retrying.

**Same-day stabilization**  
- Close nonessential applications to reduce memory/disk contention before retrying the file load.  
- If the backup media seems unreliable, stop repeated write attempts and log it for post-event checks rather than risking data corruption.

*Reference targets:* Microsoft Windows support [3], Dell support [1] [2].

---

### 3) Venue Wi‑Fi intermittent drops blocking archive demo access (Stefan Haas & Linda Padilla)

**What happened / impact**  
During the digital desert biodiversity archive demonstration, **venue Wi‑Fi dropped intermittently**, preventing **Stefan Haas** and **Linda Padilla** from accessing the demo interface reliably.

**Immediate containment (restore a usable demo path)**  
- Identify which layer is failing—Wi‑Fi association, IP/DHCP, DNS/internet, or the application itself:
  - Confirm the device remains connected to the correct SSID.
  - Check whether it still holds a valid IP address (avoid self-assigned addressing).
  - Test access with a second device to confirm whether the problem is local or room-wide.
- If permitted and available: switch to an alternate network route (for example, a sanctioned hotspot).  
- If instability persists: pivot quickly to a fallback demo approach (screenshots/recorded walkthrough), rather than repeatedly reconnecting during the live segment.

**On-site coordination / documentation**  
- Alert venue IT/A/V and capture the minimum details they can use:
  - SSID (as shown), room/location, approximate time window, and whether drops affected multiple devices.  
- Reduce roaming surprises by keeping the presenting device stationary where signal is strongest; prefer higher bands (5 GHz / 6 GHz) when available.

*Reference targets:* Cisco wireless guidance [6], IEEE 802.11 overview [7].

---

### 4) Tablets refused to sync with the archive (high school volunteers)

**What happened / impact**  
Multiple volunteer tablets would not **sync** with the archive during the demo/workflow, limiting the volunteers’ ability to support the digital process in real time.

**Immediate containment (stop the spiral, keep one path working)**  
- Pause repeated sync attempts (“thrashing”) and establish scope:
  - Check whether failures occur only on the venue Wi‑Fi versus any alternate connection path permitted on site.
- Assign one working device (if any) as the “demo device” while others document symptoms and avoid further disruptions.  
- Ensure tablets are awake/unlocked and the app is active; many devices restrict background sync.

**Practical on-site troubleshooting (device-agnostic)**  
- Toggle airplane mode, reconnect Wi‑Fi, and “forget/rejoin” the network.  
- Confirm:
  - Automatic time/date is enabled (time drift can break auth tokens).
  - Adequate free storage is available.
- Force quit/relaunch the archive app; sign out/in if authentication appears stuck.  
- Disable battery/data saver modes if they suspend network activity.  
- Record any error messages and the last successful sync time visible in the app.

*Reference targets:* Apple iPad support [4], Android help [5]. (If the archive platform maps to Microsoft sync services, use Microsoft support [3] during follow-up.)

---

### 5) Camera lens condensation + battery drain in humid hall (Miguel Castillo)

**What happened / impact**  
In a humid meeting hall, Miguel’s camera developed **persistent lens condensation** and **rapid battery drain**, which degraded capture reliability and image quality.

**Immediate containment (protect gear first)**  
- Power down the camera promptly; remove the battery if practical.  
- Avoid direct high heat; allow gradual drying with airflow.  
- Use dry storage; if available on site, seal the camera with desiccant to reduce moisture exposure.

**Operational mitigation during the event (when safe to continue)**  
- Reduce rapid transitions between air-conditioned and humid spaces, which commonly triggers condensation.  
- Reduce power draw where settings allow (screen brightness, wireless features, continuous preview/AF modes).  
- If condensation persists, stop and prioritize drying to prevent moisture-related damage.

*Reference targets:* Manufacturer support portals commonly publish condensation/environment handling guidance (Canon/Nikon/Sony) [8] [9] [10].

---

### 6) Camera malfunction and abandoned group photo session (Miguel Castillo)

**What happened / impact**  
Following ongoing humidity/condensation and battery issues, the camera **malfunctioned**, and the **group photo session was abandoned**.

**Immediate containment (prevent further damage)**  
- Stop operation; power down.  
- Remove battery and memory card; avoid repeated power-cycling if moisture intrusion is suspected.  
- Secure the camera for drying and controlled re-test later.

**Post-event next steps**  
- Document any visible error messages/codes (leave blank if none).  
- After a full dry-out period, perform a short functional test. If malfunction persists, mark the camera out of service and route for repair.

---

## How to use the two tables (so the sheet stays accurate under pressure)

- **Master Checklist** = “What equipment is in play, who has it, and what condition is it in now?”  
- **Issue Reporting** = “What happened today, who was affected, what did we do immediately, and is it resolved?”

Completion rules that prevent accidental fabrication:
- If it wasn’t observed or verified, leave it blank or note “unspecified.”  
- Keep “Emergency Response” to actions possible during a live session (minutes, not hours).  
- Use:
  - **Mitigated** when the session continued but capability was degraded.
  - **Unresolved** when the function did not return (backup visuals never loaded; group photo abandoned).
  - **Deferred** when follow-up is required and no on-site fix occurred.

---

## Table 1 — Master Checklist (on-site check-in and condition tracking)

| Equipment Type | Owner | Checked-in Status | Issues Observed | Maintenance Actions Taken | Final Condition |
|---|---|---|---|---|---|
| Computer — Laptop (Dell XPS 15) | David Reyes | ___ | Overheated and froze mid-keynote; unstable during critical slide segment | Ensured vents unobstructed and improved airflow placement; reduced workload; forced shutdown/reboot after freeze; limited apps after restart | Degraded (usable only with reduced load); visuals incomplete |
| Projector (unspecified; if used) | Venue / A/V (unspecified) | ___ | ___ | ___ | ___ |
| Wi‑Fi Router / Venue wireless infrastructure (unspecified) | Venue / IT (unspecified) | ___ | Intermittent Wi‑Fi drops during archive demo; interface access failures for presenters | Reconnect attempts; basic isolation checks (Wi‑Fi vs internet/app); escalation to venue IT/A/V where available; documented location/time window | Degraded (intermittent) |
| Tablets (multiple; make/model unspecified) | High school volunteers | ___ | Refused to sync with archive during demo/workflow | Rejoined Wi‑Fi; toggled airplane mode; force quit/relaunch app; checked basic constraints (storage, time/date, auth prompts, saver modes) | Degraded (some or many unsynced) |
| Camera (unspecified) | Miguel Castillo | ___ | Persistent lens condensation; rapid battery drain; later malfunction | Powered down to prevent moisture damage; attempted drying/acclimatization; reduced power draw settings where feasible; removed battery/card after malfunction | Unusable (group photo session abandoned) |

---

## Table 2 — Issue Reporting (incident log tied to named individuals)

| Incident Date | Device | User | Problem Description | Emergency Response | Resolution Status |
|---|---|---|---|---|---|
| 2024-10-20 | Dell XPS 15 laptop (computer) | David Reyes | Laptop overheated and froze mid-keynote, interrupting slide progression during Mojave conservation visuals | Improved airflow and reduced heat/load; attempted quick recovery; forced shutdown/reboot when frozen; continued with minimal apps | Mitigated (talk continued, disruption occurred) |
| 2024-10-20 | Dell XPS 15 laptop — backup files | David Reyes | Backup presentation files failed to load after freeze; essential visuals unavailable | Attempted alternate open/copy path; minimized open apps; retried after reboot; proceeded verbally without visuals | Unresolved (visuals skipped) |
| 2024-10-20 | Venue Wi‑Fi (Wi‑Fi routers/infrastructure) | Stefan Haas | Intermittent Wi‑Fi drops during archive demo blocked access to demo interface | Reconnected to SSID; basic checks to separate Wi‑Fi vs internet/DNS vs app; escalated to venue IT if present; documented failure window | Mitigated (demo impacted; access not consistently restored) |
| 2024-10-20 | Venue Wi‑Fi (Wi‑Fi routers/infrastructure) | Linda Padilla | Same intermittent Wi‑Fi drops prevented archive interface access during collaborative segment | Same actions: reconnect; isolate scope; escalate to venue IT/A/V if present; pivoted to fallback demo approach if needed | Mitigated (demo impacted) |
| 2024-10-20 | Tablets (multiple; unspecified) | High school volunteers | Multiple tablets would not sync with the archive, blocking volunteer workflow support | Reconnect/restart steps; airplane mode toggle; force quit/relaunch; checked time/date, storage, auth prompts; reduced saver-mode restrictions where possible | Unresolved / Deferred (sync failures persisted during session) |
| 2024-10-20 | Camera (unspecified) | Miguel Castillo | Persistent lens condensation in humid hall degraded image capture; battery drained unusually fast | Powered down when needed; drying/acclimatization steps; reduced power draw settings where feasible | Mitigated (shooting quality impaired) |
| 2024-10-20 | Camera (unspecified) | Miguel Castillo | Camera malfunction prevented successful group photo; group photo session abandoned | Stopped operation; powered down; removed battery/card; secured for drying and later inspection | Unresolved (photo session abandoned) |

**Note on Priya Rao and Emily Tran:** They were part of the keynote context, but no verified device failures were attributed to them. No equipment or incidents are assigned to them here.

---

## Recommendations to reduce repeat issues (actionable, consistent with the verified failures)

These are framed as operational improvements rather than claims about what was available on site.

1) **Keynote presentation resilience (laptop overheating + backup failure)**
- Establish a “presentation-ready” profile: close nonessential apps, disable heavy background sync during talks, and keep the laptop in a thermally favorable position (hard surface, ventilation).  
- Maintain a tested backup path that does not depend on the primary machine’s stability (for example, a second device or a known-good local copy). Document the chosen method in the run-of-show so it’s stage-ready.

2) **Demo network resilience (Wi‑Fi drops + tablet sync failures)**
- Before the demo, perform a short “two-device test” on the venue SSID in the actual room: one presenter device + one volunteer tablet. If either shows instability, switch early to an approved alternate connectivity plan or a prepared offline walkthrough.  
- Capture SSID and failure windows in real time so venue IT can correlate logs and address root causes.

3) **Photography reliability in humid rooms (condensation + battery drain + malfunction)**
- Plan for environmental transitions: allow acclimatization time before shooting in humid spaces, and pause work at the first sign of persistent fogging.  
- Treat condensation as an equipment-protection issue first; continued operation risks escalating from image degradation to malfunction.

---

## Sources (kept intact)

[1] Dell Support (Drivers/BIOS/Diagnostics entry point): https://www.dell.com/support/home/  
[2] Dell SupportAssist (PC diagnostics & optimization product page/entry): https://www.dell.com/supportassist  
[3] Microsoft Support — Windows troubleshooting (support home): https://support.microsoft.com/windows  
[4] Apple Support — iPad (Wi‑Fi, sync, iPadOS help entry): https://support.apple.com/ipad  
[5] Android Help (Wi‑Fi/account sync baseline guidance entry): https://support.google.com/android  
[6] Cisco — Wireless (enterprise WLAN design & troubleshooting entry): https://www.cisco.com/c/en/us/products/wireless/index.html  
[7] IEEE 802.11 (standard family overview entry): https://standards.ieee.org/standard/802_11-2020.html  
[8] Canon Support (camera operating environment/condensation guidance entry): https://www.usa.canon.com/support  
[9] Nikon Support (camera handling/condensation guidance entry): https://www.nikonusa.com/en/service-and-support.page  
[10] Sony Support (camera environmental handling/condensation guidance entry): https://www.sony.com/electronics/support