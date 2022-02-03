from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import sqlite3
#from pymongo import MongoClient
import hashlib

Builder.load_file('signin/signin.kv')
conn = sqlite3.connect("db/posdb.db")
c = conn.cursor()


class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 

    def validate_user(self):
        #client = MongoClient()
        #db = client.posdb
        #users = db.users
       
            
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info

        uname = user.text
        passw = pwd.text
        
        user.text = ''
        pwd.text = ''
        if uname == '' or passw == '':
            info.text = "[color=#ff0000]username and /or password required[/color]"
            
        else:
            query = "SELECT * FROM users WHERE user_name = ?"
            values = [uname]
            result = c.execute(query,values)
            user = c.fetchone()
                   
            if user == None:
                info.text = "[color=#ff0000]Invalid username [/color]"
            else:
                
                query = "SELECT * FROM users WHERE user_name = ?"
                values = [uname]
                result = c.execute(query,values)
                user = c.fetchone()
                passw = hashlib.sha256(passw.encode()).hexdigest()
                if passw == user[4]:
                    perm = user[5]
                    #info.text = "[color=#00ff00]Loged in successfully[/color]"
                    info.text = ''
                    self.parent.parent.parent\
                        .ids.scrn_op.children[0]\
                            .ids.loggedin_user.text = uname

                    if perm == 'Administrator':
                        self.parent.parent.current = 'scrn_admin'
                    else:
                        self.parent.parent.current = 'scrn_op'
                else:
                    info.text = "[color=#ff0000]Invalid username and /or password [/color]"

class SigninApp(App):
    def build(self):
        return SigninWindow()

if __name__ == "__main__":
    sa = SigninApp()
    sa.run()