from fpdf import FPDF

def save_to_pdf(cv_text: str, output_path: str = "temp_cv.pdf"):
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    for line in cv_text.split("\n"):
        clean_line = line.encode("latin-1", errors="replace").decode("latin-1").strip()
        if clean_line == "":
            pdf.ln(5)
        else:
            pdf.set_x(15)  # force every line to start from left margin
            pdf.cell(0, 8, clean_line, ln=True)

    pdf.output(output_path)
    return output_path