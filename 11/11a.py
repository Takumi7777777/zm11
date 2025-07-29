from pathlib import Path

print("このファイル")
print(Path(__file__))

print()

print("親ディレクトリ")
print(Path(__file__).parent)

print()

print("penguins.csv")
print(Path(__file__).parent / "penguins.csv")