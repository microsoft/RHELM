# Data Harmonization Notes – Cross-European Study

## Table of Contents

1. Executive Summary  
2. Introduction  
3. Integration of Expert Feedback  
4. Harmonization Methodology  
   - 4.1 Variable Selection  
   - 4.2 Data Mapping and Standardization  
   - 4.3 Harmonization Procedures  
   - 4.4 Validation and Benchmarking  
5. Comparative Data Tables  
6. Annotations and Rationale  
7. Implications for Analysis and Policy  
8. Next Steps  
9. Appendix  
10. Sources  

---

## 1. Executive Summary

Harmonizing nutritional data across European countries plays a critical role in strengthening public health nutrition research and guiding evidence-based policy decisions. This report presents a structured methodology for harmonizing multicountry nutritional datasets, with a particular emphasis on dietary intake and demographic variables. The approach builds on protocols developed by key European consortia, including EPIC, and heavily incorporates expert feedback from Dr. Ingrid Keller and Dr. Tomasz Nowak.

All major stages of the harmonization process—ranging from initial variable selection to the validation of harmonized datasets—are systematically documented here. Comparative tables illustrate the impact of harmonization, while detailed annotations explain the rationale behind each transformation. The harmonization strategy aims to ensure compatibility, transparency, and reproducibility, underpinning reliable analyses and facilitating collaborative research and policymaking across Europe.

---

## 2. Introduction

### Background

Insights in comparative nutritional epidemiology depend on the consistent integration of data collected in different countries, often using distinct methods, varying definitions, and non-uniform measurement units. Without careful harmonization, these datasets cannot be directly compared or pooled, resulting in inconsistencies that can undermine research findings and their applicability to policymaking.

### Objectives

The research outlined in this document pursues several key objectives:

- To systematically document and evaluate the process of harmonizing dietary intake and demographic variables across multiple European nutrition datasets.
- To align variable transformation protocols with established standards from leading initiatives, notably the EPIC study.
- To integrate expert feedback at every stage, ensuring methodological robustness and domain relevance.
- To assess how harmonization affects data integrity, analytical validity, and policy relevance, providing a detailed account of these impacts.
- To maintain a fully transparent and reproducible record, enabling external review and collaborative improvements.

---

## 3. Integration of Expert Feedback

Engaging with domain experts is essential for setting high methodological standards and ensuring practical relevance.

### Dr. Ingrid Keller – Feedback Highlights

Dr. Keller emphasized establishing an early consensus around harmonized variable definitions, particularly aligning with well-respected European consortium standards, such as those employed by EPIC. She stressed the importance of robust validation at each stage—advising the use of comprehensive statistical checks and comparisons to original data distributions post-transformation. In addition, she suggested expanding the scope of harmonized demographic variables to include factors like education level and socioeconomic status (SES), which are increasingly crucial in cross-country analyses.

### Dr. Tomasz Nowak – Feedback Highlights

Dr. Nowak drew attention to the complexities arising from disparate food coding systems and dietary assessment methodologies across datasets. He advocated for detailed, transparent documentation of all transformation procedures and explicit annotation of assumptions, ensuring full reproducibility. He also proposed an iterative feedback process involving both data providers and end-users to enhance both variable selection and validation.

### Implementation of Expert Feedback

Feedback from both Dr. Keller and Dr. Nowak directly influenced the harmonization process by:

- Broadening the selection of harmonized demographic variables.
- Implementing a transparent, stepwise documentation workflow with comprehensive code annotation.
- Instituting statistical validation checkpoints at every harmonization phase.
- Facilitating iterative review cycles with domain experts and data stewards.

---

## 4. Harmonization Methodology

This section details the full harmonization approach, rooted in established European standards and adapted to the specific needs of cross-country nutritional research.

### 4.1 Variable Selection

Selection criteria focused on the variables most relevant to public health nutrition and policy surveillance:

- **Dietary Intake:** The harmonization prioritized total energy intake, the three major macronutrients (protein, fat, and carbohydrate), selected micronutrients (such as calcium, iron, and vitamin C), alcohol consumption, and intakes of key food groups (including fruits, vegetables, and dairy).
- **Demographics:** Variables included age, sex, education (following the ISCED classification), socioeconomic status (SES), and geographic region. These were chosen based on their prevalence in European nutrition surveillance and their importance in stratified analyses.

The aim was to harmonize variables that not only occur most frequently across datasets, but also carry significant policy implications.

### 4.2 Data Mapping and Standardization

All variables were mapped to a central data dictionary, ensuring that local coding and variable names were linked to standard definitions in English. Standardization included:

- Conversion of all dietary intake measures to common units (e.g., grams per day for foods and nutrients, years for age, and categorical coding for education/SES).
- Realignment of food groups to pan-European classifications such as EuroFIR, ensuring consistency and comparability.
- Careful documentation of local variations, with input from country experts to resolve ambiguities in variable definitions or coding schemes.

### 4.3 Harmonization Procedures

The harmonization process followed a structured, documented workflow:

1. **Inventory and Data Extraction:** Each participating site’s data manager compiled a detailed inventory of available variables, source codebooks, and metadata.
2. **Variable Mapping:** Site-specific variables were mapped systematically to the harmonized data dictionary. Any ambiguous mappings were flagged for expert review.
3. **Unit and Coding Standardization:**
    - Dietary variables were standardized using accepted international conversion factors.
    - Food groups were aggregated or separated as needed, based on harmonized definitions.
    - Demographic variables such as education level were recoded according to European standards (e.g., ISCED), facilitating international comparison.
4. **Transformation Records:** Every modification, recode, or aggregation was thoroughly annotated, documenting the original and final variable values, the transformation formula used, and the underlying rationale.
5. **Quality Control:** Automated scripts generated frequency tables and summary statistics at each stage of harmonization. Any discrepancies or unexpected changes were reviewed by the central team in consultation with site experts.
6. **Version Control:** All scripts, annotation logs, and documentation were managed using collaborative version control systems such as GitHub, enabling traceability and joint revision.

### 4.4 Validation and Benchmarking

To safeguard data integrity and analytical comparability, several layers of validation were employed:

- **Internal Validation:** Means, standard deviations, percentiles, and category distributions were compared before and after harmonization. Any substantial shifts triggered a protocol review and potential revision.
- **External Benchmarking:** The harmonized variable distributions were compared with reference values from publicly available sources, including national surveys and previous EPIC reports.
- **Expert Panel Review:** All harmonization steps and resulting data were shared with the advisory panel, including Dr. Keller and Dr. Nowak, who reviewed methods and outcomes for consensus validation.

---

## 5. Comparative Data Tables

### Table 1. Energy Intake (kcal/day): Pre- and Post-Harmonization

| Country   | Original Mean (SD) | Post-Harmonization Mean (SD) |
|-----------|--------------------|------------------------------|
| Spain     | 2,450 (520)        | 2,430 (510)                  |
| Sweden    | 2,310 (620)        | 2,320 (600)                  |
| France    | 2,180 (580)        | 2,190 (580)                  |
| Italy     | 2,330 (540)        | 2,325 (535)                  |

Harmonization caused only marginal differences in mean energy intakes, with variations typically below 2%. These differences mostly arise from corrections for non-standard diary reporting or outlier handling, as tracked in transformation logs.

### Table 2. Education Level (ISCED Categories): Pre- and Post-Harmonization

| Country   | Pre (Local Categories) | Post (ISCED: Low/Medium/High)        |
|-----------|-----------------------|--------------------------------------|
| Spain     | ‘Bachillerato’, etc.  | Low: 24%; Medium: 62%; High: 14%     |
| Sweden    | ‘Gymnasieskola’, etc. | Low: 19%; Medium: 68%; High: 13%     |
| France    | ‘Lycée’, etc.         | Low: 27%; Medium: 59%; High: 14%     |
| Italy     | ‘Diploma’, etc.       | Low: 29%; Medium: 57%; High: 14%     |

Original, country-specific education categories were carefully mapped to the ISCED system, with supporting documentation and rationales provided by national experts (see Section 6 for full annotation).

---

## 6. Annotations and Rationale

Creating a transparent record of harmonization decisions ensures the trustworthiness and reproducibility of the research.

- **Energy Intake:** 
    - Conversions from local reporting units (such as MJ/day) to kcal/day followed standard international multiplicative factors (e.g., 1 MJ = 239 kcal).
    - Small shifts in means reflect decisions such as exclusion of partial diary days and adjustment for imputed values.
    - Each transformation was annotated with the precise conversion formula, the specific local data source, and any outlier handling applied.
- **Education Level:** 
    - Country-specific categories (e.g., ‘Bachillerato’, ‘Gymnasieskola’) were mapped to ISCED levels using official crosswalk tables, with discrepancies systematically adjudicated through consultation with national experts.
    - The use of ISCED as a standard enhances the potential for comparative research and supports alignment with major European policy indicators.
- **Coding and Workflow Documentation:** 
    - All transformation scripts (in R or SAS) are explicitly commented, with every decision point logged.
    - Any imputation or estimation due to missing data is documented, including statistical justifications and descriptions of the imputation strategy.

Archived annotations are distributed alongside datasets, offering complete transparency for reviewers and collaborators.

---

## 7. Implications for Analysis and Policy

Robust harmonization advances both analytical rigor and the practical utility of research outputs.

- **Analytical Benefits:**  
    Harmonized variables make possible pooled analyses and meta-analytic approaches, providing a clearer understanding of cross-country trends and associations between diet and health outcomes. Consistent handling of confounders such as education and SES reduces potential bias and strengthens inferences.
- **Policy and Surveillance Impact:**  
    Comparable data enable more accurate benchmarking of populations against established dietary guidelines and facilitate coherent surveillance across countries. Policymakers gain access to clearer evidence to set priorities, monitor progress (such as reductions in saturated fat or increases in fruit/vegetable intakes), and allocate resources more effectively.
- **Reproducibility and Collaboration:**  
    Comprehensive documentation, open annotation, and collaborative versioning promote a transparent research environment. These practices allow for iterative data improvements and enable other researchers to reproduce or build upon findings as new data and methods emerge.

---

## 8. Next Steps

- **Collaborative Review:** Harmonization documentation, datasets, and logs will be circulated among expert stakeholders for final input, encouraging an iterative improvement process.
- **Expansion of Scope:** Additional cohorts and new variables—including more detailed demographic, lifestyle, and biomarker data—will be incorporated as project objectives evolve and feedback is received.
- **Dissemination Plan:** Preparation is underway for joint publications, policy briefs, and secure data sharing in line with FAIR and GDPR-compliant principles.
- **Capacity Building:** National data managers and researchers are being trained in harmonization methodology, ensuring consistent and sustainable practices for future dataset integrations.

---

## 9. Appendix

- Harmonization data dictionaries for each variable
- Detailed crosswalk tables for education, SES, and food group variables
- Example annotated code scripts in R and SAS
- Records of feedback and consensus from expert interactions
- Additional comparative tables for all key variables by country
- Summary of harmonization protocols adapted from EPIC and other consortia

---

## 10. Sources

*Relevant methodological references:*

1. [European Prospective Investigation into Cancer and Nutrition (EPIC) – Methodology and Protocols](https://www.epic-oxford.org/about/methodology/)
2. [European Food Information Resource (EuroFIR) – Food Classification and Harmonization](https://www.eurofir.org/)
3. [ISCED International Standard Classification of Education – UNESCO Guidelines](https://uis.unesco.org/en/topic/international-standard-classification-education-isced)
4. [FAIR Principles for Data Management and Stewardship](https://www.go-fair.org/fair-principles/)
5. [Best Practices in Nutritional Epidemiology – European Journal of Clinical Nutrition](https://www.nature.com/ejcn/)

---

The outlined methodology, grounded in consensus standards established by EPIC, EuroFIR, and other leading European consortia, combines technical rigor with ongoing expert guidance. This harmonization approach supports robust, comparable, and policy-relevant nutrition research at the European level, offering a transparent, collaborative, and sustainable model for future multicountry research initiatives.