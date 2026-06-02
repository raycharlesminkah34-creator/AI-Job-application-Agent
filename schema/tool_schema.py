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
            "description": "Reads a CV from a PDF file and extracts the full text content. Use this tool when the user wants to load or analyse their CV.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cv_input": {
                        "type": "string",
                        "description": "The file path to the CV PDF e.g. 'C:/Users/USER/Documents/my_cv.pdf'"
                    }
                },
                "required": ["cv_input"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cv_tailor",
            "description": "Tailors a CV to match a specific job description. Use this when the user wants to customise their CV for a job.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cv_extract": {
                        "type": "string",
                        "description": "The extracted CV text from the cv_reader tool"
                    },
                    "job_description": {
                        "type": "string",
                        "description": "The full job description text including requirements and responsibilities"
                    }
                },
                "required": ["cv_extract", "job_description"]
            }
        }
    }
]