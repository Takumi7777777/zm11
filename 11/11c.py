# %%
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# data
penguins_csv = Path(__file__).parent / "penguins.csv"

# destination
# "Run cell" で実行するときと uv run ではできるフォルダが違う
dest_dir = Path().cwd() / "out"
dest_dir.mkdir(exist_ok=True, parents=True)

# %%

df = pd.read_csv(penguins_csv)

# %%
df.head()


# %%

sns.relplot(df, x="flipper_length_mm", y="body_mass_g", hue="species")
plt.savefig(dest_dir / "11c.pdf")

# %%
