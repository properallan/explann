from io import StringIO
import pandas as pd
from typing import Union

class ImportData:

    def __init__(self, 
        data: Union[str,pd.DataFrame] = None, 
        delimiter: str = ";",
        **kwargs):

        if isinstance(data, str):
            data = pd.read_csv(StringIO(data), delimiter=delimiter, **kwargs)
        self.data = data
    
    def parse_levels(self, 
        levels : Union[str,pd.DataFrame] = None,
        delimiter: str = ";"):

        if isinstance(levels, str):
            levels = pd.read_csv(StringIO(levels), delimiter=";", index_col=0)

        levels.index = levels.index.astype('str')
        self.levels = levels

        self.raw_data = self.data.copy(deep=True)

        pd.options.mode.chained_assignment = None  # default='warn'
        for column in levels.keys():
            for i,val in enumerate(self.data[column]):
                self.data[column][i] = levels[column][f"{val}"]
        pd.options.mode.chained_assignment = 'warn'  # default='warn'