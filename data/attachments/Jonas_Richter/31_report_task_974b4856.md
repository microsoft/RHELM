# Hybrid Digital Privacy Workshop  
### Workshop Summary Report

---

## Title Page

**Workshop Name:** Hybrid Digital Privacy Workshop  
**Date:** August 24, 2024  
**Location:** Seminarzentrum, Freie Universität Berlin, Germany  
**Time:** 10:00–16:30 CEST  
**Facilitators:** Jonas (primary facilitator), Dr. Katarzyna Nowak (co-facilitator)

---

## Executive Summary

The Hybrid Digital Privacy Workshop, hosted at Freie Universität Berlin, brought together participants from diverse academic and professional backgrounds to deepen both practical skills and critical understanding in the realm of digital privacy. Over the course of the day, participants engaged in technical demonstrations, collaborative discussions, and debates addressing key challenges and opportunities in privacy-preserving technologies and related policy frameworks. Emphasis was placed on real-world application and the implications of privacy tools for society, with a particular focus on open-source solutions and emerging trends within the European regulatory landscape.

### Workshop Objectives

The workshop was designed to:

- Equip participants with hands-on knowledge of leading encrypted messaging applications, specifically Signal and Session.
- Create a forum for critical discussion around current policy developments, state surveillance, and their intersection with privacy-enhancing technologies.
- Highlight the strengths and resilience of open-source, community-driven alternatives to proprietary communication tools.
- Encourage active participation, fostering ongoing collaboration and advocacy for privacy-preserving technologies.

### Policy Implications and Technology Trends

Central to the workshop was a nuanced exploration of how European data protection policies, such as the GDPR, e-evidence regulation, and exemptions for encrypted communications, are shaping the digital privacy landscape. The group recognized the persistent tension between state law enforcement interests and the right to robust personal privacy, discussing concrete examples where these collide.

Participants analyzed how open-source platforms are building public trust by offering transparent, auditable solutions. This stood in stark contrast to proprietary models, particularly given widespread debates over backdoors and metadata access. Across sessions, there was broad consensus on the need to embed privacy principles into technology design from the outset, with open-source approaches emerging as a cornerstone of trustworthy digital infrastructure.

### Open-Source Advocacy

The workshop highlighted the strategic role of open-source technologies in fostering trust, transparency, and collaborative security verification. Tools such as F-Droid and CryptPad were identified as essential components of a resilient public digital ecosystem. Participants exchanged strategies for advocating open-source solutions within their universities and civil society organizations, emphasizing that institutional inertia and usability barriers must be overcome through collective effort and clear communication.

### Participant Demographics

**Attendance:** 30 participants  
- **In-person:** 18  
- **Remote (video conference):** 12  

**Academic/Professional Backgrounds**  
(Reported based on sign-in sheets and voluntary introductions.)

| Background Type         | Approx. Number | Attendance Modality         |
|------------------------|:--------------:|:---------------------------|
| Computer Science (Students/Researchers)     | 9        | 6 in-person, 3 remote |
| Social Sciences/Ethics (Students/Faculty)   | 7        | 3 in-person, 4 remote |
| Policy & Law (Advocates/Students)           | 6        | 4 in-person, 2 remote |
| Activists/NGO Practitioners                 | 5        | 2 in-person, 3 remote |
| Independent Technologists                   | 3        | 2 in-person, 1 remote |

*Note: These figures are best estimates based on the available data and participant self-identification at the event.*

### Key Actionable Outcomes

The workshop concluded with several commitments and forward-looking initiatives:

- Participants pledged to enrich the documentation of privacy tools on Github and contribute to the EDRi (European Digital Rights) list of open-source resources.
- A quarterly privacy tools seminar series was proposed, set to begin during the 2024/25 Winter Semester.
- An interdisciplinary team agreed to perform a comparative audit of digital privacy curricula at local universities, aiming to identify gaps in digital security education.

---

## Detailed Agenda

| Time          | Session Title                         | Description                                                         | Lead/Responsible Person           |
|---------------|--------------------------------------|---------------------------------------------------------------------|-----------------------------------|
| 10:00–10:15   | Welcome & Introductions               | Opening remarks, goals overview, participant introductions, logistics| Jonas, Dr. Nowak                  |
| 10:15–11:00   | Setting the Scene: Policy and Privacy Trends | Current legal landscape, data protection updates, surveillance trends, and the significance of open-source technologies | Dr. Nowak                         |
| 11:00–12:15   | Technical Demo – Signal               | In-depth demonstration of Signal: end-to-end encryption, metadata protection, user experience, and privacy strengths & challenges | Jonas                             |
| 12:15–12:30   | Break                                |                                                                   |                                   |
| 12:30–13:30   | Technical Demo – Session              | Demo of the Session messaging app: decentralized design, onion-routing, and practical privacy considerations | Jonas                             |
| 13:30–14:15   | Interactive Q&A                      | Open-floor thematic questions, moderated online chat, cross-disciplinary dialogue | Dr. Nowak, Marta Klein (remote)   |
| 14:15–14:45   | Lunch Break                          |                                                                   |                                   |
| 14:45–15:30   | Open-Source Technology Debate         | Panel discussion exploring trust in open-source, adoption barriers, incentives for contributors | Jonas, Dr. Nowak, panel volunteers|
| 15:30–16:10   | Collaborative Roadmapping            | Group discussion to outline actionable next steps for research and advocacy | Jonas, Dr. Nowak                  |
| 16:10–16:30   | Closing & Evaluation                 | Workshop recap, gathering feedback, confirming commitments, and setting next event dates | Jonas                             |

---

## Session Summaries

### Signal App Demonstration

This session provided an in-depth look at Signal’s technical architecture and practical deployment.

- **Technical Scalability:** Participants examined Signal’s capacity to handle surge traffic and global usage, noting its centralized server architecture as both a strength and a potential point of failure. While the system scales effectively, reliance on central infrastructure can lead to bottlenecks under heavy load or in the event of targeted censorship.
- **Usability:** Attendees appreciated Signal’s intuitive and polished interface, which lowers the barrier for mainstream adoption. However, concerns were raised regarding the mandatory phone number registration, which poses challenges for individuals seeking anonymity. Feedback indicated that this requirement may deter those in sensitive roles or vulnerable contexts. While cross-platform support was widely praised, some noted that the onboarding process still presented a learning curve for older users or those less comfortable with technology.
- **Surveillance Resilience:** The group considered the effectiveness of Signal’s security protocols. End-to-end encryption is robust, and default features like “sealed sender” improve metadata privacy. Despite these strengths, the necessity of phone-based identity and centralized servers makes Signal susceptible to jurisdictional pressure and may leave metadata exposure points. Several participants advocated for further decentralization and stronger anonymization by default.
- **Discussion Highlights:**
    - The extent to which server location and legal jurisdiction affect privacy assurances
    - Ongoing debate around usability versus anonymity, particularly with contact discovery features
    - Vulnerability to national network blocking and proposed technical mitigations

### Session App Demonstration

The second technical session shifted focus to Session, a decentralized, privacy-oriented messaging platform.

- **Technical Scalability:** Building on onion-routing principles, Session distributes messaging traffic across a network of volunteer nodes, minimizing central points of failure. While this enhances censorship resistance, participants pointed out that message delivery can be subject to delays during high-traffic periods, and the system depends on the sustained engagement of node operators.
- **Usability:** Session’s registration model, which does not require a phone number, explicitly favors anonymity. Nevertheless, new users sometimes found the multi-device sync process unintuitive, and experienced occasional lag in message delivery. These challenges highlight the ongoing trade-off between strong privacy and seamless user experience.
- **Surveillance Resilience:** Session’s decentralization and lack of centralized data storage significantly increase resilience against targeted surveillance and metadata collection. The choice of onion-routing further masks message origins and destinations. Nevertheless, the group discussed risks at the edge, especially in terms of endpoint security and potential vulnerabilities in bootstrap node selection. Questions regarding the long-term sustainability of a network powered by community-run volunteer nodes were also explored.
- **Critical Reflections:**
    - The delicate balance between ultimate privacy protections and user convenience
    - Suitability of decentralized tools in high-risk environments and under resource constraints
    - Importance of transparent, open-source development and independent code audits

### Metadata & Usability Discussion

This interactive segment broadened the conversation beyond individual apps to the ecosystem as a whole:

- Participants weighed various approaches to minimizing metadata, emphasizing that default privacy-preserving configurations are crucial. Comprehensive yet accessible user documentation was seen as central to promoting correct usage and understanding.
- The discussion underscored the importance of meeting users where they are, both technically and philosophically, i.e., making it as easy as possible for users with non-technical backgrounds to make informed choices and configure privacy features effectively.

### Open-Source Alternatives & Surveillance Debate

The panel discussion highlighted the skepticism that often surrounds government involvement in funding or maintaining privacy technologies, with some participants referencing past instances of state-compromised software. It was agreed that the mere availability of source code is insufficient; robust third-party audits and active community participation are essential for verifying security claims. Common barriers to mainstream open-source adoption—including sometimes complex user experiences and lack of institutional momentum—were unpacked, with participants sharing strategies for overcoming these challenges through education and coalition-building.

---

## Technical Issues Encountered

| Problem                            | Diagnostics & Steps Taken                                                   | Tools Used           | Resolution                                   |
|-------------------------------------|-----------------------------------------------------------------------------|----------------------|----------------------------------------------|
| Projector cable failed during session setup | - Checked HDMI/VGA connections and port integrity<br>- Swapped cables and tested alternate adapters<br>- Conducted full hardware inspection using non-proprietary toolkits | iFixit toolkit, spare HDMI adapter | Fault traced to faulty HDMI adapter; swapping resolved issue before second demo |

The troubleshooting process reflected the workshop’s emphasis on transparent, open hardware approaches; organizers conducted a thorough, principle-driven inspection rather than relying on quick, proprietary fixes.

---

## Participant Engagement

| Engagement Metric                        | In-Person | Online | Total | Thematic Highlights                                        |
|------------------------------------------|:---------:|:------:|:-----:|-----------------------------------------------------------|
| Student questions during Q&A             | 14        | 8      | 22    | Focused on installation barriers, metadata handling, and legal responsibilities|
| Online chat interactions (moderated)     | —         | 23     | 23    | In-depth discussion: relay node incentives, forks of Signal|
| Feedback forms submitted                 | 17        | 7      | 24    | Responses highlighted usability needs and feature requests for NGOs|
| Expressed interest in open-source contributions| 8        | 5      | 13    | Volunteers joined Github documentation projects and translation teams |
| Concrete follow-up commitments           | 5         | 3      | 8     | Initiatives included privacy curricula audits and tool review groups |

*Additional observations:*
Several participants, particularly from law and advocacy backgrounds, volunteered to act as beta testers for new privacy tool releases in the coming months. Online participants requested more advanced technical deep-dives in future sessions. Many attendees showed enthusiasm for translation and localization of documentation to make privacy tools more accessible in non-English-speaking communities.

---

## Debrief & Next Steps

The final debrief took place at Café Morgenrot, where participants reflected on the day’s key learnings and laid plans for ongoing collaboration.

**Reflections:**
- Hybrid workshop formats significantly increased accessibility, but highlighted the need for robust technical and facilitation support to ensure seamless participation.
- Discussions reaffirmed the considerable challenges facing widespread adoption of privacy tools, especially in non-technical or at-risk groups, where user experience and contextual support are vital.
- The group collectively recognized the unique democratic value of peer-reviewed, open digital infrastructure as a bulwark against authoritarian misuse of communication systems.

**Agreed Next Steps:**

1. **Quarterly Workshop Series:**  
   Beginning in November 2024, Freie Universität will host a series of privacy tool labs, alternating between campus-based and online modules. Dr. Nowak and Jonas will lead coordination.

2. **Collaborative Documentation Sprint:**  
   A new working group comprising 13 volunteers will kick off a documentation initiative for privacy-enhancing tools, focusing first on updating resources in Github repositories and the EDRi tools list. The first documentation sprint is scheduled for September 30, 2024.

3. **Privacy Curriculum Audit:**  
   An interdisciplinary team will assess digital privacy curricula across Berlin universities, with the goal of identifying content gaps and formulating concrete recommendations by January 2025.

Plans are underway to present workshop findings to organizations such as EDRi and the Chaos Computer Club. The group is also exploring the development of a joint policy briefing for Berlin-based academic institutions to enhance hybrid privacy education.

---

## Assumptions and Limitations

- Comprehensive demographic data was unavailable; participant backgrounds are estimated from attendance sheets and introductions.
- All findings are based on direct observation, workshop materials, and participant feedback; no external sources or public data were accessed.
- Engagement metrics for remote participants were compiled from Zoom logs and moderated chat transcripts managed by Marta Klein.

---

## Sources

No external or third-party sources were referenced for this event. All information is based on workshop documentation and participant observation, as outlined in the limitations.

---

This report captures the key discussions, outcomes, and forward actions from the Hybrid Digital Privacy Workshop held on August 24, 2024, at Freie Universität Berlin. The workshop’s collaborative spirit, coupled with its practical and policy-oriented focus, laid a strong foundation for ongoing engagement and advancement in the field of digital privacy.