import pandas as pd
from collections import defaultdict
from typing import Any


def is_float(element: Any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


class FileParser:
    def __init__(self, file2analyse, column=None):
        self.file2analyse = file2analyse
        self._data_frame = None
        self.column = column

    def parse(self):
        try:
            self._data_frame = pd.read_csv(self.file2analyse, sep='\t')
        except pd.errors.ParserError as e:
            return False, str(e)

        except UnicodeDecodeError as e:
            return False, str(e)

        except ValueError as e:
            return False, str(e)

        if self.column is not None and not pd.api.types.is_numeric_dtype(
                self._data_frame.dtypes[self.column]):
            return False, f"Found non numeric value in column: {self.find_non_numeric_value()}"

        return True, "Parsing ok"

    def find_non_numeric_value(self):
        for value in self._data_frame[self.column]:
            if not is_float(value):
                return value

    def get_columns(self):
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        return list(self._data_frame.select_dtypes(include=numerics).columns)

    def get_leading_digit_distribution(self):
        leading_digit_counts = defaultdict(int)

        # use abs for move "-"
        for value in self._data_frame[self.column].abs().dropna():
            # The number can be expressed for example as "0.01" so transformation to scientific notation is necessary.
            # TODO: consider exact 0.0 value. Now we just skip it.

            digit = int("{:e}".format(value)[0])
            if digit == 0:
                continue

            leading_digit_counts[digit] += 1

        return leading_digit_counts
