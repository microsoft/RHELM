# DeltaX Embedded Firmware Bug Fix Report

**Project/Module:** DeltaX MCU I/O Control Module  
**Firmware Version:** 3.2.19  
**Report Date:** 2024-08-16  
**Author:** Martin Keller

---

## Executive Summary

On August 16, 2024, two critical bugs affecting the DeltaX embedded firmware were identified and resolved. The first, a flaw in the prioritization of DMA-driven SPI transaction interrupts, resulted in sporadic data corruption and system instability under high-load conditions. The second pertained to the propagation of configuration changes within the real-time clock (RTC) subsystem, leading to time drift and missed scheduling of periodic events.

Both defects threatened the real-time performance and reliability of the system’s control core. Each was subject to detailed root cause analysis utilizing diagnostic logs, stack traces, and targeted code review. The fixes focused on precise configuration and code amendments to ensure correct and robust behavior. Post-fix validation included comprehensive stress and regression testing to ensure system stability. All changes were thoroughly documented, with repositories updated to guarantee complete traceability and reinforce long-term fault resilience in future development cycles.

---

## 1. Detailed Description of Bugs

### 1.1 Bug #1 – DMA Interrupt Priority Misconfiguration in SPI Transaction Handler

#### Observed Symptoms

During routine and stress testing, the following anomalies were identified:

- **Intermittent Data Corruption:** High-frequency SPI2/SPI3 read operations sometimes reported lost or garbled sensor data.
- **System Instability:** The system exhibited random hard faults and watchdog-triggered resets, especially during concurrent DMA transfers.
- **Diagnostic Indicators:**
    - Frequent assertion failures reported at `sensor_manager.c:212`
    - Non-deterministic increments of DMA error counters
    - Kernel logs showing persistent pending DMA interrupts and nested ISRs, leading to unserviced interrupts
    - Example log extract:
        ```
        [2024-08-14 12:11:53.237] [ERROR] DMA_ISR SPI2 RX overflow detected (ch = 2)
        [2024-08-14 12:11:53.238] [WARN ] Pending IRQ: DMA1_Stream2, Prio: 7, Active in ISR nest: True
        [2024-08-14 12:11:53.240] [FAULT] HARDFAULT at 0x08037C10 on main loop entry - stack pointer corrupted
        [2024-08-14 12:11:53.245] [ASSERT] sensor_manager.c:212: rx_len == expected_len - failed
        ```

#### Root Cause Analysis

A detailed analysis traced the issue to an error in setting interrupt priorities:

- **Interrupt Priority Misconfiguration:** The DMA IRQ channels for SPI2 and SPI3 (`DMA1_Stream2_IRQn`, `DMA1_Stream5_IRQn`) were incorrectly assigned the lowest priority (level 7), the same as several non-critical timers and software interrupts.
- **Consequences:** Non-essential ISRs occasionally preempted crucial DMA-complete ISRs, leading to lost SPI transaction completions, unprocessed DMA completions, and, in some cases, stack corruption that triggered hard faults.
- **Supporting Evidence:**
    ```
    12:11:53.237, Enter ISR: EVENT_TIMER_IRQHandler (Pri=7)
    12:11:53.238, NVIC_PendingIRQ(DMA1_Stream2_IRQn)=1; Nested in EVENT_TIMER handler
    12:11:53.241, HARDFAULT upon main() re-entry: SP = 0x20007FA8 (corrupted)
    ```

#### Impacted Subsystems

- `spi_manager.c` (transaction logic)
- `irq_config.c` (interrupt configuration)
- `sensor_manager.c` (polling and error handling)
- **Hardware:** DELTA-X-CNTL-04 SPI2/SPI3 DMA channels
- **Reference Documentation:**
    - SPI2/SPI3 Transaction Layer Specification v2.1.4, §3.2
    - DMA Controller API, `dma_if.h` v1.3, §5.1.2
    - NVIC Configuration Table, `irq_config.c:48-72`

---

### 1.2 Bug #2 – RTC Configuration Propagation Delay

#### Observed Symptoms

After RTC calibration events—such as system clock adjustments or daylight saving transitions—the following behaviors were observed:

- **Scheduler Drift:** Scheduled events consistently showed an 800–900 ms delay in execution after RTC updates.
- **Missed Events:** Periodic tasks, particularly log synchronization and maintenance routines, occasionally failed to execute following such an update.
- **Diagnostic Log Output:**
    ```
    [2024-08-15 09:02:09.082] [WARN ] Scheduler event lag detected: Expected 09:02:09.000, Actual 09:02:09.845
    [2024-08-15 09:02:11.110] [ERROR] Missed periodic task: log_sync (ID=21)
    [2024-08-15 09:02:13.220] [INFO ] RTC RTC_CONFIG_STATUS=STALE, update_flag=1
    ```

#### Root Cause Analysis

Investigation highlighted a gap in event propagation:

- **Failed Update Notification:** The RTC calibration process—via `system_clock.c`—did not properly notify other subsystems of configuration changes, due to a missing event broadcast in the `rtc_notify_update()` routine.
- **System Impact:** As a result, the scheduler continued referencing outdated time values, resulting in significant drift and missed task executions.
- **Corroborating Logs:**
    ```
    09:02:09.081, system_clock.c: Applying RTC calibration offset
    09:02:09.082, rtc_notify_update() called - EVENT not published
    09:02:09.845, scheduler.c: Detected RTC_CONFIG_STATUS=STALE
    ```

#### Impacted Subsystems

- `system_clock.c` (RTC calibration)
- `rtc_manager.c` (RTC state management)
- `scheduler.c` (event scheduling)
- **Hardware:** Onboard RTC (DELTA-X-CNTL-04)
- **Reference Documentation:**
    - System RTC Integration Design Doc §2.3.1
    - DeltaX Scheduling API Spec v3.11, §4.5
    - RTC Manager API, `rtc_manager.h` v2.0

---

## 2. Technical Resolution

### 2.1 Bug #1 – DMA SPI Interrupt Priority Correction

The resolution of this issue involved the following steps:

1. **Fault Replication and Analysis**
    - Used the internal `INTRFLOOD` tool to simulate high-load interrupt conditions, effectively replicating the failure and capturing detailed NVIC and ISR trace data with Tracealyzer.
2. **Auditing and Verification**
    - Conducted a complete audit of `irq_config.c` to verify interrupt priority assignments. This confirmed that DMA channel interrupts used for SPI2 and SPI3 transactions were assigned the same (lowest) priority as several non-critical events.
3. **Configuration Correction**
    - Reassigned SPI-related DMA IRQs (`DMA1_Stream2_IRQn`, `DMA1_Stream5_IRQn`) to a much higher priority (level 3), ensuring they preempt non-essential ISRs.
    - Non-critical interrupts such as `EVENT_TIMER_IRQn` and `SW_EVENT_IRQn` remained at priority 7.
4. **Regression and Stability Testing**
    - The system was subjected to 48-hour regression tests under high-frequency SPI transaction loads.
    - Tests confirmed that data integrity was preserved, error counters remained at zero, and no assertion failures or hard faults were observed.
5. **Documentation and Traceability**
    - All changes were meticulously documented in the project’s changelog (`CHANGELOG.md`) and linked to issue tracker item DXC-4117.

#### Code Difference Illustration

**Prior Configuration (`irq_config.c`):**
```c
NVIC_SetPriority(DMA1_Stream2_IRQn, 7);   // SPI2 RX DMA
NVIC_SetPriority(DMA1_Stream5_IRQn, 7);   // SPI3 RX DMA
NVIC_SetPriority(EVENT_TIMER_IRQn, 7);
NVIC_SetPriority(SW_EVENT_IRQn, 7);
```

**Corrected Configuration (commit b61f4de):**
```c
NVIC_SetPriority(DMA1_Stream2_IRQn, 3);   // SPI2 RX DMA - Priority elevated
NVIC_SetPriority(DMA1_Stream5_IRQn, 3);   // SPI3 RX DMA - Priority elevated
NVIC_SetPriority(EVENT_TIMER_IRQn, 7);
NVIC_SetPriority(SW_EVENT_IRQn, 7);
```

---

### 2.2 Bug #2 – RTC Update Notification Restoration

Resolution steps included:

1. **Recreation of Issue**
    - Applied RTC calibration changes while monitoring the timing of scheduled events and the scheduler’s state via internal logging.
    - Consistently reproduced the execution lag and confirmed missed scheduled events post-update.
2. **Code Path Analysis**
    - Pinpointed the absence of an event publish in the `rtc_notify_update()` function, preventing downstream components from reacting to RTC changes.
3. **Implementation of Event Notification**
    - Inserted a call to `event_publish(EVENT_RTC_UPDATED)` within `rtc_notify_update()`, guaranteeing immediate and system-wide notification of RTC changes.
4. **Validation**
    - Conducted multiple tests involving different RTC update scenarios, observing that all scheduled events resumed correct timing and no further 'STALE' state flags were generated.
5. **Documentation and Issue Tracking**
    - Updated the relevant API documentation and the changelog, referencing bug #DXC-4132 for full traceability.

#### Code Difference Illustration

**Original Implementation (`system_clock.c`):**
```c
void rtc_notify_update() {
    rtc_state.update_flag = 1;
    // Missing: Event publish
}
```

**Corrected Implementation (commit 53e2db7):**
```c
void rtc_notify_update() {
    rtc_state.update_flag = 1;
    event_publish(EVENT_RTC_UPDATED); // Notifies scheduler immediately
}
```

---

## 3. System Behavior: Before vs. After Fix

| Aspect                                 | Before Fix                                                                      | After Fix                                                                                          |
|-----------------------------------------|---------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| **DMA/SPI Transaction Integrity**       | Data corruption, assertion failures, hard faults under high interrupt loads      | Reliable operation; all regression tests passed; no assertion failures                             |
| **DMA RX Error Count (avg/hr, stress)** | 7–15                                                                            | 0                                                                                                  |
| **Watchdog/Stack Faults (48h)**         | Avg. 2.3 per run                                                                | 0                                                                                                  |
| **Scheduled Events after RTC update**   | 800–900 ms average lag; missed scheduler tasks in 22% of cycles                 | ≤20 ms event variance; no missed scheduled tasks in over 1000 cycles                               |
| **RTC_CONFIG_STATUS**                   | Frequently marked as 'STALE'                                                    | Always 'VALID' after fix                                                                           |
| **Diagnostic Output**                   | Stack corruption, error logs, 'STALE' warnings in event logs                    | Clean logs; on-time event execution; consistent system status                                      |

These results clearly demonstrate that both problems have been fully addressed, restoring predictable, real-time performance to the affected subsystems.

---

## 4. Team Insights and Future Recommendations

- **Lessons Learned**
    - Interrupt priorities for high-throughput DMA tasks must be set above routine software and timer events to safeguard data integrity and system stability.
    - Event-driven notifications across subsystem boundaries require explicit review and regression coverage, especially when dealing with fundamental resources like system clocks and real-time counters.
    - Regular audits of ISR configuration and event propagation mechanisms are essential in maintaining robust embedded system operations.

- **Continuous Improvement Initiatives**
    - Introduced static analysis tools in the CI pipeline to automatically detect interrupt priority misconfigurations.
    - Expanded regression test suites to validate RTC and scheduler interaction under diverse calibration and update scenarios.
    - Added Tracealyzer hooks to capture ISR invocation and event notification flows, supporting rapid root cause analysis for future issues.

- **Preventative Measures**
    - Committed to periodic, structured reviews of ISR priorities and event notification logic as part of each major release cycle.
    - Reinforced inter-team code reviews to scrutinize timebase and interruption-sensitive features ahead of integration.

---

## 5. References and Documentation

- **Changelog:**  
    - [Firmware Release Notes: CHANGELOG.md – 2024-08-16](https://repo.example.com/deltax/firmware/blob/main/CHANGELOG.md)
- **Design Documents:**  
    - [SPI2/SPI3 Transaction Layer Spec (v2.1.4, §3.2)](https://docs.example.com/deltax/spi2_3-spec)
    - [System RTC Integration Doc (§2.3.1)](https://docs.example.com/deltax/rtc-integration)
- **API Specifications:**  
    - [DMA Controller API (`dma_if.h` v1.3, §5.1.2)](https://docs.example.com/deltax/dma-api)
    - [DeltaX Scheduling API (v3.11, §4.5)](https://docs.example.com/deltax/scheduler-api)
    - [RTC Manager API (`rtc_manager.h` v2.0)](https://docs.example.com/deltax/rtc-manager-api)
- **Issue Trackers and Trace Data:**  
    - [DXC-4117: NVIC Interrupt Priority Bug in SPI DMA RX](https://tracker.example.com/dx/issues/4117)
    - [DXC-4132: RTC Update Notification Regression](https://tracker.example.com/dx/issues/4132)
    - [Tracealyzer Session #2024-0814-737](https://trace.example.com/sessions/2024-0814-737)

---

### Sources

1. [DXC-4117 NVIC Interrupt Priority Bug in SPI DMA RX – Issue Tracker](https://tracker.example.com/dx/issues/4117)
2. [DXC-4132 RTC Update Notification Regression – Issue Tracker](https://tracker.example.com/dx/issues/4132)
3. [DeltaX Firmware Changelog, Commit b61f4de](https://repo.example.com/deltax/firmware/blob/main/CHANGELOG.md)
4. [SPI2/SPI3 Transaction Layer Specification v2.1.4](https://docs.example.com/deltax/spi2_3-spec)
5. [DMA Controller API Spec (`dma_if.h` v1.3)](https://docs.example.com/deltax/dma-api)
6. [System RTC Integration Design Doc](https://docs.example.com/deltax/rtc-integration)
7. [DeltaX Scheduling API Spec (v3.11)](https://docs.example.com/deltax/scheduler-api)
8. [Tracealyzer Fault Session #2024-0814-737](https://trace.example.com/sessions/2024-0814-737)
9. [RTC Manager API Documentation (`rtc_manager.h` v2.0)](https://docs.example.com/deltax/rtc-manager-api)

---

**Prepared by:**  
Martin Keller  
DeltaX Firmware Engineering Team  
2024-08-16