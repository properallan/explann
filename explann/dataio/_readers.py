from io import StringIO
import pandas as pd
from typing import Any, Union
from pathlib import Path

class BaseImport:
    def __init__(self, 
        data: pd.DataFrame = None):

        assert isinstance(data, pd.DataFrame), "data must be a pandas DataFrame"

        self.data = data
        self.raw_data = self.data.copy(deep=True)

    def parse_levels(self,
        levels : pd.DataFrame = None):

        assert isinstance(levels, pd.DataFrame), "levels must be a pandas DataFrame"

        levels.index = levels.index.astype('str')
        self.levels = levels

        pd.options.mode.chained_assignment = None  # default='warn'
        for column in levels.keys():
            for i,val in enumerate(self.data[column]):
                self.data[column][i] = levels[column][f"{val}"]
        pd.options.mode.chained_assignment = 'warn'  # default='warn'
    
class ImportString(BaseImport):
    def __init__(self, 
        data: str = None, 
        delimiter: str = "\s",
        engine: str = "python",
        **kwargs):

        assert isinstance(data, str), "data must be a string"

        data = pd.read_csv(StringIO(data), delimiter=delimiter, engine=engine,**kwargs)

        super().__init__(data)

    def parse_levels(self, 
        levels : str = None,
        delimiter: str = ";"):

        assert isinstance(levels, str), "levels must be a string"
        
        levels = pd.read_csv(StringIO(levels), delimiter=";", index_col=0)

        super().parse_levels(levels)
        

class ImportXLSX:
    def __init__(self,
        path: str = None,
        sheet_name: str = None,
        **kwargs):

        assert isinstance(path, str), "path must be a string"
        path = Path(path)
        assert path.exists(), "path does not exist"
        assert path.suffix == ".xlsx", "path must be a .xlsx file"


        data = pd.read_excel(path, sheet_name=sheet_name, **kwargs)
        
        super().__init__(data)

    def parse_levels(self,
        path: str = None,
        sheet_name: str = None,
    ):
        assert isinstance(path, str), "path must be a string"
        path = Path(path)
        assert path.exists(), "path does not exist"
        assert path.suffix == ".xlsx", "path must be a .xlsx file"

        levels = pd.read_excel(path, sheet_name=sheet_name)
        pd.options.mode.chained_assignment = None

        super().parse_levels(levels)