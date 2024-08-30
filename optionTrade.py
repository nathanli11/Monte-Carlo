# Class that describes a simple option instrument and implements methods like the pay-off of the option
from __future__ import annotations  # to reference OptionTrade objects in the class
import datetime


class OptionTrade(object):
    CALL_LABEL: str = 'Call'
    PUT_LABEL: str = 'Put'
    AMER_LABEL: str = 'American'
    EURO_LABEL: str = 'European'

    # constructor from individual members values
    def __init__(self, callPut: str, mat: datetime, k: float, ex: str):
        self.opt_type: str = callPut
        self.mat_date: datetime = mat
        self.strike: float = k
        self.exercise: str = ex
        # checks on the definition of type, exercise and strike
        self.definition_ok = (self.is_a_call() or self.is_a_put()) and \
                             (self.is_european() or self.is_american()) and 0.0 <= self.strike

    def __str__(self) -> str:
        return self.exercise + ' ' + self.opt_type + ' ' + self.mat_date.strftime("%d-%b-%Y") \
                 + ' @ ' + str(self.strike)

    def is_american(self) -> bool:
        return self.exercise == OptionTrade.AMER_LABEL

    def is_european(self) -> bool:
        return self.exercise == OptionTrade.EURO_LABEL

    def is_a_call(self) -> bool:
        return self.opt_type == OptionTrade.CALL_LABEL

    def is_a_put(self) -> bool:
        return self.opt_type == OptionTrade.PUT_LABEL

    def clone_as_call(self) -> OptionTrade:
        return OptionTrade(self.mat_date, OptionTrade.CALL_LABEL, self.exercise, self.strike)

    def clone_as_put(self) -> OptionTrade:
        return OptionTrade(self.mat_date, OptionTrade.PUT_LABEL, self.exercise, self.strike)

    # payoff of the option: max(S - K, 0) for a call and max(K - S, 0) for a put
    def pay_off(self, spot_price: float) -> float:
        if self.is_a_call():
            return max(spot_price - self.strike, 0.0)
        elif self.is_a_put():
            return max(self.strike - spot_price, 0.0)
        else:
            return 0.0
