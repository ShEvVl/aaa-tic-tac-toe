# aaa-tic-tac-toe / крестики-нолики

![tic-tac-toe](/readme_data/Tic-Tac-Toe_game.png)

<details>
<summary>Задание</summary>

## Telegram-бот для игры вкрестики-нолики

### Бизнес-логика

- бот в Telegram
- обработка нажатий
- условие победы
- ИИ-оппонент (random)
- мультиплеер (опционально)

### Q&A

- бот?! а с чего начать?

>ниже дан шаблон приложения-бота, нужно дополнить его бизнеслогикой игры

<details>
<summary>Шаблон приложения</summary>

```python
#!/usr/bin/env python

"""
Bot for playing tic tac toe game with multiple CallbackQueryHandlers.
"""
from copy import deepcopy
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
import os


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# get token using BotFather
TOKEN = os.getenv('TG_TOKEN')

CONTINUE_GAME, FINISH_GAME = range(2)

FREE_SPACE = '.'
CROSS = 'X'
ZERO = 'O'


DEFAULT_STATE = [ [FREE_SPACE for _ in range(3) ] for _ in range(3) ]


def get_default_state():
    """Helper function to get default state of the game"""
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
    """Generate tic tac toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'X (your) turn! Please, put X to the free place', reply_markup=reply_markup)
    return CONTINUE_GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Main processing of the game"""
    # PLACE YOUR CODE HERE


def won(fields: list[str]) -> bool:
    """Check if crosses or zeros have won the game"""
    # PLACE YOUR CODE HERE


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    # reset state to default so you can play again with /start
    context.user_data['keyboard_state'] = get_default_state()
    return ConversationHandler.END


def main() -> None:
    """Run the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONTINUE_GAME: [
                CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
            FINISH_GAME: [
                CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
```

### Описание шаблона

Описание шаблона: логирование

позволяет отслеживать исполнение, уровень логирования выкручен,
т.к. дефолтное значение INFO, но при работе с веб-пакетами оно
логирует много лишнего

```python
# Enable logging
logging.basicConfig(
 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(-_name-_)
```

Описание шаблона: токен

Токен, сгенерированный у BotFather. Прокидываем в приложение
через переменные окружения. ОЧЕНЬ ВАЖНО: ИЗБЕГАЙТЕ КОММИТА В Git
ТОКЕНОВ И ЛЮБЫХ ДРУГИХ СЕКРЕТОВ.

```python
TOKEN = os.getenv('TG_TOKEN')
```

Описание шаблона: дефолтные настройки

Через двойной comprehension описываем исходное состояние игровой
"клавиатуры".

```python
FREE_SPACE = '.'
CROSS = 'X'
ZERO = 'O'
DEFAULT_STATE = [ [FREE_SPACE for _ in range(3) ] for _ in range(3)
def get_default_state():
 """Helper function to get default state of the game"""
 return deepcopy(DEFAULT_STATE) # предположите, зачем тут deepcopy
```

Описание шаблона: UI клавиатуры

из списка списков 3x3 генерируем клавиатуру в Telegram. Каждая кнопка это
InlineKeyboardButton. Клавиатура, состоящая из таких кнопок описывается через
InlineKeyboardMarkup. Inline в обоих случаях означает, что клавиатура встроена в тело
сообщения от бота

```python
def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
 """Generate tic tac toe keyboard 3x3 (telegram buttons)"""
 return [
 [
 InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
 for r in range(3)
 ]
 for c in range(3)
 ]
```

Описание шаблона: старт игры

для запуска бота принято использовать слеш-команду /start (почти
как эндпойнт в браузере). update и context - дефолтные параметры
SDK, которые позволяют обращаться к данным из чата в Telegram.

```python
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
 """Send message on `/start`."""
 context.user_data['keyboard_state'] = get_default_state()
 keyboard = generate_keyboard(context.user_data['keyboard_state'])
 reply_markup = InlineKeyboardMarkup(keyboard) # сама клавиатура
 await update.message.reply_text(f'X (your) turn! Please, put X to the free
place', reply_markup=reply_markup)
 return CONTINUE_GAME # состояния приложения описаны в conv_handler
```

Описание шаблона: бизнес логика

нужно написать 2 функции - обработка процесса игры, логику оппонента(ИИ или
мультиплеер с реальным игроком) и определение победителя. часть функционала можно
выносить во вспомогательные структуры - функции, классы, модули. обратите внимание
на то, какие функции - синхронные или асинхронные - вы используете, и почему

```python
async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
 """Main processing of the game"""
 # PLACE YOUR CODE HERE
def won(fields: list[str]) -> bool:
 """Check if crosses or zeros have won the game"""
 # PLACE YOUR CODE HERE
```
Описание шаблона: зевршение игры

функция end так же управляет состоянием - завершает игру через ConversationHandler.END. conversation
сценарий из состояний, по которому выполняется программа(см. следующий слайд).
Важный момент: поле user_data в context - дефолтное место для хранения пользовательской информации.
если вам нужно как-то протаскивать пользовательские данные внутри нескольких состояний - используем
его. тут в нём храним состояние игровой клавиатуры между ходами игроков. название 'keyboard_state'-
не системное, это просто ключ, который хорошо отражает смысл переменной, в которой храним состояние

```python
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
 """Returns `ConversationHandler.END`, which tells the
 ConversationHandler that the conversation is over.
 """
 # reset state to default so you can play again with /start
 context.user_data['keyboard_state'] = get_default_state()
 return ConversationHandler.END
```

Описание шаблона: инициация и запуск

Сначала инициируем бота через Application, через токен вашего бота, полученный от
BotFather
Затем регистрируем набор состояний, между которыми переходит приложение(см.
следующий слайд)
Запускаем бота - т.е. ожидание пользовательского ввода и реакция на него в
зависимости от бизнес-логики бота

```python
 application = Application.builder().token(TOKEN).build()

 # Add ConversationHandler to application that will be used for handling updates
 application.add_handler(conv_handler)

 # Run the bot until the user presses Ctrl-C
 application.run_polling(allowed_updates=Update.ALL_TYPES)
```

```python
 # Setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
 # Use the pattern parameter to pass CallbackQueries with specific
 # data pattern to the corresponding handlers.
 # ^ means "start of line/string"
 # $ means "end of line/string"
 # So ^ABC$ will only allow 'ABC'
 # в pattern - регулярные выражения для валидации кнопки, на которую будет вызываться функция, по тексту на ней
 conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)], # точка входа в приложение /start -> def start()
    states={
        CONTINUE_GAME: [ # состояние "играть" крутится, пока не будет победы/поражения/ничьей
            CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
            for r in range(3)
            for c in range(3)
        ],
        FINISH_GAME: [ # состояние "завершить игру". возвращает всё к дефолтным значениям, завершает Conversation
            CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
            for r in range(3)
            for c in range(3)
        ],
    }, # для перехода в нужное состояние возвращаем его название (CONTINUE_GAME или FINISH_GAME)
    fallbacks=[CommandHandler('start', start)], # в случае выхода возвращаемся в /start
 )
```

</details>

- что с обработкой нажатий?

>шаблон рисует в чате клавиатуру, которая ничего не делает.
нужно добавить связь клавиатуры с приложением

- что за ИИ нужен?

>достаточно проставлять символ в случайную свободную ячейку
поля

- какое условие победы?

>победа классическая - 3 одинаковых символа в ряд -
горизонталь/вертикаль/диагональ

- мультиплеер можно не делать?

>да

- что входит в мультиплеер?

>создание игры, подключение к игре, обработка ожидания и
очерёдности запросов от двух игроков

### Технические требования

- читаемый и понятный код
- тесты на основной функционал
- понимание основ ООП (разделение и переиспользование кода)
- работа с асинхронностью
- владение git
- понимание основ ФП

### Подготовка

- создать бота
- добавить переменные окружения:
  - windows: `set VARIABLE_NAME=value`
  - mac/linux: `export VARIABLE_NAME=value`
- установить python-telegram-bot

## Как запускать?

- запускаем `.py` файл с ботом
- в переписке с ботом пишем `/start` (или
жмём предыдущее сообщение с `/start`)
- после изменений нужно
перезапустить бота (`ctrl` + `C` и
запустить снова)

</details>

## Бизнес-логика:

- [ ] бот в Telegram
- [ ] обработка нажатий
- [ ] условие победы
- [ ] ИИ-оппонент (random)
- [ ] мультиплеер (опционально)
