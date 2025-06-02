# How Zenodo and GitHub Address FAIR and RDM Requirements in a Horizon Europe Grant Context

---

## Actionable Items for FAIR Principles (with Zenodo/GitHub Solutions)

### **Findable**

- **F1: Assign globally unique and persistent identifiers (PIDs)**
  - **Action:** Assign DOIs to all datasets, software, and research outputs.
  - **Solution:** Zenodo assigns DOIs to archived GitHub releases, ensuring persistent identification.
  - **Action:** Use consistent, resolvable identifiers for files/directories.
  - **Solution:** GitHub provides stable URLs; use consistent naming conventions.

- **F2: Describe data with rich metadata**
  - **Action:** Define a comprehensive metadata schema.
  - **Solution:** GitHub manages metadata (e.g., `.zenodo.json`); Zenodo stores and makes it discoverable.
  - **Action:** Store metadata files (YAML, JSON) alongside data in GitHub.

- **F3: Metadata include the identifier of the data they describe**
  - **Action:** Include DOI or persistent identifier in metadata files.
  - **Solution:** Zenodo DOI can be referenced in GitHub metadata.

- **F4: (Meta)data are registered or indexed in a searchable resource**
  - **Action:** Deposit data/metadata in a searchable resource.
  - **Solution:** Zenodo is the searchable resource; GitHub enables transfer to Zenodo.

---

### **Accessible**

- **A1: (Meta)data are retrievable by their identifier using a standardized protocol**
  - **Action:** Ensure data is accessible via DOIs and standard web protocols (e.g., HTTP).
  - **Solution:** Zenodo ensures accessibility; GitHub stores documentation (e.g., README) on access procedures.

- **A2: Metadata are accessible even when the data are no longer available**
  - **Action:** Design metadata strategy for long-term preservation.
  - **Solution:** Zenodo preserves metadata for the long term.

---

### **Interoperable**

- **I1: (Meta)data use a formal, accessible, shared, and broadly applicable language**
  - **Action:** Choose standard data formats and controlled vocabularies.
  - **Solution:** GitHub stores/document formats; Zenodo supports many formats.
  - **Action:** Use community standards and ontologies.
  - **Solution:** Document standards in GitHub; structure metadata accordingly.

- **I2: (Meta)data use vocabularies that follow FAIR principles**
  - **Action:** Select FAIR vocabularies.
  - **Solution:** Use established metadata standards and controlled vocabularies.

- **I3: (Meta)data include qualified references to other (meta)data**
  - **Action:** Link to related datasets, publications, and resources.
  - **Solution:** Include links in metadata and documentation; Zenodo preserves these.

---

### **Reusable**

- **R1: (Meta)data are richly described with accurate and relevant attributes**
  - **Action:** Provide detailed data descriptions.
  - **Solution:** Use metadata files and READMEs in GitHub; Zenodo displays this info.

- **R2: (Meta)data are released with a clear and accessible data usage license**
  - **Action:** Define licenses for data and metadata.
  - **Solution:** Specify licenses in GitHub; Zenodo transfers this info.

- **R3: (Meta)data meet domain-relevant community standards**
  - **Action:** Adhere to community metadata/data format standards.
  - **Solution:** Version control in GitHub; Zenodo preserves data per standards.

---

## Actionable Items for Research Data Management (RDM) (with Zenodo/GitHub Solutions)

### **Data Management Planning**
- **Action:** Create a comprehensive Data Management Plan (DMP).
- **Solution:** Zenodo/GitHub support DMP implementation via storage, versioning, and publication.

### **Repository Structure**
- **Action:** Establish a clear, consistent repository structure.
- **Solution:** Organize files/directories logically in GitHub; use descriptive names and README files.

### **Metadata Management**
- **Action:** Implement a system for creating, storing, and maintaining metadata.
- **Solution:** Version-control metadata in GitHub; publish/preserve in Zenodo.
- **Action:** Use consistent metadata schema and format (JSON, YAML).
- **Solution:** Store metadata alongside data in GitHub.

### **Data Integrity**
- **Action:** Implement data integrity checks (e.g., checksums, file format validation).
- **Solution:** Automate checks with GitHub Actions; document procedures in GitHub.

### **Versioning**
- **Action:** Use Git tags/releases for versioning.
- **Solution:** GitHub provides versioning; Zenodo archives releases.
- **Action:** Document versioning scheme in GitHub.

### **Documentation**
- **Action:** Create comprehensive README files.
- **Solution:** Store documentation on workflow, metadata standards, file naming, and access in GitHub.

### **Training and Support**
- **Action:** Provide training/support on data management best practices.
- **Solution:** Host training materials or links in GitHub.

### **Collaboration**
- **Action:** Establish clear roles/responsibilities for data management.
- **Solution:** Use GitHub tools for roles, permissions, collaboration, and sharing.

### **Preservation**
- **Action:** Use a repository for long-term preservation.
- **Solution:** Zenodo is the preservation repository; GitHub helps organize data for long-term access.

### **Backups**
- **Action:** Implement a backup strategy.
- **Solution:** GitHub and Zenodo provide some backup; document additional backup strategies in GitHub.