from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet

import os


REPORT_FOLDER = "reports"

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)



def generate_pdf(filename, language, result):


    pdf_path = os.path.join(
        REPORT_FOLDER,
        filename + ".pdf"
    )


    styles = getSampleStyleSheet()


    doc = SimpleDocTemplate(
        pdf_path
    )


    story = []



    # Title

    story.append(
        Paragraph(
            "<b>AI Code Reviewer Report</b>",
            styles["Heading1"]
        )
    )


    story.append(
        Spacer(1, 12)
    )



    # Details


    story.append(
        Paragraph(
            f"<b>File:</b> {filename}",
            styles["BodyText"]
        )
    )


    story.append(
        Paragraph(
            f"<b>Language:</b> {language}",
            styles["BodyText"]
        )
    )


    story.append(
        Paragraph(
            f"<b>Score:</b> {result.get('score',0)}",
            styles["BodyText"]
        )
    )


    story.append(
        Paragraph(
            f"<b>Bugs Found:</b> {result.get('bugs',0)}",
            styles["BodyText"]
        )
    )


    story.append(
        Paragraph(
            f"<b>Suggestions:</b> {result.get('suggestions',0)}",
            styles["BodyText"]
        )
    )



    story.append(
        Spacer(1, 12)
    )



    # AI Review


    story.append(
        Paragraph(
            "<b>AI Review</b>",
            styles["Heading2"]
        )
    )


    story.append(
        Paragraph(
            result.get(
                "review",
                "No Review"
            ),
            styles["BodyText"]
        )
    )



    story.append(
        Spacer(1, 12)
    )



    # Original Code


    story.append(
        Paragraph(
            "<b>Original Code</b>",
            styles["Heading2"]
        )
    )


    story.append(
        Preformatted(
            result.get(
                "original_code",
                "Not Available"
            ),
            styles["Code"]
        )
    )



    story.append(
        Spacer(1, 12)
    )



    # Corrected Code


    story.append(
        Paragraph(
            "<b>AI Corrected Code</b>",
            styles["Heading2"]
        )
    )


    story.append(
        Preformatted(
            result.get(
                "corrected_code",
                "Not Available"
            ),
            styles["Code"]
        )
    )



    doc.build(
        story
    )


    return pdf_path