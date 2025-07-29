#%%
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf 

#%%
penguins = pd.read_csv(Path(__file__).parent / "penguins.csv")
penguins.head(10)


# %%
##
## くちばしの長いペンギンの方が体重が重いだろうと予測する。
## ただし、種ごとの違いを考慮する必要がある。
##
## ols = ordinary least squares の略。普通の最小二乗法

model = smf.ols("body_mass_g ~ bill_length_mm + species", data=penguins)
res = model.fit(cov_type="HC1")
res.summary()

# %%

print(res.params)

# %%
