===================
Begginer's tutorial
===================


Data input
----------


Data can be read from a string, by using the `ImportString` class of `explain.dataio`. The default delimiter is `\s` the spectial charactere for whitespaces

::

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


`data_reader` object stores the providade data in its `.data` attribute

::

    data_reader_string.data



