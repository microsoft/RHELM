# Orienteering App User Evaluation – ESA Collaboration

**Date:** April 22, 2024  
**Author:** Dr. Elena Markovic, Lead Spacecraft Systems Engineer, ESA

---

## Executive Summary

This report presents the results of the user evaluation for the Orienteering App, conducted as part of the ongoing ESA collaboration initiative. We employed a comprehensive and systematic assessment strategy, including online surveys, in-app analytics, and structured beta field testing. This multi-method approach enabled broad coverage of key areas such as usability, map accuracy, and feature development priorities. All phases of the evaluation followed ESA’s stringent quality and data management protocols for software engineering and documentation.

A notable challenge occurred during the field-testing component—a power outage caused several laptops to fail, resulting in the loss of real-time feedback data. Primarily, this affected qualitative feedback entries and session logs from a specific time window. The incident introduced a gap in the evaluation dataset and reduced the statistical confidence for usability and feature request analysis during that period. This event has underscored the importance of robust risk mitigation and backup protocols to ensure data integrity in future cycles.

Findings and analyses in this report reflect all available and audited data, consistently aligned with ESA best practices for research documentation and reporting.

---

## Methodology Overview

Feedback collection followed four coordinated streams:

- **Online Survey Distribution:** Registered app users received structured questionnaires to gather both quantitative ratings and qualitative comments. The survey design allowed us to explore user satisfaction and pain points with granularity.
- **In-app Analytics:** Passive telemetry tracked user interactions, session lengths, crash frequency, and feature usage. This dataset provided objective measures of engagement and app performance.
- **Beta Field Testing:** Selected participants conducted supervised, on-site evaluations, which included direct observation and real-time comment logging. Monitoring testers in various geographic environments revealed usage patterns and location-specific challenges.
- **Traceability Protocols:** Every survey response and app log was assigned a unique identifier and timestamp, ensuring that feedback was clearly linked to each app version and field environment.

All user data and logs were handled in strict compliance with ESA ECSS-E-ST-40C software standards and ECSS-Q-ST-80C data management protocols, which safeguard auditability, traceability, and statistical validity.[1][2]

---

## User Feedback Summary

Table 1 synthesizes key feedback findings into three main categories:

| Category          | Avg. Rating (1-5) | Representative User Comment                | Statistical Trend                                                            |
|-------------------|-------------------|--------------------------------------------|------------------------------------------------------------------------------|
| Usability         | 4.2               | “Intuitive interface, easy to learn.”      | 78% rated usability 4 or above; negative feedback cited sporadic crashes and UI lag. |
| Map Accuracy      | 3.7               | “Maps are mostly accurate, rural paths missing.” | 55% awarded scores of 4+, but 18% indicated significant gaps in rural testing areas. |
| Feature Requests  | 2.9               | “Would like offline mode and AR compass.”  | 41% submitted targeted feature requests, with offline and AR navigation most requested. |

**Usability** feedback was predominantly positive, with most users praising the intuitive design and learning curve. However, several participants experienced intermittent crashes, occasional UI sluggishness, and difficulties with route recalculation during peak use.

**Map Accuracy** scores reflect satisfactory coverage in urban locations, although many users in rural field tests reported incomplete path data and occasional mismatches in real-time positioning. This feedback points to a clear need for more comprehensive geographic datasets.

**Feature Requests** focused on expanding the app’s capabilities—offline access and augmented reality navigation were cited as the top priorities. There were also recurring suggestions for improved route calculation algorithms and more sophisticated guidance tools.

---

## Data Loss: Power Outage Impact

During one beta field session, a power outage led to the loss of real-time feedback data. Table 2 documents the affected items and implications:

| Category          | Affected Items                  | Nature of Lost Edits              | Implications                                                  | Mitigation Recommendation                          |
|-------------------|---------------------------------|-----------------------------------|---------------------------------------------------------------|----------------------------------------------------|
| Usability         | 3 survey responses              | Live ratings and user comments    | Diminished rating confidence for that session; minor data gap | Schedule hourly automated backups; use portable power banks |
| Map Accuracy      | 1 GPS data session              | Track points, positional logs     | Reduced granularity in rural map analysis                     | Implement offline data caching and battery alerts  |
| Feature Requests  | 2 text suggestions              | Specific feature requests         | Slightly incomplete trend analysis                            | Enable redundant mobile logging and immediate server sync   |

The lost feedback consisted almost entirely of unsynced, in-the-moment survey entries and comment logs. The overall dataset still maintained aggregate reliability, but the lack of granular, session-specific insights around usability and feature preferences constrained our ability to analyze certain regional patterns and innovation requests.

To guard against similar incidents in future evaluation cycles, I recommend strengthening field risk protocols, including more frequent automated backups and ensuring adequate portable power for test devices.

---

## Impact Assessment and Data Integrity

This data loss represents a small yet significant gap in the overall evaluation dataset. Confidence in usability and feature request analysis for the affected time frame is modestly reduced, and some aspects of rural map accuracy were not fully documented. The interruption of edit logs prevents detailed tracing of user-reported problems for that session and limits post-hoc analysis.

Aggregate findings across the evaluation remain sound. Still, fully comprehensive insight—especially regarding user needs in rural regions and critical feature demand—requires either recovered data or targeted further testing. This incident demonstrates the practical importance of robust data recovery and synchronization strategies, fully in keeping with ESA and broader aerospace quality standards.[2][3]

---

## Recommendations

### Core Improvements

- **Directly Address User Feature Requests:**  
  Begin development on offline mode and augmented reality navigation, which emerged as the most desired features. Expand geographic map coverage with particular attention to rural and under-mapped areas. Continue to refine the user interface, targeting faster response times and reduced crash rates.

- **Field Risk Protocols and Data Recovery:**  
  Install hourly automated backup systems on all testing devices and central servers[1]. Standardize usage of portable backup power solutions across all mobile field testing. Set proactive battery alerts for all testers, and integrate offline data caching wherever feasible. Strengthen data rollback and immediate sync procedures, pairing local encryption with robust server integration[2].

- **Data Management Best Practices:**  
  Adhere unwaveringly to ESA ECSS-E-ST-40C and ECSS-Q-ST-80C standards, ensuring consistent software and data quality. Make post-incident reviews standard practice. Incorporate comprehensive multi-level logging—spanning server, device, and cloud—to maximize traceability and data redundancy.

- **Documentation and Stakeholder Communication:**  
  Maintain detailed session and feedback logs for all app users, and deliver regular briefings to stakeholders following each evaluation cycle. Reports should clearly identify any data integrity events and corresponding mitigation strategies.

### Aerospace Standards Reference

- **ESA ECSS-E-ST-40C:** Mandates rigorous software testing, error handling, and backup integration[1].
- **ESA ECSS-Q-ST-80C:** Provides requirements for information management and robust data traceability[2].
- **NASA-STD-1000:** Offers additional guidance on risk-informed data assurance and critical backup planning[3].

---

## Conclusion

The orienteering app user evaluation generated valuable insights for the ongoing refinement and optimization of the product. The unexpected power outage incident has made evident the need to reinforce feedback data resilience and recovery procedures. By integrating stronger risk mitigation protocols and maintaining firm alignment with ESA and international aerospace standards, future user evaluations can achieve greater reliability, depth of insight, and stakeholder confidence.

---

## Sources

[1] ESA ECSS-E-ST-40C: Software Engineering Standard  
[2] ESA ECSS-Q-ST-80C: Data Management and Information Integrity  
[3] NASA-STD-1000: Risk-Informed Data Assurance Protocols  
[4] April 2024 ESA Field User Survey Logs (ESA internal documentation, Markovic et al.)  
[5] ESA App Telemetry Report (April 2024, in-app analytics dashboard)