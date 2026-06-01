# Peer Review Submission Document  
**Automotive Engine Control Module (ECM) Embedded Software Documentation**

**Project Name:** Automotive Engine Control Module (ECM) Documentation  
**Submission Date:** 2024-07-03  
**Author:** Martin Keller

---

## Table of Contents

1. [Introduction](#introduction)  
2. [Main Content](#main-content)  
    2.1 [Module Overview and Code Comments](#module-overview-and-code-comments)  
    2.2 [Diagrams](#diagrams)  
    2.3 [Technical Explanations and Design Rationale](#technical-explanations-and-design-rationale)  
    2.4 [Code Sections Summary Table](#code-sections-summary-table)  
3. [Issues and Inconsistencies](#issues-and-inconsistencies)  
    3.1 [Table of Missing Diagrams and Detected Inconsistencies](#table-of-missing-diagrams-and-detected-inconsistencies)  
4. [Peer Review Comments Table](#peer-review-comments-table)  
5. [Revision Plan](#revision-plan)  
6. [Sources](#sources)  

---

## Introduction

This document provides a comprehensive technical reference for the embedded software developed for an Automotive Engine Control Module (ECM). It is structured to assist embedded software professionals, system integrators, safety engineers, and multidisciplinary peer reviewers by providing clear, detailed, and verifiable information. The documentation prioritizes objectivity, traceability, and conformance to relevant safety and coding standards.

**Scope:**  
The coverage extends across the full ECM software architecture, detailing all critical modules, internal code structure, data and control flows, module interfaces, and diagnostic features. This includes annotated code segments, explanatory diagrams, and an overview of key compliance requirements, with particular attention to functions vital for engine control—such as sensor input, decision logic, and actuator control paths. All code discussed in this document follows modular development principles, enabling maintainability and clear responsibility throughout the system.

**Intended Audience:**  
- Embedded software engineers  
- Functional safety and compliance experts  
- Quality assurance professionals  
- Technical leads and system architects  
- Peer reviewers from various disciplines within automotive development

**Relevant Standards:**  
The software adheres to two fundamental industry standards:
- **MISRA C:2012**: Ensures code safety, reliability, and maintainability in automotive contexts.
- **ISO 26262**: Defines requirements for functional safety in road vehicles.

These standards guide both the development process and the documentation, providing a solid foundation for safe, compliant embedded design.

**References:**  
- [MISRA C:2012 Guidelines](https://www.misra.org.uk/)
- [ISO 26262 Overview](https://www.iso.org/standard/43464.html)

---

## Main Content

### Module Overview and Code Comments

The ECM software architecture is separated into clearly defined modules, each responsible for a specific aspect of engine control. Documentation for every module, prepared for peer review, follows established Doxygen conventions and incorporates MISRA C recommendations to ensure completeness and readability. Each code module is introduced with comments that state its primary purpose, interface details, algorithm summaries, and underlying safety assumptions.

#### Sensor Acquisition Example

```c
/**
 * @file sensor_acquisition.c
 * @brief Handles analog and digital input acquisition from engine sensors.
 * @author Martin Keller
 * @date 2024-06-15
 *
 * @details
 * - Periodically samples crankshaft and camshaft position sensors.
 * - Validates sensor readings and performs diagnostic checks for plausibility.
 * - Complies with MISRA C:2012 Rule 17.7.
 * @inputs
 * - Crankshaft position sensor (analog input)
 * - Camshaft position sensor (digital input)
 * @outputs
 * - Engine speed (RPM), camshaft alignment status
 * @safety
 * - Ensures out-of-range sensor data is detected and flagged in accordance with ISO 26262 ASIL-B.
 */
void sample_crankshaft_sensor(void)
{
    // Sample maintains timebase consistency for accurate RPM calculation
    // Convert analog signal to digital engine speed value
    // Execute plausibility and diagnostic checks, flag any faults for safety
}
```

#### Engine Control Logic Example

```c
/**
 * @file engine_control_logic.c
 * @brief Implements state machines and decision logic for fuel injection and ignition timing.
 * @author Martin Keller
 * @date 2024-06-16
 * @inputs
 * - Engine speed and load from sensor acquisition
 * - Temperature and pressure readings
 * - Diagnostics and system enable signals
 * @outputs
 * - Fuel injector timing signals
 * - Ignition coil activation signals
 * @safety
 * - Implements state transitions and error handling in compliance with ISO 26262 ASIL-C requirements.
 */
void compute_injection_timing(void)
{
    // Processes engine state machine to determine correct injector pulse width
    // Checks all relevant diagnostic flags and implements safe fallback strategies
    // Logs events and issues fault codes on anomaly detection
}
```

#### Additional Modules

Each core module in the ECM is documented using the same approach:
- **Safety Monitoring:** Handles fault detection in real time, initiates protective operations, and communicates critical failures to diagnostics.
- **Actuator Output:** Manages fuel injector and ignition coil drivers, ensuring timing aligns with computed control signals, and respecting safety overrides.
- **Diagnostics Interface:** Responsible for assembling diagnostic trouble codes (DTCs), interacting with external scan tools, and maintaining error logs for servicing.

### Diagrams

To facilitate understanding and support detailed peer review, the documentation includes a series of technical diagrams:

- **Figure 1: ECM High-Level Block Diagram (v1.0, 2024-06-10)**  
  This diagram outlines all major software modules, depicting data and control flows between Sensor Acquisition, Engine Control Logic, Safety Monitoring, Actuator Outputs, and the Diagnostics Interface. All interfaces are explicitly labeled.

- **Figure 2: Fuel Injection Control Flowchart (v1.1, 2024-06-12)**  
  Illustrates the sequence of decisions and actions required to control fuel injection timing. It maps input processing, state evaluations, fault condition handling, and output signal generation.

- **Figure 3: Engine State Machine (v1.0, 2024-06-14)**  
  Details each engine operating state—Off, Cranking, Running, Fault Detected, and Shutdown—and the logic rules governing transitions. This provides reviewers with clear insight into system behavior across normal and abnormal operating conditions.

Every diagram is version-controlled and linked to the corresponding code and document section, ensuring traceability during reviews and updates.

*Planned Additions:*  
- **Figure 4: Safety Monitoring Flowchart** – Will map fault detection paths, safety overrides, and shutdown sequences (see Revision Plan).  
- **Figure 5: Diagnostics Interface Initialization Sequence** – Will clarify startup order and communication handshakes.

### Technical Explanations and Design Rationale

**Sensor Acquisition:**  
Sensor input modules adopt a modular structure: All access to hardware peripherals is performed through well-defined interfaces, isolating sensor code from higher-level logic. To maintain functional safety, the module continuously monitors sensor inputs for plausibility, applying range and trend checks. Any abnormal readings result in immediate safe-state transitions, implementing ISO 26262 recommendations for fault containment.

**Engine Control Logic:**  
Control decisions are built on rigorously documented state machines, as illustrated in Figure 3. By formalizing all legal state transitions, the design maintains system predictability even when faults are detected. Emphasis is placed on prompt, reliable detection and handling of sensor or actuator faults—minimizing risk while maximizing system uptime. All state transitions, input checks, and output actuation strategies are documented with their rationale both in-line and in referenced diagrams.

**Safety Monitoring:**  
Real-time monitoring routines ensure continuous oversight of key system variables and health indicators. If a critical fault is detected, the module invokes protective actions such as component shutdown or forced system reset, and logs all relevant events through the Diagnostics Interface, supporting traceability and service diagnostics.

**Actuator Output:**  
Driver functions for injectors and coils are strictly controlled, only enabling outputs when all safety and logic conditions are met. Each output is checked for feedback to detect electrical faults (open/short), and any detected issues trigger alerts within both the Safety Monitoring and Diagnostics modules.

**Diagnostics Interface:**  
Designed for compatibility with standard automotive diagnostic tools, this module not only logs faults but also tracks error history and supports detailed service readouts. It cooperates with the system initialization sequence to guarantee error reporting is available from the moment the ECM is powered up.

**Compliance Strategy:**  
All source code is statically analyzed using automated tools to verify conformance to MISRA C:2012. Each safety-critical path is mapped to ISO 26262 safety goals; an internal traceability matrix links individual software requirements to specific code modules, test cases, and diagnostic outputs. Regular compliance checks help ensure both ongoing and post-revision software integrity.

### Code Sections Summary Table

| Module Name             | Purpose                                    | Author         | Review Status         |
|-------------------------|--------------------------------------------|----------------|----------------------|
| Sensor Acquisition      | Acquire and validate engine sensor data    | Martin Keller  | Reviewed – Approved  |
| Engine Control Logic    | Manage engine states and control outputs   | Martin Keller  | Reviewed – Cond. App.|
| Safety Monitoring       | Fault detection and safe-state management  | Martin Keller  | Pending              |
| Actuator Output         | Drive fuel injectors/ignition coils        | Martin Keller  | Reviewed – Approved  |
| Diagnostics Interface   | Fault logging and external diagnostics     | Martin Keller  | Under Review         |

---

## Issues and Inconsistencies

### Table of Missing Diagrams and Detected Inconsistencies

| Issue / Missing Diagram                       | Description                                                    | Reference                    | Flagged By   |
|-----------------------------------------------|----------------------------------------------------------------|------------------------------|--------------|
| Safety Monitoring Flowchart                   | The flowchart for the Safety Monitoring module has not yet been created. | Section 2.1                  | Julia        |
| Injection Timing Calculation Comment Inconsist | Code documentation is incomplete—Doxygen comments lack explicit output details. | Line 45, engine_control_logic.c | Julia        |
| Module Initialization Sequence Diagram        | Initialization sequence for Diagnostics Interface is missing a supporting diagram. | Section 2.4                  | Julia        |

All identified issues above are mapped to related document sections or source code locations for easy reference and prioritization during the revision cycle.

---

## Peer Review Comments Table

| Comment                                                       | Reviewer        | Status         | Resolution Plan                                              |
|---------------------------------------------------------------|-----------------|---------------|--------------------------------------------------------------|
| Add explanation for state transitions in Engine Control Logic  | A. Schmidt      | Open           | Expand documentation to provide clear, step-by-step rationale for all state transitions, and update related diagram notes. |
| Doxygen tags missing for Safety Monitoring module functions    | L. Weber        | In Progress    | Audit and update all function comments for Doxygen compliance, with a checklist for I/O, failure modes, and safety notes. |
| Diagram versioning not consistent                             | N. Popov        | Closed         | All diagrams have now been updated with version numbers and dates to ensure document traceability. |
| Traceability from requirements to module implementation weak   | Y. Chen         | Open           | Enrich the traceability matrix in the appendix, explicitly linking requirements to both implementation and verification artefacts. |

---

## Revision Plan

1. **Clarify State Transition Documentation:**  
   The section covering Engine Control Logic will be expanded with explicit, stepwise explanations for each possible engine state transition, referencing Figure 3. Updated explanations will also be incorporated into flowchart notes for improved clarity and traceability.

2. **Enforce Doxygen and Commenting Standards:**  
   All code modules will undergo a thorough review to ensure function-level comments adhere fully to Doxygen syntax and MISRA guidelines. Each function will document its interface, expected inputs and outputs, handling of failure modes, and inherent safety mechanisms, including references to specific MISRA rules.

3. **Complete Missing Diagrams:**  
   - Develop the Safety Monitoring flowchart, providing a visual summary of how detected faults are handled and how safe states are enforced.
   - Construct a comprehensive initialization sequence diagram for the Diagnostics Interface, detailing startup order, communication handshakes, and error reporting readiness.
   - Ensure every diagram includes the current version and date, and logs changes in the document’s update history.

4. **Strengthen Requirements Traceability:**  
   - Expand the appendix to incorporate a full requirements-to-implementation traceability matrix. This matrix will map formal requirements (e.g., RQ-001: Engine state control) to their corresponding software modules, key code sections, and designated verification steps.

5. **Review and Address Open Peer Review Comments:**  
   - Address all outstanding feedback, prioritizing safety-critical and compliance-related issues.
   - Iteratively apply changes, performing mini peer-reviews for any comprehensive section revisions.
   - Keep the code summary and comments tables continually updated, systematically tracking progress and closure of all peer-review feedback.

6. **Maintain and Demonstrate Compliance:**  
   - Rerun automated analysis tools after major revisions (including the Julia tool and static analysis checkers) to verify there are no new compliance issues.
   - Document compliance outcomes in each module section after every significant update.

---

## Sources

1. [MISRA C:2012 Guidelines](https://www.misra.org.uk/)
2. [ISO 26262 Road Vehicles – Functional Safety](https://www.iso.org/standard/43464.html)
3. [Doxygen Documentation](https://www.doxygen.nl/manual/docblocks.html)
4. [Automotive Software Best Practices (NXP)](https://community.nxp.com/t5/Kinetis-Microcontrollers/Automotive-Embedded-Software-Best-Practices/ta-p/1111808)

---

**End of Document**