# Research Paper Writing Guideline — G0–G15

> **SUPERVISOR-LOCKED SOURCE.** G0-G15 reproduce the supervisor's guideline. Do not rewrite, reorder, or drop its content. Interpretation notes and proposed additions live in `docs/guide-addenda.md` and apply only as stated there. In `SKILL.md` this file ranks with supervisor requirements (priority 3).

This file defines the **section structure and content checks** for an academic research manuscript. `docs/prompt.md` defines the writing voice, readability, editing behavior, source fidelity, and prose-level quality checks. Use both files together.

This version incorporates the supplied section-by-section guideline while excluding project-specific titles, manuscript mappings, build facts, local paths, dated deviation records, and project-specific audit commands. Examples in the sections below are illustrative; replace them with examples appropriate to the actual research.

## How to use this guide

- **Stable identifiers:** Keep the G0–G15 identifiers when planning, drafting, or auditing a manuscript. G1–G15 describe manuscript elements; G0 records the compliance audit for the current draft.
- **Checklist execution:** Treat bullets as checks for content that applies to the study. Cover applicable items in a sensible order. Do not add content merely to tick a box when the item is irrelevant or unsupported.
- **Conditional items:** Phrases such as “if applicable,” “where appropriate,” “if provided,” “may include,” and “for example” are conditional or illustrative.
- **Recommended sequences:** Labels such as “Recommended Flow,” “Recommended structure,” “Overall Flow,” and “A Simple Formula” describe the preferred logical sequence. Adapt section numbering to the actual paper type and venue.
- **Guiding prompts:** Treat each question as a prompt that the manuscript should answer if relevant. Do not copy questions into the manuscript as filler.
- **MUST:** A hard requirement when the target venue, supervisor, or chosen manuscript format makes it applicable.
- **SHOULD:** A strong recommendation. Deviations should have a research, venue, or space-related reason.
- **MAY:** Optional content to include only when it fits the paper and the evidence available.

## Precedence when requirements conflict

1. Applicable research-integrity requirements and the target journal/conference/institution's explicit template, scope, and length constraints.
2. The user's dated supervisor or coauthor instructions for the current manuscript.
3. This guide, including any current-draft decisions recorded in G0.
4. `docs/prompt.md` voice preferences, where this guide is silent.

Do not impose a generic paper structure over explicit venue instructions. When two hard requirements conflict, record the conflict and follow the highest-priority instruction. If the conflict cannot be resolved safely from the supplied context, ask the author a focused question.

## Agent workflow

1. Read the relevant rules in `docs/prompt.md` before drafting or editing prose.
2. Determine the article type and target venue, then choose a section sequence from the table below.
3. Work through G1–G15 in the order that applies to the manuscript. Renumber sections to match the selected article type and publication template.
4. After each substantive revision, audit the **current** manuscript, not a remembered or earlier version. For LaTeX manuscripts, inspect the latest successful build and its warnings when build tools and source files are available.
5. Update G0 with actual evidence, current status, and any justified deviation. Never mark a requirement PASS without checking the current draft or build.
6. Keep this guide general. Do not insert project-specific paths, metrics, build facts, paper titles, or status claims unless they are supplied for the active project.

## Section order by article type

| Article type | Recommended order | Placement notes |
|---|---|---|
| **Method-based** | Introduction → Conventional method(s) → Proposed method → Experiments (including experimental setup and dataset/corpus details) → Results → Conclusion → Author contributions → Declarations → Acknowledgements → References | Dataset/corpus details may appear inside Experiments when the dataset is used to evaluate a method rather than being a primary contribution. |
| **Dataset/corpus-based** | Introduction → Dataset/Corpus (data collection and descriptive/quality subsections) → Conventional method(s), if applicable → Proposed method, if applicable → Experiments → Results → Conclusion → Author contributions → Declarations → Acknowledgements → References | The dataset is a central contribution, so present its provenance, construction, annotations, characteristics, quality, and limitations early. |
| **Corpus + method-based** | Introduction → Dataset/Corpus → Conventional method(s) → Proposed method → Experiments → Results → Conclusion → Author contributions → Declarations → Acknowledgements → References | Use when both the corpus/dataset and the method make material contributions. |

This table is a default organization, not a replacement for a venue template. Some papers combine methods and experiments, omit an inapplicable section, move related work, or use required structured statements. Keep the substantive logic even when the heading order changes.

## G0. Compliance matrix for the current manuscript

Use this matrix as a living audit record. Fill in the evidence column with a current section, paragraph, equation, table, bibliography entry, or build result. Use `N/A` only when the requirement genuinely does not apply, and explain any material deviation from a SHOULD recommendation. Do not pre-fill PASS statuses.

| ID | Requirement | Check | Current evidence | Status / notes |
|---|---|---|---|---|
| G1 | Title is clear, specific, and accurate | Read title against actual scope and contribution | | NOT REVIEWED |
| G2 | Abstract accurately summarizes the paper | Compare abstract claims with final methods and results | | NOT REVIEWED |
| G3 | Keywords are relevant and specific | Check number and venue limits; confirm terminology | | NOT REVIEWED |
| G4 | Introduction establishes context, gap, objective, and contribution | Review paragraph roles and argument flow | | NOT REVIEWED |
| G5 | Article type and organization are appropriate | Compare section order with the paper type and venue | | NOT REVIEWED |
| G6 | Dataset/corpus is described where applicable | Check provenance, preparation, annotations, quality, and ethics | | NOT REVIEWED |
| G7 | Conventional/baseline method is explained where applicable | Check selection rationale, mechanics, formulation, and limitations | | NOT REVIEWED |
| G8 | Proposed method is reproducibly explained where applicable | Check workflow, formulation, algorithm, novelty, and inputs/outputs | | NOT REVIEWED |
| G9 | Experiments are sufficiently specified | Check setup, procedure, parameters, data splits, and metrics | | NOT REVIEWED |
| G10 | Results are accurately reported and interpreted | Check metric-wise results, comparisons, ablations, statistics, and findings | | NOT REVIEWED |
| G11 | Conclusion matches the evidence | Check objective, contribution, findings, implications, and future work | | NOT REVIEWED |
| G12 | Author contributions are accurate where required | Verify roles with the actual authors and target policy | | NOT REVIEWED |
| G13 | Declarations are complete where required | Check funding, conflicts, data/code availability, and ethics | | NOT REVIEWED |
| G14 | Acknowledgements are appropriate where applicable | Confirm permission and avoid treating non-author support as authorship | | NOT REVIEWED |
| G15 | References and citations are accurate and consistent | Cross-check citations and reference-list entries | | NOT REVIEWED |

---

## G1. Title
A research article title should be clear, concise, specific, informative, and easy to understand.

**Key principles:**

- **Clear** — communicates the research topic without ambiguity.

- **Concise** — avoids unnecessary words.

- **Specific** — identifies the main problem, method, subject, or contribution.

- **Informative** — gives readers a good idea of what the paper contains.

- **Easy to understand** — avoids unnecessary jargon, abbreviations, and complicated wording.

**Example:**

- ❌ An Investigation into the Application of Various Advanced Deep Learning-Based Computational Techniques for the Purpose of Automated Detection of Vegetable Quality

- ✔ Deep Learning for Automated Vegetable Quality Detection

---

## G2. Abstract




Answer the six questions below, in this order.

1. **Initialization — What is the research area?**

   - Identify the broad research domain, topic, and current trend.

   - Example: `Machine Learning → Deep Learning → Image Classification`

2. **Research Gap — What is missing?**

   - Identify limitations, unanswered questions, weaknesses, or unexplored areas in existing research.

   - What has not been adequately addressed by previous studies?

   - Clearly establish the need for your study.

3. **Research Objective — What do you want to do?**

   - Clearly define what the research intends to investigate, develop, improve, compare, or discover.

   - What specific problem are you trying to solve?

4. **Proposed Approach — How will you do it?**

   - Describe the methodology, models, algorithms, experimental design, dataset, and evaluation strategy.

   - What approach will you use to address the research problem?

5. **Justification — Why this Method and Dataset?**

   - Explain why the proposed method, model, dataset, or experimental design is appropriate and necessary.

   - Why should this approach be used instead of existing alternatives?

6. **Expected/Research Outcome — What will the research contribute?**

   - Identify the expected findings, performance improvement, dataset, model, framework, insights, or other research contributions.

   - What new knowledge, resource, method, or evidence will this research provide?

**A concise research journey:**

- `Research Area → Research Gap → Research Objective → Proposed Method → Justification → Experiment → Outcome → Contribution`

- **OR**

- `Research Context → Gap Identification → Objective Formulation → Methodology Design → Justification → Experimental Evaluation → Research Contribution`

**The six questions in short form:**

1. What is the context?

2. What is the gap?

3. What do you want to do?

4. How will you do it?

5. Why is your approach necessary?

6. What did you achieve?

**A simple formula:**

`Context + Gap + Objective + Method + Rationale + Outcome = Research Abstract`

---

## G3. Keywords
A simple approach is to identify 4–8 important concepts from your research.

1. **Identify the research topic**

   - What is the paper mainly about?

   - Example: *_Deep Learning for Automated Vegetable Quality Detection_*

   - Possible keyword: Deep learning, Vegetable quality

2. **Identify the research method**

   - What methods, algorithms, or technologies are used?

   - For example: Convolutional neural networks (CNN), Transfer learning, Object detection, Computer vision

3. **Identify the application/domain**

   - Where is the research applied?

   - For example: Agricultural image analysis, Food quality assessment, Smart agriculture

4. **Identify the specific research problem**

   - What problem does the research solve?

   - For example: Defect detection, Disease detection, Quality classification

5. **Use standard technical terminology**

   - Prefer terms that researchers actually use in the literature.

   - For example: ❌ Computer method for finding bad vegetables; ✔ Vegetable defect detection

6. **Avoid unnecessarily broad keywords**

   - ❌ Machine Learning ❌ Artificial Intelligence ❌ Computer Science

   - These are often too broad unless they are genuinely central to the paper.

   - Instead: ✔ Deep learning ✔ Object detection ✔ Vegetable defect detection ✔ Transfer learning

**A useful keyword formula:**

Keywords are selected from these categories:

`[Research Domain] + [Problem] + [Method] + [Application] + [Specific Technique]`

- **Paper title:** Real-Time Detection of Fresh and Defective Vegetables Using Deep Learning

- **Keywords:** Deep learning; vegetable defect detection; object detection; computer vision; transfer learning; agricultural image analysis.

Keywords should represent the core topic, research problem, methodology, application domain, and distinctive contribution of the study.

---

## G4. Introduction
Use four paragraphs for the Introduction under this guideline, in the roles defined below. Follow a target venue or supervisor override when it explicitly requires a different structure.

**Interpretation note:** Some planning prompts under G4.1 also mention the gap, objective, and scope, which are given their main roles in P2, P3, and P4 in the overall flow. Treat those overlapping questions as planning checks rather than a requirement to place every detail in P1. Use G4.5 to keep the four paragraphs focused and avoid repetition.

### G4.1 Paragraph 1 — Current State
**Coverage requirement:** Anchor the current-state discussion in **3–4 relevant cited papers**. Select papers that support the actual claims being made; do not add irrelevant citations merely to reach a count.

1. **What is currently happening/ongoing? — Current Status**

   - What is the current situation in this research area?

   - What are the existing methods, technologies, or approaches?

   - What are the recent developments or trends?

   - Why is this topic important?

2. **What is missing? — Research Gap / Challenges / Research Questions**

   - What limitations exist in current research?

   - What challenges remain unresolved?

   - What problems are not adequately addressed?

   - What research questions arise from these gaps?

3. **What do you want to do and how? — Research Objective & Approach**

   - What is the main objective of your research?

   - What do you propose or investigate?

   - How will you address the identified gap?

   - What method, model, framework, or approach will you use?

4. **What are the scopes of your Proposed Method and Dataset? — Scope & Applicability**

   - What can your proposed method do?

   - Where can it be applied?

   - What does the dataset contain?

   - Who or what can use the dataset?

   - What types of research, experiments, or applications can be supported by your method and dataset?

   - What are the boundaries or limitations of the proposed scope?

**A Simple Formula:**

- `Current State → Research Gap/Challenges → Objective & Approach → Scope & Applicability`

- Or, more simply: `What is happening? → What is missing? → What will you do and how? → What is the Scope? → Where can it be used?`

### G4.2 Paragraph 2 — Merged Literature Review
**Paragraph 2 — Existing Research + Research Gap**

**Coverage requirement:** Review **5–6 relevant prior studies** in a logical sequence. Give each study **1–2 clear sentences**: first state what the authors built, investigated, or found with the citation placed on that claim; then state a concrete limitation or an aspect it did not address. Do not attach a pooled citation list to the end of a broad paragraph-level claim. End with the specific research gap that remains across these studies. If a documented supervisor override or explicit venue constraint conflicts with the count, record and follow that higher-priority instruction.

- What have previous researchers done?

- What methods, models, datasets, or approaches have been used?

- What are the strengths and limitations of existing studies?

- What challenges or unresolved issues remain?

- Based on the literature, what is the specific research gap?

### G4.3 Paragraph 3 — Research Objective + Proposed Approach
**Paragraph 3 — Research Objective + Proposed Approach**

State what remains unresolved or unmitigated in prior work and why the existing methods struggle with it. Explain how the proposed method and dataset address that bottleneck, step by step. Justify why the selected model family and dataset fit the task, including why they are appropriate relative to heavier alternatives where that comparison is relevant.

- What do you want to do?

- What is your research objective?

- How will you address the identified gap?

- What method/model/framework do you propose?

- What dataset will you use or develop?

### G4.4 Paragraph 4 — Scope and Contribution
State the practical scope of the proposed method and dataset. Report the headline experimental outcomes using the exact supported values and their relevant metric/dataset/baseline context, then state the contributions plainly without promotional language. If final results are not available, mark them as pending rather than inventing expected gains.

### G4.5 Overall Flow
- **P1:** Current State/ongoing

- **P2:** Existing Research + Critical Literature Review + Research Gap

- **P3:** What were not done/solve/resolve/mitigate and why in literature? What You Want to Do + How You Will Do It?

- **P4:** Scope of Proposed Method + Dataset + Contribution

---

## G5. Types of article
1. Method based

2. Dataset based

3. Method + dataset based

The organization of each type is in the table under "Section order by article type".

---

## G6. Dataset / Corpus section
**For dataset/corpus-based papers, and for method-based papers when the data itself needs a dedicated account:**

For a dataset-based research paper, the Corpus/Dataset should normally be introduced immediately after the Introduction, because the dataset itself is the primary contribution of the paper.

- **2.1 Dataset Overview**

  - Purpose and scope

  - Dataset characteristics

  - Target application/domain

- **2.2 Data Collection**

  - Data sources

  - Collection procedure

  - Collection period

  - Inclusion/exclusion criteria

- **2.3 Data Preparation**

  - Cleaning

  - Preprocessing

  - Filtering

  - Formatting

- **2.4 Annotation/Labeling**

  - Annotation methodology

  - Label/class definitions

  - Annotation guidelines

  - Annotators

  - Quality-control procedure

  - Inter-annotator agreement, if applicable

- **2.5 Dataset Characteristics**

  - Number of instances

  - Classes/categories

  - Feature description

  - Class distribution

  - Statistical characteristics

- **2.6 Dataset Organization and Format**

  - File/folder structure

  - Data format

  - Metadata

  - Naming conventions

  - Train/validation/test organization, if provided

- **2.7 Dataset Validation and Quality Assessment**

  - Quality checking

  - Duplicate detection

  - Missing/inconsistent data

  - Label verification

  - Data quality statistics

- **2.8 Ethical, Privacy, and Licensing Considerations**

  - Consent, where applicable

  - Privacy/anonymization

  - Ethical approval, if applicable

  - Data license and usage restrictions

---

## G7. Conventional method/methods
(Method-based: section 2. Dataset-based: section 3.)

The Conventional Method(s) section presents the baseline or existing method(s) from which the proposed method is derived or developed. The purpose is to establish a clear technical foundation for understanding the proposed approach.

- **Baseline Method**

  - Introduce the conventional or established method.

  - Explain why it is selected as the baseline.

  - Describe its main components and assumptions.

- **Working Principle**

  - Explain how the conventional method operates.

  - Present the processing steps or workflow.

  - Demonstrate the relationship between its input, intermediate processes, and output.

- **Technical Formulation**

  - Describe the method mathematically where appropriate.

  - Include relevant equations, mathematical formulations, parameters, and objective functions.

  - Define important variables and terms clearly.

- **Algorithm / Procedure**

  - Present the method as an algorithm or step-by-step procedure when appropriate.

  - Explain the key computational operations and decision processes.

- **Main Contribution / Characteristics of the Baseline**

  - Highlight the key technical contribution or distinctive characteristics of the conventional method.

  - Explain what makes the baseline method useful or widely applicable.

- **Limitations and Research Gap**

  - Identify the specific limitations, weaknesses, or unresolved issues of the conventional method.

  - Explain how these limitations motivate the development of the proposed method.

  - End the section with the specific gap that the proposed method intends to address.

**Recommended Flow:**

`Conventional Method → Working Principle → Mathematical Formulation → Algorithm → Key Characteristics of Baseline → Limitations → Research Gap → Proposed Method`

**Important Distinction:**

The Conventional Method section should not simply repeat the Literature Review.

- The Literature Review answers: "What have previous researchers done?"

- Whereas the Conventional Method section answers: "How does the baseline method technically work, and what limitation motivates the proposed method?"

This makes the transition to the Proposed Method much clearer:

`Baseline Method → Identified Limitation → Proposed Modification/Extension → Proposed Method`

---

## G8. Proposed method
The Proposed Method section can follow a parallel structure with the Conventional Method, but it should focus on the novelty, modification, and technical contribution of your work.

The Proposed Method section describes the newly developed approach introduced to address the research gap identified in the Conventional Method. It should clearly explain how the proposed method works, how it is technically formulated, how it is implemented, and what its main contribution is.

- **3.1 Working Principle**

  - Explain the overall working mechanism of the proposed method.

  - Describe the input, processing steps, and output.

  - Explain how the proposed method differs from the conventional/baseline method.

  - Use a flowchart, block diagram, or conceptual framework where appropriate.

- **3.2 Technical Formulation**

  - Present the mathematical formulation of the proposed method.

  - Define equations, parameters, variables, constraints, objective functions, or other technical components.

  - Clearly show any modification, extension, or newly introduced component compared with the conventional method.

- **3.3 Algorithm / Procedure**

  - Present the proposed method as a step-by-step algorithm or procedure.

  - Clearly describe the computational workflow.

  - Identify the major inputs, operations, decision processes, and outputs.

  - Provide sufficient detail so that the method can be understood and reproduced.

- **3.4 Main Contribution / Characteristics of the Proposed Method**

  - Clearly identify what is new or different in the proposed method.

  - Explain how it addresses the limitation or gap of the conventional method.

  - Highlight the key technical characteristics and expected advantages.

  - Distinguish the novel contribution from components adopted from existing methods.

**Overall Methodology Flow:**

- **Conventional Method:** `Working Principle → Technical Formulation → Algorithm → Limitations → Research Gap`

- **then Proposed Method:** `Working Principle → Technical Formulation → Algorithm/Procedure → Main Contribution/Characteristics`

This creates a very clear research narrative:

`Existing Method → Limitation → Research Gap → Proposed Solution → Technical Novelty`

**A useful principle:** In the Proposed Method section, the reader should be able to answer three questions clearly:

1. What exactly is proposed?

2. How does it work technically?

3. What is new compared with the conventional method?

---

## G9. Experiments
**For method-based papers:**

- **4.1 Experimental Setup and Conditions**

  - Hardware configuration

  - Software/platform

  - Programming environment

  - Experimental parameters

  - Simulation or implementation conditions

  - Reproducibility settings

- **4.2 Dataset Introduction** (Use a separate dataset subsection in method-based papers when appropriate. For dataset/corpus-based papers, describe the dataset in the earlier dedicated section and avoid duplicating it unnecessarily.)

  - Dataset source

  - Dataset size

  - Number of classes/features

  - Data characteristics

  - Data distribution

  - Training/validation/testing split

  - Preprocessing, if applicable

- **4.3 Experimental Procedure**

  - Overall experimental workflow

  - Data preparation

  - Application of the conventional/baseline method

  - Application of the proposed method

  - Training/testing procedure

  - Repeated experiments or cross-validation

  - Experimental scenarios

- **4.4 Parameter Configuration**

  - Model/method parameters

  - Hyperparameters

  - Fixed parameters

  - Optimization settings

  - Parameter selection/tuning strategy

- **4.5 Evaluation Metrics**

  - Accuracy, Precision, Recall, F1-score, etc., where applicable

  - Error/performance measures

  - Mathematical formulation of metrics

  - Statistical measures, if applicable

**Recommended structure:**

`4.1 Experimental Setup and Conditions → 4.2 Dataset Introduction → 4.3 Experimental Procedure → 4.4 Parameter Configuration → 4.5 Evaluation Metrics`

---

## G10. Results
Results should be presented and analyzed based on the defined evaluation metrics, because the metrics provide the basis for interpreting and comparing the experimental outcomes.

- **5.1 Results Based on Evaluation Metrics**

  - Accuracy-based Results

  - Precision-based Results

  - Recall-based Results

  - F1-score-based Results

  - And so on

- **5.2 Comparative Results**

  - Conventional/baseline vs. proposed method

  - Metric-wise comparison

  - Improvement/reduction in performance measures

- **5.3 Ablation Study (if applicable)**

  - An ablation study in machine learning is an experiment where you remove, disable, or replace specific components (like layers, features, or modules) of a model to measure how much they contribute to its overall performance.

- **5.4 Statistical Analysis**

  - Confidence Interval

  - Effect size

  - t/p value

- **5.5 Discussion of Experimental/Key Findings**

  - Interpretation of the metric-wise results

  - Why the proposed method performs differently

  - Strengths and limitations observed from the experiments

**Recommended structure:**

`Metric-wise Analysis → Comparison → Ablation → Statistical Validation → Findings`

---

## G11. Conclusion
A Conclusion section should briefly summarize the research, the main contribution, the key findings, and possible future work.

**Conclusion contains:**

- **Research objective/problem** – What was addressed?

- **Proposed work/contribution** – What was developed or introduced?

- **Key findings** – What were the major experimental outcomes?

- **Research significance** – What do the findings demonstrate?

- **Future work** – What can be improved or explored next?

**Recommended structure:**

`Conclusion = Objective → Contribution → Key Findings → Significance → Future Work`

**Important:** Avoid introducing new results, new methods, or new references in the Conclusion.

---

## G12. Author Contributions
"Who did what in this research?"

Authors may contribute to:

- **Conceptualization** – Research idea, objectives, and overall research goals

- **Methodology** – Development/design of the methodology or models

- **Software** – Programming, implementation, and code development

- **Validation** – Verification and reproducibility of results

- **Formal Analysis** – Statistical, mathematical, or computational analysis

- **Investigation** – Conducting experiments and data/evidence collection

- **Resources** – Providing materials, datasets, computing resources, etc.

- **Data Curation** – Managing, cleaning, annotating, and maintaining research data

- **Writing – Original Draft** – Preparing the initial manuscript

- **Writing – Review & Editing** – Reviewing, revising, and editing the manuscript

- **Visualization** – Preparing figures, graphs, and other visualizations

- **Supervision** – Research supervision and mentorship

- **Project Administration** – Coordination and management of the research project

- **Funding Acquisition** – Obtaining financial support for the research

---

## G13. Declaration
Declaration part includes:

- Funding

- Conflict of interest

- Data availability

- Code availability

- Ethical approval statement

---

## G14. Acknowledgements
The Acknowledgements section recognizes people or organizations that supported the research but do not qualify for authorship.

Acknowledgements may include:

- **Technical assistance** — laboratory, programming, equipment, or technical support

- **Research assistance** — help with data collection, annotation, experiments, or other research activities

- **Administrative support** — institutional or departmental assistance

- **Language/editing support** — proofreading or language improvement, where appropriate

- **Data/resource providers** — individuals or organizations that provided datasets, materials, or other resources

- **Institutional support** — departments, laboratories, universities, or research centers

- **Funding support** — if the journal does not require funding information in a separate section

- **Special assistance** — individuals who provided valuable advice or feedback but did not meet authorship criteria

---

## G15. References
- Use recent and relevant literature, including contemporary journal articles, conference papers, symposium proceedings, book chapters, and books, where appropriate.

- Ensure that the references are relevant to the research topic and sufficiently up to date.

- Present all references in a consistent and uniform citation style, such as IEEE, throughout the manuscript.

- Avoid unnecessary URLs/link-based references. When a URL is required, provide the access date according to the selected reference style or journal guidelines.

- Include bibliographic information such as author(s), article/chapter title, journal/conference/book title, volume, issue, page range, publication date/year, publisher, DOI, etc., as applicable.

- Follow the reference-formatting requirements of the target journal/conference. The journal's guidelines take precedence over a generic reference format.

- Ensure that every in-text citation appears in the reference list and every listed reference is cited in the manuscript.

- Verify the accuracy of author names, article titles, publication details, DOI, volume, issue, and page numbers before submission.

**One important correction:**

"Clearly mention Vol. number, Issue, PP., date, publisher" is not universally applicable. For example, an IEEE journal reference may contain volume, issue, pages, and year, while a conference paper, book, book chapter, or article with an article number may have a different structure.

---
