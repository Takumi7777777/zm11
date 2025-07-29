import datetime

import typer

from zm11 import mathtools

app = typer.Typer()


@app.callback()
def callback():
    """
    A Collection of Useful Commands
    """


@app.command()
def now():
    """
    Show local date and time
    """
    today = datetime.datetime.today()
    typer.echo(today.strftime('%A, %B %d, %Y'))


@app.command()
def gcd(x: int, y: int):
    """
    Greatest Common Divisor
    """
    typer.echo(mathtools.gcd(x, y))


@app.command()
def bigger(num1: float, num2: float):
    """
    2つの数字を入力し、大きい方を出力します。
    """
    if num1 > num2:
        print(f"大きい数字は: {num1}")
    elif num2 > num1:
        print(f"大きい数字は: {num2}")
    else:
        print("2つの数字は同じです。")

if __name__ == "__main__":
    app()




from. import demo


@app.command()
def hello(name:str = "Takumi"):
    typer.echo(demo.hello(name))






