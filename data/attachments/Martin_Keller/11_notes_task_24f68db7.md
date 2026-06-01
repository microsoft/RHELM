# Video Call Summary – Martin & Anja Keller  
**Evening Video Call – January 29, 2024**

---

## Call Details

- **Date:** January 29, 2024  
- **Time:** 19:30–20:30 CET  
- **Participants:**  
  - Martin Keller — Embedded Systems Software Developer  
  - Anja Keller — Architecture Student

---

## Discussion Overview

Last night, Anja and I spent an hour discussing ways to combine her architectural ideas with my background in embedded systems, focusing on creating a comfortable and adaptable student flat environment. Our talk revolved around her current studio project and how technology—specifically smart lighting and automation—can enhance everyday living for students like her.

---

## Discussion Themes and Key Points

### 1. Anja’s Architecture Studio Project

Anja has been tackling the challenge of designing a modern student flat. She wants the space to be flexible and modular, with lighting that adapts to a variety of uses: studying late at night, relaxing after classes, hosting friends, or cooking quick meals. We agreed that light isn’t just functional—its quality, intensity, and placement dramatically affect how the space feels and can actually change how people interact with a room.

From a technical standpoint, I emphasized how adaptable lighting setups—using dimmable fixtures and different lighting scenes—can make small spaces truly multipurpose. For a student, every square meter counts, and the right lighting can expand the perceived dimensions of a room.

### 2. Smart Lighting: Practical Ideas

We dove into several practical ideas for smart lighting:

- **Zoning:** Splitting the flat into zones—study area, relaxation zone, and kitchen/dining—so each area has its own lighting scheme.
- **Energy Efficiency:** Students often look for ways to keep costs down, so we discussed solutions like LED lighting, automation routines to turn off lights when no one’s home, and the potential for sensors that respond to presence.
- **User-Friendly Control:** We compared the pros and cons of wired versus wireless systems. Wireless setups are less invasive—ideal for renters with limited ability to modify their flats. We explored how voice assistants like Alexa or Google Home add convenience, and why modular, upgradeable systems make the most sense for her student lifestyle.

I shared technical information about automation through occupancy sensors, timers, and integration with home assistants, explaining how these can be set up for both routine and spontaneous control.

### 3. Home Automation in Shared Living

Living with roommates adds another layer of complexity—automation needs to be reliable, simple, and considerate of privacy. We talked about:

- **Adaptive Lighting:** Preset scenarios, so lights adjust automatically for group study or alone time.
- **Affordable Upgrades:** Since most students rent, we’re favoring low-cost, non-permanent options—plug-and-play modules, smart bulbs, and open-source platforms.
- **Shared Spaces & Security:** I outlined the role of devices like ESP32 or ESP8266, and protocols such as Zigbee, Wi-Fi, and BLE for communication. We also touched on the importance of privacy and network security in flats with several people and many connected devices. Sharing a home network brings unique security challenges, so default credentials and secure network configurations are essential.

### 4. Next Steps and Resource Exchange

To move our ideas forward, we established a clear plan:

- I promised to share technical resources and platform documentation, focusing on solutions like ESPHome, Home Assistant, and developer guides for proprietary ecosystems such as Philips Hue.
- Anja will begin drafting lighting concept sketches and annotating her flat’s plan with zones and automation features.
- We want to specifically assess which platforms are most compatible with mainstream home assistants, keeping ease-of-use front and center.
- I’ll gather a list of affordable sensor and switch modules with good availability, and Anja will research basic IoT security best practices tailored to shared flats.

---

## Action Items & Follow-Up

| Action Item                                             | Responsible | Deadline     | Notes/Resources                                                            |
|---------------------------------------------------------|-------------|--------------|----------------------------------------------------------------------------|
| Compile list of recommended smart lighting platforms    | Martin      | Jan 31, 2024 | ESPHome, Home Assistant, Philips Hue developer docs [1][2][4]              |
| Draw annotated lighting zone/concept sketches           | Anja        | Feb 7, 2024  | Sketch flat plan, emphasizing areas for automation                          |
| Summarize compatibility of selected platforms           | Martin      | Feb 2, 2024  | Integration with Alexa, Google Home—core APIs [2][4]                       |
| List affordable sensor/switch hardware                  | Martin      | Feb 5, 2024  | PIR, environmental sensors, Wi-Fi/Zigbee relays/modules                    |
| Review IoT security essentials for shared flats         | Anja        | Feb 7, 2024  | Default credentials, network security, basic encryption [5]                |
| Arrange follow-up call to review initial implementations| Both        | Feb 12, 2024 | Share progress and discuss hands-on prototypes                             |

---

## Reflections & Insights

### Collaborative Insights

Our ongoing discussions highlight just how much overlap there is between architecture and technology in shaping today’s living spaces. My technical approach complements Anja's sensitivity to how spaces feel and are used. We both see tremendous value in finding solutions that make daily living smarter without compromising comfort or aesthetics.

### Key Technical Takeaways

- **Flexibility through Modularity:** Wireless, modular lighting is a practical solution, especially for renters or students. Using versatile hardware like ESP32 or Shelly modules, it’s possible to incrementally upgrade without major renovations or high costs.
- **Advantage of Open Source:** Platforms like ESPHome and Home Assistant are attractive not just for their customization, but for avoiding vendor lock-in—students move frequently, and flexibility matters [1][2].
- **Security as a Priority:** With more devices online, addressing security right from the beginning is essential—especially when multiple roommates share the network [5]. We both agreed on the need for clear defaults, strong network segmentation, and routinely updated firmware.
- **Start Small, Prove Concept:** Before going big, we’ll build and test a simple, sensor-driven lighting control setup. This prototype will provide a springboard for broader flat automation later.

### Relationship & Teamwork

Combining perspectives from both our fields not only leads to better technical solutions but deepens our understanding of each other's work. Regular knowledge-sharing sessions—whether through calls, demo reviews, or informal conversations—keep both projects and our partnership strong.

---

## Technical Next Steps & Key Resources

### Practical Steps

- Prototype a lighting controller using ESP32/ESP8266 boards, trialing automation in Anja’s flat.
- Lay out intended automation “zones” in Home Assistant; simulate different settings for focus, relaxation, and socializing.
- Experiment with integrating voice assistants to streamline control, customizing routines for daily student life.

### Reference Material

- [ESPHome Documentation](https://esphome.io/)[1]
- [Home Assistant Beginner’s Guide](https://www.home-assistant.io/docs/)[2]
- [Zigbee2MQTT Project](https://www.zigbee2mqtt.io/)[3]
- [Philips Hue Developer Program](https://developers.meethue.com/)[4]
- [OWASP IoT Security Project & Checklist](https://owasp.org/www-project-internet-of-things/)[5]

---

## Ongoing Knowledge Management

We agreed to keep a shared digital folder—probably on Google Drive or Notion—containing:

- Anja’s annotated flat sketches and lighting plans
- Technical research, integration guides, and test notes I provide
- Documentation and feedback from our prototypes
- A continuously updated repository of hardware and validated modules for quick reference

We’ve set a biweekly check-in schedule to evaluate progress, swap new insights, and strategize next steps.

---

## Sources

[1] ESPHome Documentation: https://esphome.io/  
[2] Home Assistant Beginner’s Guide: https://www.home-assistant.io/docs/  
[3] Zigbee2MQTT Project: https://www.zigbee2mqtt.io/  
[4] Philips Hue Developer Program: https://developers.meethue.com/  
[5] OWASP IoT Security Project & Checklist: https://owasp.org/www-project-internet-of-things/  

---

This collaborative process has not only helped us clarify practical solutions for student living spaces, but it’s been a great way to blend our interests—and keep our conversations both productive and enjoyable. We’re looking forward to trying out these ideas in real life and sharing our progress at the next check-in.