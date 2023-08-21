import requests
import talib
import numpy as np
import time
import hmac

# Paramètres de l'API Bybit
API_KEY = 'VOTRE_API_KEY'
API_SECRET = 'VOTRE_API_SECRET'
BASE_URL = 'https://api.bybit.com'

# Paramètres des indicateurs
emaLength = 20
rsiLength = 14
rsiOverbought = 70
rsiOversold = 30
macdShort = 12
macdLong = 26
macdSignal = 9

# Paramètres Telegram
TELEGRAM_TOKEN = 'VOTRE_TOKEN_TELEGRAM'
CHAT_ID = 'VOTRE_CHAT_ID'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    return response.json()

# Génération de la signature pour l'API Bybit
def generate_signature(secret, params):
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    encoded_params = '&'.join([f"{k}={v}" for k, v in sorted_params])
    return hmac.new(bytes(secret, 'latin-1'), msg=bytes(encoded_params, 'latin-1'), digestmod='sha256').hexdigest()

# Définir le levier à x20
def set_leverage():
    data = {
        "symbol": "BTCUSDTPERP",
        "leverage": 20,
        "timestamp": int(time.time() * 1000)
    }
    data['sign'] = generate_signature(API_SECRET, data)
    response = requests.post(f"{BASE_URL}/private/linear/position/set-leverage", headers=headers, data=data)
    return response.json()

# Obtenir le solde du portefeuille
def get_wallet_balance():
    params = {
        "coin": "USDT",
        "timestamp": int(time.time() * 1000)
    }
    params['sign'] = generate_signature(API_SECRET, params)
    response = requests.get(f"{BASE_URL}/private/linear/wallet/balance", headers=headers, params=params)
    balance = float(response.json()['result']['USDT']['available_balance'])
    return balance

# Récupérer les données historiques avec un timeframe de 1 heure
response = requests.get(f"{BASE_URL}/public/linear/kline?symbol=BTCUSDTPERP&interval=1h&limit=500")
data = response.json()["result"]
closes = np.array([item['close'] for item in data], dtype=float)

# Calcul de l'EMA
emaValue = talib.EMA(closes, timeperiod=emaLength)

# Calcul du RSI
rsiValue = talib.RSI(closes, timeperiod=rsiLength)

# Calcul du MACD
macdLine, signalLine, _ = talib.MACD(closes, fastperiod=macdShort, slowperiod=macdLong, signalperiod=macdSignal)

# Conditions d'entrée
longCondition = closes[-1] > emaValue[-1] and closes[-2] <= emaValue[-2] and rsiValue[-1] < rsiOversold and macdLine[-1] > signalLine[-1]
shortCondition = closes[-1] < emaValue[-1] and closes[-2] >= emaValue[-2] and rsiValue[-1] > rsiOverbought and macdLine[-1] < signalLine[-1]

# Définir le levier à x20 avant de passer des ordres
set_leverage()

# Calculer la quantité à trader (75% du solde du portefeuille)
balance = get_wallet_balance()
trade_qty = balance * 0.75

headers = {
    'Content-Type': 'application/json',
    'api_key': API_KEY
}

timestamp = int(time.time() * 1000)

if longCondition:
    order_data = {
        "side": "Buy",
        "symbol": "BTCUSDTPERP",
        "order_type": "Market",
        "qty": trade_qty,
        "time_in_force": "GoodTillCancel",
        "timestamp": timestamp
    }
    order_data['sign'] = generate_signature(API_SECRET, order_data)
    response = requests.post(f"{BASE_URL}/private/linear/order/create", headers=headers, data=order_data)
    response_json = response.json()
    if response_json['ret_code'] == 0:
        send_telegram_message(f"Long position ouverte avec succès!\nProfit: {response_json['result']['realised_pnl']}")

if shortCondition:
    order_data = {
        "side": "Sell",
        "symbol": "BTCUSDTPERP",
        "order_type": "Market",
        "qty": trade_qty,
        "time_in_force": "GoodTillCancel",
        "timestamp": timestamp
    }
    order_data['sign'] = generate_signature(API_SECRET, order_data)
    response = requests.post(f"{BASE_URL}/private/linear/order/create", headers=headers, data=order_data)
    response_json = response.json()
    if response_json['ret_code'] == 0:
        send_telegram_message(f"Short position ouverte avec succès!\nProfit: {response_json['result']['realised_pnl']}")
