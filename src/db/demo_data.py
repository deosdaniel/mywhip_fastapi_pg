from datetime import date, datetime
from uuid import uuid4
import random
from faker import Faker
from src.cars.models import Cars, Expenses
from src.cars.schemas import CarStatusChoices

fake = Faker("ru_RU")  # Для русскоязычных данных


def generate_expenses(count: int):
    """Генерирует список расходов"""
    expense_names = [
        "Покраска",
        "Замена масла",
        "Ремонт подвески",
        "Шиномонтаж",
        "Химчистка",
        "Полировка",
        "Замена стекла",
        "Ремонт АКПП",
        "Тонировка",
    ]
    return [
        Expenses(
            name=random.choice(expense_names), exp_summ=random.randint(5000, 50000)
        )
        for _ in range(count)
    ]


def generate_car(status: str):
    """Генерирует один автомобиль с заданным статусом"""
    base_price = random.randint(500000, 5000000)
    date_purchased = fake.date_between(start_date="-2y", end_date="today")

    car = Cars(
        uid=uuid4(),
        make=fake.random_element(
            ["Toyota", "BMW", "Mercedes", "Audi", "Ford", "Kia", "Hyundai"]
        ),
        model=fake.random_element(
            ["Camry", "X5", "C-Class", "A6", "Focus", "Rio", "Solaris"]
        ),
        year=int(
            fake.date_between(start_date="-13y", end_date="today").year
        ),  # Исправлено здесь
        vin=fake.vin(),
        pts_num=fake.bothify("##??######"),
        sts_num=fake.bothify("##??######"),
        date_purchased=date_purchased,
        price_purchased=base_price,
        status=status.value,
        created_at=datetime.now(),
    )

    # Общие для SOLD и LISTED поля
    if status in [CarStatusChoices.SOLD, CarStatusChoices.LISTED]:
        car.date_listed = fake.date_between(start_date=date_purchased, end_date="today")
        listed_price = base_price + random.randint(50000, 500000)
        car.price_listed = listed_price

        if status == CarStatusChoices.SOLD:
            car.date_sold = fake.date_between(
                start_date=car.date_listed, end_date="today"
            )
            car.price_sold = random.randint(
                int(listed_price * 0.9), listed_price + random.randint(0, 100000)
            )

        elif status == CarStatusChoices.LISTED:
            car.avito_link = f"https://avito.ru/{fake.uri_path()}"
            car.autoru_link = f"https://auto.ru/{fake.uri_path()}"
            car.drom_link = f"https://drom.ru/{fake.uri_path()}"

    if random.choice([True, False]):
        car.autoteka_link = f"https://autoteka.ru/{fake.uri_path()}"
    if random.choice([True, False]):
        car.notes = fake.sentence(nb_words=6)

    return car


def generate_demo_cars():
    """Генерирует 50 тестовых автомобилей"""
    cars = []

    for _ in range(21):  # SOLD
        car = generate_car(CarStatusChoices.SOLD)
        if random.random() > 0.3:
            car.expenses = generate_expenses(random.randint(1, 5))
        cars.append(car)

    for _ in range(17):  # Без расходов
        status = random.choice(
            [
                CarStatusChoices.FRESH,
                CarStatusChoices.REPAIRING,
                CarStatusChoices.DETAILING,
            ]
        )
        cars.append(generate_car(status))

    for _ in range(12):  # С расходами
        status = random.choice(list(CarStatusChoices))
        car = generate_car(status)
        car.expenses = generate_expenses(random.randint(1, 5))
        cars.append(car)

    return cars
