import os


def black():
    print("----running black----")
    os.system("poetry run black --check dunzo")
    os.system("poetry run black --check util")
    print("poetry run black dunzo")
    print("poetry run black util")


def isort():
    print("----running isort----")
    os.system("isort --check-only .")
    print("poetry run isort .")


# def mypy():
#     print("mypy")
#     os.system("mypy .")


def format():
    black()
    isort()
