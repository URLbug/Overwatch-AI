from aiogram.dispatcher.filters.state import State, StatesGroup


class AI_Go(StatesGroup):
    url = State()
    comand = State()
    sum_page = State()