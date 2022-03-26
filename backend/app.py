from flask import Flask, request,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_cors import CORS
from flask_sock import Sock
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import os
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
# from src.services.test_services import get_updated_data

load_dotenv()
sqlalchemyurl = os.getenv("sqlalchemyurl")

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/escreener_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host/dbname'
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemyurl

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


# models
class Changes(db.Model):  
    changesid = db.Column(db.Integer, primary_key = True)
    ticker = db.Column(db.String(15))
    dated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.now)
    iv = db.Column(db.Float)
    straddle = db.Column(db.Float)
    impliedmove = db.Column(db.Float)
    underlying = db.Column(db.Float)
    strike = db.Column(db.Float)
    quarter = db.Column(db.String(2))
    def __init__(self,ticker,dated,iv,straddle,impliedmove,underlying,strike,quarter):
        self.ticker = ticker
        self.dated = dated
        self.iv = iv
        self.straddle = straddle
        self.impliedmove = impliedmove
        self.underlying = underlying
        self.strike = strike
        self.quarter = quarter
      



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

#Schemas
class ChangesSchema(ma.Schema):
    __tablename__ = "changes"
    changesid = fields.Integer(dump_only = True)
    ticker = fields.String()
    dated = fields.DateTime(format='%Y-%m-%dT%H:%M:%S%z')
    iv = fields.Float()
    straddle = fields.Float()
    impliedmove = fields.Float()
    underlying = fields.Float()
    strike = fields.Float()
    quarter = fields.String()
    
change_schema = ChangesSchema()
changes_schema = ChangesSchema(many = True)




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

# @app.route('/get-earning-by-id/<id>', methods=['GET'])
# def get_earning_by_id(id):
#     get_earning = db.session.query(Earningsdates).order_by(Earningsdates.exactearningsdate.asc()).offset(id).first()
#     earning = earning_schema.dump(get_earning)
#     return earning

@app.route('/get-earning-by-symbol/<symbol>', methods=['GET'])
def get_earning_by_id(symbol):
    get_earning = db.session.query(Earningsdates).filter(Earningsdates.ticker == symbol).order_by(Earningsdates.exactearningsdate.asc()).first()
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




# api for changes table
@app.route('/get-all-changes', methods=['GET'])
def get_changes():
    all_changes = Changes.query.order_by(Changes.dated).all()
    result = changes_schema.dump(all_changes)
    return jsonify(result)


@app.route('/get-last-changes', methods=['GET'])
def get_last_changes():
    last_item = Changes.query.order_by(Changes.changesid.desc()).first()
    result = change_schema.dump(last_item)
    return jsonify(result)

@app.route('/add-change', methods=['POST'])
def add_change():
    ticker = request.json['ticker']
    dated = request.json['dated']
    iv = request.json['iv']
    straddle = request.json['straddle']
    impliedmove = request.json['impliedmove']
    underlying = request.json['underlying']
    strike = request.json['strike']
    quarter = request.json['quarter']
  

    new_change = Changes(ticker,dated,iv,straddle,impliedmove,underlying,strike,quarter)
    db.session.add(new_change)
    db.session.commit()
    return change_schema.jsonify(new_change)
   

#       CREATE TABLE `changes` (
#   `changesid` int(11) NOT NULL AUTO_INCREMENT,
#   `ticker` varchar(15) NOT NULL,
#   `dated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   `iv` decimal(10,2) NOT NULL,
#   `straddle` decimal(10,2) NOT NULL,
#   `impliedmove` decimal(10,2) NOT NULL,
#   `underlying` decimal(10,2) NOT NULL,
#   `strike` decimal(10,2) NOT NULL,
#   `quarter` varchar(2) NOT NULL,
#   PRIMARY KEY (`changesid`)



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