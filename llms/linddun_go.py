import json
import google.generativeai as genai
from openai import OpenAI
from misc.utils import (
    match_number_color,
    match_letter,
)
from llms.prompts import (
    LINDDUN_GO_SYSTEM_PROMPT
)

# Function to convert JSON to Markdown for display.
def linddun_go_gen_markdown(present_threats):
    markdown_output = "## Threats identified with LINDDUN Go\n\n"

    # Start the markdown table with headers
    markdown_output += "| Threat Name | Threat description | Detection reason |\n"
    markdown_output += "|-------------|--------------------|------------------|\n"

    # Fill the table rows with the threat model data
    for threat in present_threats:
        color = match_number_color(threat["threat_type"])
        color_html = f"<p style='background-color:{color};color:#ffffff;'>"
        markdown_output += f"| {color_html}{match_letter(threat['threat_type'])} - {threat['threat_title']}</p> | {threat['threat_description']} | {threat['reason']} |\n"


    return markdown_output


def questions_threats(questions_file="misc/questions.txt", threats_file="misc/threats.txt"):
    with open(questions_file, 'r') as questions, open(threats_file, 'r') as threats:
        questions_blocks = questions.read().split('\n\n')
        threats_blocks = threats.read().split('\n\n')

    joined_info = []
    for i, question_block in enumerate(questions_blocks):
        threat = threats_blocks[i] if i < len(threats_blocks) else None  # Get corresponding threat or None
        type, title, description = threat.split('\n')
        joined_info.extend([(question_block.strip(), title.strip(), description.strip(), int(type.strip()))])
    return joined_info



def get_linddun_go(api_key, model_name, inputs):
    client = OpenAI(api_key=api_key)
    questions_threats_list = questions_threats()
    present_threats = []

    for question, title, description, type in questions_threats_list:
        response = client.chat.completions.create(
            model=model_name,
            response_format={"type": "json_object"},
            temperature=0.01,
            messages=[
                {
                    "role": "system",
                    "content": LINDDUN_GO_SYSTEM_PROMPT,
                },
                {"role": "user", "content": 
                 f"""
'''
APPLICATION TYPE: {inputs["app_type"]}
AUTHENTICATION METHODS: {inputs["authentication"]}
APPLICATION DESCRIPTION: {inputs["app_description"]}
DATABASE_SCHEMA: {inputs["database"]}
DATA POLICY: {inputs["data_policy"]}
QUESTIONS: {question}
THREAT_TITLE: {title}
THREAT_DESCRIPTION: {description}
'''
                """
                },
            ],
            max_tokens=4096,
        )
        # Convert the JSON string in the 'content' field to a Python dictionary
        response_content = json.loads(response.choices[0].message.content)
        response_content["question"] = question
        response_content["threat_title"] = title
        response_content["threat_description"] = description
        response_content["threat_type"] = type
        #print(response_content)
        if response_content["reply"]:
            present_threats.append(response_content)

    return present_threats
