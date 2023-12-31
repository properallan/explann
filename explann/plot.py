# base code
import numpy as np
import seaborn as sns
from statsmodels.tools.tools import maybe_unwrap_results
from statsmodels.graphics.gofplots import ProbPlot
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
from typing import Type,Union
import statsmodels
from scipy.interpolate import interp1d
style_talk = 'seaborn-talk'    #refer to plt.style.available
import pandas as pd
from matplotlib import cm # for a scatter plot
from mpl_toolkits.mplot3d import Axes3D

class ParetoPlot:
    def __init__(self, model):
        self.model = model

    def plot(self, 
        function : Union[str,list,tuple]=None, 
        ax=None, 
        ascending:bool=True, 
        figsize:tuple=(10,10),
        attribute:str='params',
        alpha:float=0.05,
        vline:bool=True,
        **kwargs):

        try:
            if len(ax) > 0:
                ax = ax.flatten()
        except:
            pass

        if function is None:
            function = self.model.function_names
            if len(function) == 1:
                function = function[0]

        if isinstance(function, list) or isinstance(function, tuple):
            if ax is None:
                ax = [None] * len(function)
            axes = {}
            for function_i,ax_i in zip(function,ax):
                axes[function_i] = self.plot(function_i,ax=ax_i, ascending=ascending, figsize=figsize, attribute=attribute, alpha=alpha, **kwargs)
            return axes
        
        elif isinstance(function, str):
            
            if ax is None:
                fig, ax = plt.subplots(figsize=figsize)
            
            if 'title' in kwargs:
                title = kwargs['title']
                del kwargs['title']
            else:
                title = function

            if attribute == 'anova':
                model = self.model
                signed_values = model.anova(function)['F'].dropna()
                sorted_values = signed_values.abs().sort_values(ascending=ascending)
                pvalues = model.anova(function)['PR(>F)'].dropna()
                
            elif attribute in ['tvalues','params']:
                model = self.model[function]
                signed_values = model.__getattribute__(attribute)
                sorted_values = signed_values.abs().sort_values(ascending=ascending)
                pvalues = model.__getattribute__('pvalues')
            

            keys_sorted = sorted_values.keys()

            
            #ax = sorted_values.plot(kind='barh', title=title, ax=ax, **kwargs)
            
            if vline:
                sorted_index = sorted_values.index
                sorted_pvalues = pvalues[sorted_index]
                
                if sorted_pvalues.is_monotonic_decreasing:
                    pvalues = sorted_pvalues[::-1]
                    values = sorted_values[::-1]
                else:
                    pvalues = sorted_pvalues
                    values = sorted_values
                #spl = CubicSpline(pvalues, values)
                #value = abs(spl(alpha))

                spl = interp1d(pvalues, values, kind='linear', fill_value='extrapolate')
                value = abs(spl(alpha))

                ax.axvline(value, color='k', linestyle='--')
                ax.text(value, -0.01, f'p={alpha:.2f}', transform=ax.get_xaxis_transform(),
                ha='center', va='top')

            threshold = value
            # split it up
            #above_threshold = np.maximum(sorted_values - threshold, 0)
            above_threshold = sorted_values[sorted_values >= threshold]
            #below_threshold = np.minimum(sorted_values, threshold)
            below_threshold = sorted_values[sorted_values < threshold]
            
            #ax = below_threshold.plot(kind='barh', title=title, ax=ax, color="r", **kwargs)
            #ax = above_threshold.plot(kind='barh', title=title, ax=ax, color="g", **kwargs)
            
            colors = ["tab:green" if val > threshold else "tab:red" for val in sorted_values]
            ax = sorted_values.plot(kind='barh', title=title, ax=ax, color=colors, **kwargs)
                
            ax.xaxis.set_visible(False)

            blabels = ax.bar_label(ax.containers[0], labels = signed_values[keys_sorted].round(4).astype(str).values, padding=5)
            
            return ax
    
class LinearRegDiagnostic():
    """
    Diagnostic plots to identify potential problems in a linear regression fit.
    Mainly,
    
    a. non-linearity of data
    b. Correlation of error terms
    c. non-constant variance
    d. outliers
    e. high-leverage points
    f. collinearity

    Authors:
        Prajwal Kafle (p33ajkafle@gmail.com, where 3 = r)
        Does not come with any sort of warranty.
        Please test the code one your end before using.

        Matt Spinelli (m3spinelli@gmail.com, where 3 = r)
        (1) Fixed incorrect annotation of the top most extreme residuals in
            the Residuals vs Fitted and, especially, the Normal Q-Q plots.
        (2) Changed Residuals vs Leverage plot to match closer the y-axis
            range shown in the equivalent plot in the R package ggfortify.
        (3) Added horizontal line at y=0 in Residuals vs Leverage plot to
            match the plots in R package ggfortify and base R.
        (4) Added option for placing a vertical guideline on the Residuals
            vs Leverage plot using the rule of thumb of h = 2p/n to denote
            high leverage (high_leverage_threshold=True).
        (5) Added two more ways to compute the Cook's Distance (D) threshold:
            * 'baseR': D > 1 and D > 0.5 (default)
            * 'convention': D > 4/n
            * 'dof': D > 4 / (n - k - 1)
        (6) Fixed class name to conform to Pascal casing convention
        (7) Fixed Residuals vs Leverage legend to work with loc='best'
        
    """

    def __init__(self,
                 results: Type[statsmodels.regression.linear_model.RegressionResultsWrapper]) -> None:
        """
        For a linear regression model, generates following diagnostic plots:

        a. residual
        b. qq
        c. scale location and
        d. leverage

        and a table

        e. vif

        Args:
            results (Type[statsmodels.regression.linear_model.RegressionResultsWrapper]):
                must be instance of statsmodels.regression.linear_model object

        Raises:
            TypeError: if instance does not belong to above object

        Example:
        >>> import numpy as np
        >>> import pandas as pd
        >>> import statsmodels.formula.api as smf
        >>> x = np.linspace(-np.pi, np.pi, 100)
        >>> y = 3*x + 8 + np.random.normal(0,1, 100)
        >>> df = pd.DataFrame({'x':x, 'y':y})
        >>> res = smf.ols(formula= "y ~ x", data=df).fit()
        >>> cls = Linear_Reg_Diagnostic(res)
        >>> cls(plot_context="seaborn-paper")

        In case you do not need all plots you can also independently make an individual plot/table
        in following ways

        >>> cls = Linear_Reg_Diagnostic(res)
        >>> cls.residual_plot()
        >>> cls.qq_plot()
        >>> cls.scale_location_plot()
        >>> cls.leverage_plot()
        >>> cls.vif_table()
        """

        if isinstance(results, statsmodels.regression.linear_model.RegressionResultsWrapper) is False:
            raise TypeError("result must be instance of statsmodels.regression.linear_model.RegressionResultsWrapper object")

        self.results = maybe_unwrap_results(results)

        self.y_true = self.results.model.endog
        self.y_predict = self.results.fittedvalues
        self.xvar = self.results.model.exog
        self.xvar_names = self.results.model.exog_names

        self.residual = np.array(self.results.resid)
        influence = self.results.get_influence()
        self.residual_norm = influence.resid_studentized_internal
        self.leverage = influence.hat_matrix_diag
        self.cooks_distance = influence.cooks_distance[0]
        self.nparams = len(self.results.params)
        self.nresids = len(self.residual_norm)

    def __call__(self, plot_context='seaborn-paper', **kwargs):
        # print(plt.style.available)
        with plt.style.context(plot_context):
            fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10,10))
            self.residual_plot(ax=ax[0,0])
            self.qq_plot(ax=ax[0,1])
            self.scale_location_plot(ax=ax[1,0])
            self.leverage_plot(
                ax=ax[1,1],
                high_leverage_threshold = kwargs.get('high_leverage_threshold'),
                cooks_threshold = kwargs.get('cooks_threshold'))
            plt.show()

        return self.vif_table(), fig, ax,

    def residual_plot(self, ax=None):
        """
        Residual vs Fitted Plot

        Graphical tool to identify non-linearity.
        (Roughly) Horizontal red line is an indicator that the residual has a linear pattern
        """
        if ax is None:
            fig, ax = plt.subplots()

        sns.residplot(
            x=self.y_predict,
            y=self.residual,
            lowess=True,
            scatter_kws={'alpha': 0.5},
            line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8},
            ax=ax)

        # annotations
        residual_abs = np.abs(self.residual)
        abs_resid = np.flip(np.argsort(residual_abs), 0)
        abs_resid_top_3 = abs_resid[:3]
        for i in abs_resid_top_3:
            ax.annotate(
                i,
                xy=(self.y_predict[i], self.residual[i]),
                color='C3')

        ax.set_title('Residuals vs Fitted', fontweight="bold")
        ax.set_xlabel('Fitted values')
        ax.set_ylabel('Residuals')
        return ax

    def qq_plot(self, ax=None):
        """
        Standarized Residual vs Theoretical Quantile plot

        Used to visually check if residuals are normally distributed.
        Points spread along the diagonal line will suggest so.
        """
        if ax is None:
            fig, ax = plt.subplots()

        QQ = ProbPlot(self.residual_norm)
        fig = QQ.qqplot(line='45', alpha=0.5, lw=1, ax=ax)

        # annotations
        abs_norm_resid = np.flip(np.argsort(np.abs(self.residual_norm)), 0)
        abs_norm_resid_top_3 = abs_norm_resid[:3]
        for i, x, y in self.__qq_top_resid(QQ.theoretical_quantiles, abs_norm_resid_top_3):
            ax.annotate(
                i,
                xy=(x, y),
                ha='right',
                color='C3')

        ax.set_title('Normal Q-Q', fontweight="bold")
        ax.set_xlabel('Theoretical Quantiles')
        ax.set_ylabel('Standardized Residuals')
        return ax

    def scale_location_plot(self, ax=None):
        """
        Sqrt(Standarized Residual) vs Fitted values plot

        Used to check homoscedasticity of the residuals.
        Horizontal line will suggest so.
        """
        if ax is None:
            fig, ax = plt.subplots()

        residual_norm_abs_sqrt = np.sqrt(np.abs(self.residual_norm))

        ax.scatter(self.y_predict, residual_norm_abs_sqrt, alpha=0.5);
        sns.regplot(
            x=self.y_predict,
            y=residual_norm_abs_sqrt,
            scatter=False, ci=False,
            lowess=True,
            line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8},
            ax=ax)

        # annotations
        abs_sq_norm_resid = np.flip(np.argsort(residual_norm_abs_sqrt), 0)
        abs_sq_norm_resid_top_3 = abs_sq_norm_resid[:3]
        for i in abs_sq_norm_resid_top_3:
            ax.annotate(
                i,
                xy=(self.y_predict[i], residual_norm_abs_sqrt[i]),
                color='C3')

        ax.set_title('Scale-Location', fontweight="bold")
        ax.set_xlabel('Fitted values')
        ax.set_ylabel(r'$\sqrt{|\mathrm{Standardized\ Residuals}|}$');
        return ax

    def leverage_plot(self, ax=None, high_leverage_threshold=False, cooks_threshold='baseR'):
        """
        Residual vs Leverage plot

        Points falling outside Cook's distance curves are considered observation that can sway the fit
        aka are influential.
        Good to have none outside the curves.
        """
        if ax is None:
            fig, ax = plt.subplots()

        ax.scatter(
            self.leverage,
            self.residual_norm,
            alpha=0.5);

        sns.regplot(
            x=self.leverage,
            y=self.residual_norm,
            scatter=False,
            ci=False,
            lowess=True,
            line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8},
            ax=ax)

        # annotations
        leverage_top_3 = np.flip(np.argsort(self.cooks_distance), 0)[:3]
        for i in leverage_top_3:
            ax.annotate(
                i,
                xy=(self.leverage[i], self.residual_norm[i]),
                color = 'C3')

        factors = []
        if cooks_threshold == 'baseR' or cooks_threshold is None:
            factors = [1, 0.5]
        elif cooks_threshold == 'convention':
            factors = [4/self.nresids]
        elif cooks_threshold == 'dof':
            factors = [4/ (self.nresids - self.nparams)]
        else:
            raise ValueError("threshold_method must be one of the following: 'convention', 'dof', or 'baseR' (default)")
        for i, factor in enumerate(factors):
            label = "Cook's distance" if i == 0 else None
            xtemp, ytemp = self.__cooks_dist_line(factor)
            ax.plot(xtemp, ytemp, label=label, lw=1.25, ls='--', color='red')
            ax.plot(xtemp, np.negative(ytemp), lw=1.25, ls='--', color='red')

        if high_leverage_threshold:
            high_leverage = 2 * self.nparams / self.nresids
            if max(self.leverage) > high_leverage:
                ax.axvline(high_leverage, label='High leverage', ls='-.', color='purple', lw=1)

        ax.axhline(0, ls='dotted', color='black', lw=1.25)
        ax.set_xlim(0, max(self.leverage)+0.01)
        ax.set_ylim(min(self.residual_norm)-0.1, max(self.residual_norm)+0.1)
        ax.set_title('Residuals vs Leverage', fontweight="bold")
        ax.set_xlabel('Leverage')
        ax.set_ylabel('Standardized Residuals')
        plt.legend(loc='best')
        return ax

    def vif_table(self):
        """
        VIF table

        VIF, the variance inflation factor, is a measure of multicollinearity.
        VIF > 5 for a variable indicates that it is highly collinear with the
        other input variables.
        """
        vif_df = pd.DataFrame()
        vif_df["Features"] = self.xvar_names
        vif_df["VIF Factor"] = [variance_inflation_factor(self.xvar, i) for i in range(self.xvar.shape[1])]

        return (vif_df
                .sort_values("VIF Factor")
                .round(2))


    def __cooks_dist_line(self, factor):
        """
        Helper function for plotting Cook's distance curves
        """
        p = self.nparams
        formula = lambda x: np.sqrt((factor * p * (1 - x)) / x)
        x = np.linspace(0.001, max(self.leverage), 50)
        y = formula(x)
        return x, y


    def __qq_top_resid(self, quantiles, top_residual_indices):
        """
        Helper generator function yielding the index and coordinates
        """
        offset = 0
        quant_index = 0
        previous_is_negative = None
        for resid_index in top_residual_indices:
            y = self.residual_norm[resid_index]
            is_negative = y < 0
            if previous_is_negative == None or previous_is_negative == is_negative:
                offset += 1
            else:
                quant_index -= offset
            x = quantiles[quant_index] if is_negative else np.flip(quantiles, 0)[quant_index]
            quant_index += 1
            previous_is_negative = is_negative
            yield resid_index, x, y



def plot_surface(x, y, z, model, n_pts=10, other_params={}, labels:dict=None, ax=None, cmap='viridis', scaled=False):
    name_z = z #'Fso'
    name_x = x #'U'
    name_y = y #'Y'
    n_pts = 10
    if not scaled:
        X = np.linspace( model.data[name_x].min(), model.data[name_x].max(), n_pts)
        Y = np.linspace( model.data[name_y].min(), model.data[name_y].max(), n_pts)
    else:
        X = np.linspace( model.levels[name_x].min(), model.levels[name_x].max(), n_pts)
        Y = np.linspace( model.levels[name_y].min(), model.levels[name_y].max(), n_pts)
        
    x, y = np.meshgrid(X, Y)
        
    try:
        variables = pd.DataFrame({name_x:x.ravel(), name_y:y.ravel(), **other_params})
    except:
        variables = pd.DataFrame([{name_x:x.ravel(), name_y:y.ravel(), **other_params}])
        
    if not scaled:
        z = model.predict(name_z, variables).values.reshape(x.shape)
    else:
        z = model.predict_rescaled(name_z, variables).values.reshape(x.shape)
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(6,6),subplot_kw={"projection": "3d"})
    else:
        fig = plt.gcf()
    ax.set_box_aspect(None, zoom=0.8)
    
    pax = ax.plot_surface(x, y, z, cmap=cmap, edgecolor='black', linewidth=0.5, alpha=0.6, antialiased=True)
    #ax.contour(x, y, z, cmap=cmap, linestyles='solid', alpha=1)
    ax.contourf(x, y, z, zdir='z', offset=ax.get_zlim()[0], cmap=cmap, alpha=0.5,  antialiased=True)
    ax.contourf(x, y, z, zdir='x', offset=ax.get_xlim()[0], cmap=cmap, alpha=0.5,  antialiased=True)
    ax.contourf(x, y, z, zdir='y', offset=ax.get_ylim()[1], cmap=cmap, alpha=0.5,  antialiased=True)
    
    if labels is not None:
        ax.set(**labels)
        ax.zaxis.set_rotate_label(True)
        ax.xaxis.set_rotate_label(True)
        ax.yaxis.set_rotate_label(True)
        
    try:
        if 'zlabel' in labels:
            zlabel=labels['zlabel']
    except:
        zlabel=None  
        
        
    fig.colorbar(pax, ax=ax, location='top', fraction=0.04, pad=-0.05, label=zlabel)