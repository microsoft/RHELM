# Mojave Desert Collaborative Mapping Project: Progress Report  
### Reporting Period: Project Inception – June 23, 2024

---

## Project Overview

The Mojave Desert Collaborative Mapping Project is a multidisciplinary initiative focused on producing high-resolution, ecologically meaningful spatial data to advance biodiversity assessments and conservation management throughout the Mojave Desert ecoregion. This collaboration, involving ecologists, geospatial specialists, and field research teams from several institutions, is working systematically to map significant habitats, identify ecological gradients, and assess human impacts on desert ecosystems.

The Mojave Desert’s status as a critical refuge for arid-adapted species, many of which are endemic or threatened, makes accurate and up-to-date mapping essential. Our outputs are designed to serve both basic scientific research—such as studies of ecosystem resilience—and direct land management and conservation decisions, especially in the context of increasingly rapid climate shifts and mounting land-use pressures. The need for integrated, region-wide conservation strategies has never been greater, and this project aims to underpin those efforts with timely and robust spatial data.

---

## Recent Activities

### Field and Analytical Work

**Spring 2024 Field Campaign:**  
Between March and May, our field teams gathered detailed vegetation, soil, and wildlife occurrence data across 14 strategically chosen sites, ensuring representation of both relatively undisturbed habitats and areas subject to significant disturbance. Standardized mobile applications (notably Fulcrum and Survey123) streamlined data collection, increasing both efficiency and consistency across teams.

Additionally, we installed soil moisture and temperature loggers at 27 microhabitats to provide environmental context for our biodiversity records. These microhabitats were selected to capture a wide range of environmental conditions and to improve our understanding of fine-scale ecological variability.

**Remote Sensing and GIS Analysis:**  
The integration of new Sentinel-2 satellite imagery acquired during March–May 2024 has been central to improving our vegetation community mapping. Leveraging object-based image analysis, the team refined classification procedures to address the high spatial complexity found in alluvial fans—a key feature of the Mojave landscape. These enhancements have already improved the precision of habitat delineations and will support more accurate biodiversity models as mapping continues.

**Data Integration:**  
Efforts are ongoing to harmonize legacy datasets (from 2015–2019) with this season’s new field data. This integration is essential for building continuous, multi-year ecological time series, which are critical for understanding temporal changes in desert ecosystems.

#### SSD File Recovery Efforts

Data integrity is a top priority, particularly given the challenges of fieldwork in remote, harsh environments. In mid-June, the project faced a significant hurdle when one of the field SSDs exhibited severe file corruption, putting valuable data at risk.

**Technical Recovery Approaches:**
- The team utilized industry-standard forensic recovery tools—including R-Studio, FTK Imager, and ddrescue—for sector-level analysis and bitwise cloning, thereby minimizing further drive degradation.
- Custom Python scripts were developed to attempt reconstruction of fragmented `.csv` and `.shp` files, using file signatures and timestamps wherever possible. Batch recovery processes were trialed for files where partial metadata or table-of-contents information was available.

**Recovery Outcomes and Data Integrity:**
- Successful partial recovery included raw sensor data and most geolocation metadata, though some raster and vector files—crucial for mid-season microhabitat mapping—remained corrupted and unusable.
- Rigorous data integrity checks were implemented, and any records with questionable validity have been temporarily quarantined for systematic review before inclusion in final analyses.

---

## Current Status

### Active Workstreams

**Data Cleaning and Quality Assurance:**  
We are conducting thorough cross-verification between recovered datasets and existing backups. Field IDs, geographic coordinates, and time series sensor records are being triple-checked against original paper field notes to ensure accuracy.

**Geospatial Analysis:**  
Preliminary vegetation and landscape models are nearing completion. For those areas with incomplete data due to the SSD incident, the analysis team is quantifying the impact of missing layers and determining the best approaches for addressing data gaps in the interim composite maps.

**Documentation and Reporting:**  
A comprehensive progress report is being prepared for regulatory partners, and preparations for manuscript drafting are underway to ensure scientific findings will be ready for dissemination in accordance with project milestones.

### Status of Corrupted Files

Data loss has been confined to three principal categories:

1. High-resolution drone raster imagery, used for fine-scale habitat modelling;
2. Soil and temperature sensor data logs, central to microhabitat analysis;
3. Field-collected GPS shapefiles documenting precise plot locations.

The team is documenting these losses in detail and assessing impacts on downstream analyses.

### Pending Feedback: Emily Tran

Feedback on Emily Tran’s preliminary habitat classification script has been delayed. Her deliverable relies on the complete integration of spatial datasets—particularly those currently affected by data corruption. Immediate priorities have been placed on data recovery and verification, after which the feedback cycle will resume. Emily and the team have agreed to revisit cross-validation and model refinement once full data reconciliation is achieved.

### Impacts on Ongoing Analysis

- Microhabitat mapping for Survey Blocks 7, 9, and 12 remains incomplete, resulting in temporary gaps in spatial analyses.
- Composite habitat maps now underrepresent fine-scale heterogeneity, a limitation noted in draft methods and pending correction as recovery progresses.
- Certain validation and modeling efforts reliant on the unrecovered data are currently on hold but will be restarted at the earliest opportunity.

---

## Obstacles Encountered

### Technical Challenges

SSDs used in the field faced both logical (filesystem) and potential physical failures, likely intensified by abrupt power losses and extreme temperature fluctuations. On-site data redundancy was not always achievable as daily cloud uploads were twice interrupted by satellite uplink outages.

### Logistical Constraints

Vehicle breakdowns at remote sites delayed not only data collection but also endangered regular backup and charging routines, introducing additional data risk. Maintaining strict protocol adherence proved difficult under these stressful conditions, highlighting the need for ongoing team training and real-time support mechanisms.

### Collaborative Barriers

Asynchronous working schedules between field and office personnel occasionally interfered with timely troubleshooting and data validation. Furthermore, at several critical junctures, limited availability of key technical staff slowed response times during the SSD recovery process.

### Lessons Learned and Adaptive Measures

In response, the team has implemented several immediate improvements:
- A twice-daily backing-up protocol, both in-field and to the cloud, is now standard operating procedure.
- Checksums and on-the-spot data verification routines have been added to the workflow.
- Enhanced connectivity and remote troubleshooting support have been established via the deployment of a Starlink router and expanded IT presence.
- Greater transparency and systematic tracking of feedback and communication delays have been formalized to improve overall project management.

---

## Planned Next Steps

- Complete advanced data recovery procedures for remaining mission-critical files with support from institutional IT and data science groups.
- Plan and, where feasible, execute targeted re-collection of microhabitat and sensor data at affected sites, prioritizing blocks of highest ecological importance.
- Resume Emily Tran’s deliverable feedback and cross-validation cycle as soon as unified spatial datasets are available.
- Finalize and implement the adaptive data management and on-site training protocols for July’s field campaign, ensuring improved redundancy measures are embedded.
- Prepare for the upcoming August dry-season deployment. Field protocols and mapping targets will be revised based on the operational lessons and current data landscape.

---

## Project Timeline

| Milestone                              | Date/Period        | Status      | Bottlenecks/Notes                              | Upcoming Deadlines        |
|-----------------------------------------|--------------------|-------------|------------------------------------------------|--------------------------|
| Project Launch & Protocol Finalization  | Jan–Feb 2024       | Completed   | -                                              | -                        |
| Spring Field Data Collection            | Mar–May 2024       | Completed   | Vehicle issues, satellite uplink delays         | -                        |
| Initial Data Integration Begins         | May–early Jun 2024 | Completed   | -                                              | -                        |
| SSD Data Corruption Detected            | 13 Jun 2024        | Completed   | Data loss risk, instigated urgent recovery      | -                        |
| SSD Recovery & Data Triage              | 13–23 Jun 2024     | Ongoing     | Technically complex, partial restoration        | 30 Jun 2024              |
| Feedback to Emily Tran (postponed)      | 16 Jun 2024 (orig) | Delayed     | Pending data reconciliation                     | 28 Jun 2024 (rescheduled)|
| Q2 Mapping Output Dissemination         | 1 Jul 2024         | Upcoming    | Subject to recovery progress                    | 1 Jul 2024               |
| Dry-Season Field Deployment Prep        | 5–26 Jul 2024      | Upcoming    | Protocol revision and team training             | 26 Jul 2024              |

---

## Data Recovery Summary

| Filename                         | Original Date | Error Type            | Recovery Actions                               | Outcome                  | Ecological Data Category     |
|-----------------------------------|--------------|-----------------------|-----------------------------------------------|--------------------------|-----------------------------|
| plot7_drone_raster.tif            | 18 May 2024  | Partial overwrite     | R-Studio, ddrescue, Python hex scan           | Unrecovered              | High-res habitat imagery     |
| soil_block9_log1.csv              | 20 May 2024  | Logical corruption    | FTK Imager sector search, reconstructive script| Partial recovery         | Sensor log (soil)           |
| gps_plots12.shp                   | 22 May 2024  | Incomplete metadata   | Manual shapefile rebuild, header repair        | Unusable                 | GPS waypoints (plots)       |
| summary_sensor_series7.csv        | 19 May 2024  | Lost file pointer     | Batch recovery, secondary disk backup          | Fully recovered          | Integrated sensor data      |
| field_paper_photos_block2.zip     | 21 May 2024  | CRC error             | 7-Zip repair, re-extraction                    | Recovered (minor loss)   | Field photographic records  |

---

## Feedback Schedule

| Recipient         | Type/Content                | Scheduled/Original Date | Status    | New/Upcoming Date         | Notes                                 |
|-------------------|----------------------------|------------------------|-----------|--------------------------|---------------------------------------|
| Emily Tran        | Habitat mapping feedback    | 16 Jun 2024            | Delayed   | 28 Jun 2024              | Awaiting complete data reconciliation |
| Core partners     | Q2 progress report          | 24 Jun 2024            | On-time   | 24 Jun 2024              |                                      |
| Field teams       | Data management protocols   | 1 Jul 2024             | Pending   | 1 Jul 2024               | To be included in next field briefing |
| Steering committee| Milestone/analysis review   | 8 Jul 2024             | Pending   | 8 Jul 2024               | Will include dry-season planning update|

---
