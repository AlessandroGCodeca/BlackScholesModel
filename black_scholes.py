#!/usr/bin/env python3
import argparse
import numpy as np
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.greeks.analytical import delta, gamma, theta, vega, rho
from scipy.stats import norm
from typing import Tuple, Dict, Optional

class BlackScholesModel:
    """
    A class to calculate Black-Scholes option prices and Greeks using both
    manual implementation and the py_vollib library.
    """

    def __init__(self, S: float, K: float, T: float, r: float, sigma: float):
        """
        Initialize the Black-Scholes Model.

        Args:
            S (float): Current price of the underlying asset.
            K (float): Strike price of the option.
            T (float): Time to expiration in years.
            r (float): Risk-free interest rate (decimal, e.g., 0.05 for 5%).
            sigma (float): Volatility of the underlying asset (decimal, e.g., 0.2 for 20%).
        """
        if T <= 0 or sigma < 0:
            raise ValueError("Time to expiration must be positive and volatility must be non-negative.")
        
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def _calculate_d1_d2(self) -> Tuple[float, float]:
        """
        Calculate d1 and d2 parameters for Black-Scholes formula.

        Returns:
            Tuple[float, float]: The calculated d1 and d2 values.
        """
        d1 = (np.log(self.S / self.K) + (self.r + self.sigma**2 / 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return d1, d2

    def calculate_price(self, option_type: str = 'c') -> Dict[str, Optional[float]]:
        """
        Calculate option price.

        Args:
            option_type (str): 'c' for Call, 'p' for Put.

        Returns:
            Dict[str, Optional[float]]: Prices from 'Manual' calculation and 'Py_Vollib'.
        """
        d1, d2 = self._calculate_d1_d2()
        try:
            if option_type == 'c':
                price = self.S * norm.cdf(d1, 0, 1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2, 0, 1)
            elif option_type == 'p':
                price = self.K * np.exp(-self.r * self.T) * norm.cdf(-d2, 0, 1) - self.S * norm.cdf(-d1, 0, 1)
            else:
                raise ValueError("Option type must be 'c' or 'p'")
            
            lib_price = bs(option_type, self.S, self.K, self.T, self.r, self.sigma)
            return {"Manual": price, "Py_Vollib": lib_price}
        except Exception as e:
            print(f"Error calculating price: {e}")
            return {"Manual": None, "Py_Vollib": None}

    def calculate_greeks(self, option_type: str = 'c') -> Dict[str, Dict[str, Optional[float]]]:
        """
        Calculate all Greeks (Delta, Gamma, Theta, Vega, Rho).

        Args:
            option_type (str): 'c' for Call, 'p' for Put.

        Returns:
            Dict[str, Dict[str, Optional[float]]]: Dictionary containing Greeks from both methods.
        """
        d1, d2 = self._calculate_d1_d2()
        greeks = {}

        # Delta
        try:
            if option_type == 'c':
                delta_val = norm.cdf(d1, 0, 1)
            else:
                delta_val = -norm.cdf(-d1, 0, 1)
            greeks['Delta'] = {"Manual": delta_val, "Py_Vollib": delta(option_type, self.S, self.K, self.T, self.r, self.sigma)}
        except Exception: 
            greeks['Delta'] = {"Manual": None, "Py_Vollib": None}

        # Gamma
        try:
            gamma_val = norm.pdf(d1, 0, 1) / (self.S * self.sigma * np.sqrt(self.T))
            greeks['Gamma'] = {"Manual": gamma_val, "Py_Vollib": gamma(option_type, self.S, self.K, self.T, self.r, self.sigma)}
        except Exception:
            greeks['Gamma'] = {"Manual": None, "Py_Vollib": None}

        # Theta
        try:
            if option_type == 'c':
                theta_val = -self.S * norm.pdf(d1, 0, 1) * self.sigma / (2 * np.sqrt(self.T)) - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2, 0, 1)
            else:
                theta_val = -self.S * norm.pdf(d1, 0, 1) * self.sigma / (2 * np.sqrt(self.T)) + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2, 0, 1)
            greeks['Theta'] = {"Manual": theta_val / 365, "Py_Vollib": theta(option_type, self.S, self.K, self.T, self.r, self.sigma)}
        except Exception:
            greeks['Theta'] = {"Manual": None, "Py_Vollib": None}

        # Vega
        try:
            vega_val = self.S * norm.pdf(d1, 0, 1) * np.sqrt(self.T)
            greeks['Vega'] = {"Manual": vega_val * 0.01, "Py_Vollib": vega(option_type, self.S, self.K, self.T, self.r, self.sigma)}
        except Exception:
            greeks['Vega'] = {"Manual": None, "Py_Vollib": None}

        # Rho
        try:
            if option_type == 'c':
                rho_val = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(d2, 0, 1)
            else:
                rho_val = -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-d2, 0, 1)
            greeks['Rho'] = {"Manual": rho_val * 0.01, "Py_Vollib": rho(option_type, self.S, self.K, self.T, self.r, self.sigma)}
        except Exception:
            greeks['Rho'] = {"Manual": None, "Py_Vollib": None}

        return greeks

def main():
    parser = argparse.ArgumentParser(description="Calculate Black-Scholes Option Price and Greeks.")
    parser.add_argument("--price", type=float, default=34.03, help="Underlying asset price (S). Default: 34.03")
    parser.add_argument("--strike", type=float, default=40.00, help="Strike price (K). Default: 40.00")
    parser.add_argument("--rate", type=float, default=0.0412, help="Risk-free interest rate (r). Default: 0.0412")
    parser.add_argument("--time", type=float, default=30, help="Time to expiration in days. Default: 30")
    parser.add_argument("--volatility", type=float, default=0.35, help="Volatility (sigma). Default: 0.35")
    parser.add_argument("--type", type=str, choices=['c', 'p'], default='c', help="Option type: 'c' for Call, 'p' for Put. Default: 'c'")

    args = parser.parse_args()

    # Convert time from days to years
    T_years = args.time / 365.0

    print("--- Black Scholes Model ---")
    print(f"Parameters: S={args.price}, K={args.strike}, r={args.rate}, T={T_years:.4f} ({args.time} days), sigma={args.volatility}")
    print(f"Option Type: {'Call' if args.type == 'c' else 'Put'}\n")

    model = BlackScholesModel(args.price, args.strike, T_years, args.rate, args.volatility)
    
    # Calculate Price
    prices = model.calculate_price(args.type)
    print(f"Option Price:\n  Manual:    {prices['Manual']}\n  Py_Vollib: {prices['Py_Vollib']}\n")

    # Calculate Greeks
    greeks = model.calculate_greeks(args.type)
    for name, values in greeks.items():
        print(f"{name}:\n  Manual:    {values['Manual']}\n  Py_Vollib: {values['Py_Vollib']}\n")

if __name__ == "__main__":
    main()
