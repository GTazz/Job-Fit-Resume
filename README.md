# Job-Fit-Resume

Generate a tailored resume (DOCX + PDF) from a Word template (`template.docx`) and a structured JSON data file (`cv_variables.json`). The script fills the template using **docxtpl (Jinja2)** and converts the rendered DOCX to PDF via **LibreOffice (headless mode)**.

> Personal tooling / WIP. Not production‑hardened.

## Available Variables (Current JSON Keys)

| Key                     | Purpose                                       |
| ----------------------- | --------------------------------------------- |
| `mainStack`             | Primary technologies / specialization summary |
| `projectName`           | project name                                  |
| `projectDescription`    | Short project summary                         |
| `projectRepo`           | URL to project repo (auto‑hyperlinked)        |
| `experienceDescription` | Short old job experience                      |
| `relevantStack`         | Supporting / complementary tech list          |
| `collegeSkills`         | Academic skills                               |
| `courseSkills`          | Technical course skills                       |

## Next Improvements

- Use AI for variables text generation
- Support multiple resume variants (targeted roles)
- Introduce proper logging & error handling

## License

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)

