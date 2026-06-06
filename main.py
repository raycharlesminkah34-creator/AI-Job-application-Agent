import json
from config import client
from schema.tool_schema import tools
from tools.job_search import remote_job_search
from tools.cv_reader import cv_reader
from tools.cv_tailor import cv_tailor
from tools.apply import auto_apply
from tools.pdf_save import save_to_pdf



messages = []

print("Job Application Agent ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Glad I could help. Good luck with your applications!")
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
                job_title=tool_inputs["job_title"],
                job_type=tool_inputs.get("job_type"),
                location=tool_inputs.get("location"),
                num_results=tool_inputs.get("num_results", 5),
                salary_min=tool_inputs.get("salary_min")
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


        elif tool_name == "auto_apply":
            results = auto_apply(
                job_url=tool_inputs["job_url"],
                tailored_cv=tool_inputs["tailored_cv"],
                user_info={
                    "name": tool_inputs["user_name"],
                    "email": tool_inputs["user_email"],
                    "phone": tool_inputs.get("user_phone", "")
                }
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