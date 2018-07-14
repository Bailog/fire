from landsat import google_download as googl
from os import path
import rasterpy as rpy
import math
import gdal
import utm
import kmlParse
import numpy as np

# Константы для рассчета излучения и яркостной температуры
const_radiance_mul_b10 = 0.0003342
const_radiance_add_b10 = 0.1
const_k1_b10 = 774.8853
const_k2_b10 = 1321.0789
const_one = 1
const_celsius = 273.15
# TOA = 0.0003342 * “Band 10” + 0.1         Radiance
# BT = (K2 / (ln (K1 / L) + 1)) - 273.15    Temperature


# Скачивает все снимки по указанным параметрам
# Параметры: (начальная дата, конечная дата, процент облачности(0-100), широта, долгота, путь скачивания)
# Формат даты: 'ГГГГ-ММ-ДД'
def landsat_download(date_start, date_end, clouds_max, lat, lon, output):
    g = googl.GoogleDownload(start=date_start,
                             end=date_end,
                             satellite=8,
                             max_cloud_percent=clouds_max,
                             latitude=lat,
                             longitude=lon,
                             zipped=False,
                             output_path=output)
    g.download()


# Рассчитывает температуру в каждой точке изображения
# Принимает на вход путь до тифки и сам файл
def calculate_temperature(tif_path, tif_file):
    grid = rpy.Raster(tif_file, tif_path)
    grid.to_array()
    grid.reshape()
    #print(grid.array[0])

    for i in range(0, len(grid.array)):
        for j in range(0, len(grid.array[i])):
            print("id: " + str(i) + " " + str(j))
            value = float(grid.array[i][j])
            #print(value)
            toa = const_radiance_mul_b10 * value + const_radiance_add_b10
            print("Излучение: " + str(toa))

            # ЕБУЧИЕ КОМПЛЕКСНЫЕ ЧИСЛА
            foo = math.log((const_k1_b10 / toa) + 1)

            #print("TEST: " + str(math.log10((774.8853 / 9.192913599999999) + 1) ))
            bt = (const_k2_b10 / foo) - const_celsius
            print("Температура: " + str(bt))
            grid.array[i][j] = bt

            print("----------------")

    print("Максимальная температура: " + str(max(grid.array.flatten())))
    print("Минимальная температура: " + str(min(grid.array.flatten())))
    #print(len(grid.array))
    return grid.array


'''
def gdtemperature():
    #dataset = gdal.Open('f:/8/LC81470212018170LGN00/1111.tif')

    gdalData = gdal.Open('f:/8/new.tif')
    #if gdalData is None:
    #    sys.exit("ERROR: can't open raster")

    # get width and heights of the raster
    xsize = gdalData.RasterXSize
    ysize = gdalData.RasterYSize

    # get number of bands
    bands = gdalData.RasterCount

    # process the raster
    for i in range(1, bands + 1):
        band_i = gdalData.GetRasterBand(i)
        raster = band_i.ReadAsArray()

        # create dictionary for unique values count
        count = {}

        # count unique values for the given band
        for col in range(xsize):
            for row in range(ysize):
                cell_value = raster[row, col]
                print(cell_value)
                print(type(cell_value))
'''


# Обрезание тифки по мин/макс значениям области из преобразованного в кортеж кмл файла.
# Обрезанное изображение создается в той же директории, где лежит оригинал
# Принимает на вход путь до тифки, сам файл и кортеж с мин/макс координатами
def clip_tiff(tif_path, tif_file, coord_tuple):
    converted_tuple_min = lat_lon_to_utm(coord_tuple[0], coord_tuple[1])
    converted_tuple_max = lat_lon_to_utm(coord_tuple[2], coord_tuple[3])
    full_path = path.join(tif_path, tif_file)
    ds = gdal.Open(full_path)

    ds = gdal.Translate(tif_path + '/temperature.tif', ds,
                        projWin=[converted_tuple_min[0],
                                 converted_tuple_min[1],
                                 converted_tuple_max[0],
                                 converted_tuple_max[1]])
    ds = None


# Преобразование координат широты/долготы в формат utm
def lat_lon_to_utm(y, x):
    utm_convert = utm.from_latlon(y, x)
    # print(utm_convert)
    return utm_convert


if __name__ == "__main__":
    kml_base = kmlParse.openkml(kmlParse.root)
    kml_dict = kmlParse.fillkml(kml_base)

    min_max_coord = kmlParse.minmaxkml(kml_base, kml_dict[2]['id'])
    # kml_dict[0]['id'] - Черниговский разрез
    # kml_dict[2]['id'] - Харанорский разрез

    landsat_download('2018-05-01', '2018-05-20', 50, min_max_coord[0], min_max_coord[1], 'c:/downloads')
    clip_tiff("c:/downloads/LC81250252018128LGN00/", "LC08_L1TP_125025_20180508_20180517_01_T1_B10.tif", min_max_coord)
    temper_array = np.array(calculate_temperature("c:/downloads/LC81250252018128LGN00", "temperature.tif"))
    print("Точка максимальной температуры: " + str(np.unravel_index(temper_array.argmax(), temper_array.shape)))
    #print(temper_array)
