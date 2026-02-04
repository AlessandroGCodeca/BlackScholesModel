# Black-Scholes Model

This project implements the **Black-Scholes Model** in Python to calculate fair prices and Greeks (Delta, Gamma, Theta, Vega, Rho) for options contracts. It allows for comparison between manual analytical formulas and the `py_vollib` library.

## Features

- **Option Pricing:** Calculates the theoretical price of Call and Put options.
- **Greeks Calculation:** Computes Delta, Gamma, Theta, Vega, and Rho.
- **Dual Implementation:** Compares manual calculations with `py_vollib` for verification.

## Prerequisites

- Python 3.x
- `pip` package manager

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd black-scholes-model
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install py_vollib numpy pandas scipy
   ```

## Usage

Run the main script to see the calculations for a sample Call Option:

```bash
python black_scholes.py
```

## Parameters

The script currently uses hardcoded parameters for demonstration:
- **Stock Price (S):** 34.03
- **Strike Price (K):** 40.00
- **Risk-free Rate (r):** 0.0412
- **Time to Maturity (T):** 30 days
- **Volatility (sigma):** 0.35

You can modify these variables in `black_scholes.py` to test different scenarios.
