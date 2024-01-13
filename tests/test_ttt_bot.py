import pytest
from unittest.mock import Mock, AsyncMock, ANY
from src.ttt_bot import TicTacToeBot


@pytest.fixture
def bot():
    bot = TicTacToeBot("test_token")
    bot.game.reset = AsyncMock()
    return bot


@pytest.fixture
def update():
    update = AsyncMock()
    update.message.reply_text = AsyncMock()
    return update


@pytest.fixture
def context():
    context = Mock()
    return context


@pytest.mark.asyncio
async def test_start_game(bot, update, context):
    await bot.start(update, context)
    bot.game.reset.assert_awaited_once()
    update.message.reply_text.assert_awaited_once_with(
        "Ваш ход! Пожалуйста, выберите клетку.", reply_markup=ANY
    )
