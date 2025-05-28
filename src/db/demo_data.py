from datetime import datetime
from time import time
from typing import Dict, List
from uuid import uuid4
import random
from faker import Faker
from sqlalchemy import insert

from src.cars.models import Cars, Expenses
from src.cars.schemas import CarStatusChoices

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import engine
import asyncio

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


def generate_pts_num() -> str:
    """Генерирует номер ПТС в формате 12АБ 123456 или 12аб123456"""
    digits_part1 = f"{random.randint(10, 99)}"  # 2 цифры
    letters = "".join(
        random.choices(
            "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя", k=2
        )
    )  # 2 русские буквы
    digits_part2 = f"{random.randint(100000, 999999)}"  # 6 цифр
    space = " " if random.choice([True, False]) else ""  # Случайный пробел

    return f"{digits_part1}{letters}{space}{digits_part2}"


def generate_sts_num() -> str:
    """Генерирует номер СТС в формате 9999 999999 (4 цифры, пробел, 6 цифр)"""
    part1 = f"{random.randint(1000, 9999)}"  # 4 цифры
    part2 = f"{random.randint(100000, 999999)}"  # 6 цифр
    return f"{part1} {part2}"  # Всегда с пробелом (можно сделать опциональным)


def generate_car():
    """Генерирует один автомобиль с заданным статусом"""
    base_price = random.randint(500000, 5000000)
    date_purchased = fake.date_between(start_date="-20y", end_date="today")
    status = random.choice(
        [
            CarStatusChoices.FRESH,
            CarStatusChoices.REPAIRING,
            CarStatusChoices.DETAILING,
            CarStatusChoices.LISTED,
            CarStatusChoices.SOLD,
        ]
    )

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
        pts_num=generate_pts_num(),
        sts_num=generate_sts_num(),
        date_purchased=date_purchased,
        price_purchased=base_price,
        status=status.value,
        created_at=datetime.now(),
    )
    car.date_listed = fake.date_between(start_date=date_purchased, end_date="today")
    listed_price = base_price + random.randint(50000, 500000)
    car.price_listed = listed_price
    car.date_sold = fake.date_between(start_date=car.date_listed, end_date="today")
    car.price_sold = random.randint(
        int(listed_price * 0.9), listed_price + random.randint(0, 100000)
    )
    car.avito_link = f"https://avito.ru/{fake.uri_path()}"
    car.autoru_link = f"https://auto.ru/{fake.uri_path()}"
    car.drom_link = f"https://drom.ru/{fake.uri_path()}"
    car.autoteka_link = f"https://autoteka.ru/{fake.uri_path()}"
    car.notes = fake.sentence(nb_words=6)

    return car


def generate_demo_cars(quantity: int):
    """Генерирует 50 тестовых автомобилей"""
    cars = []

    for _ in range(quantity):  # SOLD
        car = generate_car()
        if random.random() > 0.3:
            car.expenses = generate_expenses(random.randint(1, 5))
        cars.append(car)

    return cars


async def bulk_insert(session: AsyncSession, car_data: List[Dict]):
    await session.execute(insert(Cars), car_data)
    await session.commit()


async def main():
    total_records = 500
    batch_size = 500
    batches = total_records // batch_size

    async with AsyncSession(engine) as session:

        print(f"Начинаю генерацию и вставку {total_records:,} автомобилей")
        start_time = time()
        for i in range(batches):

            start_gen_time = time()
            batch = generate_demo_cars(batch_size)
            total_gen_time = time() - start_gen_time

            start_insert_time = time()
            await bulk_insert(session, batch)
            total_insert_time = time() - start_insert_time
            print(
                f"Вставлено {(i+1)*batch_size} записей."
                f"Генерация текущего пакета заняла: {total_gen_time:.2f} сек,"
                f"Вставка текущего пакета заняла: {total_insert_time:.2f} сек"
            )
        remaining = total_records % batch_size
        if remaining > 0:
            batch = generate_demo_cars(remaining)
            await bulk_insert(session, batch)
    total_time = time() - start_time
    print(f"Записи вставлены! Время выполнения: {total_time:.2f}сек.")


if __name__ == "__main__":
    asyncio.run(main())
