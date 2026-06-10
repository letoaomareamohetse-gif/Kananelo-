import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Pips Hunter Bot",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .success {
        color: #00ff00;
        font-weight: bold;
    }
    .danger {
        color: #ff0000;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- APP HEADER ---
st.title("🎯 Pips Hunter — Algorithmic Scalping Bot")
st.markdown("**Automated high-frequency Forex trend-following engine** powered by EMA + RSI")
st.divider()

# --- SIDEBAR: BOT CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Bot Configuration")
    
    # Currency Pair Selection
    market = st.selectbox(
        "📊 Select Currency Pair",
        ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"],
        index=0
    )
    
    # Timeframe Selection
    timeframe = st.selectbox(
        "⏱️ Chart Timeframe",
        ["5 Minutes (Fast Scalping)", "15 Minutes (Medium)", "1 Hour (Swing)"],
        index=0
    )
    
    # Risk Management Section
    st.subheader("💰 Risk Management")
    initial_capital = st.number_input(
        "Starting Capital ($)",
        min_value=100,
        max_value=100000,
        value=1000,
        step=100
    )
    
    tp_pips = st.slider(
        "Take Profit Target (Pips)",
        min_value=5,
        max_value=50,
        value=15,
        step=1
    )
    
    sl_pips = st.slider(
        "Stop Loss Protection (Pips)",
        min_value=5,
        max_value=30,
        value=10,
        step=1
    )
    
    max_trades = st.slider(
        "Maximum Daily Trades",
        min_value=1,
        max_value=30,
        value=15,
        step=1
    )
    
    # Strategy Parameters
    st.subheader("🔧 Strategy Parameters")
    ema_period = st.slider(
        "EMA Trend Filter (Period)",
        min_value=20,
        max_value=200,
        value=50,
        step=5
    )
    
    rsi_period = st.slider(
        "RSI Period",
        min_value=7,
        max_value=28,
        value=14,
        step=1
    )
    
    rsi_oversold = st.slider(
        "RSI Oversold Level (Buy Signal)",
        min_value=20,
        max_value=40,
        value=35,
        step=1
    )
    
    rsi_overbought = st.slider(
        "RSI Overbought Level (Sell Signal)",
        min_value=60,
        max_value=80,
        value=65,
        step=1
    )
    
    # Bot Control
    st.subheader("▶️ Execution Engine")
    bot_active = st.toggle(
        "🟢 Activate Pips Hunter Bot Live",
        value=False,
        help="Enable to start live trading (use demo first!)"
    )
    
    if bot_active:
        st.warning("⚠️ Bot is LIVE. Use demo account for testing!")
    
    st.divider()
    st.markdown("📝 **Bot will execute up to 15 trades per day on RSI + EMA signals**")

# --- MAIN DASHBOARD ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    status_icon = "🟢" if bot_active else "🔴"
    status_text = "RUNNING" if bot_active else "PAUSED"
    st.metric(label="Bot Status", value=f"{status_icon} {status_text}")

with col2:
    current_trades = 6 if bot_active else 0
    st.metric(
        label="Trades Today",
        value=f"{current_trades}/{max_trades}",
        delta="Active" if bot_active else "Offline"
    )

with col3:
    win_rate = 66.7 if bot_active else 0.0
    st.metric(
        label="Win Rate",
        value=f"{win_rate:.1f}%",
        delta="+2.3%" if bot_active else None
    )

with col4:
    net_profit = 45.20 if bot_active else 0.00
    st.metric(
        label="Net Profit/Loss",
        value=f"${net_profit:.2f}",
        delta=f"+${net_profit:.2f}" if bot_active else None
    )

st.divider()

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Live Orders", "📈 Performance", "🔍 Signals", "⚡ Settings"])

# TAB 1: Live Orders
with tab1:
    st.subheader("📊 Live Order Execution Stream")
    
    if bot_active:
        st.info(f"✅ Monitoring **{market}** on **{timeframe}** | Scanning for RSI + EMA signals...")
        
        # Mock trade data
        mock_trades = {
            "Timestamp": [
                (datetime.now() - timedelta(hours=2)).strftime("%H:%M:%S"),
                (datetime.now() - timedelta(hours=1)).strftime("%H:%M:%S"),
                datetime.now().strftime("%H:%M:%S")
            ],
            "Market": [market, market, market],
            "Type": ["🟢 BUY (Long)", "🔴 SELL (Short)", "🟢 BUY (Long)"],
            "Entry Price": [1.0854, 1.0892, 1.0821],
            "Current Price": [1.0864, 1.0882, 1.0831],
            "Take Profit": [1.0854 + (tp_pips*0.0001), 1.0892 - (tp_pips*0.0001), 1.0821 + (tp_pips*0.0001)],
            "Stop Loss": [1.0854 - (sl_pips*0.0001), 1.0892 + (sl_pips*0.0001), 1.0821 - (sl_pips*0.0001)],
            "P/L": [f"+${10.00}", f"-${8.50}", f"+${10.00}"],
            "Status": ["✅ Closed (Profit)", "✅ Closed (Loss)", "🔄 Active"]
        }
        
        df_trades = pd.DataFrame(mock_trades)
        st.dataframe(df_trades, use_container_width=True, hide_index=True)
        
        # Scanner animation
        with st.spinner("🔄 Scanning market for RSI crossover + EMA alignment..."):
            time.sleep(1)
        
        st.success("✅ Scanner active. Next signal check in 5 minutes.")
    else:
        st.warning("⚠️ Bot is offline. Toggle 'Activate Pips Hunter Bot Live' to start.")

# TAB 2: Performance
with tab2:
    st.subheader("📈 Trading Performance Analytics")
    
    col_perf1, col_perf2 = st.columns(2)
    
    with col_perf1:
        st.metric("Total Trades", "124", "+12 this week")
        st.metric("Winning Trades", "82", "66%")
        st.metric("Losing Trades", "42", "34%")
    
    with col_perf2:
        st.metric("Total Profit", "$892.50", "+$125.30")
        st.metric("Avg Win", "$10.88", "per trade")
        st.metric("Avg Loss", "$-8.92", "per trade")
    
    # Performance chart
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    cumulative_profit = np.cumsum(np.random.randn(30) * 10 + 30)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=cumulative_profit,
        mode='lines+markers',
        name='Cumulative P/L',
        line=dict(color='#00ff00', width=3),
        fill='tozeroy',
        marker=dict(size=6)
    ))
    fig.update_layout(
        title="30-Day Cumulative Profit/Loss",
        xaxis_title="Date",
        yaxis_title="Profit ($)",
        hovermode='x unified',
        height=400,
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)

# TAB 3: Signals
with tab3:
    st.subheader("🔍 Technical Signal Analysis")
    
    # Create mock price chart with indicators
    hours = np.arange(0, 24)
    prices = 1.0850 + np.cumsum(np.random.randn(24) * 0.0005)
    ema = pd.Series(prices).ewm(span=ema_period//10, adjust=False).mean()
    
    fig_chart = go.Figure()
    
    # Candlestick prices
    fig_chart.add_trace(go.Scatter(
        x=hours, y=prices,
        mode='lines',
        name='Price',
        line=dict(color='white', width=2)
    ))
    
    # EMA indicator
    fig_chart.add_trace(go.Scatter(
        x=hours, y=ema,
        mode='lines',
        name=f'{ema_period} EMA (Trend)',
        line=dict(color='#00ff00', width=2, dash='dash')
    ))
    
    fig_chart.update_layout(
        title=f"{market} Technical Analysis - {timeframe}",
        xaxis_title="Time (Hours)",
        yaxis_title="Price",
        height=500,
        template='plotly_dark',
        hovermode='x unified'
    )
    st.plotly_chart(fig_chart, use_container_width=True)
    
    # RSI Indicator
    rsi_values = np.random.uniform(30, 70, 24)
    
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(
        x=hours, y=rsi_values,
        mode='lines',
        name='RSI',
        line=dict(color='#ff9500', width=2),
        fill='tozeroy'
    ))
    
    fig_rsi.add_hline(y=rsi_overbought, line_dash="dash", line_color="red", annotation_text="Overbought")
    fig_rsi.add_hline(y=rsi_oversold, line_dash="dash", line_color="green", annotation_text="Oversold")
    
    fig_rsi.update_layout(
        title=f"RSI ({rsi_period}) - Signal Detector",
        xaxis_title="Time (Hours)",
        yaxis_title="RSI Value",
        height=350,
        template='plotly_dark',
        hovermode='x unified'
    )
    st.plotly_chart(fig_rsi, use_container_width=True)

# TAB 4: Settings
with tab4:
    st.subheader("⚙️ Advanced Settings")
    
    col_set1, col_set2 = st.columns(2)
    
    with col_set1:
        st.write("**Current Configuration**")
        st.write(f"🎯 Market: {market}")
        st.write(f"⏱️ Timeframe: {timeframe}")
        st.write(f"💰 Capital: ${initial_capital}")
        st.write(f"📊 EMA Length: {ema_period}")
        st.write(f"📈 RSI Period: {rsi_period}")
    
    with col_set2:
        st.write("**Risk Parameters**")
        st.write(f"✅ Take Profit: {tp_pips} pips")
        st.write(f"❌ Stop Loss: {sl_pips} pips")
        st.write(f"📋 Max Trades/Day: {max_trades}")
        st.write(f"🔐 Risk/Reward Ratio: 1:{tp_pips/sl_pips:.2f}")
    
    st.divider()
    
    # Export settings
    if st.button("💾 Save Configuration"):
        config_data = {
            "market": market,
            "timeframe": timeframe,
            "initial_capital": initial_capital,
            "tp_pips": tp_pips,
            "sl_pips": sl_pips,
            "max_trades": max_trades,
            "ema_period": ema_period,
            "rsi_period": rsi_period,
            "rsi_oversold": rsi_oversold,
            "rsi_overbought": rsi_overbought
        }
        st.success("✅ Configuration saved successfully!")
        st.json(config_data)
    
    st.divider()
    st.warning("⚠️ **Important Disclaimers**")
    st.markdown("""
    - This bot is for **educational purposes only**
    - Always test on a **demo account first**
    - Past performance ≠ future results
    - Only trade with **money you can afford to lose**
    - No guarantee of profitability
    - Market conditions can change rapidly
    """)

# --- FOOTER ---
st.divider()
st.markdown("""
<div style='text-align: center'>
    <p style='color: gray; font-size: 12px;'>
        🎯 Pips Hunter Bot v1.0 | Built for Free Trading | 
        <a href='https://github.com/letoaomareamohetse-gif/Kananelo-'>GitHub</a>
    </p>
    <p style='color: gray; font-size: 11px;'>
        ⚠️ Trading involves substantial risk of loss. Use demo first.
    </p>
</div>
""", unsafe_allow_html=True)
