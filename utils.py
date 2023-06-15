from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    WAIT_PHOTO_STATE = State()
    WAIT_STYLE_STATE = State()



