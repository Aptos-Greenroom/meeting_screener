from openai import OpenAI
from config import OPENAI_API_KEY
from agent.logging import log

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_company_name(user_input):
    log("Generating markdown summary...", tag="INFO")
    
    # Prompt the model to extract the company name or website from the user input
    prompt = f"""
    You are a company name extractor tool. Given the following user input, extract the company name or website without any prefixes like 'https://', 'www.', or any other unnecessary text. 
    If the mail is a thread of previous emails, extract the company name from the first email and do not pick the company name from the sender's signature also. only from the body text of the most recent email.
    User Input: "{user_input}"

    Please provide the company name or website only as your output and no other text at all.
    """
    
    res = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a company name extractor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    name = res.choices[0].message.content
    log(f"Company name extracted successfully: {name}", tag="SUCCESS")
    return name
