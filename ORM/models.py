import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

def create_connection(user_name, password, host_name, port, db_name):
    DSN = f'postgresql://{user_name}:{password}@{host_name}:{port}/{db_name}'
    return DSN


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'Publisher {self.id}: {self.name}'


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id", ondelete="CASCADE"), nullable=False)

    publisher = relationship(Publisher, cascade="all,delete", backref="book",passive_deletes=True)

    def __str__(self):
        return f'Book {self.id}: (title: {self.title}, id_publisher: {self.id_publisher})'


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=30), unique=True, nullable=False)

    def __str__(self):
        return f'Shop {self.id}: ({self.name})' 

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id",ondelete="CASCADE"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id",ondelete="CASCADE"), nullable=False)

    book = relationship(Book, cascade="all,delete", backref="book",passive_deletes=True)
    shop = relationship(Shop, cascade="all,delete", backref="shop",passive_deletes=True)

    def __str__(self):
        return f'Stock {self.id}: (id_book: {self.id_book}, id_shop: {self.id_shop})'

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    data_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id",ondelete="CASCADE"), nullable=False)
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, cascade="all,delete", backref="stock",passive_deletes=True)

    def __str__(self):
        return f'Sale {self.id}: ({self.price}, {self.data_sale}, {self.id_stock}, {self.count})'

    