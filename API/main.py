from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from admin.admin import AdminWindow
from signin.signin import SigninWindow
from operate.operate import OperatorWindow
from kivy.lang import Builder
Builder.load_file('PepperShop.kv')

class PepperShopWindow(BoxLayout):
    admin_widget = AdminWindow()
    signin_widget = SigninWindow()
    operator_widget = OperatorWindow()

    def __init__(self, **kwargs):
        super().__init__(**kwargs) 

        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.operator_widget)

class PepperShopApp(App):
    def build(self):
        return PepperShopWindow()

if __name__ == "__main__":
    sa = PepperShopApp()
    sa.run()