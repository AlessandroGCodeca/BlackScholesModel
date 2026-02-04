import numpy as np
import pandas as pd
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.greeks.analytical import delta, gamma, theta, vega, rho
from scipy.stats import norm

# Define variables
S = 34.03
r = 0.0412
K = 40.00
T = 30/365
sigma = 0.35 #assumed volatility

def blackScholes(r, S, K, T, sigma, type="c"):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
        if type == "c":
            price = S*norm.cdf(d1, 0, 1) - K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
        elif type == "p":
            price = K*np.exp(-r*T)*norm.cdf(-d2, 0, 1) - S*norm.cdf(-d1, 0, 1)
        return price, bs(type, S, K, T, r, sigma)
    except Exception as e:
        print(f"Error in blackScholes: {e}")
        return None, None

def delta_value(r, S, K, T, sigma, type='c'):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    try:
        if type == "c":
            delta_val = norm.cdf(d1, 0, 1)
        elif type == "p":
            delta_val = -norm.cdf(-d1, 0, 1)
        return delta_val, delta(type, S, K, T, r, sigma)
    except Exception as e:
        print(f"Error in delta_value: {e}")
        return None, None

def gamma_value(r, S, K, T, sigma, type='c'):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    try:
        gamma_val = norm.pdf(d1, 0, 1)/(S*sigma*np.sqrt(T))
        return gamma_val, gamma(type, S, K, T, r, sigma)
    except Exception as e:
        print(f"Error in gamma_value: {e}")
        return None, None

def theta_value(r, S, K, T, sigma, type='c'):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
        if type == "c":
            theta_val = -S*norm.pdf(d1, 0, 1)*sigma/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
        elif type == "p":
            theta_val = -S*norm.pdf(d1, 0, 1)*sigma/(2*np.sqrt(T)) + r*K*np.exp(-r*T)*norm.cdf(-d2, 0, 1)
        return theta_val/365, theta(type, S, K, T, r, sigma)
    except Exception as e:
        print(f"Error in theta_value: {e}")
        return None, None

def vega_value(r, S, K, T, sigma, type='c'):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    try:
        vega_calc = S*norm.pdf(d1, 0, 1)*np.sqrt(T)
        return vega_calc*0.01, vega(type, S, K, T, r, sigma)
    except Exception as e:
        print(f"Error in vega_value: {e}")
        return None, None

def rho_value(r, S, K, T, sigma, type='c'):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
        if type == "c":
            rho_val = K*T*np.exp(-r*T)*norm.cdf(d2, 0, 1)
        elif type == "p":
            rho_val = -K*T*np.exp(-r*T)*norm.cdf(-d2, 0, 1)
        return rho_val*0.01, rho(type, S, K, T, r, sigma)
    except Exception as e:
        print(f"Error in rho_value: {e}")
        return None, None

if __name__ == "__main__":
    print("--- Black Scholes Model ---")
    print(f"Parameters: S={S}, K={K}, r={r}, T={T:.4f}, sigma={sigma}\n")
    
    option_type = 'c'
    print(f"Calculating for Option Type: {option_type}\n")

    price_manual, price_lib = blackScholes(r, S, K, T, sigma, option_type)
    print(f"Option Price:\n  Manual:    {price_manual}\n  Py_Vollib: {price_lib}\n")

    # Greeks
    greeks = {
        "Delta": delta_value,
        "Gamma": gamma_value,
        "Theta": theta_value,
        "Vega": vega_value,
        "Rho": rho_value
    }

    for name, func in greeks.items():
        val_manual, val_lib = func(r, S, K, T, sigma, option_type)
        print(f"{name}:\n  Manual:    {val_manual}\n  Py_Vollib: {val_lib}\n")
