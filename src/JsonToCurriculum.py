import json
import subprocess
from typing import Dict, Any
from docxtpl import DocxTemplate, RichText
from .__config import (
    CV_VARIABLES_JSON,
    TEMPLATE_DOCX,
    FINAL_CV_DOCX,
    FINAL_CV_PDF,
    OUTPUT_DIR,
    logging
)


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

    cv_variables: Dict[str, Any] = {}
    template: DocxTemplate = None

    def __init__(self, cv_variables: dict, debug: bool = False) -> None:
        self.cv_variables = cv_variables

        # Sequential execution of steps
        # self.load_cv_variables()
        self.load_template()
        self.special_variables()
        self.render_template()
        self.save_docx()
        self.convert_to_pdf()
        self.log_summary()

    # ---- Step methods ----
    def load_cv_variables(self) -> None:
        """Load structured CV variables from JSON variables into memory."""
        with CV_VARIABLES_JSON.open("r", encoding="utf-8") as f:
            self.cv_variables = json.load(f)

    def load_template(self) -> None:
        """Instantiate the Word template used for rendering the resume."""
        self.template = DocxTemplate(str(TEMPLATE_DOCX))

    def special_variables(self) -> None:
        """Augment variables (e.g. wrap projectRepo as a clickable hyperlink)."""
        self.cv_variables["projectRepo"] = self._build_hyperlink(self.cv_variables["projectRepo"])

    def render_template(self) -> None:
        """Render the template with the populated context variables."""
        self.template.render(self.cv_variables)

    def save_docx(self) -> None:
        """Write the rendered document to a DOCX file on disk."""
        self.template.save(str(FINAL_CV_DOCX))

    def convert_to_pdf(self) -> None:
        """Convert the generated DOCX to PDF using headless LibreOffice."""
        # Uses LibreOffice headless to convert DOCX -> PDF
        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                str(FINAL_CV_DOCX),  # run in current dir
                "--outdir",
                str(OUTPUT_DIR),
            ],
            check=True,
        )

    def log_summary(self) -> None:
        """Print filenames of the produced DOCX and PDF for quick confirmation."""
        logging.info(f"DOCX generated: {FINAL_CV_DOCX.name}")
        logging.info(f"PDF generated:  {FINAL_CV_PDF.name}")

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
    # Testing
    JsonToCurriculum()
