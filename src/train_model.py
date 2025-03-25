import pandas as pd
from river import compose, linear_model, metrics, preprocessing, datasets


# file_path = "data/input/AAPL.csv"
# # read the data
# df = pd.read_csv(file_path)
# df_dict = df.to_dict()

for x, y in datasets.AirlinePassengers():
    print(x, y)
    break

def get_ordinal_date(x):
    return {'ordinal_date': x['month'].toordinal()}


model = compose.Pipeline(
    ('ordinal_date', compose.FuncTransformer(get_ordinal_date)),
    ('scale', preprocessing.StandardScaler()),
    ('lin_reg', linear_model.LinearRegression())
)

