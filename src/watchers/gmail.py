import os
import time
import base64
from tenacity import retry, wait_fixed, stop_after_attempt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from ..foundation.logger import setup_logger
from ..foundation.config import settings

logger = setup_logger("gmail_sentinel")

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_PATH = settings.VAULT_PATH / "System" / "token.json"
CREDS_PATH = settings.VAULT_PATH / "System" / "credentials.json"

class GmailSentinel:
    def __init__(self):
        self.service = None

    def authenticate(self):
        """
        Handles the complex OAuth2 dance.
        """
        creds = None
        
        # 1. Load existing token
        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
            
        # 2. Refresh or Login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("🔄 Refreshing Expired Google Token...")
                creds.refresh(Request())
            else:
                if not CREDS_PATH.exists():
                    logger.warning("⚠️ No credentials.json found. Gmail Sentinel is DISABLED.")
                    return False
                    
                logger.info("👤 Initiating New Google Login Flow...")
                flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_PATH), SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the new token
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
                
        self.service = build('gmail', 'v1', credentials=creds)
        logger.info("✅ Gmail Authenticated")
        return True

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
    def check_for_mail(self):
        """
        Polls for UNREAD messages in INBOX.
        """
        if not self.service: return

        # Query
        results = self.service.users().messages().list(
            userId='me', q="is:unread label:INBOX"
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            return

        logger.info(f"📧 Found {len(messages)} unread emails.")
        
        for msg in messages:
            self.process_message(msg['id'])

    def process_message(self, msg_id):
        # Fetch full details
        msg = self.service.users().messages().get(userId='me', id=msg_id).execute()
        
        # Extract headers
        payload = msg['payload']
        headers = {h['name']: h['value'] for h in payload['headers']}
        
        subject = headers.get('Subject', '(No Subject)')
        sender = headers.get('From', 'Unknown')
        snippet = msg.get('snippet', '')

        # Normalize to Markdown
        content = f"""# 📧 New Email Detected
**From:** {sender}
**Subject:** {subject}
**Date:** {headers.get('Date')}

## Snippet
{snippet}

## Instructions
@Claude: Analyze this email. If it requires a reply, draft one in /20_Plans.
"""
        # Save to Inbox (Triggers File Watcher)
        filename = f"EMAIL_{msg_id}.md"
        path = settings.get_inbox_path() / filename
        path.write_text(content, encoding='utf-8')
        
        # Mark as Read (So we don't process it forever)
        self.service.users().messages().modify(
            userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}
        ).execute()
        
        logger.info(f"📥 Ingested: {filename}")

def run_gmail_loop():
    sentinel = GmailSentinel()
    if not sentinel.authenticate():
        return

    logger.info("📡 Gmail Sentinel Polling...")
    try:
        while True:
            sentinel.check_for_mail()
            time.sleep(settings.POLL_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Gmail Sentinel stopping...")

if __name__ == "__main__":
    run_gmail_loop()
