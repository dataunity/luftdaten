import datetime
from functools import partial
import unittest

import numpy as np
import pandas as pd

from data.dataframe import (
    add_month_year_columns,
    create_24_hour_means,
)


class TestAddMonthYearColumns(unittest.TestCase):

    def test_add_month_year_columns(self):
        df = pd.DataFrame({
            'data': [1, 2, 3, 4],
            'date': [
                datetime.datetime(2017, 1, 1),
                datetime.datetime(2017, 6, 1),
                datetime.datetime(2018, 1, 1),
                datetime.datetime(2018, 6, 1)
            ]
        })

        new_df = add_month_year_columns(df, 'date')

        self.assertTrue(
            np.array_equal(
                new_df.columns,
                ['data', 'date', 'year', 'month']
            )
        )

        self.assertEqual(new_df['year'][0], 2017)
        self.assertEqual(new_df['month'][0], 1)
        self.assertEqual(new_df['year'][1], 2017)
        self.assertEqual(new_df['month'][1], 6)
        self.assertEqual(new_df['year'][2], 2018)
        self.assertEqual(new_df['month'][2], 1)
        self.assertEqual(new_df['year'][3], 2018)
        self.assertEqual(new_df['month'][3], 6)


class TestCreate24HourMeans(unittest.TestCase):

    def test_create_24_hour_means(self):
        value_column = 'data'
        date_column = 'date'

        # Make 48 hours of data
        data = [
            {
                'date': datetime.datetime(2018, 6, 1) +
                    datetime.timedelta(hours=i),
                'data': float(i)
            }
            for i in range(48)
        ]
        raw_data = pd.DataFrame(data)

        results = create_24_hour_means(
            raw_data, value_column, date_column
        )

        for i in range(48):
            # Pick last 24 hours data (if available)
            start_index = max((i + 1) - 24, 0)

            mean_24_hr_sum = sum(
                d[value_column]
                for d in data[start_index:i+1]
            )
            mean_24_hour_count = len(data[start_index:i+1])

            # Prevent divide by zero
            if mean_24_hr_sum == 0:
                mean_24_hr = 0
            else:
                mean_24_hr = float(mean_24_hr_sum) / mean_24_hour_count

            self.assertEqual(
                mean_24_hr, results[value_column][i]
            )
