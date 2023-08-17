from typing import Iterable, Union
from ._pydoe import ff2n, fullfact, ccdesign
import numpy as np
import pandas as pd
from skopt.space import Space
from skopt.sampler import Lhs


class BaseDesign:
    def __init__(self, 
            variables: dict, 
            level_codes: Iterable=None, **kwargs) -> None:
        self.variables = variables
        self.level_codes = level_codes
       
    def gen_doe(self, **kwargs):
        pass
        
    @property
    def coded_levels(self):
        return np.unique(self.doe)
    
    def parse_levels(self, doe, variables):
        levels = self.coded_levels

        doe_parsed = {}
        for var, var_range in variables.items():
            doe_parsed[var] = np.interp(levels, (levels.min(), levels.max()), var_range)

        return doe_parsed
 
    
    def to_dataframe(self):
        for attr in ['doe', 'levels']:#, 'parsed_doe']:
            if attr == 'doe':
                self.__setattr__(f'{attr}', 
                    pd.DataFrame(
                        data=self.__getattribute__(attr), 
                        columns=[*self.variables.keys()],
                        index=np.arange(1, self.__getattribute__(attr).__len__()+1)
                    )
                )
                self.__getattribute__(f'{attr}').index.name = 'Index'
                
            elif attr == 'levels':
                self.__setattr__(f'{attr}', 
                    pd.DataFrame(
                        data = self.__getattribute__(attr), 
                        index = self.coded_levels
                    )
                )
                self.__getattribute__(f'{attr}').index.name = 'Levels'

        if self.level_codes:
            self.replace_level_codes(self.coded_levels, self.level_codes)

    def append_results(self, results, index=None, **kwargs):
        
        for attr in ['doe']:#, 'parsed_doe']:
            results = pd.DataFrame(results)
            if index is not None:
                if isinstance(index, str):
                    results.index = results[index]
                else:
                    results.index = index
            else:
                results.index = self.__getattribute__(f'{attr}').index

            self.__setattr__(
                f'{attr}', 
                pd.concat([ self.__getattribute__(f'{attr}'), 
                            pd.DataFrame(results)]
                            , axis=1, **kwargs)
            )
        
    def save_excel(self, path):
        with pd.ExcelWriter(path) as writer:  
            for attr in ['doe', 'levels']:
                self.__getattribute__(attr).to_excel(writer, sheet_name=attr)

    def replace_level_codes(self, to_replace, value):
        self.doe.replace(to_replace, value, inplace=True)
        self.levels.index = self.coded_levels


class LatinHypercubeSampling(BaseDesign):
    def __init__(self, 
        variables: dict,
        samples: int,
        level_codes: Iterable=None,
        **kwargs) -> None:

        super().__init__(variables, level_codes, **kwargs)

        self.space = Space(self.variables.values())
        lhs = Lhs(**kwargs)
        self.samples = samples
        self.doe_function = lhs.generate
        
        self.doe = self.gen_doe(**kwargs)
        self.doe_levels = np.unique(self.doe)
        self.levels = self.parse_levels(self.doe, variables)
    
        self.to_dataframe()

    def gen_doe(self, **kwargs):
        np.int = int
        return self.doe_function(dimensions=self.space.dimensions, n_samples=self.samples)
    

class FullFactorial(BaseDesign):
    def __init__(self,
        variables : dict,
        n_levels : Union[int,Iterable[int]]=2,
        level_codes: Iterable=None,
        **kwargs) -> None:
        self.nvars = len(variables)

        super().__init__(variables, level_codes, **kwargs)

        self.n_levels = n_levels
        self.doe_function = fullfact

        self.doe = self.gen_doe(**kwargs)
        self.doe_levels = np.unique(self.doe)
        self.levels = self.parse_levels(self.doe, variables)
     
        self.to_dataframe()

    def gen_doe(self, **kwargs):
        if 'n_levels' not in kwargs.keys():
            if isinstance(self.n_levels, list):
                levels = self.n_levels
            else:
                levels = self.variables.__len__()*[self.n_levels]
            kwargs['levels'] = levels
        return self.doe_function(**kwargs)
    

class TwoLevelFactorial(BaseDesign):
    def __init__(self,
        variables : dict,
        level_codes: Iterable=None,
        central_points: int=0,
        **kwargs) -> None:
        self.nvars = len(variables)

        super().__init__(variables, level_codes, **kwargs)

        self.central_points = central_points
        self.doe_function = ff2n

        self.doe = self.gen_doe(**kwargs)
        self.doe_levels = np.unique(self.doe)
        self.levels = self.parse_levels(self.doe, variables)
     
        self.to_dataframe()

    def gen_doe(self, **kwargs):
        doe = self.doe_function(self.nvars, **kwargs)
        if self.central_points > 0:
            doe = np.concatenate((doe, np.zeros((self.central_points, self.nvars))), axis=0)
        return doe
    
class CentralCompositeDesign(BaseDesign):
    def __init__(self,
        variables : dict,
        center : Iterable[int]=(0,0),
        alpha : str='r',
        face : str='ccc',
        **kwargs) -> None:
        self.nvars = len(variables)

        super().__init__(variables, **kwargs)

        self.doe_function = ccdesign

        if 'center' not in kwargs.keys():
            kwargs['center'] = center
        if 'alpha' not in kwargs.keys():
            kwargs['alpha'] = alpha
        if 'face' not in kwargs.keys():
            kwargs['face'] = face

        self.doe = self.gen_doe(**kwargs)
        self.doe_levels = np.unique(self.doe)
        self.levels = self.parse_levels(self.doe, variables)
     
        self.to_dataframe()

    def gen_doe(self, **kwargs):
        return self.doe_function(self.nvars, **kwargs)