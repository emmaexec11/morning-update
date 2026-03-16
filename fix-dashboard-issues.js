// Fix request for Devon's dashboard
// Last updated: 2026-03-04
const fixes = `
RESOLVED:
1. Google Tasks/Calendar: Refresh token expired 2026-02-28 (invalid_grant error)
   - Root cause: Google OAuth refresh token was revoked or expired
   - Hardcoded fallback token removed from index.html (was leaking credentials)
   - Dashboard now shows clear re-auth instructions instead of cryptic errors
   - FIX: User must click 🔐 Auth button → complete Google sign-in → paste auth code
   - New refresh token will be stored in localStorage for future sessions

STILL OPEN:
2. Sticky Notes: Not loading saved notes on page refresh
`;

console.log(fixes);

// Use Claude Code HTTP API to fix
fetch('http://127.0.0.1:3456/v1/chat/completions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    messages: [{
      role: 'user',
      content: `Fix the morning dashboard at /Users/emmalindsay/.openclaw/workspace/projects/morning-update/index.html:

1. GOOGLE TASKS FIX: The OAuth token expired (showing "Token refresh failed:400"). Add a proper error message with instructions to re-authenticate by clicking the header to go to the online version where they can refresh the token.

2. STICKY NOTES FIX: The notes save to localStorage but don't load on page refresh. Find the sticky notes initialization code and add a loadStickyNotes() function that runs on page load to restore saved notes.

3. IMPORTANT: Make ONLY these surgical changes. Do not modify any other parts of the file.`
    }]
  })
})
.then(res => res.json())
.then(data => console.log('Claude Code response:', data))
.catch(err => console.error('Error:', err));
