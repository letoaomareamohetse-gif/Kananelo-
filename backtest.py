#!/usr/bin/env python
"""
Pips Hunter Bot - Backtest Engine

Run historical backtests to validate strategy performance

Usage:
    python backtest.py
"""

import backtrader as bt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from bot import PipsHunterStrategy

class BacktestAnalyzer:
    """Analyze backtest results"""
    
    def __init__(self, results):
        self.results = results
        self.analyzer = None
        
    def generate_report(self):
        """Generate comprehensive backtest report"""
        print("\n" + "="*70)
        print("📊 BACKTEST PERFORMANCE REPORT")
        print("="*70 + "\n")
        
        # Get final value
        final_value = self.results.broker.getvalue()
        starting_value = self.results.broker.startcash
        net_profit = final_value - starting_value
        roi = (net_profit / starting_value) * 100
        
        print(f"💰 CAPITAL PERFORMANCE")
        print(f"   Starting Capital:    ${starting_value:,.2f}")
        print(f"   Final Capital:       ${final_value:,.2f}")
        print(f"   Net Profit/Loss:     ${net_profit:,.2f}")
        print(f"   ROI:                 {roi:.2f}%\n")
        
        # Trade statistics
        trade_count = self.results.analyzers.trade_total.get_analysis().total
        
        print(f"📈 TRADE STATISTICS")
        print(f"   Total Trades:        {trade_count}")
        print(f"   Win Rate:            N/A (requires trade analyzer)")
        print(f"   Avg Trade P/L:       ${net_profit/trade_count:.2f} (if {trade_count} > 0)\n" if trade_count > 0 else "\n")
        
        print("="*70 + "\n")


def create_sample_data(filename='sample_eurusd_5min.csv', days=30):
    """
    Create sample EUR/USD 5-minute OHLC data for backtesting
    
    Args:
        filename: Output CSV filename
        days: Number of days to generate
    """
    print(f"📝 Generating sample data: {filename}")
    
    # Generate date range (5-minute bars)
    start_date = datetime.now() - timedelta(days=days)
    dates = pd.date_range(start=start_date, periods=days*288, freq='5min')
    
    # Generate realistic OHLC data
    np.random.seed(42)
    base_price = 1.0850
    returns = np.random.normal(0, 0.0002, len(dates))
    close_prices = base_price + np.cumsum(returns)
    
    data = {
        'Datetime': dates,
        'Open': close_prices + np.random.normal(0, 0.0001, len(dates)),
        'High': close_prices + np.abs(np.random.normal(0, 0.0002, len(dates))),
        'Low': close_prices - np.abs(np.random.normal(0, 0.0002, len(dates))),
        'Close': close_prices,
        'Volume': np.random.randint(1000, 10000, len(dates))
    }
    
    df = pd.DataFrame(data)
    df['Datetime'] = df['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df = df[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"✅ Sample data created: {filename} ({len(df)} bars)\n")
    
    return filename


def run_backtest_example():
    """
    Run a complete backtest example
    """
    # Create sample data
    data_file = create_sample_data()
    
    # Initialize Cerebro engine
    cerebro = bt.Cerebro()
    
    # Add strategy
    cerebro.addstrategy(PipsHunterStrategy)
    
    # Set broker parameters
    cerebro.broker.setcash(1000.0)  # Starting capital
    cerebro.broker.setcommission(commission=0.00002)  # 2 pips per round trip
    
    # Load data
    data = bt.feeds.GenericCSVData(
        dataname=data_file,
        dtformat='%Y-%m-%d %H:%M:%S',
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1,
        fromdate=datetime(2024, 1, 1),
        todate=datetime(2024, 12, 31)
    )
    
    cerebro.adddata(data)
    
    # Add analyzers
    cerebro.addobserver(bt.observers.Broker)
    cerebro.addobserver(bt.observers.Value)
    
    # Add analyzer for trades
    cerebro.addobserver(name='TradeTotal')
    
    print("🎯 PIPS HUNTER BOT - BACKTEST ENGINE")
    print("="*70)
    print(f"Starting Portfolio Value: ${cerebro.broker.getvalue():.2f}")
    print(f"Data File: {data_file}")
    print("\n🔄 Running backtest...\n")
    
    # Run backtest
    results = cerebro.run()
    strategy_instance = results[0]
    
    # Generate report
    print("\n" + "="*70)
    print("BACKTEST RESULTS")
    print("="*70)
    
    final_portfolio_value = cerebro.broker.getvalue()
    starting_portfolio = 1000.0
    net_profit = final_portfolio_value - starting_portfolio
    roi = (net_profit / starting_portfolio) * 100
    
    print(f"\n💰 FINANCIAL METRICS")
    print(f"   Starting Capital:        ${starting_portfolio:,.2f}")
    print(f"   Final Capital:           ${final_portfolio_value:,.2f}")
    print(f"   Net Profit/Loss:         ${net_profit:,.2f}")
    print(f"   Return on Investment:    {roi:.2f}%")
    
    # Trade log analysis
    if hasattr(strategy_instance, 'trade_log') and strategy_instance.trade_log:
        trades_df = pd.DataFrame(strategy_instance.trade_log)
        print(f"\n📊 TRADE ANALYSIS")
        print(f"   Total Trades:            {len(trades_df)}")
        
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        win_rate = (winning_trades / len(trades_df) * 100) if len(trades_df) > 0 else 0
        
        print(f"   Winning Trades:          {winning_trades}")
        print(f"   Losing Trades:           {losing_trades}")
        print(f"   Win Rate:                {win_rate:.1f}%")
        
        if len(trades_df) > 0:
            avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean()
            avg_loss = trades_df[trades_df['pnl'] < 0]['pnl'].mean()
            print(f"   Avg Winning Trade:       ${avg_win:,.2f}")
            print(f"   Avg Losing Trade:        ${avg_loss:,.2f}")
    
    print("\n" + "="*70)
    print("✅ Backtest Complete!")
    print("="*70 + "\n")
    
    # Cleanup
    if os.path.exists(data_file):
        os.remove(data_file)
        print(f"📝 Cleaned up: {data_file}")


if __name__ == '__main__':
    run_backtest_example()
