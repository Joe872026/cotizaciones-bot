import yfinance as yf
import requests
import os
from datetime import datetime

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

acciones = {
    "Nike": "NKE",
    "Microsoft": "MSFT",
    "IAG": "IAG.MC"
    "Bitcoin": "BTC-USD"
}

def obtener_cotizacion(ticker):
    datos = yf.Ticker(ticker)
    info = datos.fast_info
    precio = round(info.last_price, 2)
    apertura = round(info.open, 2)
    variacion = round(((precio - apertura) / apertura) * 100, 2)
    return precio, variacion

def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": texto})

fecha = datetime.now().strftime("%d/%m/%Y")
mensaje = f"📈 Cotizaciones del {fecha}\n\n"

for nombre, ticker in acciones.items():
    try:
        precio, variacion = obtener_cotizacion(ticker)
        emoji = "🟢" if variacion >= 0 else "🔴"
        mensaje += f"{emoji} {nombre}: {precio} $ ({variacion:+.2f}%)\n"
    except Exception as e:
        mensaje += f"⚠️ {nombre}: error al obtener datos\n"

enviar_mensaje(mensaje)
