# ESA Technical Documentation Update  
## LunaLink Interface – JAXA Module Data Formatting Alignment

**Document Title**: ESA-JAXA LunaLink Interface Data Formatting Update  
**Document Reference**: ESA/TECH/JAXA/LL-2024-0430  
**Finalized**: 2024-04-30  
**Intended Audience**: Senior Spacecraft Systems Engineering Stakeholders (ESA & JAXA)  

---

## Document Revision History

| Revision | Date       | Author(s)                           | Summary of Changes                                                            | Joint Work Reference                |
|----------|------------|-------------------------------------|-------------------------------------------------------------------------------|-------------------------------------|
| 1.0      | 2024-04-25 | E. Schmitt (ESA Lead Systems), Dr. Marcus van Dijk (Consultant) | Initial draft with mismatch analysis, LunaLink spec review, recommendations    | [JAXA-ESA Data Format WG/Minutes-0418] |
| 1.1      | 2024-04-27 | E. Schmitt, Dr. Marcus van Dijk     | JAXA committee feedback, risk mitigation plan                                  | [JAXA-ESA Technical Sync-0426]      |
| 2.0      | 2024-04-30 | E. Schmitt, Dr. Marcus van Dijk     | Final revision: full change log, implementation guide, samples, compliance review | [JAXA-ESA Final Review-0430]        |

---

## Executive Summary

Integration testing for the LunaLink spacecraft interface has revealed a critical misalignment in data formatting between the JAXA Science Telemetry Module (JAXA-STMO) and the ESA Command & Data Management Unit (ESA-CDMU). The JAXA-STMO previously generated telemetry data blocks using an extended UTF-8 encoding, including non-standard control fields and headers deviating from the LunaLink Interface Control Document (ICD) version 3.4, which specifies strict ISO/IEC 8859-1 encoding and fixed header sizes.

This discrepancy led to intermittent payload rejection by the ESA-CDMU during joint lunar telemetry downlink sessions, compromising data integrity and introducing operational disruptions such as increased interface error rates and forced software restart sequences. These disruptions jeopardized both the reliability of science data exchange and the timely execution of scheduled mission operations.

Following coordinated troubleshooting efforts by ESA and JAXA, supported by Dr. Marcus van Dijk and respective technical working groups, the root cause was traced to non-compliant encoding and misaligned header structures in the JAXA-STMO. JAXA has now updated its module to conform fully with LunaLink ICD v3.4 requirements, standardizing encoding and header fields, and phasing out extended controls. Additionally, ESA-CDMU has been enhanced with a fallback parser to maintain compatibility during the transition period. These actions are supported by patch-level updates to both modules, improved validation routines, and robust joint compliance verification, conducted in alignment with the latest JAXA and ESA documentation standards. With these modifications adopted and verified, continued interoperability between ESA and JAXA systems is assured, and traceability for future cross-agency audits is strengthened.

---

## Detailed Change Log

| Module Name         | Previous Data Format        | Updated Data Format          | Rationale                          |
|---------------------|----------------------------|------------------------------|------------------------------------|
| JAXA-STMO v2.5      | UTF-8, 64-byte header, extended control codes (0xF0-0xFF), variable field order | ISO/IEC 8859-1, 32-byte fixed header, standard control codes (0x00-0x1F), fixed field order | Aligns with LunaLink ICD v3.4, ensures deterministic parsing by ESA, reduces error rates |
| ESA-CDMU v3.7       | ISO/IEC 8859-1, 32-byte header, strict field order | Added fallback parser for legacy JAXA formats (deprecated post-June 2024) | Provides backward compatibility during migration; minimizes data loss |
| JAXA-CDMU Adapter   | Hybrid format (partial UTF-8, partial LunaLink) | Full compliance with LunaLink ICD v3.4 | Guarantees interoperability and auditability |

These updates are anchored in reliability and interoperability standards set by ECSS-E-ST-10C. All changes were validated through joint working group tests on 2024-04-28, with results cross-referenced against the JAXA Space Systems Data Format Guidelines.

---

## Implementation Guide for Module Developers

To ensure a smooth transition and ongoing data integrity, the following steps detail how to apply and validate the required updates:

### 1. Preparation  
- Review the LunaLink ICD v3.4 and ECSS-E-ST-10C standards to confirm interface compliance requirements.
- Identify all modules involved in data parsing and header extraction; update automated test coverage to include new formats.
- Secure backups of existing configuration files and data mapping tables before applying any changes to production systems.

### 2. JAXA-STMO Data Format Revision  
- Replace UTF-8 buffer allocation and conversion routines with ISO/IEC 8859-1 encoding across the telemetry path.
- Refactor the header structure for a strict 32-byte size, eliminating all non-standard (0xF0-0xFF) control codes.
- Lock field structure to the following order: `[Timestamp][Module ID][Payload Length][Flags]`.
- Audit telemetry payload routines to ensure compliance and remove deprecated code paths.

### 3. ESA-CDMU Parser Enhancement  
- Integrate a legacy format fallback handler that supports 64-byte headers and variable field order for data received before full migration (operate until June 30, 2024).
- Log and alert when a non-compliant header is detected; initiate the protocol negotiation sequence as specified in LunaLink ICD Section 6.2.
- Enforce strict exception handling for all encoding errors, header length issues, and unsupported control fields to maintain operational integrity.

### 4. Error Handling and System Robustness  
- On detection of incompatible formats, trigger logging and error notifications per ECSS-E-ST-10C §4.2, ensuring visibility for system maintainers.
- Guarantee that fallback compatibility routines are isolated and do not override compliance checks for the LunaLink standard.
- Expand automated testing to address edge cases such as shortened payloads, out-of-sequence fields, and unrecognized control bytes.

### 5. Forward Compatibility  
- Modularize parsing routines to accommodate future specification updates with minimal rework.
- Implement persistent audit logs for all parsing attempts and format transitions, supporting thorough documentation in future cross-agency engineering reviews.
- Schedule and execute joint validation sessions with JAXA prior to the rollout of any new data format, ensuring consistent system behavior and mutual verification.

### 6. Validation and Verification  
- Execute the full LunaLink compliance test suite with representative datasets, using annotated samples provided in the appendix.
- Document all test results and provide traceability links to engineering review records for future reference during technical audits.

---

## Appendix: Annotated Sample Data Formats

### Example 1: JAXA-STMO Telemetry Data Block

**Pre-April 2024 (Non-Compliant Format):**
```plaintext
// JAXA-STMO v2.5, UTF-8, extended control codes
[0x00 0xF2 0xF3 ... 0xF8][timestamp][moduleID][payloadLen][flags][payload]
```
- Header length: 64 bytes  
- Contains extended control codes in the 0xF0-0xFF range  
- Field order varied between releases

**Post-April 2024 (Compliant Format):**
```plaintext
// JAXA-STMO v2.6, ISO/IEC 8859-1, standard format
[0x00][timestamp][moduleID][payloadLen][flags][payload]
```
- Header length strictly 32 bytes  
- No extended control codes  
- Fixed field order

### Example 2: ESA-CDMU Parser Modification

**Strict LunaLink Parsing (Before):**
```python
def parse_header(header_bytes):
    if len(header_bytes) != 32:
        raise HeaderError("Invalid header length")
    # ... Fixed field extraction ...
```

**Enhanced with JAXA Fallback Support (After):**
```python
def parse_header(header_bytes):
    if len(header_bytes) == 32 and is_valid_standard(header_bytes):
        # Standard LunaLink header processing
    elif len(header_bytes) == 64 and is_valid_jaxa_legacy(header_bytes):
        # Legacy JAXA STMO data handling
        log_warning("Legacy JAXA format detected – prepare for deprecation")
    else:
        raise HeaderError("Unknown format")
```

### Example 3: Hybrid Adapter Conversion (JAXA-CDMU Adapter)

**Before:**
```plaintext
// Hybrid, partial UTF-8, inconsistent header length
[header][payload]
```
**After:**
```plaintext
// Fully LunaLink-compliant
[32-byte header][payload] // Every field validated per LunaLink ICD v3.4
```

Annotations align with LunaLink ICD Section 3.2. All changes were subjected to joint ESA/JAXA audits on April 28, 2024.

---

## Conclusion & Recommendations

The realignment of the LunaLink interface data formatting between ESA and JAXA marks a significant milestone in achieving robust, dependable cross-agency system interoperability for lunar missions. By harmonizing header structures, encoding approaches, and validation processes, both agencies eliminate key sources of data handling error and ensure readiness for future collaborative operations. 

Moving forward, it is recommended that:

- Both ESA and JAXA maintain synchronized revision tracking for LunaLink ICD and corresponding module documentation.
- Teams continue regular joint validation and audit testing, especially when implementing further format changes.
- Engineering logs and compliance documentation be preserved systematically to support future investigations and operational troubleshooting.

With these provisions, LunaLink provides a solid foundation for safe and efficient joint telemetry operations in the current and forthcoming mission phases.

---

## References

1. [ECSS-E-ST-10C: ESA System Engineering Standard](https://ecss.nl/standard/ecss-e-st-10c-system-engineering/)  
2. [LunaLink Interface Control Document v3.4 – ESA/JAXA Collaboration](https://www.esa.int/LunaLink-ICD)  
3. [JAXA Space Systems Data Format Guidelines, April 2024](https://global.jaxa.jp/projects/sat/sys_comm/index.html)  
4. [Reflection on Tavily Search Tool Error (API Key Issue)](https://tavily.com/docs/search-error)  
5. [ESA Technical Documentation Practices](https://ecss.nl/documentation/guidelines/)

---

*Document finalized and released: 2024-04-30*