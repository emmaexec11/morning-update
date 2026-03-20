import requests
import json
from datetime import datetime

try:
    # Get top cryptos with basic market data
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 50,
        'page': 1,
        'sparkline': False,
        'price_change_percentage': '1h,24h,7d'
    }
    
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    # Filter for significant moves or key watchlist coins
    watchlist = ['bitcoin', 'ethereum', 'avalanche-2', 'sui', 'solana', 'cardano']
    urgent_signals = []
    
    for coin in data[:20]:  # Check top 20
        name = coin['name']
        symbol = coin['symbol'].upper()
        price = coin['current_price']
        change_1h = coin.get('price_change_percentage_1h', 0) or 0
        change_24h = coin.get('price_change_percentage_24h', 0) or 0
        
        # Flag urgent moves or watchlist coins
        if (abs(change_1h) > 3 or abs(change_24h) > 10 or 
            coin['id'] in watchlist):
            
            if price < 1000:
                price_str = f'${price:.2f}'
            else:
                price_str = f'${price:,.0f}'
            
            change_1h_str = f'{change_1h:+.1f}%' if change_1h else 'N/A'
            change_24h_str = f'{change_24h:+.1f}%' if change_24h else 'N/A'
            
            urgent_signals.append(
                f'{symbol}: {price_str} ({change_1h_str} 1h, {change_24h_str} 24h)'
            )
    
    print('CRYPTO_SUCCESS')
    for signal in urgent_signals[:5]:
        print(signal)
        
except Exception as e:
    print(f'CRYPTO_ERROR: {str(e)}')