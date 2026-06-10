import backtrader as bt
import datetime
import pandas as pd
from datetime import datetime as dt
import json

class PipsHunterStrategy(bt.Strategy):
    """
    Pips Hunter - High-frequency Forex scalping strategy
    
    Entry Logic:
    - LONG: Price > 50 EMA AND RSI crosses above oversold (35)
    - SHORT: Price < 50 EMA AND RSI crosses below overbought (65)
    
    Exit Logic:
    - Take Profit: +15 pips
    - Stop Loss: -10 pips
    - Daily Limit: Max 15 trades per day
    """
    
    params = (
        ('ema_period', 50),
        ('rsi_period', 14),
        ('rsi_oversold', 35),
        ('rsi_overbought', 65),
        ('tp_pips', 15),
        ('sl_pips', 10),
        ('max_trades_per_day', 15),
        ('pip_value', 0.0001),  # Standard 4-decimal pip for Forex
    )

    def __init__(self):
        # Technical Indicators
        self.ema = bt.indicators.ExponentialMovingAverage(
            self.data.close, 
            period=self.params.ema_period
        )
        
        self.rsi = bt.indicators.RelativeStrengthIndex(
            self.data.close, 
            period=self.params.rsi_period
        )
        
        # Crossover detection
        self.rsi_buy_signal = bt.indicators.CrossOver(self.rsi, self.params.rsi_oversold)
        self.rsi_sell_signal = bt.indicators.CrossOver(self.params.rsi_overbought, self.rsi)
        
        # Trade tracking
        self.order = None
        self.current_day = None
        self.trades_today = 0
        self.trade_log = []
        self.daily_log = {}
        
    def log(self, text, dt_obj=None):
        """Log trading activity"""
        dt_obj = dt_obj or self.datas[0].datetime.date(0)
        print(f"{dt_obj.isoformat()} | {text}")

    def notify_trade(self, trade):
        """Handle trade closing notifications"""
        if trade.isclosed:
            self.trades_today += 1
            
            trade_data = {
                'date': self.datas[0].datetime.date(0).isoformat(),
                'time': self.datas[0].datetime.time(0).isoformat(),
                'pnl': trade.pnl,
                'pnl_percent': trade.pnlcomm,
                'entry_price': trade.price,
                'exit_price': trade.price,
                'size': trade.size,
                'duration': trade.barlen
            }
            self.trade_log.append(trade_data)
            
            status = "✅ PROFIT" if trade.pnl > 0 else "❌ LOSS"
            self.log(
                f"{status} | P/L: ${trade.pnl:.2f} | "
                f"Trades Today: {self.trades_today}/{self.params.max_trades_per_day}"
            )

    def next(self):
        """Execute trading logic on each bar"""
        # Reset daily trade counter at start of new day
        current_date = self.datas[0].datetime.date(0)
        if self.current_day != current_date:
            self.current_day = current_date
            self.trades_today = 0
            self.log(f"📅 NEW TRADING DAY | Capital: ${self.broker.getvalue():.2f}")

        # Daily trade limit protection
        if self.trades_today >= self.params.max_trades_per_day:
            return

        # Don't enter if already in a position
        if self.position:
            return

        # Calculate pips to points conversion
        pip_size = self.data.close[0] * self.params.pip_value
        tp_distance = self.params.tp_pips * pip_size
        sl_distance = self.params.sl_pips * pip_size
        
        # ═══════════════════════════════════
        # LONG (BUY) ENTRY CONDITION
        # ═══════════════════════════════════
        if (self.data.close[0] > self.ema[0] and 
            self.rsi_buy_signal[0] > 0):
            
            entry_price = self.data.close[0]
            tp_price = entry_price + tp_distance
            sl_price = entry_price - sl_distance
            
            self.log(
                f"🟢 BUY SIGNAL | Entry: {entry_price:.5f} | "
                f"TP: {tp_price:.5f} | SL: {sl_price:.5f}"
            )
            
            # Enter position
            self.order = self.buy()
            
            # Set profit target (limit order)
            self.sell(
                exectype=bt.Order.Limit,
                price=tp_price,
                transmit=False,
                parent=self.order
            )
            
            # Set stop loss (stop order)
            self.sell(
                exectype=bt.Order.Stop,
                price=sl_price,
                transmit=True,
                parent=self.order
            )

        # ═══════════════════════════════════
        # SHORT (SELL) ENTRY CONDITION
        # ═══════════════════════════════════
        elif (self.data.close[0] < self.ema[0] and 
              self.rsi_sell_signal[0] > 0):
            
            entry_price = self.data.close[0]
            tp_price = entry_price - tp_distance
            sl_price = entry_price + sl_distance
            
            self.log(
                f"🔴 SELL SIGNAL | Entry: {entry_price:.5f} | "
                f"TP: {tp_price:.5f} | SL: {sl_price:.5f}"
            )
            
            # Enter position
            self.order = self.sell()
            
            # Set profit target (limit order)
            self.buy(
                exectype=bt.Order.Limit,
                price=tp_price,
                transmit=False,
                parent=self.order
            )
            
            # Set stop loss (stop order)
            self.buy(
                exectype=bt.Order.Stop,
                price=sl_price,
                transmit=True,
                parent=self.order
            )

    def stop(self):
        """Called when strategy finishes"""
        final_value = self.broker.getvalue()
        self.log(f"\n🏁 BACKTEST COMPLETE")
        self.log(f"Final Portfolio Value: ${final_value:.2f}")
        self.log(f"Total Trades Executed: {len(self.trade_log)}")
        self.log(f"Total Profit/Loss: ${final_value - self.broker.startcash:.2f}")


def run_backtest(data_path, start_cash=1000, commission=0.00002):
    """
    Run backtest with historical data
    
    Args:
        data_path: Path to CSV data file
        start_cash: Starting capital
        commission: Broker commission (e.g., 0.00002 for 0.002% = 2 pips per round trip)
    """
    cerebro = bt.Cerebro()
    
    # Add strategy
    cerebro.addstrategy(PipsHunterStrategy)
    
    # Broker settings
    cerebro.broker.setcash(start_cash)
    cerebro.broker.setcommission(commission=commission)
    cerebro.broker.setdefaultmaker(True)
    
    # Load data
    data = bt.feeds.GenericCSVData(
        dataname=data_path,
        dtformat='%Y-%m-%d %H:%M:%S',
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1
    )
    
    cerebro.adddata(data)
    
    # Add observers
    cerebro.addobserver(bt.observers.Broker)
    cerebro.addobserver(bt.observers.Trades)
    cerebro.addobserver(bt.observers.DrawDown)
    
    print(f"🎯 PIPS HUNTER BOT - BACKTEST")
    print(f"Starting Portfolio Value: ${cerebro.broker.getvalue():.2f}")
    print("─" * 60)
    
    # Run backtest
    results = cerebro.run()
    
    print("─" * 60)
    
    return results[0]


if __name__ == '__main__':
    # Example usage
    print("Pips Hunter Bot Module Ready")
    print("Use: from bot import PipsHunterStrategy, run_backtest")
