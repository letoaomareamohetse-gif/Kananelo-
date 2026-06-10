"""
Technical Indicators Library

Custom implementations of technical indicators used by Pips Hunter Bot
"""

import numpy as np
import pandas as pd

class TechnicalIndicators:
    """Library of technical indicators"""
    
    @staticmethod
    def ema(data, period):
        """
        Exponential Moving Average (EMA)
        
        Args:
            data: Price series
            period: EMA period
            
        Returns:
            EMA values
        """
        if isinstance(data, (list, np.ndarray)):
            data = pd.Series(data)
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def sma(data, period):
        """
        Simple Moving Average (SMA)
        
        Args:
            data: Price series
            period: SMA period
            
        Returns:
            SMA values
        """
        if isinstance(data, (list, np.ndarray)):
            data = pd.Series(data)
        return data.rolling(window=period).mean()
    
    @staticmethod
    def rsi(data, period=14):
        """
        Relative Strength Index (RSI)
        
        Args:
            data: Price series (close prices)
            period: RSI period (default: 14)
            
        Returns:
            RSI values (0-100)
        """
        if isinstance(data, (list, np.ndarray)):
            data = pd.Series(data)
        
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def macd(data, fast=12, slow=26, signal=9):
        """
        Moving Average Convergence Divergence (MACD)
        
        Args:
            data: Price series
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line EMA period
            
        Returns:
            dict with 'macd', 'signal', 'histogram'
        """
        if isinstance(data, (list, np.ndarray)):
            data = pd.Series(data)
        
        fast_ema = data.ewm(span=fast, adjust=False).mean()
        slow_ema = data.ewm(span=slow, adjust=False).mean()
        
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    @staticmethod
    def bollinger_bands(data, period=20, num_std=2):
        """
        Bollinger Bands
        
        Args:
            data: Price series
            period: Moving average period
            num_std: Number of standard deviations
            
        Returns:
            dict with 'upper', 'middle', 'lower'
        """
        if isinstance(data, (list, np.ndarray)):
            data = pd.Series(data)
        
        middle = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()
        
        upper = middle + (std * num_std)
        lower = middle - (std * num_std)
        
        return {
            'upper': upper,
            'middle': middle,
            'lower': lower
        }
    
    @staticmethod
    def atr(high, low, close, period=14):
        """
        Average True Range (ATR)
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            period: ATR period
            
        Returns:
            ATR values
        """
        high = pd.Series(high)
        low = pd.Series(low)
        close = pd.Series(close)
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr
    
    @staticmethod
    def stochastic(high, low, close, period=14, smooth_k=3, smooth_d=3):
        """
        Stochastic Oscillator
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            period: Lookback period
            smooth_k: Smoothing for %K
            smooth_d: Smoothing for %D
            
        Returns:
            dict with '%K' and '%D'
        """
        high = pd.Series(high)
        low = pd.Series(low)
        close = pd.Series(close)
        
        lowest_low = low.rolling(window=period).min()
        highest_high = high.rolling(window=period).max()
        
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        k_percent_smooth = k_percent.rolling(window=smooth_k).mean()
        d_percent = k_percent_smooth.rolling(window=smooth_d).mean()
        
        return {
            '%K': k_percent_smooth,
            '%D': d_percent
        }
    
    @staticmethod
    def crossover(series1, series2):
        """
        Detect crossover between two series
        
        Args:
            series1: First series
            series2: Second series
            
        Returns:
            Boolean array where crossover occurs
        """
        s1 = pd.Series(series1)
        s2 = pd.Series(series2)
        
        cross = (s1 > s2) & (s1.shift() <= s2.shift())
        return cross
    
    @staticmethod
    def crossunder(series1, series2):
        """
        Detect crossunder between two series
        
        Args:
            series1: First series
            series2: Second series
            
        Returns:
            Boolean array where crossunder occurs
        """
        s1 = pd.Series(series1)
        s2 = pd.Series(series2)
        
        cross = (s1 < s2) & (s1.shift() >= s2.shift())
        return cross


if __name__ == '__main__':
    # Example usage
    print("Technical Indicators Library")
    print("\nAvailable indicators:")
    print("  - EMA (Exponential Moving Average)")
    print("  - SMA (Simple Moving Average)")
    print("  - RSI (Relative Strength Index)")
    print("  - MACD (Moving Average Convergence Divergence)")
    print("  - Bollinger Bands")
    print("  - ATR (Average True Range)")
    print("  - Stochastic Oscillator")
    print("  - Crossover Detection")
