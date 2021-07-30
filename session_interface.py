import uuid
import json
from flask.sessions import SessionMixin,SessionInterface
from itsdangerous import Signer,BadSignature,want_bytes

class MySession(dict,SessionMixin):
    def __init__(self,initial=None,sessionId=None):
        self.initial=initial
        self.sessionId=sessionId
        super(MySession,self).__init__(initial or ())
    
    def __setitem__(self, key, value):
        super(MySession,self).__setitem__(key,value)
    
    def __getitem__(self, key):
        return super(MySession,self).__getitem__(key)
    
    def __delitem__(self, key):
        super(MySession,self).__delitem__(key)
    
class MySessionInterface(SessionInterface):
    session_class= MySession    
    def __init__(self):
        self.salt="my-session"
        self.container=dict()
    
    def open_session(self, app, request):
        signedsessionId=request.cookies.get(app.session_cookie_name)
        if not signedsessionId:
            sessionId=str(uuid.uuid4())
            return self.session_class(sessionId=sessionId)
        
        signer=Signer(app.secret_key,salt=self.salt,key_derivation="hmac")
        try:
            sessionId=signer.unsign(signedsessionId).decode()
        except BadSignature:
            sessionId=str(uuid.uuid4())
            return self.session_class(sessionId=sessionId)            
        
        initialSessionValueAsJson=self.container.get(sessionId)
        try:
            initialSessionValue=json.loads(initialSessionValueAsJson)
        except:
            sessionId=str(uuid.uuid4())
            return self.session_class(sessionId=sessionId)            
        
        return self.session_class(initialSessionValue,sessionId=sessionId)
    
    def save_session(self, app, session, response):
        sessionAsJson=json.dumps(dict(session))
        
        self.container[session.sessionId]=sessionAsJson
        #burada kaydetme işlemi yapılır şu an bir sözlüğe kaydedildi ama başka yere de kaydedilebilir
        signer=Signer(app.secret_key,salt=self.salt,key_derivation="hmac")
        signedSessionId=signer.sign(want_bytes(session.sessionId))
        
        response.set_cookie(app.session_cookie_name,signedSessionId)
        