# Black-Scholes Model

This project implements the **Black-Scholes Model** in Python to calculate fair prices and Greeks (Delta, Gamma, Theta, Vega, Rho) for options contracts. It allows for comparison between manual analytical formulas and the `py_vollib` library.

## Features

- **Option Pricing:** Calculates the theoretical price of Call and Put options.
- **Greeks Calculation:** Computes Delta, Gamma, Theta, Vega, and Rho.
- **Dual Implementation:** Compares manual calculations with `py_vollib` for verification.
- **Flexible Inputs:** Support for command-line arguments to test different scenarios.

## Prerequisites

- Python 3.x
- `pip` package manager

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AlessandroGCodeca/BlackScholesModel.git
   cd BlackScholesModel
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

Run the script with default values:
```bash
python black_scholes.py
```

### Custom Parameters

You can pass custom parameters via the command line:

```bash
python black_scholes.py --price 100 --strike 95 --time 30 --volatility 0.2 --type c
```

**Arguments:**
- `--price`: Current price of the underlying asset (Default: 34.03)
- `--strike`: Strike price of the option (Default: 40.00)
- `--rate`: Risk-free interest rate (decimal) (Default: 0.0412)
- `--time`: Time to expiration in days (Default: 30)
- `--volatility`: Volatility of the underlying asset (decimal) (Default: 0.35)
- `--type`: Option type, 'c' for Call or 'p' for Put (Default: 'c')