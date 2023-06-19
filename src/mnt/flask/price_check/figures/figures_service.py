from price_check.models import FiguresDetails
from sqlalchemy import func, desc, and_
from price_check.extensions import db


def find_figures_details_sorted_filtered(field_sort, order, filters, page, ROWS_PER_PAGE):
    if order == "asc":
        return FiguresDetails.query.filter_by(**filters).order_by(field_sort).paginate(page=page, per_page=ROWS_PER_PAGE)
    else:
        return FiguresDetails.query.filter_by(**filters).order_by(desc(field_sort)).paginate(page=page, per_page=ROWS_PER_PAGE)
    
def find_figures_details_sorted_filtered_all(field_sort, order, filters):
    if order == "asc":
        return FiguresDetails.query.filter_by(**filters).order_by(field_sort).all()
    else:
        return FiguresDetails.query.filter_by(**filters).order_by(desc(field_sort)).all()

def find_by_max_price(filters):
    max_price = db.session.query(func.max(FiguresDetails.price)).filter_by(**filters).scalar()
    return FiguresDetails.query.filter_by(price=max_price).first()

def find_by_min_price(filters):
    min_price = db.session.query(func.min(FiguresDetails.price)).filter_by(**filters).scalar()
    return FiguresDetails.query.filter_by(price=min_price).first()

def find_by_avg_price(filters):
    avg_price = db.session.query(func.avg(FiguresDetails.price)).filter_by(**filters).scalar()
    return FiguresDetails.query.filter_by(price=avg_price).first()

def find_number_of_products(filters):
    return FiguresDetails.query.filter_by(**filters).count()

def find_by_id(id):
    return FiguresDetails.query.get(id)

def find_last_date():
    last_date = db.session.query(func.max(FiguresDetails.download)).scalar()
    return last_date

def find_all_test(field_sort, order, filters):
    if order == "asc":
        return FiguresDetails.query.filter_by(**filters).order_by(desc(field_sort)).add_columns(func.avg(FiguresDetails.price)).group_by(FiguresDetails.title).first()
    else:
        return FiguresDetails.query.filter_by(**filters).order_by(desc(field_sort)).add_columns(func.avg(FiguresDetails.price)).group_by(FiguresDetails.id).first()


def find_figures_with_base_stats(field_sort, order, filters, page, ROWS_PER_PAGE):

    q1 = db.session.query(FiguresDetails.id, FiguresDetails.title, FiguresDetails.price, FiguresDetails.availability,
                           FiguresDetails.source, FiguresDetails.download, FiguresDetails.comments).filter_by(**filters).subquery()

    q2 = db.session.query(FiguresDetails.title, FiguresDetails.source) \
                        .add_columns(func.max(FiguresDetails.price).label('max_price'), \
                                     func.min(FiguresDetails.price).label('min_price'), \
                                     func.round(func.avg(FiguresDetails.price),2).label('avg_price')) \
                        .group_by(FiguresDetails.title, FiguresDetails.source).subquery()
    result = db.session.query(q1, q2.c.max_price, q2.c.min_price, q2.c.avg_price).join(q2, and_(q1.c.title == q2.c.title, q1.c.source == q2.c.source))
    if order == "asc":
        return result.order_by(field_sort).paginate(page=page, per_page=ROWS_PER_PAGE)
    else:
        return result.order_by(desc(field_sort)).paginate(page=page, per_page=ROWS_PER_PAGE)






