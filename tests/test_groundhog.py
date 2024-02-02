#!/usr/bin/env python3

from io import StringIO
from math import nan, isnan

import groundhog as g

################### PYTEST #####################
def test_groundhog_loop_stop(capsys, monkeypatch):
    period = 7
    monkeypatch.setattr('sys.stdin', StringIO('STOP\n'))
    return_value = g.Groundhog().run(period)
    captured = capsys.readouterr()
    assert captured.out == "There aren't enough numbers to compute statistics\n"
    assert return_value == 84

def test_groundhog_loop_not_enough(capsys, monkeypatch):
    period = 3
    monkeypatch.setattr('sys.stdin', StringIO('27.7\nSTOP\n'))
    return_value = g.Groundhog().run(period)
    captured = capsys.readouterr()
    assert captured.out == "g=nan\t\tr=nan%\t\ts=nan\nThere aren't enough numbers to compute statistics\n"
    assert return_value == 84

def test_groundhog_loop_subject_one(capsys, monkeypatch):
    period = 7
    monkeypatch.setattr('sys.stdin', StringIO('27.7\n31.0\n32.7\n34.7\n35.9\n37.4\n38.2\n39.5\n40.3\nSTOP\n'))
    return_value = g.Groundhog().run(period)
    captured = capsys.readouterr()
    assert captured.out == 'g=nan\t\tr=nan%\t\ts=nan\ng=nan\t\tr=nan%\t\ts=nan\ng=nan\t\tr=nan%\t\ts=nan\ng=nan\t\tr=nan%\t\ts=nan\ng=nan\t\tr=nan%\t\ts=nan\ng=nan\t\tr=nan%\t\ts=nan\ng=nan\t\tr=nan%\t\ts=3.46\ng=1.69\t\tr=43%\t\ts=2.82\ng=1.33\t\tr=30%\t\ts=2.50\nGlobal tendency switched 0 times\n5 weirdest values are: [40.3, 39.5]\n'
    assert return_value == 0
def test_groundhog_loop_subject(capsys, monkeypatch):
    period = 7
    monkeypatch.setattr('sys.stdin', StringIO('27.7\n31.0\n32.7\n34.7\n35.9\n37.4\n38.2\n39.5\n40.3\n65\n3\n37\n75\n223\n3271\n14\n11\nSTOP\n'))
    return_value = g.Groundhog().run(period)
    captured = capsys.readouterr()
    assert captured.out == 'g=nan\t\tr=nan%\t\ts=nan\ng=nan\t\tr=nan%\t\ts=nan\ng=nan\t\tr=nan%\t\ts=nan\ng=nan\t\tr=nan%\t\ts=nan\ng=nan\t\tr=nan%\t\ts=nan\ng=nan\t\tr=nan%\t\ts=nan\ng=nan\t\tr=nan%\t\ts=3.46\ng=1.69\t\tr=43%\t\ts=2.82\ng=1.33\t\tr=30%\t\ts=2.50\ng=4.61\t\tr=99%\t\ts=9.73\ng=4.33\t\tr=-91%\t\ts=16.73\t\ta switch occurs\ng=9.01\t\tr=3%\t\ts=16.73\t\ta switch occurs\ng=14.23\t\tr=101%\t\ts=21.33\ng=35.26\t\tr=484%\t\ts=66.38\ng=470.50\t\tr=8181%\t\ts=1120.66\ng=470.39\t\tr=-65%\t\ts=1122.34\t\ta switch occurs\ng=466.86\t\tr=-83%\t\ts=1125.67\nGlobal tendency switched 3 times\n5 weirdest values are: [11.0, 14.0, 3271.0, 37.0, 223.0]\n'
    assert return_value == 0


def test_main_help(capsys):
    return_value = g.main(["-h"])
    captured = capsys.readouterr()
    assert return_value == 0
    assert captured.out == 'SYNOPSIS\n\t./groundhog period\nDESCRIPTION\n\tperiod\t\tthe number of days defining a period\n'

def test_main_invalid_input(capsys, monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('27.7\nlala\nSTOP\n'))
    return_value = g.main(["1"])
    captured = capsys.readouterr()
    assert captured.out == 'g=nan\t\tr=nan%\t\ts=0.00\nInvalid input\n'
    assert return_value == 84

def test_main_no_args(capsys):
    return_value = g.main([])
    captured = capsys.readouterr()
    assert captured.out == 'SYNOPSIS\n\t./groundhog period\nDESCRIPTION\n\tperiod\t\tthe number of days defining a period\n'
    assert return_value == 84

def test_main_not_digit(capsys):
    return_value = g.main(["a"])
    captured = capsys.readouterr()
    assert captured.out == 'Period must be a positive integer\n'
    assert return_value == 84

def test_main_period_zero(capsys):
    return_value = g.main(["0"])
    captured = capsys.readouterr()
    assert captured.out == 'Period must be a positive integer\n'
    assert return_value == 84


def test_add_weird_value():
    groundhog = g.Groundhog()
    groundhog.add_weird_value(nan)
    assert groundhog.weirdest_values == {}
    groundhog.new_value = 16.5
    groundhog.add_weird_value(1.0)
    assert groundhog.weirdest_values == {16.5: 1.0}
    groundhog.new_value = 15
    groundhog.add_weird_value(2.0)
    assert groundhog.weirdest_values == {16.5: 1.0, 15: 2.0}


def test_update_values():
    groundhog = g.Groundhog()
    groundhog.update_values(1.0)
    assert groundhog.previous_value == 1.0
    groundhog.update_values(2.0)
    assert groundhog.previous_value == 1.0
    assert groundhog.new_value == 2.0


def test_append_values_neg():
    groundhog = g.Groundhog()
    groundhog.new_value = 1.0
    groundhog.previous_value = 2.0
    groundhog.append_values()
    assert groundhog.average_list == [0]

def test_append_values_pos():
    groundhog = g.Groundhog()
    groundhog.new_value = 2.0
    groundhog.previous_value = 1.0
    groundhog.append_values()
    val = 2.0 - 1.0
    assert groundhog.average_list == [val]


def test_increase_average_nan():
    groundhog = g.Groundhog()
    groundhog.average_list = [1.0, 2.0, 3.0]
    period = 4
    value = groundhog.increase_average(period)
    assert isnan(value) == True

def test_increase_average_zero():
    groundhog = g.Groundhog()
    groundhog.average_list = []
    period = -1
    value = groundhog.increase_average(period)
    assert value == 0

def test_increase_average_num():
    groundhog = g.Groundhog()
    groundhog.average_list = [1.0, 2.0, 3.0]
    period = 2
    value = groundhog.increase_average(period)
    assert value == 2.5


def test_relative_variation_nan():
    groundhog = g.Groundhog()
    groundhog.values_list = [1.0, 2.0, 3.0]
    period = 4
    assert isnan(groundhog.relative_variation(period)) == True

def test_relative_variation_zero():
    groundhog = g.Groundhog()
    groundhog.values_list = [0.0, 2.0, 3.0]
    period = 2
    assert groundhog.relative_variation(period) == 0

def test_relative_variation_num():
    groundhog = g.Groundhog()
    groundhog.values_list = [1.0, 2.0, 3.0]
    period = 2
    assert groundhog.relative_variation(period) == 200


def test_standard_deviation_nan():
    groundhog = g.Groundhog()
    groundhog.values_list = [1.0, 2.0, 3.0]
    period = 4
    value = groundhog.standard_deviation(period)
    assert isnan(value) == True

def test_standard_deviation_num():
    groundhog = g.Groundhog()
    groundhog.values_list = [1.0, 2.0, 3.0]
    period = 2
    value = groundhog.standard_deviation(period)
    assert value == 0.5

def test_weirdness_level_nan():
    groundhog = g.Groundhog()
    groundhog.current_s = nan
    assert isnan(groundhog.weirdness_level()) == True
def test_weirdness_level_low():
    groundhog = g.Groundhog()
    groundhog.current_s = 1
    groundhog.current_g = 10
    groundhog.new_value = 5
    assert groundhog.weirdness_level() == abs(5 - (10 - 1 * 2))