from fpdf import FPDF

def save_to_pdf(cv_text: str, output_path: str = "temp_cv.pdf"):
    """Convert tailored cv into a pdf format to be uploaded"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    for line in cv_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf.output(output_path)
    return output_path