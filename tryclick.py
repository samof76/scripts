import click

@click.group()
def test():
  pass

@test.command(help='Say hello')
@click.argument('name')
def hello(**kwargs):
  print("Hello, {}".format(kwargs['name']))


@test.command(help='Say goodbye')
@click.argument('name')
def goodbye(**kwargs):
  print("Goodbye, {}".format(kwargs['name']))


if __name__ == "__main__":
  test()