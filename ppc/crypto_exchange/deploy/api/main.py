import sqlite3from pathlib import Pathfrom fastapi import FastAPI, HTTPException, Depends, Responsefrom fastapi.middleware.cors import CORSMiddlewarefrom fastapi.security import OAuth2PasswordBearerfrom fastapi_users import FastAPIUsersfrom sqlalchemy import update, and_, insert, deletefrom sqlalchemy.ext.asyncio import AsyncSessionfrom sqlalchemy.sql import selectfrom starlette.middleware.sessions import SessionMiddlewarefrom auth.config import auth_backendfrom auth.database import User, get_async_session, CryptoCard, create_db_and_tables, UserCryptoCardfrom auth.manager import get_user_managerfrom auth.schemas import UserRead, UserCreateBASE_PATH = Path(__file__).resolve().parentcon = sqlite3.connect("my_database.db")app = FastAPI(title="Криптобиржа")oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")async def insert_crypto_card(card: CryptoCard, conn):    await conn.execute("INSERT INTO crypto_card (name, price_sell, price_buy) VALUES ($1, $2, $3)", card.name,                       card.price_sell, card.price_buy)@app.on_event("startup")async def get_crypto_cards_to_db():    await create_db_and_tables()    async_session = get_async_session()    async_gen = async_session.__aiter__()    session = await async_gen.__anext__()    crypto_cards = [        {"name": "Bitcoin", "price_sell": 13.5, "price_buy": 12},        {"name": "Ethereum", "price_sell": 0.82, "price_buy": 0.8},        {"name": "Litecoin", "price_sell": 1.11, "price_buy": 1},        {"name": "Dogecoin", "price_sell": 0.11, "price_buy": 0.1},        {"name": "BNB", "price_sell": 0.9, "price_buy": 0.8},        {"name": "Solana", "price_sell": 5.19, "price_buy": 5},        {"name": "Tron", "price_sell": 0.9, "price_buy": 0.8},        {"name": "Dot", "price_sell": 3.05, "price_buy": 3.0},        {"name": "Polkadot", "price_sell": 4.09, "price_buy": 4},        {"name": "PEPE", "price_sell": 0.7, "price_buy": 0.8},    ]    for card_data in crypto_cards:        existing_card = await session.execute(select(CryptoCard).where(CryptoCard.name == card_data["name"]))        if existing_card.scalar() is None:            card = CryptoCard(**card_data)            session.add(card)    await session.commit()    await session.close()    return {"message": "Crypto cards added successfully."}app.add_middleware(SessionMiddleware, secret_key="my_secret_key")flag = 'goctf{you_4re_rea11e_businessman}'origins = ["http://185.104.106.221:5543"]app.add_middleware(    CORSMiddleware,    allow_origins=origins,    allow_credentials=True,    allow_methods=["GET", "POST"],    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",                   "Authorization"],)fastapi_users = FastAPIUsers[User, int](    get_user_manager,    [auth_backend],)app.include_router(    fastapi_users.get_auth_router(auth_backend),    prefix="/auth/jwt",    tags=["auth"],)app.include_router(    fastapi_users.get_register_router(UserRead, UserCreate),    prefix="/auth",    tags=["auth"],)current_user = fastapi_users.current_user()@app.get("/balance")async def get_user_balance(user=Depends(current_user)):    return {"balance": user.balance}@app.get("/crypto_cards")async def get_crypto_cards(session: AsyncSession = Depends(get_async_session)):    async with session:        query = select(CryptoCard)        result = await session.execute(query)        crypto_cards = result.scalars().all()        return crypto_cards@app.get("/get_users")async def get_users(session: AsyncSession = Depends(get_async_session)):    async with session:        query = select(User)        result = await session.execute(query)        users = result.scalars().all()        return users@app.get("/get_amount_card")async def get_amount_card(card_id: int, user: User = Depends(current_user),                          session: AsyncSession = Depends(get_async_session)):    async with session as async_session:        query = select(UserCryptoCard).filter(            and_(UserCryptoCard.crypto_card_id == card_id, UserCryptoCard.user_id == user.id)        )        result = await async_session.execute(query)        amount_card = result.scalar()        if amount_card is None:            return HTTPException(status_code=403, detail="Карточки не найдено либо не куплено")        return {"amount": amount_card.amount}@app.post("/buy_crypto")async def buy_crypto(crypto_card_name: str, user=Depends(current_user),                     session: AsyncSession = Depends(get_async_session)):    """ Покупка криптовалюты """    query = select(CryptoCard).filter_by(name=crypto_card_name)    result = await session.execute(query)    crypto_card = result.scalar()    if crypto_card is None:        raise HTTPException(status_code=404, detail="Криптокарта не найдена")    # Получаем информацию о пользователе    card_price = crypto_card.price_buy    user_balance = user.balance    if user_balance < card_price:        raise HTTPException(status_code=400, detail="Недостаточно средств для покупки криптокарты")    # Вычитаем стоимость криптокарты из баланса пользователя    new_balance = user_balance - card_price    stmt = update(User).filter_by(id=user.id).values(balance=new_balance)    # Получаем необходимые данные    user_id_from_ucc = select(UserCryptoCard).filter_by(user_id=user.id)    result_user_id_from_ucc = await session.execute(user_id_from_ucc)    ucc_user_id = result_user_id_from_ucc.scalar()    crypto_card_id_from_ucc = select(UserCryptoCard).filter_by(crypto_card_id=crypto_card.id)    result_crypto_card_id_from_ucc = await session.execute(crypto_card_id_from_ucc)    ucc_crypto_card_id = result_crypto_card_id_from_ucc.scalar()    if ucc_crypto_card_id is None or ucc_user_id is None:        stmt2 = insert(UserCryptoCard).values(user_id=user.id, crypto_card_id=crypto_card.id, amount=1)        await session.execute(stmt2)        await session.commit()        await session.execute(stmt)        await session.commit()    else:        if ucc_user_id.user_id == user.id and ucc_crypto_card_id.crypto_card_id == crypto_card.id:            stmt3 = update(UserCryptoCard).where(                (UserCryptoCard.user_id == user.id) & (UserCryptoCard.crypto_card_id == crypto_card.id)            ).values(amount=UserCryptoCard.amount + 1)            await session.execute(stmt3)            await session.execute(stmt)            await session.commit()    return f"Поздравляем с покупкой {crypto_card_name}"@app.post("/sell_crypto")async def sell_crypto(crypto_card_name: str, user=Depends(current_user),                      session: AsyncSession = Depends(get_async_session)):    """ Продажа криптовалюты """    query = select(CryptoCard).filter_by(name=crypto_card_name)    result = await session.execute(query)    crypto_card = result.scalar()    if crypto_card is None:        raise HTTPException(status_code=404, detail="Криптокарта не найдена")    card_price = crypto_card.price_sell    user_balance = user.balance    query = select(UserCryptoCard).filter_by(crypto_card_id=crypto_card.id, user_id=user.id)    user_crypto_card = await session.execute(query)    user_crypto_card = user_crypto_card.scalar()    if user_crypto_card is None:        raise HTTPException(status_code=404, detail="У вас нет такой карточки")    # Запрос на количество карточек (amount)    new_balance = user_balance + card_price    stmt = update(User).filter_by(id=user.id).values(balance=new_balance)    await session.execute(stmt)    if user_crypto_card.amount > 1:        stmt2 = (            update(UserCryptoCard)            .filter_by(user_id=user.id, crypto_card_id=user_crypto_card.crypto_card_id)            .values(amount=user_crypto_card.amount - 1)        )        await session.execute(stmt2)        await session.commit()        return Response(f"Вы продали 1 карточку {crypto_card_name}")    else:        stmt3 = (            delete(UserCryptoCard)            .filter_by(user_id=user.id, crypto_card_id=user_crypto_card.crypto_card_id)        )        await session.execute(stmt3)        await session.commit()        return Response(f"Вы продали последнюю карточку {crypto_card_name}")@app.post("/by_flag")async def by_flag(user=Depends(current_user)):    if user.balance >= 10000.0:        return {"flag": flag}    else:        raise HTTPException(status_code=403, detail="Накопи больше монет (10000) и возвращайся")