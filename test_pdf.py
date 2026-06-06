# test_pdf.py
from tools.pdf_save import save_to_pdf

test_cv = """John Doe
Software Engineer

Experience:
- Built a job application agent using Python and Groq
- Developed REST APIs with FastAPI

Education:
BSc Computer Science, University of Ghana, 2023

Skills:
Python, SQL, Machine Learning, Playwright
"""

result = save_to_pdf(test_cv)
print(f"PDF saved to: {result}")