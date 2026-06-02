from config import client

def cv_tailor(cv_extract, job_description):
    messages = [{
        "role": "user",
        "content": f"""You are a world class recruiter and CV writer.
        
Tailor the following CV to match the job description below.
- Keep all facts accurate — do not invent experience or qualifications
- Reorder and rephrase to highlight relevant skills
- Use keywords from the job description
- Keep the same CV structure and format

CV:
{cv_extract}

Job Description:
{job_description}

Return the full tailored CV only — no commentary."""
    }]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    return response.choices[0].message.content