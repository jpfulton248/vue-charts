from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_cors import CORS
from flask_sock import Sock
import json
import time
from datetime import datetime
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
# from src.services.test_services import get_updated_data

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/escreener_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host/dbname'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql3480466:e4cWTVS4KE@sql3.freemysqlhosting.net/sql3480466'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
sock = Sock(app)
from datetime import datetime


# models
class Test(db.Model):
    testid = db.Column(db.Integer, primary_key = True)
    ticker = db.Column(db.String(20))
    date = db.Column(db.Integer)
    price = db.Column(db.Integer)
    def __init__(self,ticker,date,price):
        self.ticker = ticker
        self.date = date
        self.price = price
# db.create_all()

# models
class Earningsdates(db.Model):  
    earningsdateid = db.Column(db.Integer, primary_key = True)
    ticker = db.Column(db.String(15))
    exactearningsdate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.now)
    averageoptionvol = db.Column(db.Integer)
    averagestockvol = db.Column(db.Integer)
    marketcap = db.Column(db.Integer)
    impliedmove = db.Column(db.Float)
    staticstrike = db.Column(db.Float)
    staticexpiry = db.Column(db.String(12))
    staticprice = db.Column(db.Float)
    staticunderlying = db.Column(db.Float)
    staticiv = db.Column(db.Float)
    actualmove = db.Column(db.Float)
    def __init__(self,ticker,exactearningsdate,averageoptionvol,averagestockvol,marketcap,impliedmove,staticstrike,staticexpiry,staticprice,staticunderlying,staticiv,actualmove):
        self.ticker = ticker
        self.exactearningsdate = exactearningsdate
        self.averageoptionvol = averageoptionvol
        self.averagestockvol = averagestockvol
        self.marketcap = marketcap
        self.impliedmove = impliedmove
        self.staticstrike = staticstrike
        self.staticprice = staticprice
        self.staticexpiry = staticexpiry
        self.staticunderlying = staticunderlying
        self.staticiv = staticiv
        self.actualmove = actualmove
    


#Schemas
class TestSchema(ma.Schema):
    __tablename__ = "test"
    testid = fields.Integer(dump_only = True)
    ticker = fields.String()
    date = fields.Integer()
    price = fields.Integer()
test_schema = TestSchema()
tests_schema = TestSchema(many = True)    

#Schemas
class EarningsdatesSchema(ma.Schema):
    __tablename__ = "earningsdates"
    earningsdateid = fields.Integer(dump_only = True)
    ticker = fields.String()
    exactearningsdate = fields.DateTime(format='%Y-%m-%dT%H:%M:%S%z')
    averageoptionvol = fields.Integer()
    averagestockvol = fields.Integer()
    marketcap = fields.Integer()
    impliedmove = fields.Float()
    staticstrike = fields.Float()
    staticprice = fields.Float()
    staticexpiry = fields.String()
    staticunderlying = fields.Float()
    staticiv = fields.Float()
    actualmove = fields.Float()
earning_schema = EarningsdatesSchema()
earnings_schema = EarningsdatesSchema(many = True)


#api for earningsdates table
@app.route('/add-earning', methods=['POST'])
def create_earning():
    ticker = request.json['ticker']
    exactearningsdate = request.json['exactearningsdate']
    averageoptionvol = request.json['averageoptionvol']
    averagestockvol = request.json['averagestockvol']
    marketcap = request.json['marketcap']
    impliedmove = request.json['impliedmove']
    staticstrike = request.json['staticstrike']
    staticprice = request.json['staticprice']
    staticexpiry = request.json['staticexpiry']
    staticunderlying = request.json['staticunderlying']
    staticiv = request.json['staticiv']
    actualmove = request.json['actualmove']

    new_earning = Earningsdates(ticker,exactearningsdate,averageoptionvol,averagestockvol,marketcap,impliedmove,staticstrike,staticprice,staticexpiry,staticunderlying,staticiv,actualmove)
    db.session.add(new_earning)
    db.session.commit()
    return earning_schema.jsonify(new_earning)
   

@app.route('/get-all-earnings', methods=['GET'])
def get_earnings():
    all_earnings = Earningsdates.query.all()
    result = earnings_schema.dump(all_earnings)
    return jsonify(result)

@app.route('/get-earning-by-id/<id>', methods=['GET'])
def get_earning_by_id(id):
    get_earning = db.session.query(Earningsdates).order_by(Earningsdates.exactearningsdate.asc()).offset(id).first()
    earning = earning_schema.dump(get_earning)
    return earning


@sock.route('/get-updated-earnings')
def get_update_earnings(ws):
    try:
        earning = ws.receive()
        earning = json.loads(earning)
        db.session.commit()
        ws.send(earning)
        time.sleep(20)
        ws.close()

    except Exception as e:
        print(e)
        print("I am closing now due to: ", str(e))
        ws.close()



# api for test-table
@app.route('/add-test', methods=['POST'])
def create_test():
    # import pdb; pdb.set_trace()
    ticker = request.json['ticker']
    date = request.json['date']
    price = request.json['price']
    new_test = Test(ticker,date,price)
    db.session.add(new_test)
    db.session.commit()
    return test_schema.jsonify(new_test)
   

@app.route('/get-all-tests', methods=['GET'])
def get_tests():
    all_tests = Test.query.all()
    result = tests_schema.dump(all_tests)
    return jsonify(result)

@app.route('/get-test-by-id/<id>', methods=['GET'])
def get_test_by_id(id):
    get_test = Test.query.get(id)
    test = test_schema.dump(get_test)
    return test


@sock.route('/get-updated-data')
def get_update_data(ws):

    total = 45 #total rows in db

    try:
        for i in range(1,total):
            time.sleep(1)
            obj = get_earning_by_id(i)
            obj = json.dumps(obj)
            ws.send(obj)

        time.sleep(2)
        ws.close()
   
    except Exception as e:
        print(e)
        print("I am closing now due to: ", str(e))
        ws.close()



if __name__ == "__main__":
    app.run(debug = True)