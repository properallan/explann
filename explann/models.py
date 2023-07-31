import pandas as pd
from typing import Union
from statsmodels.formula.api import ols
from statsmodels.stats.api import anova_lm
import numpy as np
from patsy import ModelDesc
from scipy.stats import f
import matplotlib.pyplot as plt

def add_categorical(formula):   
    formula = ModelDesc.from_formula(formula)
    lhs = formula.lhs_termlist[0].name()
    rhs = ' + '.join([f"C({f.name()})" for f in formula.rhs_termlist])
    rhs = rhs.replace('C(Intercept)','1')
    rhs = rhs.replace(':','):C(')
    #print( lhs + ' ~ ' + rhs)
    return lhs + ' ~ ' + rhs

class BaseModel:
    def __init__(self,):
        pass

class FactorialModel(BaseModel):
    def __init__(self, 
        data : pd.DataFrame = None, 
        functions : Union[str,list,tuple] = None,
        statsmodel : object = ols,
        **fit_kwargs):

        self.data = data
        self.model = {}
        self.statsmodel = statsmodel
        self.functions = functions

        self.model = self.fit(
            data=data,
            functions=functions, 
            statsmodel=statsmodel,
            **fit_kwargs,
        )

        self.use_anova = False

    def fit(self, 
        data : pd.DataFrame = None,
        functions : Union[str,list,tuple] = None,
        statsmodel : object = ols,
        **fit_kwargs
        ):

        if isinstance(functions, str):
            key = functions.split('~')[0].strip()
            functions = {key : functions}

        if functions is not None:
            model_dict = {}
            for key, function in functions.items():
                splited = function.split('~')
                function_name = splited[0].strip()
                function_body = splited[1].strip()
                model_dict[key] = self.statsmodel(function, data).fit(**fit_kwargs)
        else:
            print('must provide function formulas')

        return model_dict

    @property
    def function_names(self):        
        return list(self.model.keys())
    
    @property
    def independent_variables(self):
        lhs = [function.split('~')[0].strip() for function in self.functions.values()]
        return [key for key in self.data.keys() if key not in lhs]

    def print_equation(self, 
            function : Union[str, list,tuple] = None,
            alpha : float = 0.05,
            precision : int = 4):
        
        if function is None:
            function = self.function_names
            if len(function) == 1:
                function = function[0]

        if isinstance(function, list) or isinstance(function, tuple):
            return_dict = {}
            for function_name_i in function:
                return_dict[function_name_i] = self.print_equation(function_name_i, alpha=alpha, precision=precision)
                
            return return_dict
        
        elif isinstance(function, str):
            sig = self.get_significant_terms(function=function, alpha=alpha)
            equation = []
            for s_i,v_i in zip(sig, self.model[function].params[sig]):
                equation.append( f"{v_i:.{precision}f} * {s_i}".
                replace(':', '').replace('Intercept', '1') )
            
            final_equation = ' + '.join(equation).replace('-',' - ').replace(' * 1', '').replace(' +  -', ' -').replace(' * ', ' ').replace('  ', ' ')
            
            return f"{function} = {final_equation}".replace('  ', ' ')
        
    def get_significant_model_functions(self,
        function : Union[str,list,tuple]=None,
        alpha : float = 0.05,
        use_anova : bool = False):

        if use_anova:
            self.use_anova = True
        else:
            self.use_anova = False

        if function is None:
            function = self.function_names
            if len(function) == 1:
                function = function[0]
        if isinstance(function, str):
            function = [function]

        significant_terms = self.get_significant_terms(function=function, alpha=alpha)

        lhs = lambda x: x.split("~")[0].strip()

        significant_model_functions_dict = {key:f"{lhs(self.functions[key])} ~ {' + '.join(val)}".replace("Intercept","1") for key,val in significant_terms.items()}

        return significant_model_functions_dict
        
    def build_significant_models(
            self, 
            function : Union[str,list,tuple]=None, 
            alpha : float = 0.05,
            use_anova : bool = False):
        
        significant_model_functions_dict = self.get_significant_model_functions(function=function, alpha=alpha, use_anova=use_anova)
        significant_models = FactorialModel(
            data=self.data, 
            functions=significant_model_functions_dict, 
            statsmodel=self.statsmodel)
        return significant_models
                               
    def get_significant_terms(self, 
            function : Union[str,list,tuple]=None,
            alpha : float = 0.05):
        
        if function is None:
            function = self.function_names
            if len(function) == 1:
                function = function[0]

        if isinstance(function, list) or isinstance(function, tuple):
            return_dict = {}
            for function_i in function:
                return_dict[function_i] = self.get_significant_terms(function_i, alpha=alpha) 
            return return_dict
        else:
            if self.use_anova:
                pvalues = self.anova(function)['PR(>F)'].dropna()
                terms = [k for k,v in pvalues.items() if v<=alpha ]
                terms.append('Intercept')
            else:
                pvalues = self.model[function].pvalues
                terms = [k for k,v in pvalues.items() if v<=alpha ]

                
            return terms
        
    def summary(self, function : Union[str,list,tuple]=None):
        if function is None:
            function = self.function_names
            if len(function) == 1:
                function = function[0]

        if isinstance(function, str):
            function = [function]

        return_dict = {}
        for function_i in function:
            return_dict[function_i] = self.model[function_i].summary()

        return return_dict
        
    def anova(self, function : Union[str,list,tuple]=None):
        if function is None:
            function = self.function_names
            if len(function) == 1:
                function = function[0]

        if isinstance(function, list) or isinstance(function, tuple):
            return_dict = {}
            for function_i in function:
                return_dict[function_i] = self.anova(function_i)
            return return_dict
        else:
            return anova_lm(self.model[function])

    
    def working_lack_of_fit(self, function : Union[str,list,tuple]=None,
        baseline : BaseModel = None):
        if function is None:
            function = self.function_names
            if len(function) == 1:
                function = function[0]
        if isinstance(function, str):
            function = [function]

        factor_data = self.data.copy()
        
        functions = {key:add_categorical(val) for key,val in self.functions.items() if key in function}

        if baseline is not None:
            factor_model = baseline
        else:
            factor_model = FactorialModel(
                data = factor_data,
                functions = functions,
                statsmodel = self.statsmodel
            )
        

        return_dict = {}
        return_dataframe = {}
        for key, function_i in functions.items():
            
            results = anova_lm(self.model[key], factor_model[key])
            an = anova_lm(self.model[key])
            
            lack_of_fit_sum_sq = results.ss_diff[1] 
            lack_of_fit_gl = results.df_diff[1]
            pure_error_sum_sq = results.ssr[1]
            pure_error_gl = results.df_resid[1]
            total_gl = an.df.sum() 
            residual_mean_sq = an.mean_sq['Residual']
            residual_sum_sq = an['sum_sq']['Residual']
            regression_sum_sq = an['sum_sq'].sum()-an['sum_sq']['Residual']
            regression_df = an['df'].sum()-an['df']['Residual']
            regression_mean_sq = regression_sum_sq/regression_df
            pure_error_mean_sq = pure_error_sum_sq/pure_error_gl
            lack_of_fit_mean_sq = lack_of_fit_sum_sq/lack_of_fit_gl
            regression_F = regression_mean_sq/an['mean_sq']['Residual']
            lack_of_fit_F = lack_of_fit_mean_sq/pure_error_mean_sq
            residual_df = an['df']['Residual']

            return_dict[key] = {}

            return_dict[key]['results'] = results

            return_dict[key]['regression_df'] = regression_df
            return_dict[key]['residual_df'] = residual_df
            return_dict[key]['lack_of_fit_df'] = lack_of_fit_gl
            return_dict[key]['pure_error_df'] = pure_error_gl
            return_dict[key]['total_df'] = total_gl 
            

            return_dict[key]['regression_sum_sq'] = regression_sum_sq
            return_dict[key]['residual_sum_sq'] = residual_sum_sq
            return_dict[key]['lack_of_fit_sum_sq'] = lack_of_fit_sum_sq
            return_dict[key]['pure_error_sum_sq'] = pure_error_sum_sq
            return_dict[key]['total_sum_sq'] = regression_sum_sq + residual_sum_sq

            return_dict[key]['regression_mean_sq'] = regression_mean_sq
            return_dict[key]['residual_mean_sq'] = residual_mean_sq
            return_dict[key]['lack_of_fit_mean_sq'] = lack_of_fit_mean_sq
            return_dict[key]['pure_error_mean_sq'] = pure_error_mean_sq
            
            return_dict[key]['regression_F'] = regression_F
            return_dict[key]['lack_of_fit_F'] = lack_of_fit_F

            from scipy.stats import f
            alpha = 0.05
            return_dict[key]['regression_table_F'] = f.ppf(q=1-alpha, dfn=regression_df, dfd=residual_df) 
            return_dict[key]['lack_of_fit_table_F'] = f.ppf(q=1-alpha, dfn=lack_of_fit_gl, dfd=pure_error_gl)

            return_dict[key]['regression_p'] = 1 - f.cdf(regression_F, regression_df, residual_df)
            return_dict[key]['lack_of_fit_p'] = 1 - f.cdf(lack_of_fit_F, lack_of_fit_gl, pure_error_gl)


            dataframe = pd.DataFrame({
                'Source_of_Variation':['Regression', 'Residual', 'Lack_of_Fit', 'Pure_Error', 'Total'],
                'df':[regression_df, residual_df, lack_of_fit_gl, pure_error_gl, total_gl],
                'sum_sq':[regression_sum_sq, residual_sum_sq, lack_of_fit_sum_sq, pure_error_sum_sq, regression_sum_sq + residual_sum_sq],
                'mean_sq':[regression_mean_sq, residual_mean_sq, lack_of_fit_mean_sq, pure_error_mean_sq, None],
                'F':[regression_F, None, lack_of_fit_F, None, None],
                'F_table':[return_dict[key]['regression_table_F'], None, return_dict[key]['lack_of_fit_table_F'], None, None],
                'p':[return_dict[key]['regression_p'], None, return_dict[key]['lack_of_fit_p'], None, None],
            })

            return_dict[key]['dataframe'] = dataframe
            return_dataframe[key] = dataframe
        return return_dataframe
    
    def lack_of_fit(self, 
        function : Union[str,list,tuple]=None,
        baseline : BaseModel = None, 
        alpha : float = 0.05):

        if function is None:
            function = self.function_names
            if len(function) == 1:
                function = function[0]

        if baseline is not None:
            factor_model = baseline

            functions = {key:val for key,val in self.functions.items() if key in function}
        else:
            factor_data = self.data.copy()
        
            functions = {key:add_categorical(val) for key,val in self.functions.items() if key in function}
        
            factor_model = FactorialModel(
                data = factor_data,
                functions = functions,
                statsmodel = self.statsmodel
            )

        if isinstance(function, list) or isinstance(function, tuple):
            return_dict = {}
            for function_i in function:
                return_dict[function_i] = self.lack_of_fit(function_i, baseline=baseline)
            return return_dict
        else:
            for key, function_i in functions.items():
                
                results = anova_lm(self.model[key], factor_model[key])
                an = anova_lm(self.model[key])
                
                lack_of_fit_sum_sq = results.ss_diff[1] 
                lack_of_fit_gl = results.df_diff[1]
                pure_error_sum_sq = results.ssr[1]
                pure_error_gl = results.df_resid[1]
                total_gl = an.df.sum() 
                residual_mean_sq = an.mean_sq['Residual']
                residual_sum_sq = an['sum_sq']['Residual']
                regression_sum_sq = an['sum_sq'].sum()-an['sum_sq']['Residual']
                regression_df = an['df'].sum()-an['df']['Residual']
                regression_mean_sq = regression_sum_sq/regression_df
                pure_error_mean_sq = pure_error_sum_sq/pure_error_gl
                lack_of_fit_mean_sq = lack_of_fit_sum_sq/lack_of_fit_gl
                regression_F = regression_mean_sq/an['mean_sq']['Residual']
                lack_of_fit_F = lack_of_fit_mean_sq/pure_error_mean_sq
                residual_df = an['df']['Residual']

                regression_table_F = f.ppf(q=1-alpha, dfn=regression_df, dfd=residual_df) 
                lack_of_fit_table_F = f.ppf(q=1-alpha, dfn=lack_of_fit_gl, dfd=pure_error_gl)

                regression_p = 1 - f.cdf(regression_F, regression_df, residual_df)
                lack_of_fit_p = 1 - f.cdf(lack_of_fit_F, lack_of_fit_gl, pure_error_gl)

                dataframe = pd.DataFrame({
                    'Source_of_Variation':
                        ['Regression', 'Residual', 'Lack_of_Fit', 'Pure_Error', 'Total'],
                    'df':
                        [regression_df, residual_df, lack_of_fit_gl, pure_error_gl, total_gl],
                    'sum_sq':
                        [regression_sum_sq, residual_sum_sq, lack_of_fit_sum_sq, pure_error_sum_sq, regression_sum_sq + residual_sum_sq],
                    'mean_sq':
                        [regression_mean_sq, residual_mean_sq, lack_of_fit_mean_sq, pure_error_mean_sq, None],
                    'F':
                        [regression_F, None, lack_of_fit_F, None, None],
                    'F_table':
                        [regression_table_F, None, lack_of_fit_table_F, None, None],
                    'p':[regression_p, None, lack_of_fit_p, None, None],
                })

            return dataframe

    def __getitem__(self, key):
        return self.model[key]
    
    
