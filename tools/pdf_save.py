from fpdf import FPDF

def save_to_pdf(cv_text: str, output_path: str = "temp_cv.pdf"):
    """Convert tailored cv into a pdf format to be uploaded"""
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    for line in cv_text.split("\n"):
        clean_line = line.encode("latin-1", errors="replace").decode("latin-1")
        if clean_line.strip() == "":
            pdf.ln(8)  # empty line — just add spacing
        else:
            pdf.multi_cell(0, 8, clean_line)
   
    pdf.output(output_path)
    return output_path