// Using native fetch API in Node.js 18+

async function updateDashboard() {
  const today = new Date();
  const dateStr = today.toLocaleDateString('en-US', { 
    weekday: 'long', 
    month: 'long', 
    day: 'numeric', 
    year: 'numeric' 
  });
  
  const prompt = `Update the morning dashboard HTML file to show today's date (${dateStr}). Make these surgical edits:
1. Update the date display to: ${dateStr}
2. Keep everything else exactly the same
3. Read the current file first
4. Make minimal changes only

File location: /Users/emmalindsay/.openclaw/workspace/projects/morning-update/index.html`;

  try {
    const response = await fetch('http://127.0.0.1:3456/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.1
      })
    });
    
    const result = await response.json();
    console.log('Dashboard update initiated via HTTP API');
    console.log('Response:', result.choices?.[0]?.message?.content?.substring(0, 200) + '...');
  } catch (error) {
    console.error('Error:', error.message);
  }
}

updateDashboard();