# Embedded Systems Certification Final Project — Final Log Entry

**Project Owner:** Martin Keller  
**Completion Date:** 2024_09_15

---

## Project Title

**Development and Real-Time Integration of an Embedded Sensor Fusion System Using FreeRTOS and ARM Cortex-M4**

---

## Overview

This final log entry summarizes the design and complete implementation of a real-time embedded sensor fusion system built on the STM32F4 Discovery platform, driven by FreeRTOS on an ARM Cortex-M4 MCU. The project’s primary objective was to develop a modular, reliable sensor fusion framework that integrates data from an accelerometer, gyroscope, and magnetometer using an extended Kalman filter (EKF), with a strong emphasis on robust real-time performance and effective resource management.

Throughout the project, I applied advanced embedded techniques to maximize reliability and maintain determinism in a resource-constrained environment. Each phase, from initial requirements definition to functional and stress testing, contributed essential knowledge and tools for the practical deployment of a high-integrity embedded system.

---

## Project Milestones

| Milestone                          | Date         | Technical Notes                                                                                                                             |
|-------------------------------------|--------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| System Requirements Definition      | 2024_07_01   | Outlined precise performance criteria, memory and processing constraints, and functional requirements for real-time fusion of three sensor streams on ARM Cortex-M4.              |
| Hardware Platform Selection         | 2024_07_05   | Chose the STM32F4 Discovery board, leveraging its comprehensive set of peripherals (I2C, SPI, UART), sufficient memory, and strong FreeRTOS compatibility.                      |
| Core System Architecture Design     | 2024_07_10   | Designed a modular block architecture, mapping out sensor interfaces, data acquisition, processing flows, RTOS-based task breakdown, and communication protocols.                  |
| Peripheral Integration & Drivers    | 2024_07_20   | Developed and thoroughly validated hardware abstraction drivers for the accelerometer, gyroscope, and magnetometer, utilizing STM HAL libraries to guarantee robust operation.    |
| RTOS Task Structuring & Scheduling  | 2024_07_30   | Implemented FreeRTOS tasks for data acquisition, sensor fusion, and output, carefully prioritizing for deterministic and high-throughput execution.                              |
| Sensor Fusion Algorithm Integration | 2024_08_07   | Integrated and tuned a high-efficiency EKF to combine sensor data streams, optimized for real-time responsiveness and minimal memory consumption.                                |
| Real-Time Data Logging & Debugging  | 2024_08_14   | Enabled UART-based serial data export and configured the SWO interface for live debugging, enabling precise timing analysis and in-depth traceability.                            |
| System Integration & Verification   | 2024_08_21   | Combined and synchronized all modules, conducted full data flow testing, and rigorously analyzed timing and reliability under integration-lab conditions.                       |
| Functional and Stress Testing       | 2024_08_28   | Executed comprehensive test scenarios handling live sensor input, boundary cases, simulated power loss, and enforced fault conditions to assure robustness.                      |
| Documentation & Portfolio Packaging | 2024_09_10   | Compiled detailed architecture diagrams, code documentation, integration and verification reports, along with a professional summary for portfolio presentation.                  |

---

## System Architecture Diagram

```
          +-------------------+
          |   Sensors (I2C)   |
    +-----+ Accel  Gyro  Mag  +-----+
    |     +-------------------+     |
    |                               |
    v                               v
+---------------------------+   +--------------------+
| Sensor Interface Drivers  |-->|  FreeRTOS Tasks    |
+---------------------------+   |  - Data Acquisition|
                                |  - Sensor Fusion   |
                                |  - Comms Output    |
                                +--------------------+
                                         |
                                         v
                              +--------------------+
                              | Sensor Fusion (EKF)|
                              +--------------------+
                                         |
                                         v
                              +--------------------+
                              | UART/Serial Output |
                              +--------------------+
```

---

## Key Technical Insights

This project facilitated significant advances in the following technical domains:

### Hardware-Software Integration  
Effectively interfacing hardware and software components was a cornerstone of the system’s reliability. I became adept at configuring low-level I2C and SPI communications, using hardware interrupts to minimize timing uncertainties and securing consistent data throughput between sensor modules and the main processor.

### RTOS Mastery  
In-depth experience with FreeRTOS kernel internals enabled me to design and prioritize tasks for optimal real-time performance. Balancing throughput with deterministic response, I established clear inter-task synchronization using queues and semaphores to prevent data bottlenecks, while maintaining a scheduler configuration apt for embedded constraints.

### Sensor Fusion & Algorithm Optimization  
Porting and optimizing the EKF for the Cortex-M4 presented challenges in both speed and memory use. Careful management of floating-point operations and internal state buffers reduced the memory footprint. Utilizing static allocation wherever possible enhanced predictability and prevented heap fragmentation—a critical factor in embedded workloads.

### Advanced Debugging and Profiling  
Utilizing the SWO for live tracing, alongside UART for periodic data logs, allowed for extensive visibility into real-time execution. Logic analyzer tools were instrumental in catching intermittent bus contention and profiling the exact timing of task switches. Systematic, module-level unit testing using JTAG/SWO proved invaluable for identifying subtle synchronization and data alignment issues.

### Modular Integration and Verification  
Merging independently-developed modules forced rigorous validation of interface contracts and defensive data checking. Automated regression testing scripts were established so that every codebase change could be quickly verified for system-wide stability, significantly reducing integration bugs and ensuring an agile development process.

---

## Technical Challenges and Solutions

Throughout the development process, several notable technical hurdles emerged:

### Resource Constraints  
The limited SRAM and flash on the STM32F4 required extremely careful memory management. I implemented static allocation for critical buffers, eliminated unused branches, and profiled all stack and heap regions using FreeRTOS utilities to avoid overruns.

### Peripheral Timing and Bus Arbitration  
Initially, simultaneous task access to the I2C bus led to sporadic contention and missed sensor data. Introducing mutex-protected access to the bus and prioritizing the frequency of high-criticality sensor reads stabilized data streams and eliminated race conditions.

### RTOS Scheduling Under Load  
During initial RTOS task scheduling, periods of high sensor activity introduced jitter and missed deadlines. After profiling with FreeRTOS trace facilities, I refined task priorities and minimized blocking sections within the data acquisition routines. This improved both the consistency and reliability of real-time performance even under heavy computation loads.

### Debugging Multi-Module Systems  
Integrating multiple hardware interfaces made debugging considerably more complex, especially when faults surfaced as data misalignment or sporadic freezes. By isolating responsibilities in smaller modules and introducing explicit API contracts, fault localization became more straightforward, accelerating the root-cause analysis process.

### Data Integrity Across Modules  
During cross-module data transfer—such as moving processed sensor data to the fusion task—early runs revealed inconsistencies. Introducing well-defined interface contracts, with versioned data structures and validation checks, prevented silent failures and made future expansions easier to manage.

---

## Outcomes, Impact, and Recommendations

Successful completion of this project not only delivered a fully functional real-time embedded sensor fusion system but also provided a strong template for scalable sensor data integration on resource-limited platforms. The modular hardware abstraction, robust RTOS configuration, and systematic debugging routines established in this process directly transfer to future embedded projects with similar requirements.

For those looking to take on similar embedded integration tasks, I recommend the following:

- Invest early in a robust modular architecture; this makes debugging and maintenance far more straightforward as complexity grows.
- Rigorously test resource usage and timing with the actual target hardware.
- Use trace and logging facilities to their fullest—live insight reduces time spent chasing elusive bugs.
- Treat interface contracts and validation mechanisms as first-class citizens in cross-module integration.
- Maintain comprehensive, clear technical documentation throughout, as it pays dividends in both integration and portfolio presentation.

---

## Next Steps for Career and Portfolio Development

To further leverage this project for professional growth, I plan to:

- **Expand Technical Documentation:** Develop detailed user and developer guides, broaden the architectural visualizations, and formalize API references. These assets will enhance my ability to communicate both the high-level design and the nitty-gritty technical details to recruiters, peers, and interviewers.
- **Portfolio Enhancement:** Present the full project log, annotated source code, technical briefs, and integration tests in a polished digital portfolio format. This will include conversion to GitHub Pages and an expandable personal website section, employing accessible user interfaces and structured navigation.
- **Technical Communication:** Author a whitepaper and/or technical article outlining the novel approaches used in resource-optimized sensor fusion and RTOS-driven real-time systems. These writings are intended both to solidify my own understanding and to give back to the embedded community.
- **Skill Development:** Continue professional development in advanced topics such as predictive control methods (e.g., model predictive control, adaptive PID), secure device communication protocols, and ultra-low-power embedded design. These will keep my skillset at the cutting edge for embedded software engineering roles.

---

## Sources

All project decisions, architecture, and report structuring closely followed established industry practices for embedded system design and real-time software engineering. No external sources were consulted due to research limitations, but references and templates were modeled after widely-adopted portfolio and technical documentation standards within the field.

---

This project has provided not only a working system—a robust, real-time sensor fusion platform—but also a culminating, hands-on demonstration of professional embedded engineering principles. Looking ahead, I am eager to apply these competencies in future challenges and to continue building on this strong technical foundation.