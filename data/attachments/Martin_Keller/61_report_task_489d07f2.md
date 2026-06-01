# Firmware Bug Review – Technical Meeting Minutes  
**Date:** 2024-08-13  
**Time:** 09:00 CEST  
**Location:** Stuttgart Engineering Office (onsite) & Video Conference (hybrid)  
**Attendees:**  
- Martin, Embedded Systems Software Developer (onsite)  
- Mehmet (onsite)  
- Julia (remote, video call)  

---

## Meeting Overview

The team convened at 09:00 CEST, with Martin and Mehmet present at the Stuttgart Engineering Office and Julia participating remotely via video call. The primary focus of this session was to investigate a persistent firmware bug affecting CAN bus communications, evaluate diagnostic evidence, and align on both immediate remediation steps and longer-term architectural improvements. Notably, Martin attended despite experiencing significant eye strain and fatigue, which at times affected his engagement and pace during the meeting.

---

## Agenda

1. Review of the reported firmware bug and symptoms.
2. Examination of diagnostic logs and relevant code sections.
3. In-depth root cause analysis.
4. Discussion of short-term fixes and long-term solutions.
5. Identification and debate of conflicting viewpoints.
6. Assigning tasks, responsibilities, milestones, and deadlines.
7. Confirming decisions based on documented evidence.
8. Summary of points of contention, final decisions, and follow-up items.

---

## Discussion Summary

### 1. Bug Symptoms and Diagnostics

The team began by reviewing the specific issues reported in production firmware v2.11.4. Devices have shown intermittent CAN bus communication failures, particularly after more than four hours of continuous operation. The failures typically manifest as a loss of CAN data frames and unexpected device resets, especially during periods of elevated traffic load. Importantly, watchdog timers were confirmed to be operating normally when these resets occurred, ruling out some common causes of unexpected reboots.

The supporting diagnostic data included:
- **CAN Bus Capture Log ([1])**: Patterns showed dropping of frames within sequences 0x202–0x210. As uptime increased, the frequency of these dropouts also rose. Significant timing variance between CAN messages was recorded, with peaks reaching six times the baseline value at approximately 148,573 seconds of runtime.
- **System Debug Log ([2])**: Repeated entries noted, such as "CAN Rx buffer overflow" at around 15,937 seconds, and warnings about “Critical section locked >120ms” just before resets occurred.
- **Code Review Focus**:  
  - **can.c**: ISR section (lines 101–129) revealed conditional logic tied to buffer overflow error logging.
  - **scheduler.c**: Sensor polling task employs extended critical sections, which raised concerns about their duration and consequences.

### 2. Root Cause Analysis

Martin initiated the analysis, despite his clear exhaustion, by proposing that the issue was triggered by a race condition in the management of the CAN receive buffer. He pointed out that both the ISR and a FreeRTOS task might be attempting to access the buffer simultaneously, citing problematic code in `can.c`.

Julia offered a counter-perspective, referencing diagnostic logs indicating that receive buffer saturation did not always coincide with data dropouts. She highlighted that delays within critical sections of the scheduler were often present during failure events. Julia backed her argument with a trace log ([6]) covering 148.3–152.1 seconds, demonstrating extended blocking times that could interfere with timely buffer handling.

Mehmet reinforced Julia’s findings by referencing empirical data that showed a high correlation between CAN dropouts and critical section durations exceeding 100ms—much longer than the intended <16ms windows. He observed that whenever these blockages occurred, buffer processing was delayed enough to result in communication errors and device resets.

### 3. Short-Term and Long-Term Solution Proposals

**Short-Term Actions:**
- **Martin** suggested increasing the CAN RX buffer size from 32 to 64 packets (an update to a `can.h` macro), and implementing immediate overflow detection hooks. However, given his current eye condition, Martin noted he might not be able to comprehensively test these modifications within the planned timeframe.
- **Julia** cautioned that simply enlarging the buffer risks concealing the underlying real-time processing issue and flagged that memory constraints on the STM32F765 MCU (RAM: 128KB) could limit this approach.
- **Mehmet** advocated migrating buffer management to a FreeRTOS queue, which would provide atomic access and reduce contention between ISR and task operations. He also proposed reducing the duration of critical sections in the sensor polling task to minimize delays.

**Long-Term Approach:**
- **Julia** recommended a thorough redesign using a lock-free ring buffer with a double-buffering approach to safely separate ISR and task-level access. She further proposed the development of a dedicated unit test suite (`test_can_overflow_stress.c`) to robustly evaluate buffer handling.
- **Mehmet** concurred with this direction and added that utilizing DMA for CAN RX could offload buffer management from the CPU, further reducing ISR dependency. He recognized, however, that this path would entail hardware changes beyond the current project scope.

### 4. Disagreement and Evidence-Based Debate

Two primary viewpoints were debated:
- **Buffer Sizing vs. Concurrency Fix:**  
  Martin maintained that increasing buffer size was justified, using recent memory mapping data ([5]) to support feasibility. He felt this would provide headroom for in-depth troubleshooting.
- Julia and Mehmet, however, consistently highlighted trace and log evidence linking missed CAN interrupts and overflows directly to excessive time spent in critical sections, not static buffer size. Their position was that the core problem was concurrent access and task blocking, not buffer length.
- The idea of adopting DMA-based CAN reception was briefly discussed; Julia pointed out that without new hardware, this solution would not be immediately applicable, regardless of its technical merit.

---

## Action Items

| Task Description                                                                                  | Responsible Person(s) | Milestone/Acceptance Criteria                           | Deadline    |
|---------------------------------------------------------------------------------------------------|-----------------------|--------------------------------------------------------|-------------|
| Refactor CAN RX buffer implementation to use FreeRTOS queue; validate on target hardware          | Mehmet                | Code passes `test_can_rx_basic` over a 5-hour runtime  | 2024-08-16  |
| Improve profiling of critical section durations; prepare correlation report                       | Julia                 | Complete coverage and correlation for all tasks & ISRs | 2024-08-20  |
| Prepare buffer size increase hotfix proposal (for contingency use only)                           | Martin                | Proposal reviewed, resources and regression tests clear | 2024-08-16  |
| Update on developer health and availability for ongoing/urgent work                               | Martin                | Communicate any changes promptly                       | 2024-08-14  |
| Upload CAN buffer patch and fresh trace logs for peer review to shared repository                 | Mehmet, Julia         | All evidence available in internal Git branch           | 2024-08-16  |

---

## Decisions and Rationale

After thorough discussion and review of logs, trace data, and memory resources, the team agreed to prioritize concurrency improvements—specifically refactoring the RX buffer to utilize a FreeRTOS queue with minimal blocking in critical sections. Diagnostic evidence strongly linked prolonged critical section durations to buffer overflows and CAN frame loss.

A temporary hotfix increasing buffer size will only be considered if the concurrency refactor cannot be validated quickly. This safeguard is justified by current RAM usage reports ([5]), but all agreed it risks masking the underlying issue.

For the long-term, the roadmap now includes the development of a lock-free, double-buffer solution fortified with automatic regression testing. While DMA-driven reception remains an attractive optimization, it will be tabled until hardware development aligns with that capability.

All decisions are firmly supported by logs, trace data, and observed system behavior.

---

## Contentions and Resolutions

| Issue                                     | Supporting Evidence             | Alternatives Considered              | Final Decision                                 | Assigned Follow-Up                |
|--------------------------------------------|---------------------------------|--------------------------------------|------------------------------------------------|-----------------------------------|
| Buffer sizing vs. concurrent access issues | Diagnostic logs [1][2], code [3][4], trace [6] | Increase buffer size temporarily (Martin) | Implement FreeRTOS queue-based solution         | Mehmet: Queue refactor, testing   |
| Excess critical section duration           | Trace data [6], debug logs [2]  | Adjust task priorities, optimize CS  | Profile and minimize critical section lengths   | Julia: Profiling enhancement      |
| Masking issue with larger buffer           | RAM map [5]                     | Larger buffer as stopgap             | Only as fallback if concurrency fix delays     | Martin: Draft hotfix proposal     |
| Hardware-based DMA for CAN RX              | N/A for present hardware        | Hardware upgrade                     | Consider for future, not immediate action      | None (future review, Q4)          |

---

## References

[1] log_20240813_002.can (CAN Bus Capture Log)  
[2] debug_20240813_002.log (System Debug Log)  
[3] can.c (ISR routine, lines 101–129)  
[4] scheduler.c (critical sections, lines 244–267)  
[5] memory_map_2024-08-13.pdf (Memory Map Figures)  
[6] trace_148.3-152.1 (Critical Section Trace Data)  
[7] test_can_overflow_stress.c (Unit Test Suite)  
[8] feature/can_buffer_refactor (Internal Git repository: prototype hardware and patch)  
[9] Internal meeting attendee list and schedules

---

## Summary

The team agreed that the recurring CAN bus communication problems stem primarily from concurrency issues between ISRs and FreeRTOS tasks, accentuated by lengthy blocking in scheduler critical sections. The next development milestone will focus on implementing a FreeRTOS queue to mediate access to the CAN RX buffer and reduce task contention. Increasing the buffer size is reserved solely as a short-term fallback. Longer-term, a move to a lock-free double-buffered architecture with dedicated stress-testing is targeted for the next major firmware revision. DMA support will remain on the horizon, awaiting future hardware alignment.

All follow-up actions are scheduled with defined deadlines, and meeting participants are committed to prompt communication regarding progress and any barriers, including personal capacity and health.

---

**End of Minutes.**