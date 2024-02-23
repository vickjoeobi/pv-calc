from datetime import datetime, date

def calculate_annual_energy_production(nominal_power_kwp, annual_yield_kwh_per_kwp, degradation_rate_per_year, project_lifetime):
    """Calculates yearly energy production accounting for power degradation."""
    return [
        nominal_power_kwp * annual_yield_kwh_per_kwp * (1 - degradation_rate_per_year * (year - 1))
        for year in range(1, project_lifetime + 1)
    ]

def calculate_fit_revenue(yearly_energy_productions, price_per_kwh, fit_years, index_rate):
    """Calculates revenue from Feed-in Tariff (FIT) over the project lifetime."""
    return [
        production * price_per_kwh * (1 + index_rate) ** year
        for year, production in enumerate(yearly_energy_productions, start=1)
    ]

def calculate_annual_costs(rate, total_cost, inflation_rate, project_lifetime):
    """Calculates yearly costs for insurance and maintenance."""
    return [
        -rate * total_cost * (1 + inflation_rate) ** (year - 1)
        for year in range(1, project_lifetime + 1)
    ]

def calculate_net_earnings(revenue_from_fit, insurance_costs, maintenance_costs):
    """Calculates net earnings by subtracting costs from FIT revenue."""
    return [
        revenue + insurance + maintenance
        for revenue, insurance, maintenance in zip(revenue_from_fit, insurance_costs, maintenance_costs)
    ]

def calculate_xnpv(discount_rate, cash_flows, dates):
    """Calculates the Net Present Value (NPV) for non-periodic cash flows."""
    min_date = min(dates)
    return sum(
        cash_flow / (1 + discount_rate) ** ((date - min_date).days / 365)
        for cash_flow, date in zip(cash_flows, dates)
    )

def calculate_project_npv(earnings, discount_rate, total_installation_cost):
    """Calculates the NPV of the project including the initial investment."""
    start_year = datetime.now().year - 1
    dates = [date(start_year, 1, 1)] + [date(start_year + i, 1, 1) for i in range(1, len(earnings) + 1)]
    cash_flows = [-total_installation_cost] + earnings
    return calculate_xnpv(discount_rate, cash_flows, dates)

def calculate_pv_net_income(npv, total_installation_cost):
    """Calculates the Present Value of Net Income."""
    return npv + total_installation_cost

def find_lcoe(nominal_power_kwp, annual_yield_kwh_per_kwp, degradation_rate_per_year, project_lifetime, price_per_kwh, fit_years, index_rate, insurance_premium_rate, maintenance_rate, inflation_rate, discount_rate, total_installation_cost, max_iterations=100000, tolerance=1e-6):
    """Finds the Levelized Cost of Electricity (LCOE) to match the investment goal."""
    lcoe_guess = price_per_kwh
    step = 0.01
    for _ in range(max_iterations):
        yearly_energy_productions = calculate_annual_energy_production(nominal_power_kwp, annual_yield_kwh_per_kwp, degradation_rate_per_year, project_lifetime)
        revenue_from_fit = calculate_fit_revenue(yearly_energy_productions, lcoe_guess, fit_years, index_rate)
        earnings = calculate_net_earnings(
            revenue_from_fit,
            calculate_annual_costs(insurance_premium_rate, total_installation_cost, inflation_rate, project_lifetime),
            calculate_annual_costs(maintenance_rate, total_installation_cost, inflation_rate, project_lifetime)
        )
        npv = calculate_project_npv(earnings, discount_rate, total_installation_cost)
        present_value_of_net_income = calculate_pv_net_income(npv, total_installation_cost)
        
        if abs(present_value_of_net_income - total_installation_cost) <= tolerance:
            return lcoe_guess
        elif present_value_of_net_income < total_installation_cost:
            lcoe_guess += step
        else:
            lcoe_guess -= step
            step /= 2
    
    return lcoe_guess

if __name__ == "__main__":

    PROJECT_LIFETIME = 20  # years
    NOMINAL_POWER_KWP = 110000  # kWp
    ANNUAL_YIELD_KWH_PER_KWP = 102.6  # kWh/kWp
    DEGRADATION_RATE_PER_YEAR = 0.003  # %/year
    FIT_YEARS = 20
    PRICE_PER_KWH_EUR = 0.15  # EUR/kWh
    INDEX_RATE = 0.0  # %
    TOTAL_INSTALLATION_COST_EUR = 50000000  # EUR
    INSURANCE_PREMIUM_RATE = 0.00138  # % of total installation cost/year
    MAINTENANCE_RATE = 0.027  # % of total installation cost/year
    INFLATION_RATE = 0.02  # %/year
    DISCOUNT_RATE = 0.04  # %

    # Outputs
    lcoe = find_lcoe(
        NOMINAL_POWER_KWP,
        ANNUAL_YIELD_KWH_PER_KWP,
        DEGRADATION_RATE_PER_YEAR,
        PROJECT_LIFETIME,
        PRICE_PER_KWH_EUR,
        FIT_YEARS,
        INDEX_RATE,
        INSURANCE_PREMIUM_RATE,
        MAINTENANCE_RATE,
        INFLATION_RATE,
        DISCOUNT_RATE,
        TOTAL_INSTALLATION_COST_EUR
    )
    nominal_power_output = NOMINAL_POWER_KWP
    return_on_investment = "N.A."
    npv = calculate_project_npv(
        calculate_net_earnings(
            calculate_fit_revenue(
                calculate_annual_energy_production(NOMINAL_POWER_KWP, ANNUAL_YIELD_KWH_PER_KWP, DEGRADATION_RATE_PER_YEAR, PROJECT_LIFETIME),
                PRICE_PER_KWH_EUR,
                FIT_YEARS,
                INDEX_RATE
            ),
            calculate_annual_costs(INSURANCE_PREMIUM_RATE, TOTAL_INSTALLATION_COST_EUR, INFLATION_RATE, PROJECT_LIFETIME),
            calculate_annual_costs(MAINTENANCE_RATE, TOTAL_INSTALLATION_COST_EUR, INFLATION_RATE, PROJECT_LIFETIME)
        ),
        DISCOUNT_RATE,
        TOTAL_INSTALLATION_COST_EUR
    )
    present_value_of_net_income = calculate_pv_net_income(npv, TOTAL_INSTALLATION_COST_EUR)

    # Print the results
    print(f"LCOE: {lcoe:.6f} EUR/kWh")
    print(f"Nominal Power Output: {nominal_power_output} kWp")
    print(f"Return on Investment: {return_on_investment}")
    print(f"NPV: {npv:.2f} EUR")
    print(f"Present Value of Net Income: {present_value_of_net_income:.2f} EUR")