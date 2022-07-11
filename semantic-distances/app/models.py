from . import db


class Subject(db.Model):
    __tablename__ = 'subjects'
    
    subject_id = db.Column(db.String, primary_key=True)
    completion_code = db.Column(db.String)
    age = db.Column(db.String)
    gender = db.Column(db.String)
    nationality = db.Column(db.String)
    country = db.Column(db.String)
    student = db.Column(db.String)
    language = db.Column(db.String)
    education = db.Column(db.String)

    def __repr__(self):
        return '<Subject %r>' % self.id


class Trial(db.Model):
    __tablename__ = 'trials'
    row_id = db.Column(db.String, primary_key=True)
    items = db.Column(db.String)
    features = db.Column(db.String)
    generations = db.Column(db.String)
    generations_rt = db.Column(db.String)
    sim_dict = db.Column(db.String)
    sim_dict_rt = db.Column(db.String)
    rate_dict = db.Column(db.String)
    
    def __repr__(self):
        return '<Subject %r>' % self.id