from agent.logging import log
import requests
from config import AFFINITY_API_KEY, AFFINITY_BASE_URL

HEADERS = {
    'Authorization': f'Basic {AFFINITY_API_KEY}',
    'Content-Type': 'application/json'
}

def get_organization_by_name(name):
    log(f"Searching for '{name}'", tag="INFO")
    url = f"{AFFINITY_BASE_URL}/organizations?term={name}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        organizations = res.json().get("organizations", [])  # Get the organizations list
        if not organizations:  # Check if the list is empty
            log(f"No organizations found for name: {name}", tag="WARNING")
            return None  # Return None if no organizations are found
        org = organizations[0]  # Get the first organization
        log(f"Found organization: {org['name']}", tag="SUCCESS")
        return org
    log(f"No match for {name}", tag="WARNING")
    return None

def get_organization_details(org_id):
    log(f"Getting details for {org_id}", tag="INFO")
    url = f"https://api.affinity.co/v2/companies/{org_id}?fieldTypes=enriched"
    headers = {
        'Authorization': 'Bearer SbqwlV5EKFGOouceK-2fPWNmf_v_WXAphnvioAVz0ks',
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Return the complete JSON received
    else:
        log(f"Failed to get organization details: {response.status_code}", tag="ERROR")
        return None

def get_organization_notes(org_id):
    log(f"Searching for Notes for organization id: '{org_id}'", tag="INFO")
    url = f"{AFFINITY_BASE_URL}/notes?organization_id={org_id}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        notes = res.json().get("notes", [])  # Get the notes array
        content_only = [note['content'] for note in notes]  # Keep only the content key
        log(f"Found {len(content_only)} notes for organization id: {org_id}", tag="SUCCESS")
        return content_only  # Return the list of content only
    log(f"No match for notes for {org_id}", tag="WARNING")
    return None

