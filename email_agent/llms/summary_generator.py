from openai import OpenAI
from config import OPENAI_API_KEY
from agent.logging import log
from pprint import pprint
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_markdown_summary(data):
    log("Generating markdown summary...", tag="INFO")
    prompt = f"""
    You are preparing a concise, professional briefing on a company for someone about to meet its team. 
    Given a JSON object containing the company’s data, generate a detailed, markdown-formatted summary according to the structure and guidelines below.

   Overall Summary  
    • Provide 2–3 bullet points for each of the five sections listed below. Cover the subsections given in the information and the bullet points need to be information heavy.  
    • This report should be adequate enough for the reader to get an overview of the company and understand what to focus on in the meeting.
    • If information is not available for a subsection, skip it and give relevant information for the parent section from the given data. Don't say that info is not available. 
    Sections to Cover (each as its own Markdown heading):  
    - Founders  
        - Background: education, previous work experience  
        - Reference-check highlights  
    - Market  
        - Total Addressable Market (TAM)  
        - Key competitors  
        - Principal pain points in the space  
        - Summary of thesis discussions  
        - Ideal customer persona  
    - Product  
        - Core offering and features  
        - Differentiators vs. competitors  
    - Business & Traction  
        - Recent growth metrics and milestones  
        - Notable customer logos or key accounts  
        - Retention rates and other SaaS KPIs  
        - 6–12-month forecast  
    - Funding  
        - Round history and amounts  
        - Lead investors  
    - Summary of notes 
        - summary of the given notes in data and previous interactions recorded
    Do not say information is not available at any point. Proceed with what information is available.
    Utilize all information available in the notes as well to generate the information above.
    Formatting & Style Guidelines:  
    - Make sure the markdown is very well formatted with the correct symbols for links (like this [link](https://www.google.com) .), headings, bullets etc. Give correct spacing before and after links as well. 
    - Use bullet points throughout—avoid long paragraphs.  
    - Bold any major issues or opportunities.  
    - Maintain a professional but friendly tone.  
    - Keep the entire summary to 1–2 pages (approximately 500–800 words).  

    Data: {data}
    """
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a data summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    summary = res.choices[0].message.content
    pprint(summary)
    log("Markdown summary generated successfully.", tag="SUCCESS")
    return summary
