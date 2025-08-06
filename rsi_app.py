import ccxt
import pandas as pd
import ta
import streamlit as st

st.title("📊 Analisador de RSI - Criptomoedas")

# Lista de pares populares
pares_populares = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "SOL/USDT",
    "DOGE/USDT", "ADA/USDT", "MATIC/USDT", "DOT/USDT", "LTC/USDT"
]

# Seleção do par
par = st.selectbox("Escolha o par de criptomoedas", pares_populares, index=0)

# Função para pegar dados da Binance
def pegar_dados(par):
    try:
        exchange = ccxt.binance()
        ohlcv = exchange.fetch_ohlcv(par, timeframe='1h', limit=200)
        if not ohlcv:
            st.error("Não foi possível obter dados. Verifique o par de moedas.")
            return None
        df = pd.DataFrame(ohlcv, columns=['timestamp','open','high','low','close','volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except ccxt.BaseError as e:
        st.error(f"Erro CCXT: {e}")
        return None
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return None

# Calcular RSI
if st.button("Analisar RSI"):
    df = pegar_dados(par)
    if df is not None and not df.empty:
        try:
            rsi = ta.momentum.RSIIndicator(df['close'], window=14).rsi().iloc[-1]
            st.subheader(f"RSI Atual: {rsi:.2f}")

            # Barra visual simples
            cor = "green" if rsi < 30 else "red" if rsi > 70 else "yellow"
            st.progress(min(max(rsi, 0), 100) / 100)  # barra 0-100
            st.markdown(f"<p style='color:{cor};font-size:20px;'>Status: {'Sobrevenda' if rsi < 30 else 'Sobrecompra' if rsi > 70 else 'Neutro'}</p>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro ao calcular RSI: {e}")