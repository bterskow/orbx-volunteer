import asyncio, json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from env import Env
from modules.applications import Applications

env = Env()
bot_token = env.bot_token

applications = Applications(env)

dp = Dispatcher()
bot = Bot(token=bot_token)

categories = [
	'Автотранспорт',
	'РЕБ',
	'Зв\'язок',
	'Продукти харчування',
	'Медичні засоби',
	'Засоби захисту',
	'Одяг та взуття',
	'Обладнання',
	'Будівельні матеріали',
	'Логістика',
	'Побутові речі',
	'Навчання та тренінги',
]

def create_message(_from, item):
	if _from == 'military':
		message = f'''
- Ім'я та прізвище: {item.get('fullname')}
- Контактний номер телефону: {item.get('phonenumber')}
- Електронна пошта: {item.get('email')}
- Місцезнаходження: {item.get('place')}
- Категорія: {item.get('category')}
- Ресурси: {item.get('resource')}
- Кількість доступних ресурсів: {item.get('resourcecount')}
- Додаткова інформація: {item.get('additioninformation')}
- Час додавання: {item.get('created_at')}
'''
	
	elif _from == 'volunteer':
		message = f'''
- Ім'я та прізвище: {item.get('fullname')}
- Контактний номер телефону: {item.get('phonenumber')}
- Електронна пошта: {item.get('email')}
- Місцезнаходження: {item.get('place')}
- Категорія: {item.get('category')}
- Потреби: {item.get('resource')}
- Кількість: {item.get('resourcecount')}
- В/ч: {item.get('union')}
- Додаткова інформація: {item.get('additioninformation')}
- Час додавання: {item.get('created_at')}
'''

	return message

def menu():
	kb = [
		[
		    types.KeyboardButton(text='Отримати допомогу'),
		    types.KeyboardButton(text='Надати допомогу'),
		],
		[
			types.KeyboardButton(text='Переглянути допомогу волонтерів'),
		],
		[
			types.KeyboardButton(text='Переглянути потреби військових'),
		]
	]

	keyboard = types.ReplyKeyboardMarkup(
		keyboard=kb,
		resize_keyboard=True,
		# input_field_placeholder=''
	)

	return keyboard

def categories_menu(_from='military'):
	builder = InlineKeyboardBuilder()

	for index, category in enumerate(categories):
		builder.row(types.InlineKeyboardButton(
			text=category, callback_data=f'category_{index}_{_from}')
		)

	return builder

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
	user_fullname = message.from_user.full_name
	greetings_message = f'''
		Вітаю, <strong>{user_fullname}</strong>! 👋

Ласкаво просимо до нашого Telegram-бота для підтримки військових! 

Тут ви можете:
- Подати заявку на отримання волонтерської допомоги 📝
- Переглянути пости волонтерів, щоб знайти потрібну допомогу 📦
- Залишити свої побажання або запитання 🗣️

Волонтери, ви також можете:
- Додати свої оголошення про доступну допомогу 🌟
- Зв'язатися з тими, хто потребує вашої підтримки 🤝

Разом ми сильніші! 🇺🇦

З будь-яких питань звертайтесь до нашої служби підтримки. Дякуємо, що приєдналися до нашої спільноти! 💙💛
	'''
	await message.answer(greetings_message, reply_markup=menu(), parse_mode='HTML')

@dp.message(F.text.lower() == 'отримати допомогу')
async def need_help(message: types.Message):
    await message.reply(f'''
    	Перейдіть за посиланням нижче, та заповніть форму.

ЇЇ отримає більше, ніж 20 волонтерьский організацій та стане доступним для перегляду волонтерам, що до нас долучились! 

Разом ми - Україна 🇺🇦

<a href='{env.google_from_url}'>📨📨📨</a>
''', parse_mode='HTML')

@dp.message(F.text.lower() == 'надати допомогу')
async def give_help(message: types.Message):
    await message.reply(f'''
    	Перейдіть за посиланням нижче, та заповніть форму.

Переглянути її зможуть усі військові, що до нас долучились! 

Разом ми - Україна 🇺🇦

<a href='{env.google_from_url}'>📨📨📨</a>
''', parse_mode='HTML')

@dp.message(F.text.lower() == 'переглянути допомогу волонтерів')
async def give_help(message: types.Message):
    await message.answer(
        'Виберіть потрібну категорію:',
        reply_markup=categories_menu().as_markup(),
    )

@dp.message(F.text.lower() == 'переглянути потреби військових')
async def give_help(message: types.Message):
    await message.answer(
        'Виберіть потрібну категорію:',
        reply_markup=categories_menu('volunteer').as_markup(),
    )

# CALLBACKS

@dp.callback_query(lambda callback: callback.data.startswith('category_'))
async def callback_category(callback: types.CallbackQuery):
	data = callback.data.split('_')
	index = int(data[1])
	_from = str(data[2])
	category = categories[index]

	await callback.answer(f'Зачекайте будь-ласка ⏳')

	select = applications.select(category, _from)
	if select['status'] == 'error':
		await bot.send_message(callback.from_user.id, select['err_description'])

	else:
		items = select.get('items', [])
		for item in items:
			message = create_message(_from, item)
			await bot.send_message(callback.from_user.id, message)

async def main():
	await dp.start_polling(bot)

if __name__ == '__main__':
	try:
		asyncio.run(main())
		
	except KeyboardInterrupt:
		print('Exit!')