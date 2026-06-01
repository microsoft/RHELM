# Martin Keller’s Wireframe Sketching Session: Designing a Home Automation Dashboard  
**Date:** January 27, 2024

---

## 1. Devices Utilized

I began this wireframe design project for a home automation dashboard by carefully selecting hardware that would address both my development and prototyping needs, with a particular focus on the constraints typical of embedded devices.

### Prototyping Stage

**Dell XPS 15 (Model 9500):**  
This was my primary workstation for all digital sketching, wireframe creation, and hardware configuration. The laptop had plenty of processing power for running design software, managing design files, and maintaining version control of all assets. It became the command center for every stage of ideation, letting me move quickly between sketching in design tools and reviewing hardware configurations.

**Raspberry Pi 4 Model B (4GB RAM):**  
To best simulate real-world constraints, I set up a Raspberry Pi as a stand-in for the eventual hardware target. Using it, I could measure actual UI responsiveness, integrate a touchscreen, and confirm communication between the Pi’s GPIO pins and various peripherals. This step made it possible to anticipate possible performance bottlenecks and minimized surprises down the line.

### Planned/Deployment Devices

**Raspberry Pi 4 Model B:**  
This device will eventually serve as the embedded controller for the deployed dashboard, likely running a lightweight Linux OS to keep overhead low. I chose the Pi 4 for its balance of capability, community support, and compatibility with both software toolkits and home automation technologies.

**Official Raspberry Pi 7” Touchscreen Display:**  
To test how designs would function in their final setting, I used the official Pi touchscreen for physical prototyping. This gave me valuable insights into aspect ratio, touch responsiveness, and the real tactile experience users would have. Touch accuracy and latency were especially important to verify, ensuring the dashboard would feel smooth and responsive at the hardware level.

**Philips Hue Bridge (v2):**  
For the smart lighting integration, I used the Philips Hue Bridge as an endpoint to demonstrate true device communication rather than simulating data. This tested whether my UI patterns and backend calls worked reliably with popular IoT lighting hardware.

---

## 2. Design and Sketching Tools

Selecting the right tools set the tone for my entire workflow and allowed me to quickly iterate ideas while addressing the specific challenges of embedded UI.

**Figma (Desktop, v121.12.0):**  
Figma became my main platform for both wireframing and prototyping. Its Auto Layout capabilities made it easy to create responsive components sized for a 7" display, and component variants simplified the creation of different device states. I incorporated plugins like *Wireframe* for quick structural layouts, *Touch Frames* to ensure touch targets were finger-friendly, and *Icons8* to pull in clear and consistent icon sets suited to smart home interfaces.

**Krita (v5.2.0):**  
For looser ideation, I switched to Krita. Its freehand sketching tools let me break from the constraints of grid-based layouts and explore unorthodox interface ideas, especially when imagining more compact or irregular screen spaces. This stage revealed interface designs that might never have occurred in a strictly digital environment.

**Raspberry Pi’s Default Image Viewer:**  
Whenever I exported PNG mockups, I previewed them directly on the Pi’s touchscreen. This quick verification step showed me how my designs scaled and rendered on actual hardware—not just my development laptop. I made several small but vital adjustments after seeing the difference between simulation and the Pi’s real display output.

---

## 3. Key UI Elements

Through sketching and iteration, I focused on building an interface that was both visually approachable and physically practical within the limits of embedded screens.

**Dashboard Home Screen:**  
Each room or smart device gets its own large, tap-friendly tile, helping avoid missed touches on the 7” panel. Status indicators—like color-coded icons or glowing bulbs—give instant, at-a-glance feedback, and each tile includes direct actions: toggling a device on or off, locking doors, or changing room modes, all accessible with a single tap.

**Room Selector:**  
A horizontally scrollable tab bar sits at the top of the interface, each tab generously spaced for easy selection by fingertip. I included a snap-back animation to let users switch quickly between rooms and see immediate feedback, reducing navigation errors and keeping sessions fluid.

**Detailed Device View:**  
Drilling down into a device opens controls sized for effortless thumb use. For example, sliders for lights and thermostats are deliberately wide and tall, lowering the chance of missed or misinterpreted touches. I included mode picker buttons—simple toggles for presets like “Eco,” “Comfort,” or “Away”—as well as mini-graphs showing recent activity (like temperature changes over the last hour), allowing for quick status checks with minimal UI overhead.

**Settings and Alerts:**  
System alerts and key configuration options appear as lightweight modal popups, designed to minimize memory and resource usage. Critical warnings display as persistent banners along the screen edge, ensuring users never miss important notifications (like a door left open or lost network connectivity).

**Navigation Controls:**  
A persistent Home/Back bar is always available along the bottom, following established mobile conventions but tailored for the Pi’s GPIO hardware buttons as well. Each button is generously sized for reliable touch and can be mapped to dedicated physical controls on embedded hardware, helping users regain orientation at any time.

**Accessibility & Embedded Constraints:**  
- All interactive elements maintain a minimum 44x44 pixel area, tuned for accurate touch on the 7” panel.
- The color palette favors minimal, high-contrast combinations, reducing GPU load and preserving clarity in varied lighting.
- Fonts are no smaller than 16px to ensure readability from arm’s length.
- I avoided complex transitions or heavy animations to keep UI performance snappy on the Pi’s limited CPU/GPU.

---

## 4. Inspirations

My design choices were directly shaped by personal experiences and thoughtful observation throughout my day.

**Café Pause Décor:**  
I drew inspiration from the muted, warm ambiance of the local Café Pause, where I often spent my breaks. The gentle color palette, abundance of whitespace, and rounded corners in their decor influenced me to build an interface that feels welcoming and calm, not cluttered or techy. The café’s understated signage and subtle spatial organization also led me to favor minimal, outlined icons—easy to read, even in sunlight or with glare—avoiding the eye fatigue I often feel with over-decorated UIs.

**Day's Activities Informing UI Hierarchy:**  
Stepping away from my desk and relaxing in low-distraction settings gave me clarity on how best to structure the interface. Observing the uncluttered, logical arrangement of space in the café, I realized how groupings by room before function could simplify user flow. This inspired my decision to use large, tile-based navigation and to avoid nested menus wherever possible. That “one action per screen” philosophy, drawn from a desire for mental clarity amidst daily distractions, shaped nearly every screen layout.

---

## 5. Peer Feedback and Iteration

Collaborating with Lukas, a peer well-versed in embedded systems, led to several important enhancements:

- **Reduced Device Polling:** Lukas highlighted that querying each device’s status individually would drain resources. In response, I switched all status updates to a single asynchronous call occurring every three seconds, and redesigned the UI to display these consolidated updates more efficiently.

- **Graphics Optimization:** Recognizing the GPU limits of the Pi, I flattened dashboard visuals, abandoned ornamented gradients, and kept to solid fills with subtle drop shadows. This not only improved performance but also refined the dashboard’s visual discipline.

- **Fail-Safe Navigation:** To ensure users aren’t trapped in modal states or lose orientation, I anchored a persistent navigation bar to the bottom of every screen and made sure these controls were explicitly mapped to the Pi’s hardware buttons (via GPIO), as shown in my sketches.

- **Improved Slider Controls:** To combat accidental multi-touch input (or “ghosting”) on sliders, I implemented single-touch logic and added tooltip guidance directly on sliders, providing immediate help for unfamiliar users.

- **Smarter Alerts Workflow:** For alerts and warnings, Lukas recommended an override/acknowledge flow so states don’t get stuck. I redesigned all alert modals with a clear “Acknowledge” button and programmed non-critical warnings to auto-dismiss after a brief period.

---

## 6. Next Steps

Moving forward, I have outlined a precise action plan:

- **Finalize Wireframe Prototypes:**  
  I’ll present the latest Figma layouts to the embedded team to collect further feedback from real hardware testing. Each screen will be annotated with relevant platform notes and implementation hints.

- **Build a Clickable Figma Prototype:**  
  My goal is to create a fully interactive wireframe that mirrors the core user flow—from Home to Room to Device to Settings and back—making it easy to identify usability issues and fine-tune screen transitions before code is written.

- **Deploy on Raspberry Pi Hardware:**  
  I will render static PNGs of the UI directly on the Pi with the 7” touchscreen to simulate performance in actual lighting conditions. This will confirm if color contrasts and UI clarity hold up in varied environments.

- **Document UI-to-Backend API Specifications:**  
  I’m drafting comprehensive API requirements, detailing expected JSON payloads for both device and room status updates as well as command/control endpoints. This will streamline handoff between front-end and backend teams.

- **Plan for Embedded/UI Integration Sprint:**  
  Next, I will split tasks across the React/Python UI stack, prioritize event handling for LCD interaction, and finalize GPIO button mapping for physical inputs.

- **Second Round of Technical Feedback:**  
  After first integration testing, I’ll actively seek input from system integrators and a few usability testers, making their real-world observations central to subsequent design refinements.

---

## 7. Wireframe Screens Overview

| Screen Name      | Main Features                                                                                                     | Rationale                                                                                                    | Feedback Incorporated                                                               |
|------------------|------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| Home Dashboard   | - Large device tiles<br>- Status indicators<br>- Quick-action buttons                                            | Prioritizes rapid access and error-free touch on 7” screens; clear device states at a glance                 | Flat vector icons, batched status polling, tile sizing confirmed via Pi simulation  |
| Room Selector    | - Horizontal tab bar<br>- Snap-back animation<br>- Room iconography                                              | Simplifies navigation and keeps orientation consistent                                                       | Large, touchable tab areas; GPU-friendly muted palette; prevents nav input errors   |
| Device Detail    | - Slider controls<br>- Mode picker buttons<br>- Live mini-graph for sensor data                                  | Single-finger operation; transparent feedback on device state without overloading hardware                   | Single-touch guarded sliders, in-place help, anti-ghosting verified on Pi HW        |
| Settings/Alerts  | - Modal popups<br>- Banner alerts<br>- Explicit “Acknowledge”/auto-dismiss flow                                 | Key info delivered without UI clutter; resource-efficient overlays                                           | Modal acknowledge, banner for non-blocking alerts, memory overhead tightly managed  |
| Navigation Bar   | - Persistent bottom bar<br>- Home/Back controls<br>- Hardware/GPIO mapping highlighted                           | Ensures fail-safe navigation; supports both on-screen and hardware inputs                                    | All screens consistently display nav bar; GPIO mapping detailed in wireframe notes  |

---

## Sources

All content is based on my research brief and the documented results of this session. At this time, no external sources were referenced.

---

By chronicling this session, I’ve established a clear, actionable blueprint for how I’ll translate wireframe concepts into a working, user-friendly home automation dashboard—optimized for both embedded constraints and everyday usability.