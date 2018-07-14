# Чтобы скачать только 10 канал, нужно изменить в band_map.py:

        band_mapping = {#'LC8': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],
                        'LC8': ['10'],
                        'LE7': ['1', '2', '3', '4', '5', '6_VCID_1', '6_VCID_2', '7', '8'],
                        'LT5': ['1', '2', '3', '4', '5', '6', '7']}

# и
        b = {'LANDSAT_1': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6.TIF', 'B7.TIF', 'MTL.txt'],
             'LANDSAT_2': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6.TIF', 'B7.TIF', 'MTL.txt'],
             'LANDSAT_3': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6.TIF', 'B7.TIF', 'MTL.txt'],
             'LANDSAT_4': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6.TIF', 'B7.TIF', 'MTL.txt'],
             'LANDSAT_5': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6.TIF', 'B7.TIF', 'BQA.TIF', 'MTL.txt'],

             'LANDSAT_7': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF',
                           'B6_VCID_1.TIF', 'B6_VCID_2.TIF', 'B7.TIF', 'B8.TIF', 'BQA.TIF', 'MTL.txt'],

             #'LANDSAT_8': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6.TIF',
             #              'B7.TIF', 'B8.TIF', 'B9.TIF', 'B10.TIF', 'B11.TIF', 'BQA.TIF', 'MTL.txt']}
             'LANDSAT_8': ['B10.TIF', 'MTL.txt']}
