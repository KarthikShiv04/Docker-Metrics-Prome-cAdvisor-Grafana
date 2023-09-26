import requests

# Define your SonarQube server URL and authentication token
SONARQUBE_URL = 'http://3.6.87.81:9000'
SONARQUBE_TOKEN = 'sqa_3b1cb7e9555bcd73a97f9c8b16a52fe6849c5aa9'

# Define your ChatGPT API endpoint and API key
CHATGPT_API_URL = 'https://api.openai.com/v1/chat/completions'
CHATGPT_API_KEY = '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'

# Function to fetch SonarQube issues
def fetch_sonarqube_issues():
    issues_url = f'{SONARQUBE_URL}/api/issues/search'
    params = {
        'resolved': 'false',  # Get unresolved issues
        'ps': 100,  # Number of issues to retrieve (adjust as needed)
    }
    headers = {
        'Authorization': f'Bearer {SONARQUBE_TOKEN}',
    }

    try:
        response = requests.get(issues_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses (e.g., 404, 500)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SonarQube issues: {e}")
        return None

# Function to generate code review comments using ChatGPT
def generate_code_review_comments(sonarqube_issues):
    if sonarqube_issues is None:
        return []  # Return an empty list if there was an issue with fetching SonarQube issues

    comments = []
    for issue in sonarqube_issues['issues']:
        # Extract relevant information from SonarQube issue
        issue_key = issue['key']
        issue_message = issue['message']

        # Prepare a message to send to ChatGPT
        chatgpt_input = f"SonarQube issue {issue_key}: {issue_message}"
        
        # Send the message to ChatGPT for review
        chatgpt_response = send_message_to_chatgpt(chatgpt_input)

        # Extract ChatGPT's response with suggested fixes
        suggested_fixes = chatgpt_response.get('choices', [{'text': 'No suggested fixes available.'}])[0]['text']
        
        # Format the comment with the issue key, message, and suggested fixes
        comment = f"SonarQube issue {issue_key}: {issue_message}\n\nSuggested fixes:\n{suggested_fixes}"
        comments.append(comment)

    return comments

# Function to send a message to ChatGPT for review
def send_message_to_chatgpt(message):
    headers = {
        'Authorization': f'Bearer {CHATGPT_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'}, {'role': 'user', 'content': message}]
    }

    try:
        response = requests.post(CHATGPT_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to ChatGPT: {e}")
        return {'choices': [{'text': 'Error communicating with ChatGPT.'}]}

if __name__ == "__main__":
    sonarqube_issues = fetch_sonarqube_issues()
    code_review_comments = generate_code_review_comments(sonarqube_issues)

    # Print or process the code review comments as needed
    for comment in code_review_comments:
        print(comment)
