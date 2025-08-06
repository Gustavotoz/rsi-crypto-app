import ccxt
import pandas as pd
import ta
import streamlit as st

st.title("📊 Analisador de RSI - Criptomoedas")

# Entrada do par de moedas
par = st.text_input("Digite o par (ex: BTC/USDT)", value="BTC/USDT")

# Função para pegar dados da Binance
def pegar_dados(par):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(par, timeframe='1h', limit=200)  # candles de 1 hora
    df = pd.DataFrame(ohlcv, columns=['timestamp','open','high','low','close','volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Calcular RSI
if st.button("Analisar RSI"):
    try:
        df = pegar_dados(par)
        rsi = ta.momentum.RSIIndicator(df['close'], window=14).rsi().iloc[-1]
        st.subheader(f"RSI Atual: {rsi:.2f}")

        # Barra visual simples
        cor = "green" if rsi < 30 else "red" if rsi > 70 else "yellow"
        st.progress(min(max(rsi, 0), 100) / 100)  # barra 0-100
        st.markdown(f"<p style='color:{cor};font-size:20px;'>Status: {'Sobrevenda' if rsi < 30 else 'Sobrecompra' if rsi > 70 else 'Neutro'}</p>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
