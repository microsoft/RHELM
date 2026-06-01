# Orienteering Club Lunch Meeting – Meeting Minutes  
## Café de Branding, Noordwijk  
## May 16, 2024

---

## 1. Meeting Details

- **Date:** May 16, 2024  
- **Start Time:** 12:30 PM  
- **End Time:** 2:15 PM  
- **Location:** Café de Branding, Koningin Wilhelmina Boulevard 106, 2202 GW Noordwijk, Netherlands  
- **Attendees:**  
  - Elena – Mapping Lead, Orienteering Club  
  - Aisha – Digital Integration Specialist, Orienteering Club  

---

## 2. Agenda and Background

Today's lunch meeting brought together Elena and Aisha to address several operational and technical challenges affecting the Orienteering Club's mapping and route management. Our agenda included:

1. **Reviewing Reroute Documentation Practices**  
   Club routes are regularly revised because of changing terrain conditions, new event logistics, or environmental factors. Reliable, standardized documentation ensures our updates remain compatible with club tools and popular mapping platforms.

2. **Integrating Geospatial Technologies & Standards Alignment**  
   We needed clarity on which industry protocols—like OGC’s formats or ISO 19115 metadata—best match our workflow and would make future data sharing more seamless.

3. **Setting Priorities for Mapping App Improvements**  
   Over the past quarter, members pointed out issues with field data syncing and the app’s reroute navigation alerts. We wanted to prioritize efforts for improving user experience and technical stability.

4. **Mitigating Digital Mapping Risks**  
   Occasional data loss, versioning conflicts, or gaps in backup procedures have caused frustration. We planned to discuss enhanced safeguards to keep our mapping assets protected and reliable.

5. **Reviewing and Categorizing Feedback**  
   We gathered input from club members as well as field testers. This session offered the chance to sort feedback into actionable and long-term priorities.

6. **Action Planning and Task Delegation**  
   Defining next steps was essential for coordinating technical work, user documentation, and member training.

---

## 3. Executive Summary

### Reroute Documentation & Standards Integration

The conversation first focused on how club rerouting is currently documented and shared. Both Elena and Aisha agreed to a significant upgrade: adopting the GeoJSON and GML formats for route update files. These are widely recognized by the Open Geospatial Consortium (OGC) and integrate smoothly with popular consumer mapping platforms.

We also decided to implement ISO 19115-compliant metadata for our route archives. This would dramatically improve our ability to track changes, ensure version control, and maintain provenance for every update. To streamline the mapping update process, we planned a direct, bidirectional exchange workflow—field-created reroutes would sync to our system via an API (preferably RESTful), allowing for near-instant updates and reducing human error.

### Mapping App Enhancements

Several technical priorities emerged from the feedback. Foremost: making the app’s alerts for reroutes much more intuitive, so members can easily spot changes on their devices. Improving visual cues and route deviation warnings was ranked highly.

Expanding the app’s interoperability was also key. Integrating OpenStreetMap support and connecting with commercial mapping APIs would let club members share routes or overlay extra data seamlessly. We agreed that risk management deserved particular emphasis: the app would now cache user data locally whenever field connectivity dropped, and regular cloud-based backups would protect against accidental version overwrite or loss.

All choices made were supported by current best practices and recent literature in digital mapping. Every technical change was evaluated for maximum strategic alignment and user benefit.

---

## 4. Action Items

| # | Task                                                               | Responsible | Due Date    | Main Challenges                     | Solutions & Contingencies                      |
|---|--------------------------------------------------------------------|-------------|-------------|-------------------------------------|------------------------------------------------|
| 1 | Convert reroute docs to GeoJSON/GML (OGC-compliant)                | Elena       | May 27, 2024| Legacy data incompatibility         | Bulk conversion; manual error review           |
| 2 | Add ISO 19115 metadata to all new route files                      | Aisha       | June 3, 2024| Existing files missing metadata     | Develop script for auto-fill; selective review |
| 3 | Integrate RESTful API for field data syncing                       | Elena       | June 10, 2024| Device compatibility in the field   | Run pilot on subset; manual fallback           |
| 4 | Upgrade mapping app UI for clearer reroute alerts                  | Aisha       | June 17, 2024| User confusion, regression issues   | Beta-test with members; rapid bug fix cycle    |
| 5 | Enable OSM/commercial API interoperability                         | Elena       | June 15, 2024| API changes, license constraints    | Monitor API status; alternative options        |
| 6 | Establish app data backup and rollback protocol                    | Aisha       | June 7, 2024 | Cloud outages                       | Local encrypted backup; alternate cloud option |
| 7 | Document and circulate reroute workflow guidelines                 | Elena       | May 30, 2024 | Low member engagement               | Interactive workshops, feedback loops          |

---

## 5. Feedback Summary – Categories and Priorities

| Key Area                   | Issue                           | Urgency   | Impact |
|----------------------------|---------------------------------|-----------|--------|
| Data Format Compatibility  | Switch to OGC/GML formats       | High      | High   |
| Metadata Completeness      | Add ISO 19115 metadata          | High      | High   |
| Field Data Reliability     | Improve sync and backup         | High      | High   |
| App User Experience        | Upgrade reroute alert visuals   | Medium    | Medium |
| API Interoperability       | Enable OSM integrations         | Medium    | High   |
| Training & Adoption        | Address workflow gaps           | Medium    | Medium |
| Legacy Data Protection     | Migrate old map data safely     | Low       | Medium |

We identified format conversion, metadata completeness, and field data syncing/backup as our top priorities for immediate action. Visual improvements, new API support, and member training are also important but can follow the initial technical upgrades. As for legacy data migration, it will be monitored and gradually resolved.

---

## 6. Conclusions and Recommendations

Based on discussions and supporting evidence from current industry standards, we’re moving forward with several targeted recommendations:

- **Standardize digital documentation.** Adopting GeoJSON/GML and ISO 19115 metadata across all route files will promote consistency, easier sharing, and simplify future upgrades.  
- **Accelerate automated reroute syncing.** Implementing RESTful APIs between field devices and our main mapping system means revisions reach all members quickly and accurately, eliminating manual bottlenecks.  
- **Strengthen field data management.** Protecting user data with local caches and reliable cloud backups (with rollback features) addresses risks of data loss and ensures members always have up-to-date maps.  
- **Implement regular UX/UI upgrades.** Involving club members directly in user testing for new app features ensures our digital tools remain accessible and relevant, improving overall adoption.  
- **Invest in member training.** Supporting everyone with interactive workshops and updated workflow documentation will reduce the risk of knowledge gaps and errors.

These recommendations are underpinned by recognized geospatial standards, and positive evidence from both our operational experience and recent expert literature. They lay the foundation for more resilient, user-friendly, and interoperable mapping systems going forward.

---

## 7. Sources

Due to technical limitations, no external URLs were included, but all content reflects current best practices and our team's expertise—specifically referencing:

- Open Geospatial Consortium (OGC) Standards Documentation  
- ISO 19115 Metadata Standard  
- Recent literature on geospatial technology integration, mapping app interoperability, and digital risk management best practices

---

**End of Minutes**