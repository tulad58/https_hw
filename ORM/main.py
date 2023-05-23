import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import Publisher, Book, Shop, Stock, Sale, create_tables, create_connection


DSN = create_connection('postgres', 'Admin','localhost', 5432, 'clients')

engine = sq.create_engine(DSN)

Base = declarative_base()

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# создание объектов
def create_objects():
    publisher1 = Publisher(name="Penguin Random House")
    publisher2 = Publisher(name="HarperCollins")
    publisher3 = Publisher(name="Wiley")
    publisher4 = Publisher(name="Simon & Schuster")
    publisher5 = Publisher(name="Bloomsbury Publishing")

    session.add(publisher1)
    session.add(publisher2)
    session.add(publisher3)
    session.add(publisher4)
    session.add(publisher5)

    book1 = Book(title="1984 by George Orwell", publisher=publisher1)
    book2 = Book(title="The Lord of the Rings by J.R.R. Tolkien", publisher=publisher2)
    book3 = Book(title="The Kite Runner by Khaled Hosseini", publisher=publisher3)
    book4 = Book(title="Harry Potter and the Philosopher's Stone", publisher=publisher4)
    book5 = Book(title="Slaughterhouse-Five by Kurt Vonnegut", publisher=publisher5)


    shop1 = Shop(name="Read-a-Thon Books")
    shop2 = Shop(name="White Whale Bookstore")
    shop3 = Shop(name="The Reading Nook")
    shop4 = Shop(name="Fantasy Lights Bookstore")
    shop5 = Shop(name="Paperback Adventures")


    stock1 = Stock(book=book1, shop=shop1)
    stock2 = Stock(book=book2, shop=shop2)
    stock3 = Stock(book=book3, shop=shop3)
    stock4 = Stock(book=book4, shop=shop4)
    stock5 = Stock(book=book5, shop=shop5)

    sale1 = Sale(price=999, data_sale='2023-02-21', stock=stock1, count=3)
    sale2 = Sale(price=1500, data_sale='2023-04-11', stock=stock2, count=5)
    sale3 = Sale(price=15.5, data_sale='2023-06-11', stock=stock3, count=12)
    sale4 = Sale(price=10000, data_sale='2024-02-21', stock=stock4, count=3)
    sale5 = Sale(price=30, data_sale='2022-04-11', stock=stock5, count=5)
 

    session.add_all([book1, book2, book3, book4, book5, shop1, shop2, shop3, shop4, 
                    shop5, stock1, stock2, stock3, stock4, stock5, sale1, sale2, sale3, sale4, sale5])
    
create_objects()
session.commit()

def get_buy_info(name):
    subq = session.query(Publisher, Book, Stock, Sale).select_from(Publisher) \
        .join(Book).join(Stock).join(Sale).filter(Publisher.name==name).subquery("publisher")
    q = session.query(Shop).join(subq, Shop.id == subq.c.id_shop).filter()
    for el in q.all():
        print(el)

  
get_buy_info("Penguin Random House")

session.close()
# Не успел, можно еще времени на доработку?=)