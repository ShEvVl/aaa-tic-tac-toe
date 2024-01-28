import pytest
from unittest.mock import Mock, AsyncMock, ANY, MagicMock
from src.ttt_bot import TicTacToeBot


@pytest.fixture
def bot():
    bot = TicTacToeBot("test_token")
    bot.game.reset = Mock()
    return bot


@pytest.fixture
def update():
    update = AsyncMock()
    update.message.reply_text = AsyncMock()
    return update


@pytest.fixture
def context():
    context = MagicMock()
    context.user_data = {}
    return context


@pytest.mark.asyncio
async def test_start_game(bot, update, context):
    await bot.start(update, context)
    update.message.reply_text.assert_awaited_once_with(
        "Ваш ход! Пожалуйста, выберите клетку.", reply_markup=ANY
    )
