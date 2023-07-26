from io import StringIO
import pandas as pd
from typing import Any, Union
from pathlib import Path

class BaseImport:
    """
        Base class for importing data from a file or string.

        Parameters
        ----------
        data : pandas.DataFrame
        Data to be imported.
    
    Attributes
    ----------
    data : pandas.DataFrame

    raw_data : pandas.DataFrame

    levels : pandas.DataFrame

    delimiter : str

    Methods
    -------
    parse_levels(data)
        Parse levels from a pandas.DataFrame.

    parse_levels_from_string(data, delimiter)
        Parse levels from a string.

    parse_levels_from_xlsx(path, sheet_name, index_col)
        Parse levels from an xlsx file.
    """
    def __init__(self, 
        data: pd.DataFrame = None):

        assert isinstance(data, pd.DataFrame), "data must be a pandas DataFrame"

        self.data = data
        self.raw_data = self.data.copy(deep=True)

    def parse_levels(self,
        data : pd.DataFrame = None):

        assert isinstance(data, pd.DataFrame), "data must be a pandas DataFrame"

        data.index = data.index.astype('str')
        self.levels = data

        parsed_data = self.data.copy(deep=True)
        pd.options.mode.chained_assignment = None  # default='warn'
        for column in data.keys()[1:]:
            for i,val in enumerate(self.raw_data[column]):
                self.data[column][i] = data[column][f"{val}"]      
        pd.options.mode.chained_assignment = 'warn'  # default='warn'
    
    
    def parse_levels_from_string(self, 
        data : str = None,
        delimiter: str = None):

        if delimiter is None:
            try:
                delimiter = self.delimiter
            except:
                delimiter = '\s'

        assert isinstance(data, str), "levels must be a string"
        
        data = pd.read_csv(StringIO(data), index_col=0, delimiter=delimiter)

        self.parse_levels(data)

    def parse_levels_from_xlsx(self,
        data: str = None,
        sheet_name: str = None,
        index_col: int = 0,
    ):
        assert isinstance(data, str), "path must be a string"
        data = Path(data)
        assert data.exists(), "path does not exist"
        assert data.suffix == ".xlsx", "path must be a .xlsx file"

        data = pd.read_excel(io=data, sheet_name=sheet_name, index_col=index_col)

        self.parse_levels(data)

class ImportString(BaseImport):
    def __init__(self, 
        data: str = None, 
        delimiter: str = "\s",
        engine: str = "python",
        **kwargs):

        assert isinstance(data, str), "data must be a string"

        data = pd.read_csv(StringIO(data), delimiter=delimiter, engine=engine,**kwargs)
        
        self.delimiter = delimiter

        super().__init__(data)        

class ImportXLSX(BaseImport):
    def __init__(self,
        path: str = None,
        sheet_name: str = 0,
        **kwargs):

        assert isinstance(path, str), "path must be a string"
        path = Path(path)
        assert path.exists(), "path does not exist"
        assert path.suffix == ".xlsx", "path must be a .xlsx file"

        data = pd.read_excel(io=path, sheet_name=sheet_name, **kwargs)
        
        super().__init__(data)

    
