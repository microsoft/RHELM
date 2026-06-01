# Embedded Systems: Interrupt Handling – Study Notes (August 26, 2024)

**Date:** 2024-08-26  
**Textbook Reference:** *Embedded Systems: Introduction to ARM Cortex-M Microcontrollers* by J. W. Valvano  
**Study Device:** Dell XPS 15  

---

## Summary of Objectives

During this session, I focused on developing a deeper understanding of interrupt handling in ARM Cortex-M microcontrollers, drawing extensively from Valvano’s textbook. My main goals were to clarify the architecture and behavior of exceptions and interrupts, master the configuration of the NVIC (Nested Vectored Interrupt Controller), and develop strategies for achieving low and predictable interrupt latency. I also aimed to strengthen my practical skills in designing reliable, maintainable ISRs (Interrupt Service Routines), and address typical challenges encountered when deploying firmware in real-world embedded systems.

---

## Detailed Notes

### Exception and Interrupt Architecture

ARM Cortex-M microcontrollers implement a flexible and robust interrupt system, designed to handle both processor-generated and external events efficiently.

- **Types of Exceptions:**  
  Cortex-M processors classify exceptions into two broad categories: system exceptions (e.g., reset, NMI, faults such as hard fault, memory management fault, bus fault, usage fault, and others like SVCall, debug monitor, PendSV, and SysTick) and external interrupts triggered by peripherals. System exceptions generally have higher or fixed priorities compared to user-configurable peripheral interrupts ([1], Ch. 6, pp. 127–130).

- **Vector Table:**  
  The vector table serves as the anchor point for exception and interrupt handling, containing pointers to all handler routines. Its default address is 0x00000000, but relocation is supported via the Vector Table Offset Register (VTOR). This flexibility is particularly important for bootloaders and systems with multiple firmware images ([1], p. 129).  
  **Example initialization:**
  ```c
  SCB->VTOR = (uint32_t)&vector_table;
  ```

- **Exception Prioritization:**  
  ARM Cortex-M exceptions are prioritized, with lower numerical values indicating higher priority. Reset and NMI always have the highest fixed priorities, while other exceptions and external interrupts can be configured as needed through NVIC registers ([1], pp. 138–140). Understanding and correctly configuring these priorities is crucial for ensuring time-critical responses in complex applications.

### NVIC Configuration

The NVIC is tightly integrated with the processor core, enabling swift and predictable interruption and resumption of processing.

- **Enabling and Disabling Interrupts:**  
  Individual interrupts are managed using the NVIC_ISERx (Interrupt Set-Enable Registers) and NVIC_ICERx (Interrupt Clear-Enable Registers), allowing precise control over which interrupts can preempt normal operation.
  ```c
  NVIC->ISER[0] = (1 << IRQn);
  NVIC->ICER[0] = (1 << IRQn);
  ```

- **Configuring Interrupt Priority:**  
  The Cortex-M NVIC provides at least eight priority levels (exact number depends on the device), subdivided into preempt priorities and subpriorities. This subdivision is controlled by the PRIGROUP bits in the Application Interrupt and Reset Control Register (AIRCR), which is critical for correct nesting and arbitration among simultaneous interrupts ([1], p. 142).
  ```c
  NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_4);
  ```
  Setting an appropriate grouping helps ensure that particularly urgent ISRs are never starved by lower-priority activity.

- **Software-Triggered Interrupts:**  
  The NVIC_STIR register enables software to trigger interrupts, which is especially useful for inter-process signaling or in self-test routines ([1], p. 145). This mechanism complements the hardware-driven interrupts, supporting flexible software-architected interrupt-driven workflows.

### Interrupt Latency Management

Minimizing and controlling interrupt latency is a focal point for real-time programming.

- **Sources of Latency:**  
  ARM Cortex-M3/M4 processors are capable of entering an interrupt in as few as 12 CPU cycles ([1], p. 151), but the true latency experienced depends on factors such as stacking overhead (processor automatically pushes key registers), memory wait states (especially relevant with slower Flash memory or shared buses), and overall system bus load (e.g., concurrent DMA transfers).
  
- **Tail-Chaining and Late-Arrival Handling:**  
  - **Tail-Chaining:** When one interrupt is finishing and a higher-priority interrupt is pending, the core can avoid restoring and re-saving registers, thus reducing the total latency substantially ([1], p. 152).
  - **Late-Arrival:** If a higher-priority interrupt arrives while the processor is stacking for a lower-priority one, the hardware can rapidly switch, aborting the current stack sequence to handle the urgent request.  
  These optimizations are depicted clearly in the timeline diagrams in Figure 6.15 ([1], p. 153).

- **Best Practices:**  
  It’s vital to minimize the time during which interrupts are globally disabled. For truly critical sections, a common idiom is:
  ```c
  __disable_irq();
  // Perform critical update
  shared_flag = 1;
  __enable_irq();
  ```
  The critical region should be as brief as possible to avoid impacting system latency. Highest priorities should be reserved strictly for the most time-sensitive signals.

### ISR (Interrupt Service Routine) Design Considerations

Designing effective ISRs is central to reliable embedded firmware.

- **Standard Prototype:**  
  All ISRs follow the `void ISRname(void)` prototype, with no arguments or return value. Each handler is referenced in the vector table at the corresponding exception or IRQ slot ([1], pp. 136–137).

- **Automatic Stack Usage:**  
  On exception entry, the hardware pushes registers R0–R3, R12, LR, PC, and xPSR onto the current stack ([1], p. 153). Developers need to size stack memory appropriately, especially in applications with deep nesting, recursive ISRs, or active RTOS tasks.

- **Returning from ISR:**  
  Exception return must use a special sequence so that the processor correctly restores program state, commonly via `BX LR` with a specific return value.

- **Design Best Practices:**  
  ISRs should always be succinct: avoid loops, complex logic, or calls to blocking routines or non-reentrant APIs. Instead, the best pattern is to immediately acknowledge the event, perform any essential register operations, set a flag (declared `volatile`) or release a semaphore, and then allow the foreground (main loop or thread) to handle bulk processing.
  ```c
  volatile int data_ready = 0;
  void ADC_IRQHandler(void) {
      ADC->SR = ~ADC_FLAG_EOC;
      latest_data = ADC->DR;
      data_ready = 1; // Signal to main application
  }
  ```
  Correct use of `volatile` is mandatory to prevent unintended compiler optimizations across ISRs and foreground code. In RTOS or multicore setups, resource contention must be managed carefully. For some peripheral accesses, memory barriers (Data Memory Barrier - DMB, Data Synchronization Barrier - DSB) should be used for correct ordering and visibility.

- **Debugging and Reliability:**  
  Every slot in the vector table should point to a valid handler; leaving any uninitialized can lead to obscure hard faults. Implementing weak default handlers allows unexpected cases to be caught during testing and increase diagnostic robustness.

---

## Insights and Clarifications

| Topic                        | Description                                                                                                 | Reference Page   |
|------------------------------|------------------------------------------------------------------------------------------------------------|:----------------:|
| NVIC Priority Grouping       | Proper configuration of PRIGROUP is essential for intended preemption and nesting—misconfiguration can quietly undermine interrupt structure | p. 142           |
| Exception Stacking/Unstacking | The book’s timing diagram (Fig. 6.15) clarifies the phases of stacking/unstacking, helping to estimate true interrupt overhead | p. 153           |
| Tail-Chaining Optimization   | Hardware optimization that reduces latency when multiple interrupts follow directly, as in bursty event streams | p. 152           |
| Vector Table Relocation      | Relocating the vector table enables dynamic bootloaders or multi-stage firmware upgrades, but introduces memory mapping and startup code challenges | p. 129           |
| Software-Triggered IRQs      | Software-accessible interrupts, via NVIC_STIR, are important for facilitating internal signaling and debugging | p. 145           |
| Latency Bottlenecks          | Measured latency is often dominated by system-level delays, beyond the on-core stacking/unstaking, such as slow Flash or bus contention | p. 151           |
| ISR-to-Main Communication    | The industry-standard, reliable method is to signal main code by setting flags/semaphores in ISRs and deferring major work | p. 155           |

---

## Action Items

- **Test Vector Table Relocation:**  
  Evaluate and implement vector table relocation in current firmware. This is especially relevant for custom bootloader support, ensuring that exception handling remains intact during startup transitions.

- **Measure Actual Latency:**  
  Set up hardware or QEMU-based tests (using the Dell XPS 15) to measure actual interrupt entry and tail-chaining latency, comparing theoretical timing from the textbook against real system performance.

- **Review Peripheral Access in ISRs:**  
  Examine all ISR code to verify appropriate use of memory barriers and ensure shared resources are managed safely, avoiding subtle synchronization bugs.

- **Audit NVIC Priority Grouping:**  
  Review and, if necessary, correct NVIC priority grouping settings throughout the codebase to ensure that intended priority and preemption schemes are achieved.

- **Investigate Bus and DMA Impact:**  
  Research how off-core transactions (DMA, external peripherals) impact worst-case interrupt latency, going beyond the intra-core focus of Valvano’s discussion.

- **Study RTOS Examples:**  
  Analyze interrupt management patterns in real RTOS projects, especially regarding use of subpriority versus preemption priority, to inform practical implementation and scheduling.

---

## Sources

[1] Valvano, J. W. *Embedded Systems: Introduction to ARM Cortex-M Microcontrollers*, Chapter 6, pp. 127–155.  
[Online Reference Diagram](https://microcontrollernotes.files.wordpress.com/2020/03/armcortexmtiming.png)

---

**End of Study Notes.**