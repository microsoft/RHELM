# Digital Privacy Workshop: Comprehensive Meeting Minutes and Policy Analysis

## 1. Meeting Header

**Title:**  
Digital Privacy Workshop—Best Practices, Technical Challenges, and Academic Policy

**Date:**  
11 May 2024

**Time:**  
09:00–11:45 CET

**Platform:**  
Jitsi Video Meeting (secure link provided to approved participants)

**Facilitator:**  
Jonas Müller, Digital Privacy Consultant

**Attendees:**

| Name                | Role           | Affiliation                   |
|---------------------|----------------|-------------------------------|
| Jonas Müller        | Facilitator    | Independent Consultant        |
| Frau Becker         | Educator       | Universität Heidelberg        |
| Dr. Max Schröder    | Educator       | Universität Leipzig           |
| Prof. Hans Keller   | Educator       | Ruhr-Universität Bochum       |
| Dr. Anna Hoffmann   | Educator       | TU München                    |
| Sabine Jung         | Educator       | Universität Hamburg           |
| David Schwarz       | Educator       | Unverified, confirmed via email domain |
| Dr. Petra Lang      | Educator       | Freie Universität Berlin      |
| Markus Weber        | Educator       | Unverified, confirmed via email domain |
| Prof. Ilona Stern   | Educator       | Universität Frankfurt         |

*Note: Institutional affiliations were verified where possible. For a minority of participants, confirmation was obtained via institutional email addresses.*

---

## 2. Agenda Overview

| Time        | Session Topic                                         | Lead                |
|-------------|------------------------------------------------------|---------------------|
| 09:00–09:10 | Welcome, Rules & Introductions                       | Jonas Müller        |
| 09:10–09:40 | Open-Source Tools in Educational Contexts            | Frau Becker         |
| 09:40–10:10 | Best Practices for Privacy Compliance                | Prof. Keller        |
| 10:10–10:25 | Break                                                | –                   |
| 10:25–10:55 | Technical Deep Dive: Jitsi & Encryption              | Jonas Müller        |
| 10:55–11:20 | Privacy Implications for Academic Institutions       | Dr. Hoffmann        |
| 11:20–11:35 | Open Discussion, Q&A                                 | All Participants    |
| 11:35–11:45 | Conclusions and Next Steps                           | Jonas Müller        |

This agenda was structured to address both immediate technical concerns and broader policy considerations surrounding digital privacy in German universities. The group aimed to balance practical application with the need for forward-looking policy discussions.

---

## 3. Technical Challenges and Findings

### 3.1 Overview of Key Technical Issues

The workshop devoted substantial attention to the technical limitations inherent in current open-source communication tools, particularly regarding their use in educational settings. A recurring concern was the actual scope and reliability of end-to-end encryption (E2EE) in group video conferencing applications such as Jitsi.

### 3.2 Detailed Assessment: Jitsi Encryption

**Limitations of E2EE in Practice**  
Jonas Müller provided a technical breakdown of Jitsi’s encryption protocols. While Jitsi publicly supports E2EE, this is functionally available only for one-on-one calls. During multi-user sessions, audio and video streams are decrypted and re-encrypted by the server, which introduces vulnerabilities that compromise confidentiality. This design is dictated by current WebRTC standards and is not unique to Jitsi; similar constraints disturb most open-source and even some commercial platforms.

**Live Demonstration**  
To illustrate these limitations, Müller conducted a simulated group call. The participants observed that the Jitsi server visibly processed sensitive metadata—user identities, session join and leave times, and IP addresses were all accessible at the server level. As these data are subject to the General Data Protection Regulation (GDPR), their exposure presents significant compliance challenges.

**Comparative Perspective**  
The group discussed alternative tools, such as BigBlueButton and Nextcloud Talk. However, these platforms were also found to lack robust E2EE support in group calls, confirming the challenge is widespread and not the result of individual software projects lagging behind. Instead, it stems from the foundational challenges in scaling E2EE for real-time group communication.

**Implications for Compliance and Institutional Policy**  
Given these technical realities, the group agreed that institutions must not rely solely on vendor or developer claims about privacy features. Instead, comprehensive and accurate user guidance is essential, particularly whenever platform technology fails to provide the desired level of cryptographic protection. The need to revise privacy notices and ongoing compliance documentation for university users was clearly established.

**Recommendations from Jonas Müller**  
- Clearly communicate the scope and limits of encryption in institutional platforms.
- Implement routine audits of self-hosted Jitsi servers for compliance and security.
- Strengthen procedures around user consent and breach response.
- Expand collaboration with open-source communities to advocate and contribute to the advancement of multi-party E2EE.

### 3.3 Broader Context: Institutional Responsibility

The live demonstration emphasized the necessity for academic institutions to maintain up-to-date and reliable information about the tools they deploy. As both end-users and technology stakeholders, universities are in a unique position to demand improvements from open-source projects while fostering a culture of transparency among their staff and students.

---

## 4. Key Decisions and Group Discussions

| Decision/Proposal                                 | Arguments Presented                                          | Evidence and Input                                  | Outcome and Reasoning                      | Follow-up Action                  |
|---------------------------------------------------|-------------------------------------------------------------|-----------------------------------------------------|--------------------------------------------|-----------------------------------|
| Maintain Jitsi with explicit user guidance        | Jitsi is accessible, self-hostable, no superior FOSS alternatives; E2EE shortcomings must be made clear | Technical reviews confirmed E2EE gaps; input from IT teams | Agreement to continue Jitsi usage with clear user disclaimers and frequent reassessment | Comprehensive review in Q3/2024   |
| Standardized privacy communications for platforms | Urgent need for clarity and compliance with GDPR; reduce ambiguity for users | DPAs, GDPR, and feedback noting poor user understanding | New privacy notices and consent forms to be drafted and circulated | Draft by 30/06/2024 (Frau Becker) |
| Advocate for improvements in open-source tools    | Universities have leverage to encourage OSS development; proven track record | Example: Academic feedback led to Nextcloud privacy feature upgrades | Consensus to draft and send an open letter to Jitsi developers | Letter by 31/05/2024 (Jonas Müller) |
| Schedule follow-up privacy education workshop     | Ongoing evidence of gaps in digital literacy among educators and staff | Results from Q1 2024 survey; repeated questions at workshops | Follow-up workshop scheduled for Q4 2024   | Planning led by Dr. Hoffmann      |

These outcomes reflect a unified approach to pragmatic decision-making, with a strong emphasis on transparency, compliance, and proactive engagement with both users and software communities.

---

## 5. Action Items and Accountability

| Action Item                                                    | Responsible Party      | Deadline       | Output/Tracking                            |
|---------------------------------------------------------------|-----------------------|---------------|--------------------------------------------|
| Audit all institutional Jitsi servers for privacy compliance   | University IT teams   | 15/06/2024    | Formal audit reports; review in next session|
| Draft standardized privacy notice for university platforms     | Frau Becker           | 30/06/2024    | Circulated document; collected feedback     |
| Prepare and send open letter to Jitsi developers               | Jonas Müller          | 31/05/2024    | Copy distributed among group and IT leads   |
| Schedule Q4 privacy education session                          | Dr. Anna Hoffmann     | 01/09/2024    | Detailed agenda and invitations sent        |
| Gather faculty feedback on tool usability and data protection  | All educators         | 31/07/2024    | Aggregated report for Q4 session planning   |

Each responsible party will provide status updates at the next workshop or through the quarterly digital privacy policy reviews.

---

## 6. Reflections and Strategic Directions

### 6.1 Workshop Impact and Key Takeaways

Participants left the workshop with a clearer understanding of the technical and organizational gaps currently affecting digital privacy in academic communications. The reality that many open-source platforms only partially deliver on E2EE, especially in group contexts, underscored the need for continuous oversight rather than a passive reliance on software assurances.

Recognizing these exposures, the group emphasized that universities play a pivotal role—not only as consumers of technology but as active contributors and advocates for stronger standards. Institutional transparency, regular technical and policy reviews, and open dialogue with software communities emerged as actionable priorities.

### 6.2 Forward-Looking Actions

**Commitment to Cross-Institutional Coordination**  
Universities will form collaborative working groups that regularly assess open-source communications tools, share findings, and represent the sector’s needs to developers and policymakers.

**Continuous Improvement Loop**  
A biannual schedule of audits, feedback collection, and policy adaptation will ensure that privacy standards keep pace with technological change and regulatory requirements.

**Broader Advocacy and Engagement**  
Participants agreed to deepen engagement with both the open-source developer community and relevant national policy discussions. By doing so, they aim to both enhance the security of their own environments and contribute meaningfully to the broader digital rights ecosystem.

### 6.3 Conclusion

This Digital Privacy Workshop provided a comprehensive platform for surfacing current challenges and developing a tangible action plan to address digital privacy in German higher education. The group’s commitment to open communication, regular auditing, and direct advocacy will support the ongoing professionalization of privacy governance within universities. Future sessions will continue to build on these efforts, with the aim of uniting technical solutions and policy best practice in service of the academic community.

**Meeting adjourned at 11:45 CET.**  
The minutes will be circulated among all participants, relevant university policy committees (IT, legal, and compliance), and archived with the German Academic Digital Privacy Working Group.

---

## Sources

[1] Professionally structured meeting minutes (Best-practice synthesis): Content and format informed by current standards for academic reporting, digital privacy policy, and open-source communications management in higher education.