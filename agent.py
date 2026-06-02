import json
import requests
from groq import Groq
import PyPDF2
import os
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.environ.get("ADZUNA_APP_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

tools = [
    {
        "type": "function",
        "function": {
            "name": "remote_job_searcher",
            "description": """Search for remote jobs across multiple platforms including 
            LinkedIn, Indeed, Glassdoor, and Upwork. Use this tool when the user asks 
            for job opportunities, freelance work, or career options. Always use this 
            tool for job searches — never answer from memory as job listings change daily.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "job_title": {
                        "type": "string",
                        "description": "The job title or role to search for e.g. 'Data Scientist', 'ML Engineer', 'Python Developer'"
                    },
                    "location": {
                        "type": "string",
                        "description": "Location filter e.g. 'Ghana', 'USA', 'Remote'. Defaults to remote if not specified."
                    },
                    "experience_level": {
                        "type": "string",
                        "enum": ["entry", "mid", "senior", "lead"],
                        "description": "Experience level filter for the job search"
                    },
                    "job_type": {
                        "type": "string",
                        "enum": ["full-time", "part-time", "freelance", "contract", "internship"],
                        "description": "Type of employment"
                    },
                    "salary_min": {
                        "type": "number",
                        "description": "Minimum salary filter in USD"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of job results to return. Default is 5, maximum is 20."
                    }
                },
                "required": ["job_title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cv_reader",
            "description": """This tool is used to read a cv in a pdf format and extract the content into words. """,
            "parameters": {
                "type": "object",
                "properties": {
                    "cv_input": {"type": "string", "description": "This is the file path to the CV pdf"}
                },
                "required": ["cv_input"]
            }
           
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cv_tailor",
            "description": "This tool takes the extracted cv as input and precisely and accurately tailors the cv to suit the job description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cv_extract": {"type": "string", "description": "This is the cv input of the user"},
                    "job_description": {"type": "string", "description": "This describe the skill and character requirements of a job."}
                },
                "required": ["cv_extract", "job_description"]
            }
        }
    }
]

def remote_job_search(job_title, location=None, experience_level=None, job_type=None, salary_min=None, num_results=5):
    try:
        query = job_title
        if experience_level:
            query += f" {experience_level}"
        if job_type:
            query += f" {job_type}"

        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": query,
            "results_per_page": num_results
        }

        
        
        response = requests.get(
            "https://api.adzuna.com/v1/api/jobs/us/search/1",
            params=params,
            timeout=10
        )

        data = response.json()
        jobs = []

        for job in data.get("results", []):
            jobs.append({
                "title":       job.get("title"),
                "company":     job.get("company", {}).get("display_name"),
                "location":    job.get("location", {}).get("display_name"),
                "salary_min":  job.get("salary_min"),
                "salary_max":  job.get("salary_max"),
                "description": job.get("description", "")[:300],
                "apply_url":   job.get("redirect_url")
            })

        return jobs

    except requests.exceptions.ReadTimeout:
        return {"error": "Timeout — server not responding"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error — can't reach server"}
    except Exception as e:
        return {"error": str(e)}

def cv_reader(cv_input):
    try:
        with open(cv_input, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            return text
    except FileNotFoundError:
        return {"error": "File not found"}
    except Exception as e:
        return {"error": str(e)}

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


messages = [] 
client = Groq(api_key=GROQ_API_KEY)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "cool"]:
        print("Glad i could help")
        break
    
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools
    )

    if response.choices[0].finish_reason == "tool_calls":
        tool_call = response.choices[0].message.tool_calls[0]
        tool_name = tool_call.function.name
        tool_inputs = json.loads(tool_call.function.arguments)
        tool_id = tool_call.id

        if tool_name == "remote_job_searcher":
            results = remote_job_search(
                job_title = tool_inputs["job_title"],
                job_type = tool_inputs.get("job_type"),
                location = tool_inputs.get("location"),
                num_results = tool_inputs.get("num_results", 5),
                salary_min = tool_inputs.get("salary_min")
            )

            

        elif tool_name == "cv_reader":
            results = cv_reader(
                cv_input=tool_inputs["cv_input"]
            )

        elif tool_name == "cv_tailor":
            results = cv_tailor(
                cv_extract=tool_inputs["cv_extract"],
                job_description=tool_inputs["job_description"]
            )



        messages.append(response.choices[0].message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_id,
            "content": json.dumps(results)
        })

        final_call = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                tools=tools
            )
        
        reply = final_call.choices[0].message.content
    else:
        reply = response.choices[0].message.content   

    messages.append({"role": "assistant", "content": reply})
   
    print(f"\nAgent: {reply}\n")

