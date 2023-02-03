import numpy as np
import pandas as pd
import numpy_financial as npf


class Project:
    def __init__(self,
                 price: float,
                 file_name: str,
                 fixed_cost: float,
                 investment: float,
                 risk_free_rate: float,
                 production_cost: float):
        data_units = pd.read_csv(file_name)
        gross_income = data_units * (price - production_cost)
        operating_income: pd.DataFrame = gross_income - fixed_cost
        operating_income.insert(loc=0,
                                column=operating_income.columns.values[0].replace('1', '0'),
                                value=-investment)

        self.nvp_irr: pd.DataFrame = pd.DataFrame()
        self.nvp_irr['NPV'] = operating_income.apply(lambda row: np.round(npf.npv(risk_free_rate, row), 1), axis=1)
        self.nvp_irr['IRR'] = operating_income.apply(lambda row: npf.irr(row), axis=1)

    def prob(self, p: float, mode: int, lower: bool = False):
        m = ['NPV', 'IRR'][mode]
        prob = len(self.nvp_irr[self.nvp_irr[m] > p]) / len(self.nvp_irr[m])
        if lower:
            prob = 1 - prob

        return prob


print("Homework 1.1")

p1 = Project(price=5.0,
             file_name="Data_OilCompany.csv",
             fixed_cost=40_000,
             investment=1_800_000,
             risk_free_rate=0.03,
             production_cost=0.8, )

print(p1.nvp_irr.head())

print("probability that the IRR is over the Risk free rate: ")

print(p1.prob(p=0.03, mode=1))

print("probability that the IRR is over the 35%: ")

print(p1.prob(p=0.35, mode=1))

print("probability that the project value is over $2M: ")

print(p1.prob(p=2_000_000, mode=0))

print("probability that the IRR is between 10% and 20%: ")

print(p1.prob(p=0.2, mode=1, lower=True) - p1.prob(p=0.1, mode=1, lower=True))

print("\n\nHomework 1.2\n")


class Oldstock:
    def __init__(self, s0: float, risk_free_rate: float, average_div: float, increase: float):
        self.s0 = s0
        self.risk_free_rate = risk_free_rate
        self.average_div = average_div
        self.increase = increase
        self.fair_value = average_div * (1 + increase) / (risk_free_rate - increase)
        self.ret = self.fair_value / s0 - 1

    def montecarlo_norm_increase(self, iterations: int, mean: float, sd: float):
        increases = np.random.normal(mean, sd, iterations)
        fair_values = (increases + 1) * self.average_div / (self.risk_free_rate - self.increase)
        returns = fair_values / self.s0 - 1
        return pd.DataFrame({"increase": increases, "fair_value": fair_values, "return": returns})


print("I have selected option c 'Buy an old company stock' with the following characteristics")

print("S0=15 \nrisk_free_rate=0.03 \naverage_div=0.4 \nincrease=.01")

investment1 = Oldstock(s0=15,
                       risk_free_rate=0.03,
                       average_div=0.4,
                       increase=.01)

print(
    f"this would mean that in this case the fair value is {round(investment1.fair_value, 2)} "
    f"and the return will be: {round(investment1.ret * 100, 2)} %")

mean = .012
sd = .05
print(f"\nIn order to evaluate how this investment would performance with different increases"
      f"\nand the probability of this scenarios, we have asumed normal distribution with mean "
      f"\n{mean} and a standard deviation of {sd}. ")

scenarios = investment1.montecarlo_norm_increase(100_000, mean, sd)

ret_op = .372

print(f"\nCurrenly, the decision on this exescise is to not invest in this option because the"
      f"\nexpected return rate is {round(investment1.ret * 100, 2)}% whereas the best option's expected return rate was {ret_op * 100}%"
      f"\nIn order to make my decision change, the return should be higher than the best option's")

cases_higher = scenarios[scenarios['return'] > ret_op]
expected_return_cases_higher = cases_higher['return'].mean()
probability_higher = len(cases_higher) / len(scenarios)

min_increase = cases_higher['increase'].min()

expected_return_cases_lower = scenarios[scenarios['return'] < ret_op]['return'].mean()

print(f"\nWith this distribution, the probability of getting a highier return than current best"
      f"\noption is {probability_higher} but if this happens, the expected return will be"
      f" {round(expected_return_cases_higher * 100, 2)}%.")
print(f"\nIn order for this to happen the increase will have to be at least {round(min_increase, 4)}")

print('\nDecision Tree:\n')

print(f'                      ____________________________')
print(f'                      |increase > {round(min_increase, 4)}          |')
print(f'                      |return > {ret_op * 100} %           |')
print(f'                      |Expected return = {round(expected_return_cases_higher * 100, 2)} % |')
print(f'                      ---------------------------- ')
print(f'                   p={probability_higher}')
print(f'                 /')
print(f'________________/')
print(f'|increase=0.1  |')
print(f'|return={round(investment1.ret * 100, 2)} %|')
print(f'----------------\\ ')
print(f'                 \\')
print(f'                   p={round(1 - probability_higher, 4)}')
print(f'                      ____________________________')
print(f'                      |increase < {round(min_increase, 4)}          |')
print(f'                      |return < {ret_op * 100} %           |')
print(f'                      |Expected return = {round(expected_return_cases_lower * 100, 2)} % |')
print(f'                      ---------------------------- ')

overall_er=(expected_return_cases_lower * (1 - probability_higher) + expected_return_cases_higher * probability_higher)
print(f"The overall expected return will be "
      f"{round(100 * overall_er, 2)}%")
