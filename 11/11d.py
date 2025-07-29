# %%
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib

# data
penguins_csv = Path(__file__).parent / "penguins.csv"

# destination
# "Run cell" で実行するときと uv run ではできるフォルダが違う
dest_dir = Path().cwd() / "out"
dest_dir.mkdir(exist_ok=True, parents=True)

# %%

df = pd.read_csv(penguins_csv)

# %%

p = sns.displot(df, x="flipper_length_mm", hue="species", multiple="stack")
p.set_xlabels("翼の長さ (mm)")
p.set_ylabels("個体数")

plt.savefig(dest_dir / "11d.pdf")

# %%
