from price_check import db

class FiguresDetails(db.Model):

    __tablename__ = 'figures_details'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable= True)
    availability = db.Column(db.Integer(), nullable=True)
    source = db.Column(db.String(), nullable=True)
    comments = db.Column(db.String(), nullable=True)
    download = db.Column(db.DateTime(), nullable=True)

    def __init__(self, title, price, availability, source, comments, download) -> None:
        self.title = title
        self.price = price
        self.availability = availability
        self.source = source
        self.comments = comments
        self.download = download

    def __repr__(self) -> str:
        return f'{self.title}'
    