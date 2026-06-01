# Revised Mojave Ground Squirrel (MGS) Survey Map: Technical Summary for Conservation and Land Management Near Ridgecrest, California

## Introduction

Ensuring the long-term survival of the Mojave ground squirrel (*Xerospermophilus mohavensis*, MGS) requires careful, ongoing monitoring across its central habitat in the Mojave Desert. The Ridgecrest region in eastern Kern County has emerged as a conservation priority for both state and federal agencies, given its significant biodiversity, its key role as a population stronghold, and the increasing pressures from development and land use changes.

MGS populations near Ridgecrest face a multifaceted set of threats, including continued urban expansion, proliferation of large-scale renewable energy projects, military activities, off-highway recreation, and ongoing drought conditions that further stress habitat quality and availability. Responding to these urgent challenges, recent survey efforts from 2022 to 2024 have focused on improving monitoring protocols, refining survey designs, and integrating adaptive management practices. These efforts have been informed not only by agency guidance from the California Department of Fish & Wildlife and U.S. Fish & Wildlife Service, but also by ground-level observations and feedback from experienced field staff, including detailed daily notes supplied by Elder.

Recent literature and agency guidance underscore the need for precise spatial documentation, consistent data management, and transparent logic in site selection and transect modifications. The following summary provides an overview of the refined survey methodologies, field protocols, data management workflows, and actionable recommendations that underpin current conservation and land management strategies in the Ridgecrest area.

## Survey Methodology

### Sampling Design and Field Protocols

Transect placement was optimized to capture a representative cross-section of suitable habitats, minimize edge effects from fragmentation, and permit stratified sampling across key microhabitats. Each selected transect is surveyed at least three times during the active season (mid-March through late May), in accordance with both USFWS and CDFW protocols. Survey timing is closely aligned with the peak activity periods for MGS, typically following post-dormancy emergence and scheduled to avoid extreme heat or high winds that can reduce detection probability.

Detection methods incorporate a combination of visual encounter surveys, strategically positioned camera traps, and, when justified by site conditions and permits, live trapping. Additionally, non-invasive scat surveys are utilized to enhance detection coverage. Every field observation is georeferenced using high-precision handheld GPS units, ensuring strict spatial consistency throughout the monitoring program.

### GPS and GIS Data Management

High-accuracy GPS equipment (Trimble Geo7X or equivalent, capable of real-time WAAS/GLONASS correction) is standard for all field teams. Field-derived spatial data are imported into ArcGIS Pro 3.x for map generation, spatial analysis, and attribute table updates. All mapping data maintain a minimum horizontal RMS error of 3 meters or less and are stored in NAD83, California State Plane Zone V (Meters). Comprehensive metadata, including date, observer, equipment model, RMS error, and weather conditions, accompany each spatial dataset.

Prior to field validation, proposed transect adjustments and new placements are visualized within GIS platforms. Peer review of all map edits ensures the accuracy and practicality of recommended site changes before implementation on the ground.

### Criteria for Transect Modification

Transects are modified or relocated based on the following criteria:

- **Habitat Change:** Documented loss or fragmentation from recent land use changes, infrastructure construction, or pronounced vegetation die-off.
- **Field Access Restrictions:** Gaining permission for private properties, safety issues due to terrain, or legal/military site closures.
- **Site History and Population Trends:** Patterns deduced from multi-year non-detections or recurring occupancy, indicating ecological shifts or declining suitability.
- **Observational Feedback:** Incorporation of field staff observations, such as those from Elder’s daily logs, noting site visibility, flag positions, and habitat edge dynamics.

### Data Quality Assurance and Multi-Year Integration

Annual and historical spatial datasets are merged to allow for longitudinal trend tracking. Data harmonization includes standardizing attribute fields, reconciling coordinate systems, and ensuring consistent projection (NAD83, UTM, or State Plane as project-specific). Quality checks are built into the data pipeline: routine spatial joins identify points outside known habitat polygons, and manual reviews cross-reference raw GPS logs with final datasets. Device settings are regularly cross-checked with GIS defaults to prevent systematic projection drift or coordinate misalignment. Version control, thorough readme documentation, and transparent change logs underpin database integrity across survey years.

## Comparative Table of Transect Changes

The table below highlights key changes in transect placement following recent surveys, linking each adjustment to underlying ecological or logistical changes and referencing relevant field notes for traceability.

| Transect Name | Previous Coordinates (NAD83, CA State Plane V) | Current Coordinates (NAD83, CA State Plane V) | Rationale for Change | Relocation Attribution (Elder Ref.) | Ecological/Logistical Driver |
|---------------|------------------------------------------------|-----------------------------------------------|---------------------|-------------------------------|-------------------------------|
| T-Red Mesa-4  | X: 586210 Y: 3958210                           | X: 586410 Y: 3958450                          | Habitat edge lost to widening road (2023 aerial survey) | Field note 2023-04-18: "Blue flag moved 200m NW to account for road expansion, route flagged to maximize cover patches" | Habitat loss, observer safety |
| T-Dry Lake-7  | X: 590360 Y: 3959115                           | X: 590160 Y: 3959115                          | Access blocked by new solar field fencing | Oral comm: Elder 2024-03-08: "No safe entry to south boundary, shifted east, marked with blue/white tape" | Land development, field access |
| T-Gamma-East  | X: 592700 Y: 3958700                           | X: 592700 Y: 3958700 (unchanged)              | Reconfirmed optimal – retained | Elder review: "Flags remain as placed—intact shrub cover" | Site quality stable           |

All coordinates are presented in standardized datum and projection. Field note references tie each change to explicit observations, ensuring clarity and defensibility in all modifications.

An expanded table, including additional attributes, GPS metadata, and segment-level field notes, is available as part of the supplementary GIS data layer for further detail.

## Flagging Protocols and Stewardship Recommendations

Field teams deploy a standardized flag color system to communicate transect status and guidance directly in the field, supporting rapid interpretation by all team members and project partners.

- **Blue Flags (“David’s blue”)**  
  - *Meaning:* Transect is optimal for MGS survey; remains unmodified and cleared for monitoring.
  - *Management Interpretation:* Meets habitat suitability criteria, access confirmed, and demonstrates no recent threats.
- **Red Flags**  
  - *Meaning:* Requires immediate review due to evidence of disturbance or recent habitat alteration.
  - *Management Interpretation:* Indicates new construction, anthropogenic barriers, or detectable displacement of MGS.
- **Yellow Flags**  
  - *Meaning:* Caution is advised; partial site access or signs of marginal or at-risk habitat.
  - *Management Interpretation:* Habitat exhibits signs of degradation (e.g., vegetation thinning, fragmentation); requires increased survey vigilance and more frequent monitoring.
- **White Flags**  
  - *Meaning:* Transect is retired or currently suspended from monitoring.
  - *Management Interpretation:* Site is not viable due to persistent non-detection or irreversible habitat loss; not suitable for regular survey unless conditions change.

### Operational Recommendations

- Continue prioritizing transects marked with blue flags for core monitoring efforts. These sites provide the most reliable data for long-term population and trend analyses.
- For transects flagged red or yellow, institute prompt management review and adapt survey schedules as needed. Decisions should incorporate both field observations and new remote-sensing data.
- Photograph all blue-flag placements and georeference these records within the GIS database. Before each new field season, conduct geo-rectification audits to confirm the integrity of all mapping data.
- Each year, systematically reevaluate transects with white flags. If evidence of habitat recovery emerges, consider reactivating these sites for future surveys.

## Data and Methodological Challenges

Despite careful planning, several challenges regularly arise during fieldwork and data integration:

- **GPS Data Quality:** Occasional issues include reversed coordinate entry (X/Y swapped), loss of decimal precision, or unwanted datum conversions between field devices and main GIS workstations. For example, an entry such as “3959115, 590160” should read “590160, 3959115” (X=Eastings, Y=Northings).
- **Buffer Application Variability:** Inconsistent implementation of habitat buffer rules by field staff has on occasion led to either overestimating or underestimating available habitat area, potentially affecting survey coverage.
- **Flagging Materials:** Periodic supply shortages have resulted in the use of non-standard flag colors, increasing the risk of misinterpretation of in-field guidance.

### Troubleshooting and Quality Control Procedures

To address these issues, the following stepwise checks are enforced:

1. **Coordinate Validation:** Prior to GIS upload, batch scripts automatically verify that coordinate pairs fall within acceptable bounds for CA State Plane V. Anomalies are flagged for manual review.
2. **Projection Consistency:** Field teams provide device setting screenshots to verify datum and projection before uploading data. GIS technicians cross-reference these against system defaults.
3. **Flag Color Audits:** At the start and end of each survey season, all field flags are inspected and compared with the master assignment log. Non-standard colors are noted and replaced with approved materials where possible.
4. **Error Reconciliation:** Any data discrepancies are resolved by referencing original field logbooks and raw device logs. Corrections are transparently documented in the master database.
5. **QA/QC Sign-Off:** All final data and map edits undergo secondary review by a staff member not involved in original data entry before archiving for the year.

## Visual Documentation

Survey map products visually relate all flagged transects to recent threats—such as roads, solar installations, and urban boundaries—using high-resolution aerial imagery as a base layer. The following standardized symbology is applied:

- **Blue lines/points:** Designate core monitoring transects (David’s blue flags)
- **Red polygons:** Denote zones of recent anthropogenic disturbance
- **Yellow buffers:** Indicate at-risk habitat edges requiring caution
- **White Xs:** Represent retired transect locations

Figure 1 (provided in the full digital report) presents the revised geography of MGS transect placement and flag assignments for the Ridgecrest region. This visual approach enables clear and efficient communication among field teams, technical staff, and interdisciplinary management groups.

Digital map data are available in GIS shapefile and KML formats, compatible with both ArcGIS and Google Earth, to support both office-based analysis and portable field access.

## Sources

Detailed standards, procedures, and field guidance referenced herein are defined by the following agency sources:

1. [California Department of Fish and Wildlife Survey Protocols for Mojave Ground Squirrel](https://wildlife.ca.gov/Conservation/Survey-Protocols#552771285-mojave-ground-squirrel)
2. [U.S. Fish & Wildlife Service MGS Monitoring Technical Guidance (2023)](https://www.fws.gov/sites/default/files/documents/2023-mgs-monitoring)

Field methods and stewardship recommendations also integrate extensive feedback from on-the-ground practitioners, as recorded in Elder’s recent field logs and interviews.

## Closing

This technical summary serves as a reference and practical guide for all staff engaged in Mojave ground squirrel conservation and land management in the Ridgecrest area. Adopting these refined monitoring protocols and integrating transparent, adaptive workflows will ensure continued accountability and data quality. Consistent application of these standards will foster better population trend data, inform targeted restoration actions, and help safeguard the viability of MGS populations facing an accelerating pace of ecological change. All guidance provided here should be reviewed annually and adjusted as new research and agency directives become available.