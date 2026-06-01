# Pilot Study Data Review Summary  
## Nutritional Epidemiology Pilot Using Device-Based Activity Tracking

### Executive Summary

This pilot study evaluated the practicality, usability, and data quality of using Garmin fitness trackers to objectively measure physical activity during nutritional epidemiology fieldwork. The overarching aim was to assess key operational workflows and spotlight any technical or methodological risks before expanding the project to a larger cohort.

Integrating device-based tracking into nutritional field studies offers a significant methodological advantage, providing objective physical activity data to complement traditional dietary intake reporting. However, the success of this approach depends on smooth device syncing, consistent data uploads, and robust real-time monitoring. During this pilot, several operational hurdles were encountered, with synchronization failures emerging as a particular challenge.

**Key findings include:**

- **Device Sync Reliability:** Intermittent or failed Bluetooth connections between Garmin devices and the companion app led to incomplete or missing activity records.
- **Data Gaps:** Unstable connectivity or device errors meant that some fieldworkers lost days of data despite diligent usage.
- **Support Limitations:** Manufacturer support was often unhelpful, prompting the team to rely on internal troubleshooting and peer expertise.
- **Impact on Data Quality:** Even with experienced fieldworkers, technical failures compromised the completeness and consistency of the dataset, highlighting the need for rigorous pre-emptive strategies and more responsive support mechanisms.

This report systematically documents each instance of data loss attributed to device syncing failures, outlines all troubleshooting measures, and assesses the resulting impact on data integrity and study findings. It concludes with clear, data-driven recommendations for strengthening future large-scale deployments.

---

### Data Overview

A comprehensive review compared the activity data expected from each participant to the actual data recorded, with particular focus on identifying the periods and causes of missing data. Devices, impacted timeframes, and types of data gaps are detailed below.

#### Table 1. Participant Activity Data: Completeness and Sync Failures

| Participant ID | Device Model         | Expected Days | Recorded Days | Missing Days | Affected Period(s)            | Sync Failure Description |
| -------------- | ------------------- | ------------- | ------------- | ------------ | ----------------------------- | ----------------------- |
| P001           | Garmin Vivosmart 4  | 14            | 9             | 5            | 2024-10-27 to 2024-10-31      | Device-app pairing loss; entire period without uploads |
| P002           | Garmin Forerunner 45| 14            | 14            | 0            | None                          | No issues; full data captured |
| P003           | Garmin Vivosmart 4  | 14            | 12            | 2            | 2024-10-29, 2024-11-01        | Intermittent Bluetooth dropouts; partial gap resolved manually |
| P004           | Garmin Forerunner 45| 14            | 11            | 3            | 2024-10-25, 2024-10-30–31     | Post-battery depletion, sync failed; missing intervals |
| P005           | Garmin Vivosmart 4  | 14            | 10            | 4            | 2024-10-28 to 2024-10-31      | App crash after update; missed auto-sync window           |

All missing data points have been cross-validated against internal logs and device notifications. Device assignment and fieldwork conditions were tracked throughout the pilot.

---

### Troubleshooting Log

Throughout the pilot, a structured troubleshooting log captured all technical interventions, support interactions, and outcomes associated with device synchronization problems. The team maintained daily records of actions taken, those responsible, and the resolution or persistence of each issue.

#### Table 2. Troubleshooting Actions and Outcomes

| Date       | Action                                 | Responsible         | Context                              | Outcome |
|------------|----------------------------------------|---------------------|--------------------------------------|---------|
| 2024-10-28 | Manual Bluetooth restart & re-sync     | Field technician    | Sync loss noticed (P001, P005)       | P005 temporarily recovered; P001 unresolved |
| 2024-10-29 | Contacted Garmin customer support      | Study coordinator   | Persistent errors (P001, P003)       | No meaningful resolution; generic advice |
| 2024-10-30 | Device firmware update via app         | Field technician    | Follow-up per Garmin instructions    | Sync problems continued; further data loss (P001, P004) |
| 2024-10-31 | Internal escalation to lead (J. Ortega)| Study coordinator   | Ongoing unreliability (multiple)     | App log review retrieved some cached data for P003 |
| 2024-11-01 | Group device reset & full re-pair      | Full field team     | Coordinated troubleshooting          | Normal sync restored for 3/5; data unrecoverable for P001, P005 |

Peer intervention and internal expertise proved more effective than manufacturer support. Cross-functional collaboration reduced ongoing downtime, although not all data could be salvaged.

---

### Impact Assessment

The challenges with device synchronization and data uploads had direct implications for data quality across several critical dimensions:

#### Completeness

Across the pilot, some participants experienced sustained data gaps, with up to 35% of expected days missing in the worst cases. Inconsistencies in device syncing reduced the overall reliability of the dataset, and missing data can undermine the accuracy of physical activity assessments—especially if data loss is related to participant characteristics like behavior or technical confidence.

#### Timeliness

Delays and losses in syncing led to non-contemporaneous data capture, with some activity records failing to align with concurrent dietary questionnaires. This disconnect complicates analyses that rely on accurate time-matching between diet and physical activity episodes.

#### Accuracy and Reliability

Incomplete data not only reduce the statistical validity of physical activity estimates but also risk introducing measurement errors and misclassification. Such limitations can obscure true relationships between dietary intake and activity levels.

#### Systematic Bias

The clustering of syncing failures—particularly in specific device models or among certain users—raises the possibility of systematic bias, especially if the affected individuals share demographic or behavioral traits. These risks must be addressed through careful analysis, including sensitivity and imputation methods where appropriate, and should inform both interpretation and reporting in main study findings.

Given these factors, uninterrupted technical support, regular device quality checks, and continuous monitoring should be embedded in any expanded research protocol.

---

### Recommendations and Next Steps

Drawing on the pilot’s findings, the following measures are recommended to safeguard data integrity and ensure a smooth scale-up:

#### 1. Device and Protocol Optimization

- Conduct comprehensive pre-study stress-tests of all device models with a range of user profiles to flag potential syncing issues in advance.
- Standardize both firmware and app versions to ensure consistent performance across the study cohort, following manufacturer compatibility guidelines.

#### 2. Real-Time Monitoring

- Enable real-time monitoring tools on all field devices, configured to alert for uploads delayed beyond 12 hours.
- Institute daily manual reconciliation between device-side logs and central data repositories, especially during initial deployment.

#### 3. Structured Troubleshooting

- Develop and deliver staff training on a standardized troubleshooting protocol (shared as an appendix), which should outline:
    - Immediate technical steps (restart, re-pair, update procedures)
    - Clear escalation pathways to data management leads (leveraging internal experts)
    - Contingency plans, including manual log export methods, for persistent device failures

#### 4. Proactive Manufacturer Engagement

- Establish a dedicated point of contact with the device supplier or alternative vendors, ensuring prompt escalation for field-specific needs around retention and data continuity.

#### 5. Team Communication

- Use a live, visible issue tracker accessible to all field staff to document ongoing and resolved issues.
- Schedule regular meetings with the data management lead, with cross-training to promote self-sufficiency and rapid issue resolution.

#### 6. Protocol Amendments and Quality Control

- Incorporate pilot lessons into the main study manuals, checklists, and participant guides.
- Plan for periodic quality control audits covering both device procedures and backend data aggregation during the main study.

---

### Troubleshooting Protocols & Data Monitoring (Appendix)

**Field Troubleshooting Protocol:**

1. Attempt Bluetooth restart and manual device sync.
2. Update device firmware and companion app; confirm successful sync after updates.
3. If unresolved, escalate internally to the data management lead for deeper log review.
4. Contact device manufacturer with full log files if necessary.
5. If device support fails, extract data manually from the device when possible and provide a replacement unit.

**Data Monitoring Best Practices:**

- Deploy automated daily sync checks with system alerts for missing or overdue data uploads.
- Maintain redundant logs on both device and cloud systems.
- Record all deviations from protocol, sync failures, and corrective actions in a centralized, time-stamped log.
- Monitor for abnormally low or flat activity records as potential flags for missing data, integrating analytic review into regular quality control.

---

### Sources

1. Internal best practices and methods adapted from established nutritional epidemiology fieldwork, device-based activity monitoring, and pilot study quality assurance standards.

---

This pilot underscores the importance of rigorous technical protocols and responsive team structure when integrating wearable devices into nutritional research. Addressing technical gaps early and fostering internal expertise will enhance data quality and support the successful, scalable use of digital tracking in future studies.