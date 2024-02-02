#!/usr/bin/env python3

import sys
from math import sqrt, nan, isnan


class Groundhog:  # Groundhog class

    # --------- Init Values --------- #

    def __init__(self) -> None:
        self.tendency = 0
        self.previous_value = nan
        self.new_value = nan
        self.current_period = 0
        self.average_list: list[float] = []
        self.values_list: list[float] = []
        self.weirdest_values: dict[float, float] = {}
        self.previous_r = nan
        self.current_g = nan
        self.current_s = nan
        self.current_r = nan

    # --------- Groundhog main loop --------- #

    def run(self, period: int) -> int:

        while True:
            input = sys.stdin.readline()
            input = input[:-1]

            if input == "STOP":
                break

            try:
                float(input)
            except ValueError:
                print("Invalid input")
                return 84

            self.current_period += 1
            self.update_values(input)
            self.append_values()
            self.update_grs(period)

            print(
                f"g={self.current_g:.2f}\t\tr={self.current_r:.0f}%\t\ts={self.current_s:.2f}",
                end="",
            )

            if self.current_period > period:
                self.add_weird_value(self.weirdness_level())

            self.check_switch()
            self.update_relative_variation(period)

            print()

        return self.print_tendency_and_weirdest_values(period)

    # --------- Update Lists --------- #

    def update_values(self, input: str) -> None:
        if self.previous_value is nan:
            self.previous_value = float(input)
        else:
            self.previous_value = self.new_value
        self.new_value = float(input)

    # append values
    def append_values(self) -> None:
        self.values_list.append(self.new_value)
        if self.new_value - self.previous_value > 0:
            self.average_list.append(self.new_value - self.previous_value)
        else:
            self.average_list.append(0)

    # --------- Update GRS --------- #

    def update_grs(self, period: int) -> None:
        self.current_g = self.increase_average(period)
        self.current_r = self.relative_variation(period)
        self.current_s = self.standard_deviation(period)

    # G
    def increase_average(self, period: int) -> float:
        if len(self.average_list) < period + 1:
            return nan
        else:
            if len(self.average_list) == 0:
                return 0
            list_over_period = self.average_list[-period:]
            return sum(list_over_period) / len(list_over_period)

    # R
    def relative_variation(self, period: int) -> float:
        if len(self.values_list) < period + 1:
            return nan
        else:
            value_n_days_ago = self.values_list[-period - 1]
            latest_value = self.values_list[-1]
            if value_n_days_ago == 0:
                return 0
            return (latest_value - value_n_days_ago) / abs(value_n_days_ago) * 100

    # S
    def standard_deviation(self, period: int) -> float:
        if len(self.values_list) < period:
            return nan
        else:
            list_over_period = self.values_list[-period:]
            mean = sum(list_over_period) / len(list_over_period)
            variance = sum((x - mean) ** 2 for x in list_over_period) / len(
                list_over_period
            )
            return sqrt(variance)

    # Update Relative Variation Value
    def update_relative_variation(self, period: int) -> None:
        if self.relative_variation(period) != 0:
            self.previous_r = self.relative_variation(period)

    # --------- Weird Values --------- #

    def weirdness_level(self) -> float:
        if isnan(self.current_s):
            return nan
        else:
            high = self.current_g + (2 * self.current_s)
            low = self.current_g - (2 * self.current_s)

            if self.new_value < low:
                return abs(self.new_value - low)
            if self.new_value > high:
                return abs(self.new_value - high)
            return max(abs(low - self.new_value), abs(self.new_value - high))

    def add_weird_value(self, weirdness_level: float) -> None:
        if isnan(weirdness_level):
            return
        self.weirdest_values[self.new_value] = weirdness_level

    # --------- Switches --------- #

    def check_switch(self) -> None:
        if self.previous_r is not None:
            if (self.current_r > 0 and self.previous_r < 0) or (
                self.current_r < 0 and self.previous_r > 0
            ):
                self.tendency += 1
                print("\t\ta switch occurs", end="")

    # --------- Print --------- #

    def print_tendency_and_weirdest_values(self, period: int) -> int:
        if period > self.current_period:
            print("There aren't enough numbers to compute statistics")
            return 84
        print("Global tendency switched " + str(self.tendency) + " times")
        print("5 weirdest values are: ", end="")
        self.print_top_5_weirdest_values()
        return 0

    def print_top_5_weirdest_values(self) -> None:
        sorted_map = sorted(
            self.weirdest_values.items(), key=lambda x: x[1], reverse=True
        )
        first_five = [x[0] for x in sorted_map[:5]]
        print(first_five)


# --------------------------- END Groundhog CLASS --------------------------- #

# --------------------------- MAIN --------------------------- #
def main(args: list[str]) -> int:  # Main

    # help message => no args or -h
    if len(args) != 1 or args[0] == "-h":
        print("SYNOPSIS")
        print("\t./groundhog period")
        print("DESCRIPTION")
        print("\tperiod\t\tthe number of days defining a period")
        if len(args) != 1:
            return 84
        return 0

    # start groundhog
    if args[0].isdigit():
        period = int(args[0])
        if period <= 0:
            print("Period must be a positive integer")
            return 84

        g = Groundhog()
        return g.run(period)
    else:
        print("Period must be a positive integer")
        return 84