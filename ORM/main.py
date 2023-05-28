import sqlalchemy as sq
import json
from pathlib import Path
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import Publisher, Book, Shop, Stock, Sale, create_tables, create_connection



def get_data_json(route):
    p = Path(route)
    print(p)
    with open(p, 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data

def serialize_json_to_sqlalchemy(data):
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
        
def get_shops(request):
    q = session.query(
        Book.title, Shop.name, Sale.price, Sale.date_sale
    ).select_from(Shop).\
        join(Stock).\
        join(Book).\
        join(Publisher).\
        join(Sale)
    
    if request.isdigit():
        res = q.filter(Publisher.id == request).all()
    else:
        res = q.filter(Publisher.name == request).all()
    
    for title, name, price, date_sale in res: 
        print(f"{title: <40} | {name: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}")
    
    if res == []:
            print(f'Такого значения "{request}" в базе существует')
            
if __name__ == "__main__":
    DSN = create_connection('postgres', 'Admin','localhost', 5432, 'clients')
    engine = sq.create_engine(DSN)
    Base = declarative_base()
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = get_data_json('fixtures\\data.json')
    serialize_json_to_sqlalchemy(data)
    session.commit()
    users_input = input('Введите имя или идентификатор издателя ')
    get_shops(users_input)
    session.close()