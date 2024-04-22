from datetime import datetime

from sqlalchemy import insert, select, update, func, and_, text, case
from sqlalchemy.orm import Session
from database.models import engine, currency


class SQL:
    session = Session(engine)

    def insert(self, name: str, rate: float, updated: str):
        data = insert(currency).values(
            name=name,
            rate=rate,
            updated=updated
        )
        self.session.execute(data)
        self.session.commit()

    def update(self, currency_id: int, rate: float, updated: str, last_request: str):
        data = update(currency).where(currency.c.id == currency_id).values(
            rate=rate,
            updated=updated,
            last_request=last_request
        )
        self.session.execute(data)
        self.session.commit()

    def get_currencies(self):
        data = select(currency.c.name, currency.c.rate, currency.c.updated)
        request = self.session.execute(data)
        result = request.fetchall()

        formatted_result = {}

        formatted_result['updated'] = result[0][2].strftime('%H:%M час. %d.%m.%Y')

        currency_rates = {}
        for row in result:
            if row[0] == 'Евро':
                currency_rates['EUR'] = row[1]
            elif row[0] == 'Доллар США':
                currency_rates['USD'] = row[1]
            elif row[0] == 'Японская Иена':
                currency_rates['JPY'] = row[1]
            elif row[0] == 'Китайский Юань':
                currency_rates['CNY'] = row[1]

        formatted_result['currency'] = currency_rates

        return formatted_result

