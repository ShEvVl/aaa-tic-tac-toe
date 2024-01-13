import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
)
from .ttt_game import TicTacToeGame


class TicTacToeBot:
    """
    Класс для взаимодействия с игрой крестики-нолики в Telegram.
    """

    CONTINUE_GAME = 0
    FINISH_GAME = 1

    def __init__(self, token: str) -> None:
        """
        Инициализация бота для игры в крестики-нолики.

        :param token: Токен бота.
        """
        self.token = token
        self.game = TicTacToeGame()

    def generate_keyboard(self) -> InlineKeyboardMarkup:
        """
        Генерация клавиатуры для игры.

        :return: Объект клавиатуры Telegram.
        """
        keyboard = [
            [
                InlineKeyboardButton(
                    self.game.board[i][j], callback_data=f"{i}{j}"
                )
                for j in range(3)
            ]
            for i in range(3)
        ]
        return InlineKeyboardMarkup(keyboard)

    async def start(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Начать новую игру при команде /start.
        """
        await self.game.reset()
        keyboard = self.generate_keyboard()
        await update.message.reply_text(
            "Ваш ход! Пожалуйста, выберите клетку.", reply_markup=keyboard
        )
        return self.CONTINUE_GAME

    async def game_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Обработчик ходов в игре.
        """
        query = update.callback_query
        await query.answer()
        row, col = int(query.data[0]), int(query.data[1])

        if not self.game.make_move(row, col, TicTacToeGame.CROSS):
            await query.edit_message_text(
                text="Эта клетка уже занята!",
                reply_markup=self.generate_keyboard(),
            )
            return self.CONTINUE_GAME

        if self.game.check_win(TicTacToeGame.CROSS):
            await query.edit_message_text(
                text="Поздравляем! Вы выиграли!",
                reply_markup=self.generate_keyboard(),
            )
            return self.FINISH_GAME

        if self.game.is_draw():
            await query.edit_message_text(
                text="Ничья!", reply_markup=self.generate_keyboard()
            )
            return self.FINISH_GAME

        # Ход ИИ
        empty_cells = self.game.get_empty_cells()
        if empty_cells:
            ai_move = random.choice(empty_cells)
            self.game.make_move(ai_move[0], ai_move[1], TicTacToeGame.ZERO)

            if self.game.check_win(TicTacToeGame.ZERO):
                await query.edit_message_text(
                    text="Вы проиграли!", reply_markup=self.generate_keyboard()
                )
                return self.FINISH_GAME

            if self.game.is_draw():
                await query.edit_message_text(
                    text="Ничья!", reply_markup=self.generate_keyboard()
                )
                return self.FINISH_GAME

        await query.edit_message_text(
            text="Ваш ход!", reply_markup=self.generate_keyboard()
        )
        return self.CONTINUE_GAME

    async def end(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Закончить игру и сбросить состояние.
        """
        self.game.reset()
        return ConversationHandler.END

    def run(self) -> None:
        """
        Запустить бота.
        """
        from telegram.ext import Application

        application = Application.builder().token(self.token).build()

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                self.CONTINUE_GAME: [CallbackQueryHandler(self.game_handler)],
                self.FINISH_GAME: [CallbackQueryHandler(self.end)],
            },
            fallbacks=[CommandHandler("start", self.start)],
            per_message=False,
        )

        application.add_handler(conv_handler)
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()
    token = os.getenv("TOKEN")
    bot = TicTacToeBot(token)
    bot.run()
