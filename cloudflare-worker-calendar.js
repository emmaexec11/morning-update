// Cloudflare Worker for Google Calendar API
// Deploy this as a separate Worker to keep your API keys secure

export default {
  async fetch(request, env) {
    // Enable CORS for your dashboard domain
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*', // In production, use your specific domain
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Handle preflight requests
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // Your Google Calendar API key from environment variables
      const API_KEY = env.GOOGLE_CALENDAR_API_KEY;
      
      // Your calendar ID (usually your email address)
      const CALENDAR_ID = env.GOOGLE_CALENDAR_ID || 'primary';
      
      // Get today's events
      const now = new Date();
      const timeMin = now.toISOString();
      const timeMax = new Date(now.getTime() + 24 * 60 * 60 * 1000).toISOString();
      
      const calendarUrl = `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(CALENDAR_ID)}/events?` +
        `key=${API_KEY}&timeMin=${timeMin}&timeMax=${timeMax}&singleEvents=true&orderBy=startTime&maxResults=10`;

      const response = await fetch(calendarUrl);
      
      if (!response.ok) {
        throw new Error(`Calendar API error: ${response.status}`);
      }

      const data = await response.json();
      
      // Filter out routine events (optional - customize based on your needs)
      const filteredEvents = data.items?.filter(event => {
        const summary = event.summary?.toLowerCase() || '';
        const routineEvents = ['morning routine', 'power hour', 'workout', 'lunch', 'dinner'];
        return !routineEvents.some(routine => summary.includes(routine));
      }) || [];

      // Return filtered events
      return new Response(JSON.stringify({
        events: filteredEvents.slice(0, 5), // Limit to 5 events
        count: filteredEvents.length
      }), {
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders
        }
      });

    } catch (error) {
      return new Response(JSON.stringify({
        error: 'Failed to fetch calendar events',
        message: error.message
      }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders
        }
      });
    }
  }
};

/* 
DEPLOYMENT INSTRUCTIONS:

1. In Cloudflare Dashboard → Workers & Pages → Create → Worker
2. Name it: morning-update-calendar  
3. Paste this code
4. Go to Settings → Variables → Add:
   - GOOGLE_CALENDAR_API_KEY: your_google_api_key
   - GOOGLE_CALENDAR_ID: your_email@gmail.com (or 'primary')
5. Deploy

Your dashboard will call: https://morning-update-calendar.YOUR-SUBDOMAIN.workers.dev
*/