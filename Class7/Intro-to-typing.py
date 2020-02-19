"""Module to showcase examples of adding type hints to functions."""

from typing import Union

import numpy as np
import pandas as pd


def bin_departure_delays(delay_min: float) -> str:
    """Fcn to bin flight delays via if-else statements, rather than cut()
       function, to compare performance of computation in Class 5.
    """
    if (delay_min >= -60.0) & (delay_min < 15.0):
        return "no_delay"
    elif (delay_min >= 15.0) & (delay_min < 30.0):
        return "small_delay"
    elif (delay_min >= 30.0) & (delay_min < 60.0):
        return "medium_delay"
    elif (delay_min >= 60.0) & (delay_min < 120.0):
        return "big_delay"
    elif (delay_min >= 120.0):
        return "compensated_delay"
    else:
        return "missing_delay"


def delays_requiring_compensation(arrival_delay: np.float64,
                                  departure_delay: np.float64) -> int:
    """Fcn to return if arrival and/or departure delay resulted in passenger
       compensation.

       Arguments:
           - arrival_delay:   delay in minutes
           - departure_delay: delay in minutes

       Returns:
           - number of delays (arrival and or departure) that were delayed
             so long that passenger got compensated
    """
    count = 0
    if (arrival_delay >= 3.0 * 60.0) | (departure_delay >= 2.0 * 60.0):
        # If arrival delay is 3+ hours, or if departure delay is 2+ hours:
        count += 1
    return count


def delays_requiring_compensation_vec(
        arrival_delay: Union[pd.Series, np.ndarray],
        departure_delay: Union[pd.Series, np.ndarray]) -> Union[pd.Series,
                                                                np.ndarray]:
    """Vectorized fcn to return if arrival and/or departure delay resulted in
       passenger compensation.

       Arguments:
           - arrival_delay:   vector of flight departure delays, in minutes
           - departure_delay: vector of flight arrival delays, in minutes

       Returns:
           - compensated_delays: vector of flights with "1s" when delay
                                 resulted in passenger
                                 compensation
    """
    count_arrival_delays = arrival_delay >= (3 * 60.0)
    count_depaprture_delays = departure_delay >= (2 * 60.0)
    # Leveraging Boolean logic:
    compensated_delays = count_arrival_delays | count_depaprture_delays
    return compensated_delays


if __name__ == '__main__':
    # file_name = "https://s3.amazonaws.com/h2o-airlines-unpacked/year2012.csv"
    file_name = "../Class3/2012.csv"
    df = pd.read_csv(filepath_or_buffer=file_name,
                     encoding='latin-1',
                     nrows=100)
    # Replace times of cancelled flights with value -9999:
    df['DepDelay'] = df['DepDelay'].fillna(-9999)
    df['ArrDelay'] = df['ArrDelay'].fillna(-9999)

    df['compensated_delays'] = df[['ArrDelay', 'DepDelay']].apply(
        lambda row: delays_requiring_compensation(row[0], row[1]), axis=1)

    df['compensated_delays_vec'] = delays_requiring_compensation_vec(
        df['ArrDelay'], df['DepDelay'])

    df['compensated_delays_vec_np'] = delays_requiring_compensation_vec(
        df['ArrDelay'].values, df['DepDelay'].values)
