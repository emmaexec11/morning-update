#!/usr/bin/env python3
"""
Quick OAuth2 token helper for Google Calendar + Tasks.
Starts a local server, opens the consent screen, catches the redirect,
and exchanges the code for tokens.
"""

import http.server
import urllib.parse
import webbrowser
import json
import urllib.request
import ssl
import sys

CLIENT_ID = "310221293117-eiv0ouknutm3mjchgio5ceopf9hvbnr8.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8080"
SCOPES = "https://www.googleapis.com/auth/tasks.readonly https://www.googleapis.com/auth/calendar.readonly"

auth_url = (
    "https://accounts.google.com/o/oauth2/v2/auth?"
    f"client_id={CLIENT_ID}&"
    f"redirect_uri={urllib.parse.quote(REDIRECT_URI)}&"
    "response_type=code&"
    f"scope={urllib.parse.quote(SCOPES)}&"
    "access_type=offline&"
    "prompt=consent"
)

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if "code" not in params:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No authorization code received.")
            return

        code = params["code"][0]
        print(f"\n[+] Authorization code received: {code[:20]}...")

        # Exchange code for tokens
        token_data = urllib.parse.urlencode({
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }).encode()

        req = urllib.request.Request(
            "https://oauth2.googleapis.com/token",
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        ctx = ssl.create_default_context()
        try:
            resp = urllib.request.urlopen(req, context=ctx)
            result = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            print(f"[!] Token exchange failed: {body}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Token exchange failed: {body}".encode())
            return

        refresh_token = result.get("refresh_token", "")
        access_token = result.get("access_token", "")

        print("\n" + "=" * 60)
        print("SUCCESS! Tokens obtained.")
        print("=" * 60)
        print(f"\nRefresh Token:\n{refresh_token}")
        print(f"\nAccess Token (first 40 chars):\n{access_token[:40]}...")
        print(f"\nExpires in: {result.get('expires_in')} seconds")
        print("=" * 60)

        # Write tokens to a file for easy retrieval
        with open("new-tokens.json", "w") as f:
            json.dump({
                "refresh_token": refresh_token,
                "access_token": access_token,
                "expires_in": result.get("expires_in"),
                "token_type": result.get("token_type"),
            }, f, indent=2)
        print("\nTokens saved to new-tokens.json")

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(f"""
        <html>
        <body style="font-family: system-ui; background: #0f172a; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
        <div style="text-align: center; max-width: 500px;">
            <h1>✅ Authentication Successful!</h1>
            <p>Refresh token obtained. You can close this tab.</p>
            <p style="background: rgba(0,0,0,0.5); padding: 1rem; border-radius: 8px; font-family: monospace; word-break: break-all; font-size: 0.8rem;">{refresh_token}</p>
        </div>
        </body>
        </html>
        """.encode())

        # Shut down after handling
        import threading
        threading.Thread(target=self.server.shutdown).start()

    def log_message(self, format, *args):
        pass  # Suppress default logging


if __name__ == "__main__":
    print("=" * 60)
    print("Google OAuth2 Token Helper")
    print("=" * 60)
    print(f"\nStarting local server on {REDIRECT_URI}")
    print("Opening browser for Google sign-in...\n")
    print("Sign in with Devon's account (devondoherty07@gmail.com)")
    print("and approve Calendar + Tasks access.\n")

    server = http.server.HTTPServer(("localhost", 8080), Handler)
    webbrowser.open(auth_url)
    print("Waiting for authorization callback...")
    server.serve_forever()
    print("\nDone! Check new-tokens.json for the tokens.")
