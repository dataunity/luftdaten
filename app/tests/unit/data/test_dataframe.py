import datetime
import unittest

import numpy as np
import pandas as pd

from data.dataframe import add_month_year_columns


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
