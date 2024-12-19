import asyncio, json, requests
from random import randint
from aiogram import Bot, Dispatcher, html
from aiogram.enums import ParseMode
from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ErrorEvent, WebAppInfo, WebAppData, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command, ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import grpc
import grpc_pb2_grpc, grpc_pb2

#docker run --name weather_page -p 80:80 -v ./pages:/usr/share/nginx/html -d nginx:1.27.1-alpine
#python -m http.server 80

dp = Dispatcher()
key = '||weather api key||'

def check_winner(data: list) -> int:
    if abs(data[0] + data[1] + data[2]) == 3 or abs(data[3] + data[4] + data[5]) == 3 or abs(data[6] + data[7] + data[8]) == 3:
        return 1
    elif abs(data[0] + data[3] + data[6]) == 3 or abs(data[1] + data[4] + data[7]) == 3 or abs(data[2] + data[5] + data[8]) == 3:
        return 1
    elif abs(data[0] + data[4] + data[8]) == 3 or abs(data[2] + data[4] + data[6]) == 3:
        return 1
    else:
        return 0


def bot_turn(data: list) -> list[int]:
    plays_as = -1 if data.count(0) % 2 == 0 else 1
    can_win = False
    advice = None
    if not can_win and abs(data[0] + data[1] + data[2]) == 2:
        can_win = (data[0] + data[1] + data[2]) == (2 * plays_as)
        advice = 0 if data[0] == 0 else 1 if data[1] == 0 else 2
    if not can_win and abs(data[3] + data[4] + data[5]) == 2:
        can_win = (data[3] + data[4] + data[5]) == (2 * plays_as)
        advice = 3 if data[3] == 0 else 4 if data[4] == 0 else 5
    if not can_win and abs(data[6] + data[7] + data[8]) == 2:
        can_win = (data[6] + data[7] + data[8]) == (2 * plays_as)
        advice = 6 if data[6] == 0 else 7 if data[7] == 0 else 8

    if not can_win and abs(data[0] + data[3] + data[6]) == 2:
        can_win = (data[0] + data[3] + data[6]) == (2 * plays_as)
        advice = 0 if data[0] == 0 else 3 if data[3] == 0 else 6
    if not can_win and abs(data[1] + data[4] + data[7]) == 2:
        can_win = (data[1] + data[4] + data[7]) == (2 * plays_as)
        advice = 1 if data[1] == 0 else 4 if data[4] == 0 else 7
    if not can_win and abs(data[2] + data[5] + data[8]) == 2:
        can_win = (data[2] + data[5] + data[8]) == (2 * plays_as)
        advice = 2 if data[2] == 0 else 5 if data[5] == 0 else 8

    if not can_win and abs(data[0] + data[4] + data[8]) == 2:
        can_win = (data[0] + data[4] + data[8]) == (2 * plays_as)
        advice = 0 if data[0] == 0 else 4 if data[4] == 0 else 8
    if not can_win and abs(data[2] + data[4] + data[6]) == 2:
        can_win = (data[2] + data[4] + data[6]) == (2 * plays_as)
        advice = 2 if data[2] == 0 else 4 if data[4] == 0 else 6

    if advice is None:
        while True:
            pos = randint(0,8)
            if not data[pos]:
                advice = pos
                break

    data[advice] = 1 * plays_as

    return data

def gen_keyboard(symbol: str) -> InlineKeyboardMarkup:
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(InlineKeyboardButton(text=symbol, callback_data=symbol + str(i * 3 + j)))
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def gen_field(field: list = None) -> str:
    default = "─ ─ ─ ─ ─\n … |  …  |  …\n─ ┼ ─ ┼ ─\n … |  …  |  …\n─ ┼ ─ ┼ ─\n … |  …  |  …\n─ ─ ─ ─ ─"
    if field:
        s_ch = lambda x: "O" if x == -1 else "X" if x == 1 else "…"
        return f"─ ─ ─ ─ ─\n {s_ch(field[0])} |  {s_ch(field[1])}  |  {s_ch(field[2])}\n─ ┼ ─ ┼ ─\n {s_ch(field[3])} |  {s_ch(field[4])}  |  {s_ch(field[5])}\n─ ┼ ─ ┼ ─\n {s_ch(field[6])} |  {s_ch(field[7])}  |  {s_ch(field[8])}\n─ ─ ─ ─ ─"
    else:
        return default


def gen_field_data(field: str) -> dict:
    rows = field.split("\n")[:-1]
    field = []
    for row in rows:
        for sym in row:
            if sym == "…":
                field.append(0)
            elif sym == "O":
                field.append(-1)
            elif sym == "X":
                field.append(1)
    return field


def get_task_list(chat_id: str) -> str:
    msg = ''
    for task in stub.GetTasks(grpc_pb2.ChatId(id=chat_id)):
        msg += f'{task.num}. {task.text} {'✅' if task.is_completed else '❌'}\n'
    return msg


def is_present_task_by_num(chat_id: str, num: int) -> bool:
    for task in stub.GetTasks(grpc_pb2.ChatId(id=chat_id)):
        if task.num == num:
            return True
    return False


class Form(StatesGroup):
    task_create = State()
    task_edit_num = State()
    task_edit_text = State()
    task_complete_num = State()
    task_delete_num = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("game"))
async def command_game_handler(message: Message) -> None:
    player = randint(0,1)
    if player:
        await message.answer(text = gen_field() + "\nYou play as X", reply_markup = gen_keyboard("X"))
    else:
        data = [0,0,0,0,0,0,0,0,0]
        data[randint(0,8)] = 1
        await message.answer(text = gen_field(data) + "\nYou play as O", reply_markup = gen_keyboard("O"))


@dp.message(Command("lib_manage"))
async def command_lib_manage_handler(message: Message) -> None:
    url = f"https://niktopol.github.io/weather_page/forms.html"
    button = KeyboardButton(text="Write request", web_app=WebAppInfo(url=url))
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    await message.answer('Write request data using keyboard button Mini App', reply_markup=keyboard)


@dp.message(F.content_type.in_({'web_app_data'}))
async def form_input_handler(message: Message) -> None:
    data = message.web_app_data.data.split(',')
    type, data = data[-1], json.loads(','.join(data[:-1]))
    request = {}
    for field in data:
        if field['value']:
            if field['name'] == 'id':
                try:
                    request[field['name']] = int(field['value'])
                except:
                    await message.answer('ID must be a number')
            else:
                request[field['name']] = field['value']
    method = request['method']
    del request['method']
    if method == 'PUT' or method == 'PATCH' or method == 'DELETE' or method == 'POST':
        res = None
        if method == 'PUT':
            res = requests.put(f'http://127.0.0.1:8000/api/{type}', json=request)
        elif method == 'PATCH':
            res = requests.patch(f'http://127.0.0.1:8000/api/{type}', json=request)
        elif method == 'DELETE':
            res = requests.delete(f'http://127.0.0.1:8000/api/{type}/{request["id"]}')
        elif method == 'POST':
            res = requests.post(f'http://127.0.0.1:8000/api/{type}', json=request)
        if res.status_code // 100 == 2:
            await message.answer("Operation successful")
        else:
            await message.answer("An error occurred")
    else:
        res = requests.get(f'http://127.0.0.1:8000/api/{type}').json()
        await message.answer(json.dumps(res, indent=4))
    

@dp.message(F.content_type.in_({'location'}))
async def weather_report_handler(message: Message) -> None:
    url = f"https://niktopol.github.io/weather_page?data={key}&lat={message.location.latitude}&lon={message.location.longitude}"
    button = InlineKeyboardButton(text="Check weather", web_app=WebAppInfo(url=url))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.reply('Location selected', reply_markup=keyboard)


@dp.callback_query()
async def turn_handler(query: CallbackQuery) -> None:
    player_num = 1 if query.data[0] == "X" else -1
    data = gen_field_data(query.message.text)
    if not data[int(query.data[1:])]:
        data[int(query.data[1:])] = player_num
        win_check = check_winner(data)
        if win_check:
            await query.message.edit_text(gen_field(data) + "\nYou win", reply_markup=None)
        elif data.count(0) == 0:
            await query.message.edit_text(gen_field(data) + "\nDraw", reply_markup=None)
        else:
            data = bot_turn(data)
            win_check = check_winner(data)
            if win_check:
                await query.message.edit_text(gen_field(data) + "\nBot wins", reply_markup=None)
            elif data.count(0) == 0:
                await query.message.edit_text(gen_field(data) + "\nDraw", reply_markup=None)
            else:
                await query.message.edit_text(gen_field(data) + f"\nYoy play as {query.data[0]}", reply_markup=gen_keyboard(query.data[0]))
    await query.answer()


@dp.message(Command("create_task"))
async def command_task_create_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.task_create)
    await message.answer("Write text for your task")


@dp.message(Form.task_create)
async def process_task_create(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(stub.CreateTask(grpc_pb2.Task(id=grpc_pb2.ChatId(id=str(message.chat.id)), text=message.text)).text)


@dp.message(Command("edit_task"))
async def command_task_update_handler(message: Message, state: FSMContext) -> None:
    msg = get_task_list(str(message.chat.id))
    if len(msg):
        await state.set_state(Form.task_edit_num)
        msg += 'Write the number of the task you want to edit'
        await message.answer(msg)
    else:
        await message.answer('You have no tasks to edit')


@dp.message(Form.task_edit_num, F.text.regexp(r'^\d+$'))
async def process_task_edit_num(message: Message, state: FSMContext) -> None:
    num = int(message.text)
    if is_present_task_by_num(str(message.chat.id), num):
        await state.update_data(num=num)
        await state.set_state(Form.task_edit_text)
        await message.answer("Write text for your task")
    else:
        await state.clear()
        await message.answer('Task not found')


@dp.message(Form.task_edit_num)
async def process_task_edit_num(message: Message) -> None:
    await message.answer('Please enter a number')


@dp.message(Form.task_edit_text)
async def process_task_edit_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await message.answer(stub.UpdateTask(grpc_pb2.TaskUpdate(id=grpc_pb2.ChatId(id=str(message.chat.id)), num=data['num'], text=message.text)).text)


@dp.message(Command("get_tasks"))
async def command_get_tasks_handler(message: Message) -> None:
    msg = get_task_list(str(message.chat.id))
    if len(msg):
        await message.answer(msg)
    else:
        await message.answer('You have no tasks')


@dp.message(Command("complete_task"))
async def command_complete_task_handler(message: Message, state: FSMContext) -> None:
    msg = get_task_list(str(message.chat.id))
    if len(msg):
        await state.set_state(Form.task_complete_num)
        msg += 'Write the number of the task you want to mark as completed'
        await message.answer(msg)
    else:
        await message.answer('You have no tasks to complete')


@dp.message(Form.task_complete_num, F.text.regexp(r'^\d+$'))
async def process_complete_task_num(message: Message, state: FSMContext) -> None:
    num = int(message.text)
    await state.clear()
    if is_present_task_by_num(str(message.chat.id), num):
        await message.answer(stub.CompleteTask(grpc_pb2.TaskIdent(id=grpc_pb2.ChatId(id=str(message.chat.id)), num=num)).text)
    else:
        await message.answer('Task not found')


@dp.message(Form.task_complete_num)
async def process_task_edit_num(message: Message) -> None:
    await message.answer('Please enter a number')


@dp.message(Command("delete_task"))
async def command_delete_task_handler(message: Message, state: FSMContext) -> None:
    msg = get_task_list(str(message.chat.id))
    if len(msg):
        await state.set_state(Form.task_delete_num)
        msg += 'Write the number of the task you want to delete'
        await message.answer(msg)
    else:
        await message.answer('You have no tasks to delete')


@dp.message(Form.task_delete_num, F.text.regexp(r'^\d+$'))
async def process_delete_task_num(message: Message, state: FSMContext) -> None:
    num = int(message.text)
    await state.clear()
    if is_present_task_by_num(str(message.chat.id), num):
        await message.answer(stub.RemoveTask(grpc_pb2.TaskIdent(id=grpc_pb2.ChatId(id=str(message.chat.id)), num=num)).text)
    else:
        await message.answer('Task not found')


@dp.message(Form.task_delete_num)
async def process_delete_task_num(message: Message) -> None:
    await message.answer('Please enter a number')


@dp.error(ExceptionTypeFilter(TelegramBadRequest))
async def handle_my_repeat_exception(event: ErrorEvent):
    pass

async def main() -> None:
    bot = Bot('||bot token||', default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    global channel, stub
    channel = grpc.insecure_channel('localhost:50051')
    stub = grpc_pb2_grpc.TaskServiceStub(channel)
    asyncio.run(main())
