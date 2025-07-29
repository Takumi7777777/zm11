from pathlib import Path

print("作業ディレクトリ")
print(Path.cwd())

print()

print("penguins.csv")
print(Path.cwd() / "11" / "penguins.csv")
