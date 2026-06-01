# GPS Mapping App Beta Field Test Report Meeting ESA Technical Evidence Standards

---

## Title Page

**Field Test Date:** 18 May 2024  
**Location:** Amsterdamse Waterleidingduinen, Noord-Holland, Netherlands  
**GPS Coordinates (approx.):** 52.3300° N / 4.5840° E  
**Test Lead and Participants:**  
- Dr. Elena Markovic, Lead Spacecraft Systems Engineer, European Space Agency (ESA)  
- Pieter  
- Aisha

---

## Executive Summary

This report documents a comprehensive field evaluation of the GPS Mapping App Beta, conducted under conditions designed to mirror requirements for aerospace-grade navigation. Our aims were to measure real-time positioning accuracy, mapping reliability, application responsiveness, and overall stability, referencing standards critical to both ESA missions and advanced civil navigation.

The performance of the Samsung Galaxy S23 Ultra was generally strong, with a consistent median GPS error of approximately 2.2 meters—acceptable for consumer outdoor recreation but not sufficient for more demanding ESA operational tolerances. While environmental conditions were favorable and allowed for uninterrupted satellite connectivity, several technical concerns were observed. The app experienced intermittent instability, notably crashing during rapid map layer toggling and responding sluggishly to input from accessibility devices. These factors, coupled with a minor but persistent delay in compass recalibration, reveal that the software needs enhancements in fail-safe operation and multi-device interoperability to be considered for aerospace deployment.

Our assessment identifies key upgrade pathways for improving reliability, redundancy, and accessibility, all of which are required for compliance with ECSS navigation and safety standards.

---

## Methodology

### Devices Under Test

- **Primary Device:** Samsung Galaxy S23 Ultra  
  - Qualcomm Snapdragon 8 Gen 2 chipset, dual-frequency GNSS (GPS, GLONASS, Galileo, BeiDou)
  - Firmware: One UI 6.1 (Android 14)  
  - GPS Mapping App Beta version: 0.9.5b
- **Backup Device:** A mid-tier Android smartphone with single-frequency GPS (L1), running the same app version for direct comparison

### Test Route Description

The evaluation was performed along a circular trail in the Amsterdamse Waterleidingduinen.  
- **Start:** Entrance Zandvoortselaan (52.3312° N, 4.5828° E)  
- **Finish:** Oase Visitor Center (52.3280° N, 4.5843° E)  
- **Total Distance:** 5.3 km  
- **Waypoints:** 15, spaced 350–400 meters apart, as recorded in the GPS track logs appended to this report

### Environmental Conditions

Field testing occurred under steady atmospheric conditions, with air temperatures between 17–19°C and humidity in the 62–68% range. Broken clouds with no precipitation ensured continuous reception of 12–16 satellite signals throughout. No significant atmospheric anomalies, such as multipath or solar interference, were encountered.

### Data Acquisition Protocols

- GPS data logged every second (1 Hz)
- Trail markers provided by local management served as ground-truth reference, surveyed for position accuracy
- Each device performed a GPS cold start before starting the test; compass recalibration was executed at all main trail branches
- Risk controls included:  
  - Backup device with identical software, in parallel logging  
  - Manual notation of positions every 500 m (both paper and digital)  
  - Review of emergency procedures in accordance with ESA field safety standards [2]

---

## Observations and Issues

### Trail and GPS Position Comparison

| Waypoint | Trail Marker (Lat/Lon) | GPS Device (Lat/Lon) | Error (m) | Satellites | Atmos. Notes  |
|----------|-----------------------|----------------------|-----------|------------|---------------|
| WP1      | 52.3312 / 4.5828      | 52.3311 / 4.5827     |    1.6    |     13     | Clear         |
| WP2      | 52.3315 / 4.5825      | 52.3316 / 4.5826     |    2.2    |     14     | Clear         |
| WP3      | 52.3319 / 4.5822      | 52.3317 / 4.5820     |    2.7    |     13     | Light cloud   |
| ...      | ...                   | ...                  |   ...     |    ...     | ...           |
| WP15     | 52.3280 / 4.5843      | 52.3282 / 4.5840     |    2.1    |     15     | Clear         |

Median positional error was 2.2 meters. The largest discrepancy, observed at WP11, reached 4.4 meters during a brief episode of denser cloud cover and foliage intrusion, which reduced satellite counts.

### Device and App Performance

| Metric                      | S23 Ultra (Primary) | Backup Device        | Notes                                           |
|-----------------------------|---------------------|----------------------|-------------------------------------------------|
| Mapping Accuracy (%)        | 98.7                | 94.2                 | Most points aligned closely to trail markers     |
| Compass Calibration Lag (s) | 0.8                 | 1.3                  | More evident during abrupt directional changes   |
| Wrist Brace Input Delay (s) | 1.1                 | 1.4                  | Input sluggishness affected usability            |
| App Crash Instances         | 1 (WP7, 78 min in)  | 2                    | Linked to rapid map layer toggling               |
| Recovery Time (Crash, s)    | 20                  | 38                   | Automated restart worked well, esp. on S23 Ultra |

The primary issues encountered included reduced responsiveness when interacting through a wrist brace, longer calibration lag on backup device, and isolated crashes upon switching between terrain and satellite map overlays, revealing insufficient error-handling.

---

## User Feedback

### Direct Participant Commentary

**Dr. Elena Markovic:**  
"GPS accuracy met civilian standards, but multipath effects near denser vegetation were handled poorly. Overlay refresh lagged when quickly toggling map layers, and the app crash, though recoverable, is not acceptable for mission-critical contexts."

**Pieter:**  
"Live tracking was usually accurate for hiking. I did notice some small mismatches near trail markers, particularly when using input controls through my wrist brace—the delay or occasional freeze made route changes slower and navigation less intuitive."

**Aisha:**  
"The app was simple to use visually, which kept me confident in orientation, but it crashed twice when I switched view modes quickly. Restarting was straightforward, although it disrupted concentration and could be improved for reliability."

### Identified Issues

- Sluggish or delayed navigation when using wrist-brace accessibility device
- Application instability and crashes during rapid map overlay changes, especially pronounced on non-premium hardware
- Recurring lag in compass recalibration after turning onto new trail branches
- Occasional GPS signal loss in dense foliage

### Satisfaction and Usability Ratings

| User           | Satisfaction | Usability |
|----------------|-------------|-----------|
| Dr. Markovic   |      4      |     4     |
| Pieter         |      4      |     3     |
| Aisha          |      5      |     4     |

**Average Scores:** Satisfaction: 4.3 / 5 | Usability: 3.7 / 5

---

## Recommendations

### 1. Reliability and Fault Tolerance

- Improve error-handling routines to ensure seamless operation during rapid map layer switches. This should include implementing fail-safe mechanisms as outlined by ECSS-Q-ST-40C [3].
- Augment GNSS support with multi-frequency capability and real-time signal quality analysis to reinforce navigation integrity for mission-critical scenarios.

### 2. Risk and Contingency Controls

- Integrate a real-time watchdog system and automated diagnostic logging. This will aid swift root-cause identification of anomalies and support rapid recovery procedures.
- Add notification prompts after auto-recovery following crashes so users are always informed of the system state, preventing unnoticed interruptions in operational navigation.

### 3. Device and Accessibility Interoperability

- Standardize calibration procedures and optimize app responsiveness to minimize error and lag across different device models and accessibility input hardware.
- Conduct formal validation across a broader range of Android devices to guarantee consistent performance and rendering, in accordance with ECSS-E-ST-10-06C [4].

### ESA Implementation Priorities

1. **Crash and error resilience** — highest priority for safety and reliability  
2. **Accurate real-time tracking** — required for data integrity  
3. **Accessibility support** — enables inclusive, user-friendly interfaces  
4. **Cross-device reliability** — ensures continuity in mixed hardware environments

---

## Appendices

### A. Extracts from Raw Field Notes

- "WP7: Both devices crashed after changing map layers; altitude data was unaffected. S23 Ultra restarted in 20 seconds, backup device took almost twice as long."
- "At WP11, GPS error peaked at over 4 meters. Signal count reduced by dense foliage."
- "Compass response was noticeably slow after sharp turns, particularly at crossroads."

### B. Annotated Screenshots

- Screenshot 1: Map overlay at WP3, with discrepancies highlighted
- Screenshot 2: Crash notification at WP7, timestamped 12:47 UTC
- Screenshot 3: Compass recalibration prompt during trail branch navigation

### C. GPS Track Logs

- All recorded positions provided as NMEA trace files (.log format)
- Overall route heatmap generated by the app
- Complete waypoint list with timestamps, position errors, and environmental data

### D. Environmental Data

- Temperature/humidity measurements collected at multiple points
- Hourly sky condition log
- Map of GNSS satellite visibility throughout the trail route

---

## Sources

[1] ECSS-E-ST-50-14C Navigation software — ESA System Standards  
[2] ESA Field Test Safety Guidelines  
[3] ECSS-Q-ST-40C Software Safety Assurance  
[4] ECSS-E-ST-10-06C Technical Documentation  
[5] Samsung Galaxy S23 Ultra Official Specifications  
[6] Amsterdamse Waterleidingduinen Official Trail Info

---

## Conclusion

The GPS Mapping App Beta provided reliable civilian-grade navigation in favorable field conditions. Its ease of use and clarity on premium devices ensure strong baseline suitability for hiking and general outdoor activities. Nevertheless, observed weaknesses—particularly in crash resilience, device interoperability, and accessibility responsiveness—require attention before adoption in aerospace or critical mission contexts. Implementation of robust error handling, greater hardware compatibility, and accessibility support remain top priorities for advancing towards ESA certification and future operational deployment.