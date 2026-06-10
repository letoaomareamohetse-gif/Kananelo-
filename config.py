"""
Pips Hunter Bot Configuration

Centralized configuration file for all bot parameters
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ═══════════════════════════════════════════════════════════
# TRADING STRATEGY PARAMETERS
# ═══════════════════════════════════════════════════════════

STRATEGY_CONFIG = {
    # Technical Indicators
    'EMA_PERIOD': 50,  # Exponential Moving Average period for trend detection
    'RSI_PERIOD': 14,  # Relative Strength Index period
    'RSI_OVERSOLD': 35,  # RSI level to trigger BUY signals (cross above)
    'RSI_OVERBOUGHT': 65,  # RSI level to trigger SELL signals (cross below)
    
    # Risk Management
    'TAKE_PROFIT_PIPS': 15,  # Profit target in pips
    'STOP_LOSS_PIPS': 10,  # Stop loss in pips
    'MAX_TRADES_PER_DAY': 15,  # Maximum number of trades per day
    
    # Position Sizing
    'PIP_VALUE': 0.0001,  # Standard Forex pip (4 decimal places)
    'POSITION_SIZE_PERCENT': 10,  # % of account per trade
    
    # Trading Hours
    'TRADING_START_HOUR': 0,  # Start trading at (UTC)
    'TRADING_END_HOUR': 23,  # Stop trading at (UTC)
}

# ═══════════════════════════════════════════════════════════
# ACCOUNT CONFIGURATION
# ═══════════════════════════════════════════════════════════

ACCOUNT_CONFIG = {
    'STARTING_CAPITAL': 1000,  # Initial account balance ($)
    'LEVERAGE': 50,  # Leverage ratio (1:50)
    'CURRENCY': 'USD',  # Account currency
    'BROKER_COMMISSION': 0.00002,  # Commission per round-trip trade
}

# ═══════════════════════════════════════════════════════════
# CURRENCY PAIRS (WATCHLIST)
# ═══════════════════════════════════════════════════════════

CURRENCY_PAIRS = {
    'EUR/USD': {'pip_digits': 4, 'spread': 1.5},  # 1.5 pips spread
    'GBP/USD': {'pip_digits': 4, 'spread': 2.0},  # 2.0 pips spread
    'USD/JPY': {'pip_digits': 2, 'spread': 1.0},  # 1.0 pips spread (3 decimal)
    'AUD/USD': {'pip_digits': 4, 'spread': 2.5},  # 2.5 pips spread
    'USD/CAD': {'pip_digits': 4, 'spread': 1.8},  # 1.8 pips spread
}

# ═══════════════════════════════════════════════════════════
# TIMEFRAME CONFIGURATION
# ═══════════════════════════════════════════════════════════

TIMEFRAMES = {
    '5M': {'minutes': 5, 'bars_per_day': 288, 'strategy': 'scalping'},
    '15M': {'minutes': 15, 'bars_per_day': 96, 'strategy': 'scalping'},
    '1H': {'minutes': 60, 'bars_per_day': 24, 'strategy': 'swing'},
    '4H': {'minutes': 240, 'bars_per_day': 6, 'strategy': 'swing'},
}

# ═══════════════════════════════════════════════════════════
# BROKER SETTINGS (API CONFIGURATION)
# ═══════════════════════════════════════════════════════════

BROKER_CONFIG = {
    # OANDA (forex.com)
    'OANDA': {
        'api_endpoint': 'https://api-fxpractice.oanda.com',  # Demo
        'account_id': os.getenv('OANDA_ACCOUNT_ID', ''),
        'api_key': os.getenv('OANDA_API_KEY', ''),
        'enable_live_trading': False,  # ⚠️ Set to True only for live trading
    },
    
    # IQ Option (CFDs)
    'IQOPTION': {
        'email': os.getenv('IQOPTION_EMAIL', ''),
        'password': os.getenv('IQOPTION_PASSWORD', ''),
        'enable_live_trading': False,
    },
}

# ═══════════════════════════════════════════════════════════
# ALERT & NOTIFICATION SETTINGS
# ═══════════════════════════════════════════════════════════

ALERT_CONFIG = {
    'ENABLE_EMAIL': False,
    'SMTP_SERVER': os.getenv('SMTP_SERVER', ''),
    'SMTP_PORT': 587,
    'SENDER_EMAIL': os.getenv('SENDER_EMAIL', ''),
    'SENDER_PASSWORD': os.getenv('SENDER_PASSWORD', ''),
    'NOTIFY_EMAIL': os.getenv('NOTIFY_EMAIL', ''),
    
    'ENABLE_TELEGRAM': False,
    'TELEGRAM_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID', ''),
    
    'ENABLE_SMS': False,
    'TWILIO_ACCOUNT_SID': os.getenv('TWILIO_ACCOUNT_SID', ''),
    'TWILIO_AUTH_TOKEN': os.getenv('TWILIO_AUTH_TOKEN', ''),
    'TWILIO_PHONE': os.getenv('TWILIO_PHONE', ''),
    'NOTIFY_PHONE': os.getenv('NOTIFY_PHONE', ''),
}

# ═══════════════════════════════════════════════════════════
# LOGGING & DATABASE
# ═══════════════════════════════════════════════════════════

LOGGING_CONFIG = {
    'LOG_LEVEL': 'INFO',
    'LOG_FILE': 'pips_hunter.log',
    'LOG_MAX_SIZE': 10485760,  # 10MB
    'LOG_BACKUP_COUNT': 5,
    'LOG_FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
}

DATABASE_CONFIG = {
    'DATABASE_URL': os.getenv(
        'DATABASE_URL',
        'sqlite:///pips_hunter.db'
    ),
    'ENABLE_DB_LOGGING': True,
}

# ═══════════════════════════════════════════════════════════
# BACKTESTING PARAMETERS
# ═══════════════════════════════════════════════════════════

BACKTEST_CONFIG = {
    'BACKTEST_YEARS': 1,  # Years of historical data to test
    'BACKTEST_OPTIMIZE': False,  # Run parameter optimization
    'OPTIMIZATION_PARAMS': {
        'ema_period': range(20, 100, 10),
        'rsi_period': range(7, 28, 2),
        'tp_pips': range(5, 50, 5),
        'sl_pips': range(5, 30, 5),
    },
}

# ═══════════════════════════════════════════════════════════
# DATA SOURCES
# ═══════════════════════════════════════════════════════════

DATA_SOURCES = {
    'YAHOO_FINANCE': 'https://finance.yahoo.com',
    'ALPHA_VANTAGE': {
        'api_key': os.getenv('ALPHA_VANTAGE_API_KEY', ''),
        'endpoint': 'https://www.alphavantage.co/query',
    },
    'CSV_DATA_PATH': './data/',
}

# ═══════════════════════════════════════════════════════════
# PERFORMANCE TARGETS
# ═══════════════════════════════════════════════════════════

PERFORMANCE_TARGETS = {
    'DAILY_PROFIT_TARGET': 50,  # $ per day target
    'MONTHLY_PROFIT_TARGET': 1000,  # $ per month target
    'MAX_DAILY_LOSS': 100,  # $ max daily loss before stopping
    'WIN_RATE_TARGET': 0.60,  # 60% win rate target
    'RISK_REWARD_RATIO': 1.5,  # Risk:Reward ratio
}

# ═══════════════════════════════════════════════════════════
# ADVANCED SETTINGS
# ═══════════════════════════════════════════════════════════

ADVANCED_CONFIG = {
    'ENABLE_POSITION_AVERAGING': False,  # Add to losing positions
    'ENABLE_BREAKEVEN_STOP': True,  # Move SL to breakeven after +5 pips
    'ENABLE_TRAILING_STOP': False,  # Use trailing stop loss
    'ENABLE_RISK_PARITY': False,  # Equal risk per trade
    'ENABLE_CORRELATION_FILTER': False,  # Filter correlated pairs
    'ENABLE_NEWS_FILTER': False,  # Avoid trading during major news
    
    # Backtesting
    'SLIPPAGE_PIPS': 0.5,  # Assumed slippage in pips
    'FILL_PROBABILITY': 0.95,  # % of orders filled at target price
}

# ═══════════════════════════════════════════════════════════
# SAFETY & SECURITY
# ═══════════════════════════════════════════════════════════

SECURITY_CONFIG = {
    'ENABLE_AUTHENTICATION': False,
    'API_KEY_REQUIRED': False,
    'ALLOWED_IPS': [],  # Empty = allow all
    'REQUIRE_2FA': False,
    'ENABLE_RATE_LIMITING': False,
    'RATE_LIMIT_REQUESTS': 100,
    'RATE_LIMIT_WINDOW': 60,  # seconds
}

# ═══════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════

def get_strategy_config():
    """Get current strategy configuration"""
    return STRATEGY_CONFIG

def get_account_config():
    """Get current account configuration"""
    return ACCOUNT_CONFIG

def validate_config():
    """Validate configuration for consistency"""
    assert STRATEGY_CONFIG['TAKE_PROFIT_PIPS'] > 0, "Take profit must be positive"
    assert STRATEGY_CONFIG['STOP_LOSS_PIPS'] > 0, "Stop loss must be positive"
    assert STRATEGY_CONFIG['MAX_TRADES_PER_DAY'] > 0, "Max trades must be positive"
    assert ACCOUNT_CONFIG['STARTING_CAPITAL'] > 0, "Starting capital must be positive"
    return True

if __name__ == '__main__':
    print("🎯 Pips Hunter Bot Configuration")
    print("\nStrategy Config:")
    for key, value in STRATEGY_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\nAccount Config:")
    for key, value in ACCOUNT_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\nValidation:", "✅ Passed" if validate_config() else "❌ Failed")
