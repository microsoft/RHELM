# Field Test Report: Katwijk Dunes Mapping App Update  
**Event Date:** 2024-04-06  
**Location:** Katwijk dunes, Netherlands  
**Participants:**  
- Elena Markovic (Lead Navigator)  
- Aisha Rahman (Equipment Specialist / UI Feedback Lead)  
- Pieter (Technical Observer / Data Logger)  

---

## Executive Summary

This field test set out to evaluate the orienteering club’s newly updated mapping app (v2.1.4-beta) under authentic conditions in the Katwijk dunes. Our assessment focused on three key areas: overall app reliability (particularly GPS performance and error resilience), intuitiveness of the user interface, and how efficiently our team could navigate together using the app. Over the course of a 7.5 km route through varied terrain—including open sand, scrub, and pine forest—the app performed reliably in most respects, showing smooth GPS tracking and responsive map rendering. Although the system encountered a few brief GPS signal dropouts, it managed to recover without losing route progress or data integrity.

Strengths included a robust system recovery from connectivity lapses, improvements in switching between map layers, and clear location updates. Team members provided targeted feedback, especially around the app’s alert tones—some were too quiet to be heard in windy conditions, leading to missed notifications. Immediate risk mitigation steps were recommended to address these high-impact navigational concerns. The test surfaced several routine and critical reliability issues, offering clear direction for the next development and validation stages.

---

## Test Procedure

### Route Overview

- **Distance:** 7.5 km
- **Terrain:** Coastal dunes comprising stretches of open sand, low scrub vegetation, and intermittent pine forest
- **Planned Waypoints:**  
  1. Start (52.2067, 4.4022)  
  2. Checkpoint 1 (52.2075, 4.4071)  
  3. Ridge Crossing (52.2090, 4.4108)  
  4. Forest Edge (52.2112, 4.4133)  
  5. Water Point (52.2130, 4.4155)  
  6. Finish (52.2067, 4.4022)

We began at the designated start point, progressing through each waypoint while monitoring device connectivity, app functionality, and team communication. Each waypoint involved active use of the app’s real-time navigation, alert, and tracking features.

### Weather Conditions

- **Timing:** 10:00–13:00  
- **Wind:** 18–24 km/h, with noticeable gusts on exposed ridgelines
- **Temperature:** 10–13°C; comfortably cool and consistent throughout
- **Visibility:** Clear, with more than 10 km of unobstructed line of sight; some haze present in dips and hollows

Wind at times made touchscreen interaction less responsive and occasionally reduced comfort during prolonged exposure. The absence of moisture led to dry, stable sand conditions, supporting confident footing over all sections. Bright sunlight, especially at mid-morning, sometimes diminished screen visibility due to glare.

### Equipment Used

- **Mapping App:** Version 2.1.4-beta (March 2024 release)
- **Devices:**  
  - Elena: Samsung Galaxy S21 (Android 13)  
  - Aisha: iPhone 13 (iOS 17)  
  - Pieter: Google Pixel 6 (Android 13)
- **GPS Receivers:** Native dual-mode (GLONASS + GPS)
- **Network:**  
  - LTE coverage available for approximately 85% of the route; dropped to 4G or disconnected entirely around the thick forest zone (Checkpoint 4)
- **Accessories:** Portable power banks, screen protectors, and an external compass, ensuring redundancy in the event of device failure or navigation uncertainty

---

## Results

### Performance Metrics

| Metric                         | Value                             | Location(s)                | Notes                               |
|------------------------------- |-----------------------------------|----------------------------|-------------------------------------|
| GPS Signal Dropouts            | 3                                 | Forest Edge, Ridge Crossing| 2–4 minutes per incident; required device reconnection, app recovered location automatically |
| Route Update Speed (Latency)   | 1.1–2.3 seconds                   | Across route               | Average response was 1.7 seconds; slowest in forested sections |
| Map Layer Switching Lag        | 0.6–1.5 seconds                   | Across route               | Water Point showed most noticeable delay |

#### Table 1: Core Performance Metrics

While most locations experienced smooth navigation and fast response times, we observed recurring delay and connectivity issues in areas covered by dense vegetation. The app recovered from dropouts without data loss, though users sometimes had to prompt the device to reconnect manually.

### User Feedback

#### Annotated Screenshots

- **Screenshot 1:** North arrow obscured by map overlay—made orientation challenging, particularly in the dunes  
  ![Annotated Screenshot Sample: Overlay/Arrow Issue](placeholder_url)
- **Screenshot 2:** “Waypoint Reached” alert tone was inaudible against wind noise—team missed several checkpoint notifications  
  ![Annotated Screenshot Sample: Quiet Alert](placeholder_url)
- **Screenshot 3:** Map layer switching speed improved since prior versions, but layer labels remained ambiguous  
  ![Annotated Screenshot Sample: Layer UX](placeholder_url)

#### Feedback Summary

**Aisha Rahman (Equipment / UX):**  
- Requested louder and more attention-grabbing notification tones for critical waypoint alerts, referencing incidents where the alert was not noticed in wind (see Screenshot 2).
- Noted the need for clearer visual feedback during map layer changes; brief confusion occurred when switching between layers with unclear labels.
- Pointed out visibility problems in bright sunlight—app font size and icon contrast occasionally hindered rapid confirmation of waypoint status.

**Elena Markovic (Lead Navigator):**  
- Reported brief disorientation and delay during GPS dropouts where the app failed to reconnect automatically, requiring manual intervention.
- Suggested adding an option for manual position entry when in low-signal areas, enabling continued navigation without waiting for GPS.

**Pieter (Technical Observer):**  
- Tracked latency throughout the route, identifying the forested zone as a hotspot for lost connectivity and increased navigation risk.
- Recommended a more robust auto-reconnect routine and offline map caching for future releases.

---

## Issues & Recommendations

| Issue                                               | Root Cause Analysis                       | Risk Level | Recommendation                      |
|-----------------------------------------------------|-------------------------------------------|------------|-------------------------------------|
| GPS dropouts in forested area                       | Dense canopy, weak LTE, app lacks auto-retry | High       | Fortify auto-reconnect routine; enable offline cached maps |
| Quiet alerts missed in windy segments               | Default notification volume too low, environmental noise | Medium     | Add custom volume/tone settings for critical alerts |
| Overlays obscure orientation tools                  | UI layering issue                         | Medium     | Redesign overlays to maintain clear access to directional cues |
| Unclear map layer names                             | Non-standard terminology, poor labeling   | Low        | Standardize and clarify map layer nomenclature |
| Lag in map refresh after movement                   | Device processing, irregular network performance | Medium     | Optimize app code for smoother updates, add pre-buffering |
| Screen glare reduces visibility                     | Bright ambient light, device screen limitations | Low        | Implement adaptive contrast, larger fonts and icons |

#### Table 2: Issues and Recommendations

Each identified issue was analyzed according to its impact on navigation and user safety, with priority assigned based on risk level and frequency of occurrence. Recommendations target both immediate fixes and longer-term improvements.

---

## Conclusions & Next Steps

The mapping app demonstrated strong core functionality during the field test, but its limitations under certain real-world conditions require attention. Most notably, GPS signal dropouts in forested areas and quiet notification tones during inclement weather represent safety-critical risks in navigation. Addressing these gaps will substantially improve reliability and user experience.

### Action Items for the Development Team

- **GPS Stability:**  
  - Integrate an auto-reconnect function to recover from lost signals promptly.
  - Provide offline map access, particularly where network coverage is inconsistent.
  - Include manual position entry as a backup when GPS is unavailable.

- **Interface and Alerts:**  
  - Allow users to adjust the volume and prominence of key alert tones.
  - Refine overlay transparency to keep orientation and navigation tools unobstructed.
  - Standardize map layer terminology and supplement with instructional overlays for clarity.

- **Performance Optimization:**  
  - Review app logic to minimize route update latency.
  - Add adaptive brightness and contrast modes; increase default font and icon sizes for visibility in direct sunlight.

### Validation Plan

The next stage will include:
- A repeat field test in environments characterized by variable signal strength (multipath, denser foliage) and a larger participant group.
- Inclusion of older device models and alternative operating systems to check compatibility and robustness.
- Simulated connectivity loss scenarios to rigorously test new auto-reconnect and manual override features.
- Expanded user feedback collection on audio and visual notification schemes under realistic outdoor conditions.

### Risk Mitigation

To lower the risk of navigational failures in future events, we will:
- Provide comprehensive offline features prior to deployment for areas with unreliable network access.
- Test notification systems at maximum expected ambient noise levels.
- Train club members on manual override and device recovery methods to ensure quick responses during signal or functionality loss.

---

## Technical Diagrams

### Annotated Route Map: Katwijk Dunes Field Test

![Annotated Route Map](placeholder_url)

**Legend:**
- Red shading marks locations with repeated GPS dropouts
- Blue markers indicate points where map layer switching was assessed
- Highlighted icons pinpoint feedback collection events

---

## Sources

All findings in this report are derived from direct club protocols, participant reflections, and established best-practice methodologies for field testing digital navigation tools. No external sources were used.

---

**Prepared by:**  
Elena Markovic, Aisha Rahman, Pieter  
Orienteering Club Katwijk, 2024-04-06