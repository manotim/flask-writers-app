from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from writingapp import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Auth.query.get(int(user_id))

class Auth(db.Model, UserMixin):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(255))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Auth.query.get(user_id)

class Client(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key = True)
    auth_id = db.Column(db.Integer, db.ForeignKey("auth.id"))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    username = db.Column(db.String(20))
    dob = db.Column(db.DateTime())
    phone = db.Column(db.Integer)
    balance = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    auth = db.relationship("Auth", backref = "client")
    reviews = db.relationship("Reviews", backref = "client")
    message = db.relationship("Message", backref = "client")

class Writer(db.Model):
    __tablename__ = "writer"
    id = db.Column(db.Integer, primary_key = True)
    auth_id = db.Column(db.Integer, db.ForeignKey("auth.id"))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    username = db.Column(db.String(20))
    dob = db.Column(db.DateTime())
    phone = db.Column(db.Integer)
    residence = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    auth = db.relationship("Auth", backref = "writer")
    skill = db.relationship("Skills", backref = "writer")
    progress = db.relationship("Progress", backref = "writer")
    reviews = db.relationship("Reviews", backref = "writer")
    message = db.relationship("Message", backref = "writer")

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key= True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    writer_id = db.Column(db.Integer, db.ForeignKey("writer.id"))
    text = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

class Job(db.Model):
    __tablename__ = "job"
    id = db.Column(db.Integer, primary_key = True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    complexity = db.Column(db.String(255))
    deadline = db.Column(db.Date)
    amount = db.Column(db.Integer)
    assignment_type = db.Column(db.String(255))
    service = db.Column(db.String(255))
    education_level = db.Column(db.String(255))
    number_of_pages = db.Column(db.Integer)
    number_of_words = db.Column(db.Integer)
    line_spacing = db.Column(db.String(255))
    assignment_language = db.Column(db.String(255))
    sources_required = db.Column(db.String(255)) 
    citation_style = db.Column(db.String(255))
    subject = db.Column(db.String(255))
    instructions = db.Column(db.Text)
    submit_date = db.Column(db.DateTime, nullable=False)

    client = db.relationship("Client", backref = "job")
    skills = db.relationship("Skills", backref = "job")
    payment = db.relationship("Payment", backref = "job")
    attachment = db.relationship("Attachment", backref = 'job')

class Skills(db.Model):
    __tablename__ = "skills"
    
    id = db.Column(db.Integer, primary_key = True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    writer_id = db.Column(db.Integer, db.ForeignKey("writer.id"))
    name = db.Column(db.String(255))

class Attachment(db.Model):
    __tablename__ = "attachment"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.String(255))

class Payment(db.Model):
    __tablename__ = "payment"
  
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    amount = db.Column(db.Integer, nullable=False)  
    payment_method = db.Column(db.String(255), nullable=False) 
    status = db.Column(db.String(255), nullable=False) 
    transaction_date = db.Column(db.DateTime, nullable=False)  
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    

class Resource(db.Model):
    __tablename__ = "resource"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    link = db.Column(db.String(255))
    
class Progress(db.Model):
    __tablename__ = "progress"
  
    id =  db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey("writer.id"))
    state = db.Column(db.Float)

class Reviews(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    writer_id = db.Column(db.Integer, db.ForeignKey("writer.id"))
    review = db.Column(db.String(255))
