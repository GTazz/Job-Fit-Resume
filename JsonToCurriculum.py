import json
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

    VARIABLES_FILENAME = "cv_variables.json"
    TEMPLATE_FILENAME = "template.docx"
    OUTPUT_DOCX = "final_cv.docx"  # keeping original filenames
    OUTPUT_PDF = "final_cv.pdf"
    base_dir: Path = Path(__file__).parent
    docx_path: Path = base_dir / OUTPUT_DOCX
    pdf_path: Path = base_dir / OUTPUT_PDF
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
        config_path = self.base_dir / self.VARIABLES_FILENAME
        with config_path.open("r", encoding="utf-8") as f:
            self.cv_variables = json.load(f)

    def load_template(self) -> None:
        """Instantiate the Word template used for rendering the resume."""
        template_path = self.base_dir / self.TEMPLATE_FILENAME
        self.template = DocxTemplate(str(template_path))

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
                str(self.docx_path.name),  # run in current dir
                "--outdir",
                ".",
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
