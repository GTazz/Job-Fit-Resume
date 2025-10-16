import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Any
from docxtpl import DocxTemplate, RichText


class JsonToCurriculum:
    """Generate resume (DOCX + PDF) using docxtpl and external JSON config.

    Steps executed sequentially in __init__:
      1. load_cv_variables
      2. special_variables
      3. render_template
      4. save_docx
      5. convert_to_pdf
      6. log_summary
    """

    DATA_DIR = Path("data")
    TEMPLATES_DIR = Path("templates")
    OUTPUT_DIR = Path("output")
    
    VARIABLES_FILENAME = Path("cv_variables.json")
    TEMPLATE_FILENAME = Path("template.docx")
    OUTPUT_DOCX_FILENAME = Path("final_cv.docx")
    OUTPUT_PDF_FILENAME = Path("final_cv.pdf")
    
    docx_path: Path = OUTPUT_DIR / OUTPUT_DOCX_FILENAME
    pdf_path: Path = OUTPUT_DIR / OUTPUT_PDF_FILENAME
    config_path: Path = DATA_DIR / VARIABLES_FILENAME
    template_path: Path = TEMPLATES_DIR / TEMPLATE_FILENAME
    
    cv_variables: Dict[str, Any] = {}
    template: DocxTemplate = None

    def __init__(self) -> None:

        # Sequential execution of steps
        self.load_cv_variables()
        self.load_template()
        self.special_variables()
        self.render_template()
        self.save_docx()
        self.convert_to_pdf()
        self.log_summary()

    # ---- Step methods ----
    def load_cv_variables(self) -> None:
        """Load structured CV variables from JSON variables into memory."""
        with self.config_path.open("r", encoding="utf-8") as f:
            self.cv_variables = json.load(f)

    def load_template(self) -> None:
        """Instantiate the Word template used for rendering the resume."""
        self.template = DocxTemplate(str(self.template_path))

    def special_variables(self) -> None:
        """Augment variables (e.g. wrap projectRepo as a clickable hyperlink)."""
        self.cv_variables["projectRepo"] = self._build_hyperlink(self.cv_variables["projectRepo"])

    def render_template(self) -> None:
        """Render the template with the populated context variables."""
        self.template.render(self.cv_variables)

    def save_docx(self) -> None:
        """Write the rendered document to a DOCX file on disk."""
        self.template.save(str(self.docx_path))

    def convert_to_pdf(self) -> None:
        """Convert the generated DOCX to PDF using headless LibreOffice."""
        # Uses LibreOffice headless to convert DOCX -> PDF
        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                str(self.docx_path),  # run in current dir
                "--outdir",
                str(self.OUTPUT_DIR),
            ],
            check=True,
        )

    def log_summary(self) -> None:
        """Print filenames of the produced DOCX and PDF for quick confirmation."""
        print(f"DOCX generated: {self.docx_path.name}")
        print(f"PDF generated:  {self.pdf_path.name}")

    # ---- Helpers ----
    def _build_hyperlink(self, url: str) -> RichText:
        """Return styled RichText hyperlink for insertion into the document."""
        rt = RichText()
        rt.add(
            url,
            url_id=self.template.build_url_id(url),
            underline=True,
            color="#1155cc",
            font="Calibri",
            size=12 * 2,
        )
        return rt


if __name__ == "__main__":

    JsonToCurriculum()
