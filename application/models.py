from application import db

class UserHotelClick(db.Model):
    __tablename__ = 'UserHotelClick'

    id = db.Column(db.String(50), primary_key=True)
    userId = db.Column(db.String(50))
    hotelId = db.Column(db.String(50))
    clickedAt = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'userid': self.userId,
            'hotelid': self.hotelId,
            'click_time': self.clickedAt
        }
    
class UserHotelBookmark(db.Model):
    __tablename__ = 'UserHotelBookmark'

    id = db.Column(db.String(50), primary_key=True)
    userId = db.Column(db.String(50))
    hotelId = db.Column(db.String(50))
    bookmarkedAt = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'userid': self.userId,
            'hotelid': self.hotelId,
            'click_time': self.bookmarkedAt
        }
    
class Hotel(db.Model):
    __tablename__ = 'Hotel'  # Table name in the database
    
    # Define columns
    id = db.Column(db.String(36), primary_key=True)  # UUID as primary key
    name = db.Column(db.String(255), nullable=False)  # Hotel name
    cheap = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    luxurious = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    clean = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    cozy = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    goodService = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    niceView = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    parking = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    pool = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    spa = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    gym = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    strategic = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    delicious = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    breakfast = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    safety = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    family = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    pet = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    aesthetic = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    disability = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    laundry = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    wifi = db.Column(db.Integer, nullable=False)  # Integer (0 or 1)
    
    def __repr__(self):
        return f"<Hotel {self.name}>"
    
    def to_dict(self):
        """Convert model instance to dictionary with hotelid as key."""
        # Convert to dictionary, then modify the key 'id' to 'hotelid'
        result = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        result['hotelid'] = result.pop('id')  # Rename 'id' to 'hotelid'
        return result