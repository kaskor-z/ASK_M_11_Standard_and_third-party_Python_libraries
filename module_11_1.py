import pandas as pn
import matplotlib.pyplot as plt
import requests
from pprint import pprint

"""
*** ПОЛУЧЕНИЕ ДАННЫХ с сайта https://www.imf.org/ для визуализации и анализа
"""
analyz_year = input(f'Введите год  для анализа население земли по странам (в интервале от 2012 до 2029): ')
print(f"\n\tИСТОЧНИК ДАННЫХ:")
POPULATION = "https://www.imf.org/external/datamapper/api/v1/LP?periods=" + analyz_year
print('**** ', POPULATION)
LIST_COUNTRIES = "https://www.imf.org/external/datamapper/api/v1/countries"
print('**** ', LIST_COUNTRIES)
response = requests.get(POPULATION)
"""
*** ПОДГОТОВКА ДАННЫХ для визуализации: включая выборку, сортировку и формирование DataFrame
"""
df_01_Tr = (pn.DataFrame(response.json()["values"]["LP"])).T
wold_population = df_01_Tr.at["WEOWORLD", analyz_year]
print(f'Население земли = {wold_population}')
response = requests.get(LIST_COUNTRIES)
df_02_Tr = (pn.DataFrame(response.json()["countries"])).T
df_03_Tr = pn.concat([df_02_Tr, df_01_Tr], axis=1, sort=True)
df_03_Tr.dropna(inplace=True)
df_03_Tr[analyz_year] = df_03_Tr[analyz_year].astype(float)
df_03_Tr.sort_values(by=[analyz_year], inplace=True, ascending=False)
df_04 = df_03_Tr.loc[df_03_Tr[analyz_year] >= wold_population * 0.01]
print(f'\nВыборка для диограммы:\n{df_04}')
pprint(df_04.info())
z = df_04[analyz_year].sum()
print("\n*****")
print(f'Численность население Земли в {analyz_year} году составила: {wold_population} мил.человек')
print(f'Численность населения 19 стран, выбранных для визуализации: {z} мил.человек')
print(f'Численность населения остальных страны:'
      f' {round((wold_population - z), 3)} мил.человек\n (с численностью '
      f'менее 1 % от населения планеты)\nэто - 19 стран :'
      f' {round((z / wold_population * 100), 1)} %\n '
      f'\t  остальные : {round(((wold_population - z) / wold_population * 100), 1)} %')
df_05 = pn.DataFrame({"label": ["All other countries", ],
                      analyz_year: [(wold_population - z), ]}, index=["all_other", ])
df_06 = pn.concat([df_04, df_05])
print(f'\nРЕЗУЛЬТАТ:\n{df_06}')
"""
*** ВИЗУАЛИЗАЦИЯ ДАННЫХ
"""
exp = (
    0.1, 0.1, 0, 0, 0, 0, 0, 0.01, 0.02, 0.03,
    0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0
)
plot = df_06.plot.pie(y=analyz_year, subplots=False, figsize=(12, 7),
                      autopct='%1.2f%%', explode=exp, shadow=1,
                      labeldistance=1.1, pctdistance=0.85, center=(-2, 0),
                      textprops=dict(color="r"), labels=df_06['label'],
                      title=f'Население земли в {analyz_year} \n'
                            f'составляло {wold_population} миллионов человек')
plot.legend(loc=1, fontsize=8, bbox_to_anchor=(1.13, 0.6, 0.3, 0.3), framealpha=0.3, labelspacing=0.3)
plt.show()
pprint(response.reason)
