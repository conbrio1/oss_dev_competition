from featurecatcher import db


def createModel(tableName):
    tabledict = {
        "uid": db.Column(db.Integer, primary_key=True),
        "id": db.Column(db.Integer, nullable=False),
        "frame": db.Column(db.Integer, nullable=False),
        "millisec": db.Column(db.Integer, nullable=False),
        "age": db.Column(db.Integer, nullable=False),
        "gender": db.Column(db.String(10), nullable=False),
        "img_person": db.Column(db.String(100), nullable=False),
        "top_color": db.Column(db.Integer, nullable=False),
        "bottom_color": db.Column(db.Integer, nullable=False),
    }

    newModel = type(tableName, (db.Model,), tabledict)
    return newModel
