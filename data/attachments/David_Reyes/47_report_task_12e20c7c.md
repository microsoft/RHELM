# Device Recovery Log: Dell XPS 15 SSD Recovery – David Reyes  
Oscar’s Shop, Ridgecrest, California | June 26, 2024

---

## 1. Device Details

### Overview: Dell XPS 15 – Primary Field Research Laptop

| Field                        | Details                                                                        |
|------------------------------|--------------------------------------------------------------------------------|
| Model                        | Dell XPS 15 (9500 Series)                                                      |
| Processor (CPU)              | Intel Core i7-11800H (8 cores, 2.3 GHz base, up to 4.6 GHz)                    |
| Memory (RAM)                 | 32 GB DDR4                                                                     |
| Storage (SSD)                | 1 TB NVMe PCIe M.2 SSD                                                         |
| Display                      | 15.6" 4K UHD+ (3840 x 2400) InfinityEdge Touch                                |
| Graphics                     | NVIDIA GeForce GTX 1650 Ti with Max-Q                                          |
| Ports                        | 2x Thunderbolt 3 (USB-C), 1x USB-C 3.2, SD card reader, HDMI 2.0               |
| Network                      | Intel Wi-Fi 6 AX201, Bluetooth 5.1                                             |
| Serial Number                | [Redacted for Privacy]                                                         |
| Installed Operating System   | Windows 11 Pro 22H2 (primary), Ubuntu 22.04 (dual-boot for certain units)\*     |
| Primary User                 | David Reyes                                                                    |
| Device Usage Context         | Primary platform for field data storage, ecological data analysis, and grant reporting |

\* Device review confirmed Windows 11 Pro 22H2 as the active system at time of recovery.

#### Backup Status Prior to Recovery

| Backup Field                     | Details                                                                                        |
|----------------------------------|------------------------------------------------------------------------------------------------|
| Backup Type                      | Hybrid (Local external HDD and cloud services: Box, Google Drive)                              |
| Last Successful Backup Date      | June 17, 2024                                                                                  |
| Last Backup Method               | Local: 2 TB USB-C external HDD; Cloud: automated Box sync                                       |
| Retention Policy (Lab SOP)       | Minimum 5 years storage in line with NSF and institutional requirements (FAIR principles)      |
| Backup Rotation                  | Weekly full backup to local HDD, daily incremental uploads to cloud during active research days |
| Backup Scope                     | Comprehensive: “Research_Projects”, “Wildlife_Photos”, “Grants”, “Field_Data” directories      |
| Current Backup Issues            | Cloud sync failed post-last backup (see Section 6 for detail)                                  |

All backup protocols align with best practices—requiring data redundancy, encryption, and full auditability per federal grant stipulations and FAIR data standards [1].

---

## 2. Recovery Date & Location

- **Date of Recovery:** June 26, 2024  
- **Location:** Oscar’s Shop, Ridgecrest, California ([Redacted for privacy])

Ridgecrest is centrally situated near major ecological research sites in the Mojave Desert. Oscar’s Shop provides specialized support for scientific field teams, including rapid turnaround for essential equipment. This proximity is crucial to keeping ongoing ecological monitoring and conservation activities on schedule.

---

## 3. Technician Information

| Name    | Role and Affiliation                                                   | Relevant Certifications                                                     |
|---------|-----------------------------------------------------------------------|-----------------------------------------------------------------------------|
| Oscar   | Owner/Lead Technician, Oscar’s Shop, Ridgecrest, CA                   | SANS GIAC Certified Forensic Examiner (GCFE); ACM Member; NSF compliance experience |

Oscar brings extensive experience in data recovery for research organizations, regularly working under grant-funded data management protocols. His workflows are designed to ensure proper chain-of-custody, accurate documentation, and regulatory compliance at every stage—requirements fundamental for ecological research involving sensitive biological and geographical information.

---

## 4. Recovery Process

The following steps were performed to maximize data security, integrity, and recoverability:

| Step | Description                                                                                                                | Rationale/Best Practice                                              |
|------|----------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| 1    | Device intake and detailed consent review with Principal Investigator (David Reyes) to confirm recovery scope and priorities| Ensures proper handling and respect for sensitive research/PII       |
| 2    | Physical assessment, cleaning, and SSD health check (including SMART diagnostics)                                           | Mitigates risk of hardware failure and verifies SSD readiness        |
| 3    | Connection of SSD via forensic-grade write-blocker                                                                         | Prevents any modification to source data, preserving legal integrity |
| 4    | Full byte-for-byte sector imaging with FTK Imager                                                                          | Enables recovery even with corruption; creates verifiable raw backup |
| 5    | Verification of disk image integrity with MD5 and SHA-256 hashes                                                           | Confirms imaging accuracy for audit/reproducibility                  |
| 6    | Logical examination: Mounted disk images, checked file systems using R-Studio/TestDisk tools                                | Detects file system errors commonly caused by field conditions       |
| 7    | Targeted data extraction by research priority:  
       - Wildlife photos (“/Wildlife_Photos/2024_June/<Site_Name>”)  
       - Grant documentation (“/Grants/2024/”)  
       - Specialized field datasets (“/Field_Data/2024_June/”)                                  | Ensures compliance with grant/FAIR priorities and continuity         |
| 8    | Batch integrity validation (file opening, checksum comparison, user sample review)                                         | Detects silent corruption or incomplete recovery                     |
| 9    | Secure temporary storage: All recovered data was held on AES-256 encrypted drives until retrieval                           | Protects data in transit—required for sensitive ecological data      |
| 10   | Documentation: Comprehensive incident/action log maintained, including all relevant hashes and procedural details           | Essential for compliance, reproducibility, and post-recovery auditing|
| 11   | Data delivery: Recovered files transferred to encrypted external drive, PI review and confirmation of recovery              | Final quality-control step, closes audit chain                       |

Each step above followed established data recovery and research data stewardship protocols to maintain data accuracy, privacy, and auditability.

---

## 5. Data Retrieved

### Summary of Recovered Data

| Data Category   | Field Site / Month        | Original Folder Path                           | File Types         | Data Size | Project/Grant Relevance                                             |
|-----------------|--------------------------|------------------------------------------------|--------------------|-----------|---------------------------------------------------------------------|
| Wildlife Photos | Site_Alpha               | /Wildlife_Photos/2024_June/Site_Alpha          | JPG, RAW           | 15.8 GB   | Habitat disturbance assessment (Mojave Small Mammal Study)           |
| Wildlife Photos | Site_Beta                | /Wildlife_Photos/2024_June/Site_Beta           | JPG, RAW           | 13.2 GB   | Camera trapping, Invasive Species Control Grant                      |
| Wildlife Photos | Site_Gamma               | /Wildlife_Photos/2024_June/Site_Gamma          | JPG, RAW           | 9.3 GB    | Reptile baseline study, wildlife corridors project                   |
| Field Data Logs | All Sites (June 2024)    | /Field_Data/2024_June/All_Sites                | CSV, XLSX, TXT     | 2.4 GB    | Instrumental readings, trapping logs, observation data               |
| Grant Memos     | Award_87345_FY24         | /Grants/2024/NFWF_Award_87345_FY24             | DOCX, PDF          | 225 MB    | Required for NFWF grant reporting                                    |
| GIS Layers      | June Map Layers          | /GIS_Data/2024_June                            | SHP, KML, TIF      | 860 MB    | Habitat/gap analysis, conservation planning                          |
| Outreach/Photos | Workshop_Docs_June       | /Outreach/Workshops/2024_June                  | JPG, PPTX, PDF     | 520 MB    | Stakeholder outreach, education, habitat management workshops        |

*Data volumes and folder structures were matched to the project’s master data inventory for accountability. All mission-critical directories were restored in full, cross-checking size and structure against institutional logs.*

---

## 6. Issues & Recommendations

### Issues Identified During Recovery

| Issue ID | Description                                                              | Impact                                   | Resolution                                      |
|----------|--------------------------------------------------------------------------|------------------------------------------|-------------------------------------------------|
| 001      | Box cloud sync failed after June 17 (fieldwork interruptions/auth expiry) | Recent files not uploaded to cloud       | Sync rescheduled; account authentication pending|
| 002      | Google Drive desktop client stalled on large June batch uploads           | Some folders incomplete on cloud         | Attempted manual transfer; partial cloud recovery|
| 003      | Local USB backup lagged ~10 days behind SSD state                        | ~7GB gap in local backup                 | Addressed by full SSD imaging during recovery   |
| 004      | 12 corrupt RAW files from Site_Gamma batch (06/15)                       | Minor data loss within batch             | Attempted repair; 4 RAW files unrecoverable    |

#### Recommendations for Improved Data Security and Compliance

| ID   | Recommendation                                                                                         | Justification                                                   |
|------|-------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| R-1  | Transition to a cloud backup service supporting end-to-end AES-256 encryption (e.g., institutional OneDrive or Tresorit) | Enhances sensitive data protection; aligns with NSF and privacy guidelines |
| R-2  | Automate and schedule both cloud and local backups, ensuring offsite redundancy                       | Reduces risk of data loss, matches FAIR “Accessible/Reusable” criteria     |
| R-3  | Implement routine integrity checks (hashes, checksums) after each backup cycle                        | Early detection of silent corruption or transfer faults                    |
| R-4  | Maintain a detailed living data audit/inventory documenting all data movement and recovery actions     | Essential for auditability and long-term reproducibility                    |

Key frameworks referenced include the NSF/NIH Data Management Policies, FAIR Principles for ecological data [2], and institutional stewardship/encryption standards.

---

## 7. Final Outcome & Next Steps

### Recovery Assessment

- **Recovery Rate:** 99.7% of targeted data was successfully restored. All primary project directories were fully recovered, and all vital research assets were returned. The minor loss involved four unrecoverable image files in a single photo batch.
- **Validation:** All restored data was checked for integrity through a combination of automated hash validation and manual review by PI David Reyes, ensuring no silent corruption or undetected loss.
- **Chain-of-Custody:** The data remained secure and fully documented throughout the process, supporting institutional and grant compliance.

### Immediate and Future Actions

- **Immediate:**  
  - Complete upload of recovered directories to an institution-approved, encrypted cloud platform.
  - Restore cloud sync functionality for Box and Google Drive, updating credentials and performing test uploads.

- **Short-term (within 7 days):**  
  - Convene a project team meeting to review and update backup/retention workflows per recommendations R-2 and R-3.
  - Store an encrypted secondary copy of recovery data offsite following redundancy policy.

- **Ongoing:**  
  - Schedule quarterly backup audits and disaster recovery simulations.
  - Regularly update and review the data management plan to reflect ongoing grant and institutional requirements.

These steps will improve long-term research data security and ensure seamless compliance with funding, institutional, and regulatory bodies.

---
