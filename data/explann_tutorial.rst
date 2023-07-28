===================
Begginer's tutorial
===================


Data input
----------

Data can be read from a string, by using the ``ImportString`` class of
``explain.dataio``. The default delimiter is ``\s`` the spectial
charactere for whitespaces.

.. code:: ipython3

    from explann.dataio import ImportString
    
    data_string = """
    Observação	Dureza	Temperatura
    1	137	220
    2	137	220
    3	137	220
    4	136	220
    5	135	220
    6	135	225
    7	133	225
    8	132	225
    9	133	225
    10	133	225
    11	128	230
    12	124	230
    13	126	230
    14	129	230
    15	126	230
    16	122	235
    17	122	235
    18	122	235
    19	119	235
    20	122	235
    """
    
    data_reader_string = ImportString(data=data_string, delimiter="\s")


``data_reader`` object stores the providade data in its ``.data``
attribute

.. code:: ipython3

    data_reader_string.data




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Observação</th>
          <th>Dureza</th>
          <th>Temperatura</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>137</td>
          <td>220</td>
        </tr>
        <tr>
          <th>1</th>
          <td>2</td>
          <td>137</td>
          <td>220</td>
        </tr>
        <tr>
          <th>2</th>
          <td>3</td>
          <td>137</td>
          <td>220</td>
        </tr>
        <tr>
          <th>3</th>
          <td>4</td>
          <td>136</td>
          <td>220</td>
        </tr>
        <tr>
          <th>4</th>
          <td>5</td>
          <td>135</td>
          <td>220</td>
        </tr>
        <tr>
          <th>5</th>
          <td>6</td>
          <td>135</td>
          <td>225</td>
        </tr>
        <tr>
          <th>6</th>
          <td>7</td>
          <td>133</td>
          <td>225</td>
        </tr>
        <tr>
          <th>7</th>
          <td>8</td>
          <td>132</td>
          <td>225</td>
        </tr>
        <tr>
          <th>8</th>
          <td>9</td>
          <td>133</td>
          <td>225</td>
        </tr>
        <tr>
          <th>9</th>
          <td>10</td>
          <td>133</td>
          <td>225</td>
        </tr>
        <tr>
          <th>10</th>
          <td>11</td>
          <td>128</td>
          <td>230</td>
        </tr>
        <tr>
          <th>11</th>
          <td>12</td>
          <td>124</td>
          <td>230</td>
        </tr>
        <tr>
          <th>12</th>
          <td>13</td>
          <td>126</td>
          <td>230</td>
        </tr>
        <tr>
          <th>13</th>
          <td>14</td>
          <td>129</td>
          <td>230</td>
        </tr>
        <tr>
          <th>14</th>
          <td>15</td>
          <td>126</td>
          <td>230</td>
        </tr>
        <tr>
          <th>15</th>
          <td>16</td>
          <td>122</td>
          <td>235</td>
        </tr>
        <tr>
          <th>16</th>
          <td>17</td>
          <td>122</td>
          <td>235</td>
        </tr>
        <tr>
          <th>17</th>
          <td>18</td>
          <td>122</td>
          <td>235</td>
        </tr>
        <tr>
          <th>18</th>
          <td>19</td>
          <td>119</td>
          <td>235</td>
        </tr>
        <tr>
          <th>19</th>
          <td>20</td>
          <td>122</td>
          <td>235</td>
        </tr>
      </tbody>
    </table>
    </div>



Data can also be read from a ``.xlsx`` (Excel extension) file. To do so,
use the ``ImportXLSX`` class of ``explain.dataio``. Default is to read
the first ``Sheet``, otherwise desired provide the additional argument
``sheet_name``

.. code:: ipython3

    from explann.dataio import ImportXLSX
    
    data_reader_xlsx = ImportXLSX(path="../../data/paper_data_24.xlsx")
    
    data_reader_xlsx.data




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>U</th>
          <th>A</th>
          <th>P</th>
          <th>Y</th>
          <th>F</th>
          <th>C</th>
          <th>B</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>-1</td>
          <td>-1</td>
          <td>-1</td>
          <td>-1</td>
          <td>39</td>
          <td>1.328</td>
          <td>170</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>-1</td>
          <td>-1</td>
          <td>-1</td>
          <td>87</td>
          <td>1.699</td>
          <td>122</td>
        </tr>
        <tr>
          <th>2</th>
          <td>-1</td>
          <td>1</td>
          <td>-1</td>
          <td>-1</td>
          <td>48</td>
          <td>1.332</td>
          <td>473</td>
        </tr>
        <tr>
          <th>3</th>
          <td>1</td>
          <td>1</td>
          <td>-1</td>
          <td>-1</td>
          <td>71</td>
          <td>1.979</td>
          <td>511</td>
        </tr>
        <tr>
          <th>4</th>
          <td>-1</td>
          <td>-1</td>
          <td>1</td>
          <td>-1</td>
          <td>43</td>
          <td>1.458</td>
          <td>156</td>
        </tr>
        <tr>
          <th>5</th>
          <td>1</td>
          <td>-1</td>
          <td>1</td>
          <td>-1</td>
          <td>84</td>
          <td>2.189</td>
          <td>204</td>
        </tr>
        <tr>
          <th>6</th>
          <td>-1</td>
          <td>1</td>
          <td>1</td>
          <td>-1</td>
          <td>45</td>
          <td>1.343</td>
          <td>385</td>
        </tr>
        <tr>
          <th>7</th>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>-1</td>
          <td>112</td>
          <td>1.707</td>
          <td>288</td>
        </tr>
        <tr>
          <th>8</th>
          <td>-1</td>
          <td>-1</td>
          <td>-1</td>
          <td>1</td>
          <td>19</td>
          <td>1.257</td>
          <td>114</td>
        </tr>
        <tr>
          <th>9</th>
          <td>1</td>
          <td>-1</td>
          <td>-1</td>
          <td>1</td>
          <td>146</td>
          <td>2.148</td>
          <td>116</td>
        </tr>
        <tr>
          <th>10</th>
          <td>-1</td>
          <td>1</td>
          <td>-1</td>
          <td>1</td>
          <td>50</td>
          <td>1.592</td>
          <td>244</td>
        </tr>
        <tr>
          <th>11</th>
          <td>1</td>
          <td>1</td>
          <td>-1</td>
          <td>1</td>
          <td>92</td>
          <td>1.726</td>
          <td>126</td>
        </tr>
        <tr>
          <th>12</th>
          <td>-1</td>
          <td>-1</td>
          <td>1</td>
          <td>1</td>
          <td>107</td>
          <td>1.203</td>
          <td>72</td>
        </tr>
        <tr>
          <th>13</th>
          <td>1</td>
          <td>-1</td>
          <td>1</td>
          <td>1</td>
          <td>172</td>
          <td>2.261</td>
          <td>210</td>
        </tr>
        <tr>
          <th>14</th>
          <td>-1</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>62</td>
          <td>1.434</td>
          <td>234</td>
        </tr>
        <tr>
          <th>15</th>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>82</td>
          <td>1.848</td>
          <td>154</td>
        </tr>
        <tr>
          <th>16</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>75</td>
          <td>1.726</td>
          <td>223</td>
        </tr>
        <tr>
          <th>17</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>70</td>
          <td>1.782</td>
          <td>219</td>
        </tr>
        <tr>
          <th>18</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>89</td>
          <td>1.753</td>
          <td>226</td>
        </tr>
      </tbody>
    </table>
    </div>



Any importer has the functionality to parse levels of an factorial
design such as the above one.

.. code:: ipython3

    levels_string = """
    Levels;U;A;P;Y
    -1;0.15;0.7; 0.40;0.13
    0; 0.30;1.4; 0.75;0.26
    1; 0.45;2.1; 1.10;0.38
    """
    
    levels_reader = ImportString(
        data = levels_string, 
        delimiter = ";",
        index_col = 0  # should pass the column name or index containing the level.
    )
    levels_reader.data




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>U</th>
          <th>A</th>
          <th>P</th>
          <th>Y</th>
        </tr>
        <tr>
          <th>Levels</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>-1</th>
          <td>0.15</td>
          <td>0.7</td>
          <td>0.40</td>
          <td>0.13</td>
        </tr>
        <tr>
          <th>0</th>
          <td>0.30</td>
          <td>1.4</td>
          <td>0.75</td>
          <td>0.26</td>
        </tr>
        <tr>
          <th>1</th>
          <td>0.45</td>
          <td>2.1</td>
          <td>1.10</td>
          <td>0.38</td>
        </tr>
      </tbody>
    </table>
    </div>



The same data should be imported from a ``.xlsx`` file.

.. code:: ipython3

    levels_reader_xlsx = ImportXLSX(
        path="../../data/paper_data_24.xlsx",
        sheet_name="Levels",
        index_col=0,
    )
    levels_reader_xlsx.data




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>U</th>
          <th>A</th>
          <th>P</th>
          <th>Y</th>
        </tr>
        <tr>
          <th>Levels</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>-1</th>
          <td>0.15</td>
          <td>0.7</td>
          <td>0.40</td>
          <td>0.13</td>
        </tr>
        <tr>
          <th>0</th>
          <td>0.30</td>
          <td>1.4</td>
          <td>0.75</td>
          <td>0.26</td>
        </tr>
        <tr>
          <th>1</th>
          <td>0.45</td>
          <td>2.1</td>
          <td>1.10</td>
          <td>0.38</td>
        </tr>
      </tbody>
    </table>
    </div>



The data reader ``parse_levels`` acept a ``pd.Dataframe`` constructed
from any one of the methods above, you can pass ``string`` or ``.xlsx``
files to the methos ``parse_levels_from_string`` and
``parse_levels_from_xlsx``.

.. code:: ipython3

    # passing a pd.DataFrame
    data_reader_xlsx.parse_levels(
        data = levels_reader.data
    )
    
    # passing a string
    data_reader_xlsx.parse_levels_from_string(
        data = levels_string, 
        delimiter=";"
    )
    
    # passing a path
    data_reader_xlsx.parse_levels_from_xlsx(
        data = "../../data/paper_data_24.xlsx", 
        sheet_name = "Levels",
        index_col=0,
    )


The results are the same, ``data`` attribute has its values parsed to
the corresponding index levels for each variable as described in the
``levels_reades_<type>.data`` table.

.. code:: ipython3

    data_reader_xlsx.data




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>U</th>
          <th>A</th>
          <th>P</th>
          <th>Y</th>
          <th>F</th>
          <th>C</th>
          <th>B</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>-1</td>
          <td>0.7</td>
          <td>0.40</td>
          <td>0.13</td>
          <td>39</td>
          <td>1.328</td>
          <td>170</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>0.7</td>
          <td>0.40</td>
          <td>0.13</td>
          <td>87</td>
          <td>1.699</td>
          <td>122</td>
        </tr>
        <tr>
          <th>2</th>
          <td>-1</td>
          <td>2.1</td>
          <td>0.40</td>
          <td>0.13</td>
          <td>48</td>
          <td>1.332</td>
          <td>473</td>
        </tr>
        <tr>
          <th>3</th>
          <td>1</td>
          <td>2.1</td>
          <td>0.40</td>
          <td>0.13</td>
          <td>71</td>
          <td>1.979</td>
          <td>511</td>
        </tr>
        <tr>
          <th>4</th>
          <td>-1</td>
          <td>0.7</td>
          <td>1.10</td>
          <td>0.13</td>
          <td>43</td>
          <td>1.458</td>
          <td>156</td>
        </tr>
        <tr>
          <th>5</th>
          <td>1</td>
          <td>0.7</td>
          <td>1.10</td>
          <td>0.13</td>
          <td>84</td>
          <td>2.189</td>
          <td>204</td>
        </tr>
        <tr>
          <th>6</th>
          <td>-1</td>
          <td>2.1</td>
          <td>1.10</td>
          <td>0.13</td>
          <td>45</td>
          <td>1.343</td>
          <td>385</td>
        </tr>
        <tr>
          <th>7</th>
          <td>1</td>
          <td>2.1</td>
          <td>1.10</td>
          <td>0.13</td>
          <td>112</td>
          <td>1.707</td>
          <td>288</td>
        </tr>
        <tr>
          <th>8</th>
          <td>-1</td>
          <td>0.7</td>
          <td>0.40</td>
          <td>0.38</td>
          <td>19</td>
          <td>1.257</td>
          <td>114</td>
        </tr>
        <tr>
          <th>9</th>
          <td>1</td>
          <td>0.7</td>
          <td>0.40</td>
          <td>0.38</td>
          <td>146</td>
          <td>2.148</td>
          <td>116</td>
        </tr>
        <tr>
          <th>10</th>
          <td>-1</td>
          <td>2.1</td>
          <td>0.40</td>
          <td>0.38</td>
          <td>50</td>
          <td>1.592</td>
          <td>244</td>
        </tr>
        <tr>
          <th>11</th>
          <td>1</td>
          <td>2.1</td>
          <td>0.40</td>
          <td>0.38</td>
          <td>92</td>
          <td>1.726</td>
          <td>126</td>
        </tr>
        <tr>
          <th>12</th>
          <td>-1</td>
          <td>0.7</td>
          <td>1.10</td>
          <td>0.38</td>
          <td>107</td>
          <td>1.203</td>
          <td>72</td>
        </tr>
        <tr>
          <th>13</th>
          <td>1</td>
          <td>0.7</td>
          <td>1.10</td>
          <td>0.38</td>
          <td>172</td>
          <td>2.261</td>
          <td>210</td>
        </tr>
        <tr>
          <th>14</th>
          <td>-1</td>
          <td>2.1</td>
          <td>1.10</td>
          <td>0.38</td>
          <td>62</td>
          <td>1.434</td>
          <td>234</td>
        </tr>
        <tr>
          <th>15</th>
          <td>1</td>
          <td>2.1</td>
          <td>1.10</td>
          <td>0.38</td>
          <td>82</td>
          <td>1.848</td>
          <td>154</td>
        </tr>
        <tr>
          <th>16</th>
          <td>0</td>
          <td>1.4</td>
          <td>0.75</td>
          <td>0.26</td>
          <td>75</td>
          <td>1.726</td>
          <td>223</td>
        </tr>
        <tr>
          <th>17</th>
          <td>0</td>
          <td>1.4</td>
          <td>0.75</td>
          <td>0.26</td>
          <td>70</td>
          <td>1.782</td>
          <td>219</td>
        </tr>
        <tr>
          <th>18</th>
          <td>0</td>
          <td>1.4</td>
          <td>0.75</td>
          <td>0.26</td>
          <td>89</td>
          <td>1.753</td>
          <td>226</td>
        </tr>
      </tbody>
    </table>
    </div>



Original data is retained in a ``raw_data`` attribute

.. code:: ipython3

    data_reader_xlsx.raw_data




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>U</th>
          <th>A</th>
          <th>P</th>
          <th>Y</th>
          <th>F</th>
          <th>C</th>
          <th>B</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>-1</td>
          <td>-1</td>
          <td>-1</td>
          <td>-1</td>
          <td>39</td>
          <td>1.328</td>
          <td>170</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>-1</td>
          <td>-1</td>
          <td>-1</td>
          <td>87</td>
          <td>1.699</td>
          <td>122</td>
        </tr>
        <tr>
          <th>2</th>
          <td>-1</td>
          <td>1</td>
          <td>-1</td>
          <td>-1</td>
          <td>48</td>
          <td>1.332</td>
          <td>473</td>
        </tr>
        <tr>
          <th>3</th>
          <td>1</td>
          <td>1</td>
          <td>-1</td>
          <td>-1</td>
          <td>71</td>
          <td>1.979</td>
          <td>511</td>
        </tr>
        <tr>
          <th>4</th>
          <td>-1</td>
          <td>-1</td>
          <td>1</td>
          <td>-1</td>
          <td>43</td>
          <td>1.458</td>
          <td>156</td>
        </tr>
        <tr>
          <th>5</th>
          <td>1</td>
          <td>-1</td>
          <td>1</td>
          <td>-1</td>
          <td>84</td>
          <td>2.189</td>
          <td>204</td>
        </tr>
        <tr>
          <th>6</th>
          <td>-1</td>
          <td>1</td>
          <td>1</td>
          <td>-1</td>
          <td>45</td>
          <td>1.343</td>
          <td>385</td>
        </tr>
        <tr>
          <th>7</th>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>-1</td>
          <td>112</td>
          <td>1.707</td>
          <td>288</td>
        </tr>
        <tr>
          <th>8</th>
          <td>-1</td>
          <td>-1</td>
          <td>-1</td>
          <td>1</td>
          <td>19</td>
          <td>1.257</td>
          <td>114</td>
        </tr>
        <tr>
          <th>9</th>
          <td>1</td>
          <td>-1</td>
          <td>-1</td>
          <td>1</td>
          <td>146</td>
          <td>2.148</td>
          <td>116</td>
        </tr>
        <tr>
          <th>10</th>
          <td>-1</td>
          <td>1</td>
          <td>-1</td>
          <td>1</td>
          <td>50</td>
          <td>1.592</td>
          <td>244</td>
        </tr>
        <tr>
          <th>11</th>
          <td>1</td>
          <td>1</td>
          <td>-1</td>
          <td>1</td>
          <td>92</td>
          <td>1.726</td>
          <td>126</td>
        </tr>
        <tr>
          <th>12</th>
          <td>-1</td>
          <td>-1</td>
          <td>1</td>
          <td>1</td>
          <td>107</td>
          <td>1.203</td>
          <td>72</td>
        </tr>
        <tr>
          <th>13</th>
          <td>1</td>
          <td>-1</td>
          <td>1</td>
          <td>1</td>
          <td>172</td>
          <td>2.261</td>
          <td>210</td>
        </tr>
        <tr>
          <th>14</th>
          <td>-1</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>62</td>
          <td>1.434</td>
          <td>234</td>
        </tr>
        <tr>
          <th>15</th>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>82</td>
          <td>1.848</td>
          <td>154</td>
        </tr>
        <tr>
          <th>16</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>75</td>
          <td>1.726</td>
          <td>223</td>
        </tr>
        <tr>
          <th>17</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>70</td>
          <td>1.782</td>
          <td>219</td>
        </tr>
        <tr>
          <th>18</th>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>89</td>
          <td>1.753</td>
          <td>226</td>
        </tr>
      </tbody>
    </table>
    </div>


