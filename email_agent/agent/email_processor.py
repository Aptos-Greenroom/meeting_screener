import email
from llms.company_name_extractor import extract_company_name
from llms.summary_generator import generate_markdown_summary
from agent.tools.affinity_tool import get_organization_by_name, get_organization_details, get_organization_notes
from agent.tools.pdf_generator import convert_markdown_to_pdf
from agent.tools.email_tool import send_email_with_attachment, send_error_email
from agent.logging import log

def process_email(uid, mail):
    log("Starting email processing agent...", tag="INFO")
    log(f"Processing UID: {uid.decode()}", tag="INFO")
    result, data = mail.uid('fetch', uid, '(RFC822)')
    if result != 'OK':
        log(f"Failed to fetch UID {uid}", tag="ERROR")
        return

    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    sender = email.utils.parseaddr(msg['From'])[1]
    subject = msg['Subject']
    log(f"Email from: {sender} | Subject: {subject}", tag="INFO")

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = msg.get_payload(decode=True).decode()
    company_name = extract_company_name(body)   
    org = get_organization_by_name(company_name)
    if not org:
        log("Org not found.", tag="WARNING")
        send_error_email(sender, f"Org not found for {company_name}", f"Org not found for {company_name}")
        return

    details = get_organization_details(org['id'])
    if details is None:
        details = {}
    notes = get_organization_notes(org['id'])
    if notes is not None:
        details['notes'] = notes
    else:
        log(f"No notes found for organization id: {org['id']}", tag="WARNING")
    summary = generate_markdown_summary(details)

    filename = f"summaries/{company_name.replace(' ', '_')}_summary.pdf"
    pdf_path = convert_markdown_to_pdf(summary, filename)
    send_email_with_attachment(sender, f"Summary for {company_name}", "Find attached summary.", pdf_path)
