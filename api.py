from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databse.db'
db = SQLAlchemy(app)
api = Api(app)

class UFCChampModel(db.Model):
    __tablename__ = 'champions'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    # num_champ = db.Column(db.Integer, unique=False, nullable=True)
    current = db.Column(db.Boolean, unique=False, nullable=True)
    duration = db.Column(db.String(20), unique=False, nullable=True)
    # defenses = db.Column(db.String(100), unique=False, nullable=True)
    division = db.Column(db.String(20), unique=False, nullable=True)
    # nation = db.Column(db.String(30), unique=False, nullable=True)
    # event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    
    # event = db.relationship('Event', back_populates='champions')

    def __repr__(self):
        return f'UFCChampModel(first_name={self.first_name}, last_name={self.last_name})'

# class Event(db.Model):
#     __tablename__ = 'events'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), unique=True, nullable=False)
#     location = db.Column(db.String(20), unique=False, nullable=False)
#     date = db.Column(db.String(20), unique=False, nullable=False)
#     winner = db.Column(db.String(20), unique=False, nullable=False)
#     loser = db.Column(db.String(20), unique=False, nullable=False)

#     champions = db.relationship('UFCChampModel', back_populates='event', lazy='dynamic')
    
#     def __repr__(self):
#         return f'Event(name={self.name})'


@app.route('/')
def home():
    return '<h1>UFC API</h1>'

champ_args = reqparse.RequestParser()
champ_args.add_argument('first_name', type=str, required=True, help='first name cannot be blank')
champ_args.add_argument('last_name', type=str, required=True, help='last name cannot be blank')
# champ_args.add_argument('num_champ', type=int, required=False)
champ_args.add_argument('current', type=bool, required=False)
champ_args.add_argument('duration', type=str, required=False)
# champ_args.add_argument('defenses', type=str, required=False)
champ_args.add_argument('division', type=str, required=False)
# champ_args.add_argument('nation', type=str, required=False)
# champ_args.add_argument('event_id', type=int, required=False)

# event_args = reqparse.RequestParser()
# event_args.add_argument('name', type=str, required=False)
# event_args.add_argument('location', type=str, required=False)
# event_args.add_argument('date', type=str, required=False)
# event_args.add_argument('winner', type=str, required=False)
# event_args.add_argument('loser', type=str, required=False)

# eventFields = {
#     'id': fields.Integer,
#     'name': fields.String,
#     'location': fields.String,
#     'date': fields.String,
#     'winner': fields.String,
#     'loser': fields.String,
# }
champFields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    # 'num_champ': fields.Integer,
    'current': fields.Boolean,
    'duration': fields.String,
    # 'defenses': fields.String,
    'division': fields.String,
    # 'nation': fields.String,
    # 'event_id': fields.Integer,
    # 'event': fields.Nested(eventFields)
}


class Champs(Resource):
    @marshal_with(champFields)
    def get(self):
        champs = UFCChampModel.query.all()
        return champs
    @marshal_with(champFields)
    def post(self):
        kwargs = champ_args.parse_args()
        champ = UFCChampModel(**kwargs)
        db.session.add(champ)
        db.session.commit()
        champs = UFCChampModel.query.all()
        return champs, 201
    
class Champ(Resource):
    @marshal_with(champFields)
    def get(self, id):
        champ = UFCChampModel.query.filter_by(id=id).first()
        if not champ:
            abort(404)
        return champ, 201
    @marshal_with(champFields)
    def patch(self, id):
        args  = champ_args.parse_args()
        champ = UFCChampModel.query.filter_by(id=id).first()
        if not champ:
            abort(404)
        champ.first_name = args['first_name']
        champ.last_name = args['last_name']
        # champ.num_champ = args['num_champ']
        champ.current = args['current']
        champ.duration = args['duration']
        # champ.defenses = args['defenses']
        champ.division = args['division']
        # champ.nation = args['nation']
        # champ.event_id = args['event_id']
        db.session.commit()

        return champ, 201
    @marshal_with(champFields)
    def delete(self, id):
        champ = UFCChampModel.query.filter_by(id=id).first()
        if not champ:
            abort(404)
        
        db.session.delete(champ)
        db.session.commit()

    #NOT TESTED
    @marshal_with(champFields)
    def delete_all(self):
        champs = UFCChampModel.query.all()
        if not champs:
            abort(404)
        for champ in champs:
            db.session.delete(champ)

        db.session.commit()
    

# class Events(Resource):
#     @marshal_with(eventFields)
#     def get(self):
#         events = Event.query.all()
#         return events
#     @marshal_with(eventFields)
#     def post(self):
#         kwargs = event_args.parse_args()
#         event = Event(**kwargs)
#         db.session.add(event)
#         db.session.commit()
#         events = Event.query.all()
#         return events, 201
    
# class EventResource(Resource):
#     @marshal_with(eventFields)
#     def get(self, id):
#         event = Event.query.filter_by(id=id).first()
#         if not event:
#             abort(404)
#         return event, 201
#     @marshal_with(eventFields)
#     def patch(self, id):
#         args  = event_args.parse_args()
#         event = Event.query.filter_by(id=id).first()
#         if not event:
#             abort(404)
#         event.name = args['name']
#         event.location = args['location']
#         event.date = args['date']
#         event.winner = args['winner']
#         event.loser = args['loser']
#         db.session.commit()

#         return event, 201
#     @marshal_with(eventFields)
#     def delete(self, id):
#         event = Event.query.filter_by(id=id).first()
#         if not event:
#             abort(404)
        
#         db.session.delete(event)
#         db.session.commit()

 


api.add_resource(Champs, '/api/champs/')
api.add_resource(Champ, '/api/champs/<int:id>')
# api.add_resource(Events, '/api/events/')
# api.add_resource(EventResource, '/api/events/<int:id>')
    

if __name__ == '__main__':
    app.run(debug=True)