import pandas as pd
def convert_to_csv():
    dataa = {
        'CHN': {'COUNTRY': 'China', 'POP': 1_398.72, 'AREA': 9_596.96,
                'GDP': 12_234.78, 'CONT': 'Asia'},
        'IND': {'COUNTRY': 'India', 'POP': 1_351.16, 'AREA': 3_287.26,
                'GDP': 2_575.67, 'CONT': 'Asia', 'IND_DAY': '1947-08-15'}
        }
    df = pd.DataFrame(data=dataa).T
    df.to_csv('data.csv')