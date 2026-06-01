# Firmware Debugging Report: Timing Bug in Sensor Calibration  
**Project Name:** Industrial Sensor Firmware  
**Date:** January 29, 2024  
**Author:** Martin Keller  

---

## Executive Summary

This report documents the investigation and resolution of a critical timing issue within the sensor calibration routines of the industrial sensor firmware project. Reliable and accurate sensor calibration is essential for robust system control and monitoring in industrial automation environments. During routine testing and field deployment, we uncovered intermittent failures in the calibration sequence, which resulted in inconsistent sensor outputs, sporadic calibration timeouts, and a higher rate of system faults, particularly under elevated temperatures and increased system loads. 

The analysis presented here describes the origins of the issue, the methods used to isolate and diagnose it, and the corrective actions implemented to restore calibration accuracy and dependability. Furthermore, the report includes a thorough impact and risk assessment, recommendations for maintaining long-term quality assurance, and supporting technical references.

---

## Problem Description

Inconsistent time management within the sensor calibration routine led to unpredictable delays and unexpected timeouts. Detailed investigation revealed that these failures often coincided with varying environmental conditions and elevated system load, indicating a connection between RTOS scheduling, hardware timer behavior, and task prioritization.

### Symptom Summary Table

| Timestamp           | Log Snippet/Observation                  | Affected Module/Component | Frequency/Count | Environmental Context     |
|---------------------|------------------------------------------|---------------------------|-----------------|--------------------------|
| 2024-01-25 08:13:41 | `WARN: CalTimeout @ SensorCal()`         | Sensor Calibration        | 7/30 runs       | +38°C, Low CPU (20%)     |
| 2024-01-25 08:21:18 | `ERROR: Calibration Mismatch`            | Calibration Mgmt         | 5/30 runs       | +44°C, High CPU (85%)    |
| 2024-01-25 09:02:06 | `INFO: Retry Cal. Elapsed: 3020ms`       | Scheduler, Cal Routine   | 11/50 runs      | Load spike, Nom. Temp    |
| 2024-01-25 10:41:09 | `FAULT: No Response from Sensor`         | Sensor Driver            | 2/30 runs       | +41°C, Power fluctuation |
| 2024-01-25 11:27:54 | `WARN: Calibration completed late`       | Calibration Task         | 10/50 runs      | +43°C, RTOS context switch overhead |

#### Observed Trends

- The frequency of calibration failures increased significantly at ambient temperatures above 40°C.
- Higher system CPU loads led to more frequent timeouts and anomalous calibration results.
- Calibration timing inconsistencies were closely linked to RTOS context switching and resultant delays.

### Affected Modules and Components

A number of interrelated software and hardware components contributed to the observed behavior:

- **Sensor Calibration Routine** (`sensor_cal.c`)
- **Calibration Management Layer** (`cal_manager.c`)
- **Sensor Driver Interface** (`sensor_drv.c`)
- **RTOS Scheduler and Task Context**

### Bug Frequency and Statistics

During diagnostics, 160 calibration attempts were monitored. Timing irregularities—such as missed deadlines, excessive retries, or outright timeouts—were observed in 35 runs, representing 21.9% of all attempts. Problem severity peaked when system CPU utilization exceeded 75% or ambient temperature surpassed 40°C.

### Environmental and System Factors

Several contributing factors were identified:
- Elevated ambient temperatures resulted in increased RTOS tick jitter and measurable hardware timer drift.
- CPU load spikes impeded reliable scheduling of the calibration task, further distorting timing.
- Power fluctuations aggravated hardware timer instability, adding another layer of unpredictability to calibration timing.

---

## Root Cause Analysis

The investigation proceeded systematically with the following diagnostic steps:

### 1. Symptom Correlation

Detailed log analysis revealed clear correlations among high system load, elevated temperature, and an escalation in timing errors during calibration. Timing anomalies were most pronounced under these stress conditions.

### 2. Reproducibility Testing

Controlled experiments were arranged on the development testbed. By artificially increasing system load and raising enclosure temperature, the calibration failures could be reliably reproduced, confirming environmental sensitivity.

### 3. Code and Architecture Review

Focused examination of the `SensorCal()` implementation within `sensor_cal.c` exposed a critical flaw: reliance on the RTOS delay mechanism inside the calibration loop.  

#### Annotated Code Snippet (Excerpt)
```c
// sensor_cal.c
void SensorCal() {
    uint32_t start = get_system_time_ms();
    while (!cal_success && (get_system_time_ms() - start) < CAL_TIMEOUT_MS) {
        // Calibration steps
        ...
        rtos_delay(CAL_RETRY_DELAY_MS);   // Non-deterministic delay under system load
    }
    if (!cal_success) {
        log_warn("CalTimeout @ SensorCal()");
    }
}
```
**Identified Issue:**  
The use of `rtos_delay()` introduces variable timing as its actual delay length is dictated by RTOS scheduling and system load, not strictly by a hardware timer. Under heavy CPU usage or frequent context switching, these delays stretch beyond the intended interval. Moreover, the underlying system time source (`get_system_time_ms()`) is susceptible to temperature-induced drift, as outlined in the hardware datasheet.

### System Flow Visualization

```
+-----------------+
| Start Calibration
+-----------------+
        |
        v
+-----------------------+
| Start Timer: t_start  |
+-----------------------+
        |
        v
+-----------------------------+
| [Loop] Attempt Calibration  |
+-----------------------------+
        |
        v
+-----------------------------+
| RTOS Delay (jitter risk)    |
+-----------------------------+
        |
        v
+-----------------------------+
| Check Elapsed Time: t_now   |--[Timeout]--> [Log Timeout Error]
| t_now - t_start < Timeout?  |      
+-----------------------------+
        |
     [Success]
        |
        v
+-----------------------------+
| Finish Calibration          |
+-----------------------------+
```
**Critical Weak Point:**  
The RTOS-dependent delay in each calibration iteration undermines strict control of timing, particularly as the task can be interrupted or delayed in high-load situations, or as hardware timers waver due to thermal or supply variations.

### Analysis of Timing Constraints

- **RTOS Delay Behavior:**  
  The `rtos_delay()` function essentially yields control back to the scheduler. Its wakeup timing is subject to the current RTOS tick and may be delayed further if higher-priority tasks occupy the CPU, especially common during system logging or network operations.

- **Timer and Priority Dependencies:**  
  The calibration task held only 'Normal' priority, often being preempted by higher-priority system functions. The hardware timer used for measuring elapsed time was directly affected by temperature—drifting up to ±2% according to device specifications.

---

## Solution and Implementation

To address these findings, several corrective actions were planned and executed:

### 1. Switch to Precise Hardware-Timed Wait Loop

The calibration loop was modified to use a dedicated hardware timer (`hw_timer_ms()`) for time measurement and delay. By eschewing the potentially variable RTOS delay and basing all timing on a peripheral timer, we achieved predictable delay intervals, unaffected by context switching.

### 2. Elevate Task Priority

The calibration task’s priority was raised within the RTOS configuration, reducing the likelihood of preemption by higher-priority logging or network routines and ensuring more consistent processing time.

### 3. Temperature-Aware Timeout Correction

The timeout logic was augmented to dynamically compensate for estimated hardware timer drift by referencing the onboard temperature sensor, leveraging manufacturer-recommended drift correction algorithms.

### 4. Reinforced Error Logging and Watchdog Integration

Enhanced error detection was implemented, including more granular logging (error source, elapsed time, context data) and coordinated watchdog integration to recover gracefully from unrecoverable calibration stalls.

#### Code Revision Example

**Original:**
```c
while (!cal_success && (get_system_time_ms() - start) < CAL_TIMEOUT_MS) {
    ...
    rtos_delay(CAL_RETRY_DELAY_MS);
}
```

**Revised:**
```c
while (!cal_success && (hw_timer_ms() - start) < (CAL_TIMEOUT_MS * drift_correction_factor())) {
    ...
    wait_until(hw_timer_ms() - prev_retry >= CAL_RETRY_DELAY_MS); // Tight hardware-based wait
    prev_retry = hw_timer_ms();
}
// Task priority set to high in RTOS config
```
In this revision:
- `hw_timer_ms()` is sourced from a hardware timer peripheral, offering consistent timing even under load.
- `drift_correction_factor()` computes a scaling factor according to the measured temperature.
- The calibration loop now waits deterministically for each retry interval, maintaining tight control over total elapsed time.

### Risk Assessment

| Potential Impact                                 | Mitigation                                  | Likelihood | Residual Risk           |
|--------------------------------------------------|----------------------------------------------|------------|------------------------|
| Reduced RTOS responsiveness to non-critical tasks | Monitor for task starvation during stress testing; adjust priorities as needed | Low-Med     | Minor queue delays     |
| Hardware timer misconfiguration or faults        | Extensive regression and hardware-in-loop testing | Low        | Minimal                |
| Calibration still times out under extreme stress | Improved error handling and transparent logging for rapid diagnosis | Low        | Acceptable             |
| Slight increase in power consumption due to tight wait loop | Optimize by allowing low-power sleep during waits when feasible | Low        | Negligible             |

---

## Quality Assurance and Validation

Multiple QA strategies will ensure the robustness of the implemented fixes:

- **Regression Testing:**  
  All calibration-related tests will be rerun across the entire supported temperature range (0°C–60°C) and CPU load spectrum (idle to 100%), with explicit comparison to pre-fix baselines.

- **Automated Test Integration:**  
  The firmware will be incorporated into the continuous integration pipeline. Automated testing with frameworks such as Unity and CMock will facilitate simulation of timer faults and scheduler anomalies.

- **Edge Condition Verification:**  
  Validation will include stress scenarios such as:
  - Extreme temperature and voltage variations influencing timer drift.
  - Forced context switch storms stressing RTOS scheduling.
  - Watchdog intervention during induced calibration stalls.

- **Long-Term Endurance Testing:**  
  The calibration routines will undergo continuous cycling for durations exceeding 24 hours under varying environmental conditions, ensuring stability over time.

- **Peer Code Review:**  
  The revised codebase will undergo rigorous walkthroughs with the firmware development team, focusing on timing algorithms, hardware interfaces, and RTOS integration.

---

## Appendix

### Technical References

- Sensor datasheet: Calibration and timing specifications
- FreeRTOS documentation: Task scheduling and timer primitives
- IEEE 1838-2019: Standard for Calibration of Sensors in Industrial Automation
- Internal timing diagrams: System clock and hardware timer interactions

### Toolchain and Platform Details

- **Compiler:** ARM GCC v10.2.1
- **RTOS:** FreeRTOS v10.4.3
- **Testbed hardware:** STM32L4 family on custom-designed boards

### Contact Information

- Martin Keller, Firmware Engineering Lead  
  martin.keller@company.com  
  Office: +1-555-123-4567  
- Peer Reviewers:  
  - Dr. Ana Tsai, QA Lead  
  - Jonas Schmidt, Embedded Systems Specialist

---

### Sources

1. ARM. "Cortex-M4 Devices Generic User Guide." https://developer.arm.com/documentation/dui0553/a
2. FreeRTOS. "Task Management and Scheduling." https://www.freertos.org/RTOS-task-priority.html
3. IEEE. "IEEE 1838-2019 – Standard for Calibration of Sensors in Industrial Automation." https://standards.ieee.org/standard/1838-2019.html
4. STM32L4 Series Datasheet, STMicroelectronics. https://www.st.com/resource/en/datasheet/stm32l4.pdf
5. Unity Test Framework for Embedded C. https://www.throwtheswitch.org/unity/
6. CMock Framework for Embedded C. https://www.throwtheswitch.org/cmock/

---

**End of Report**