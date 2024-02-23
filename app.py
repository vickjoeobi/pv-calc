import streamlit as st
from funcs import calculate_annual_energy_production, calculate_fit_revenue, calculate_annual_costs, calculate_net_earnings, calculate_project_npv, calculate_pv_net_income, find_lcoe

# Streamlit app layout
st.title('Calculations')

# Inputs
st.sidebar.header('Input Parameters')
PROJECT_LIFETIME = st.sidebar.number_input('Project Lifetime (years)', value=20)
NOMINAL_POWER_KWP = st.sidebar.number_input('Nominal Power (kWp)', value=110000)
ANNUAL_YIELD_KWH_PER_KWP = st.sidebar.number_input('Annual Yield (kWh/kWp)', value=102.6)
DEGRADATION_RATE_PER_YEAR = st.sidebar.number_input('Degradation Rate Per Year (%)', value=0.3) / 100
FIT_YEARS = st.sidebar.number_input('FIT Years', value=20)
PRICE_PER_KWH_EUR = st.sidebar.number_input('Price Per kWh (EUR)', value=0.15)
INDEX_RATE = st.sidebar.number_input('Index Rate (%)', value=0.0) / 100
TOTAL_INSTALLATION_COST_EUR = st.sidebar.number_input('Total Installation Cost (EUR)', value=50000000)
INSURANCE_PREMIUM_RATE = st.sidebar.number_input('Insurance Premium Rate (%)', value=0.138) / 100
MAINTENANCE_RATE = st.sidebar.number_input('Maintenance Rate (%)', value=2.7) / 100
INFLATION_RATE = st.sidebar.number_input('Inflation Rate (%)', value=2.0) / 100
DISCOUNT_RATE = st.sidebar.number_input('Discount Rate (%)', value=4.0) / 100

# Calculations
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
yearly_energy_productions = calculate_annual_energy_production(NOMINAL_POWER_KWP, ANNUAL_YIELD_KWH_PER_KWP, DEGRADATION_RATE_PER_YEAR, PROJECT_LIFETIME)
revenue_from_fit = calculate_fit_revenue(yearly_energy_productions, PRICE_PER_KWH_EUR, FIT_YEARS, INDEX_RATE)
insurance_costs = calculate_annual_costs(INSURANCE_PREMIUM_RATE, TOTAL_INSTALLATION_COST_EUR, INFLATION_RATE, PROJECT_LIFETIME)
maintenance_costs = calculate_annual_costs(MAINTENANCE_RATE, TOTAL_INSTALLATION_COST_EUR, INFLATION_RATE, PROJECT_LIFETIME)
earnings = calculate_net_earnings(revenue_from_fit, insurance_costs, maintenance_costs)
npv = calculate_project_npv(earnings, DISCOUNT_RATE, TOTAL_INSTALLATION_COST_EUR)
present_value_of_net_income = calculate_pv_net_income(npv, TOTAL_INSTALLATION_COST_EUR)

# Output
st.header('Results')
st.write(f'Nominal Power (kWp): {nominal_power_output}')
st.write(f'Present Value of Net Income (€): {present_value_of_net_income:.2f}')
st.write(f'Levelised Costs of Electricity "LCOE" (€/kWh): {lcoe:.6f}')
st.write('Return on Investment (%): N.A.')  # Placeholder for actual ROI calculation
st.write(f'NPV (€): {npv:.2f}')

