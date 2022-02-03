from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.utils import get_color_from_hex
import datetime
import re
import sqlite3
import os
import random
Builder.load_file('operate/operate.kv')

conn = sqlite3.connect("db/posdb.db")
cn = conn.cursor()
date = datetime.datetime.now().date()



products_lists = []
product_price = []
product_quantity = []
product_id = []
product_stock = []
product_sold = []
product_cost = []

class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.7,.7)
        self.background = "get_color_from_hex('#FFFFFF')"
        

class OperatorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cart = []
        self.qty = []
        self.total = 0.00
        self.change = 0.00
        self.notify = Notify()
    # query = "SELECT * FROM stocks WHERE product_code = ?"
    # #values = [pcode]
    # result = c.execute(query)
    def logout(self):
        self.parent.parent.current = 'scrn_si'

    def update_purchase(self):
        self.ppty = self.ids.qty_inp.text
        self.pcode = self.ids.code_inp.text
        self.pnamee = self.ids.name_inp.text
        self.products_container = self.ids.products
        squery = "SELECT * FROM stocks WHERE product_code = ? OR product_name = ?"
        values = [self.pcode,self.pnamee]
        res = cn.execute(squery,values)
        conn.commit()
        
        for productcode in res:
            pcodee = productcode[1]
            self.pname = productcode[2]
            pweight = str(productcode[3])
           
            if self.pcode == str(pcodee) or self.pnamee == str(self.pname):
                
                self.details = BoxLayout(size_hint_y=None,height=30,pos_hint={'top': 1})
                self.products_container.add_widget(self.details)

                if self.ppty == '':
                    self.ty = int(1)
                else:
                    self.ty = int(self.ppty)

                self.itotal = int(self.ty)*int(productcode[7])

                self.code = Label(text=str(pcodee),font_name=('0WAG.TTF'),size_hint_x=.2,color=(.06,.45,.45,1))
                name = Label(text=self.pname,font_name=('0WAG.TTF'),size_hint_x=.3,color=(.06,.45,.45,1))
                qty = Label(text=str(self.ty),font_name=('0WAG.TTF'),size_hint_x=.1,color=(.06,.45,.45,1))
                disc = Label(text='0.00',font_name=('0WAG.TTF'),size_hint_x=.1,color=(.06,.45,.45,1))
                price = Label(text=str(productcode[7]),font_name=('0WAG.TTF'),size_hint_x=.1,color=(.06,.45,.45,1))
                total = Label(text=str(self.itotal),font_name=('0WAG.TTF'),size_hint_x=.1,color=(.06,.45,.45,1))
                delete = Button(text='Delete',font_name=('0WAG.TTF'),size_hint_x=.1,width=80,background_normal='',background_color=get_color_from_hex('#698B22'),on_release=lambda x: self.delete_item())
                self.details.add_widget(self.code)
                self.details.add_widget(name)
                self.details.add_widget(qty)
                self.details.add_widget(disc)
                self.details.add_widget(price)
                self.details.add_widget(total)
                self.details.add_widget(delete)

                #Update Preview
                pname = str(self.pname)
                self.stocks = productcode[4]
                self.sold = productcode[5]
                self.cost = productcode[6]
                self.pprice = productcode[7]
                if self.ppty == '':
                    self.pqty = str(1)
                else:
                    self.pqty = self.ppty
                self.total += self.pprice * int(self.ty)
                purchase_total = '`\n\nTotal\t\t\t\t\t\t'+str(round(self.total,2))                
                # amount = self.ids.change_inp.text
                # ttotal = self.total
                # change = float(amount) - ttotal
                #tchange = '`\n\nChange\t\t\t\t\t\t\t\t'+str(self.change_bal())
                self.ids.cur_product.text = pname
                self.ids.cur_price.text = str(self.pprice)
                self.preview = self.ids.receipt_preview
                prev_text = self.preview.text
                _prev = prev_text.find('`')
                if _prev > 0:
                    prev_text = prev_text[:_prev]

                ptarget = -1
                for i,c in enumerate(self.cart):
                    if c == self.pcode:
                        ptarget = i

                if ptarget >= 0:
                    self.pqty = self.qty[ptarget] + int(self.ty)
                    self.qty[ptarget] = self.pqty
                    expr = '%s\t\tx\d\t'%(pname)
                    rexpr = pname+'\t\tx'+str(self.pqty)+'\t'
                    nu_text = re.sub(expr,rexpr,prev_text)
                    self.preview.text = nu_text + purchase_total 
                else:
                    products_lists.append(self.pname)
                    product_id.append(self.pcode)
                    product_quantity.append(self.pqty)
                    product_price.append(self.pprice)
                    product_stock.append(self.stocks)
                    product_sold.append(self.sold)
                    product_cost.append(self.cost)
                    self.cart.append(self.pcode)
                    self.qty.append(self.ty)
                    self.nu_preview = '\n'.join([prev_text,pname+'\t\tx'+self.pqty+'\t\t'+str(self.pprice),purchase_total])
                    self.preview.text = self.nu_preview
                    
                    
    
        
    def killswitch(self,dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def change_bal(self):
       # get the amount give by the customer and the amount generated by the computer 
        self.amount = self.ids.change_inp.text
        self.change = float(self.amount) - self.total
        self.tchange = '\n\nChange\t\t\t\t' + str(round(self.change,2))
        self.ids.change_preview.text = self.tchange
      
        
        #print(self.change)
        #return change

    


    def clear(self):
        self.products_container.clear_widgets()
                
        self.preview.text = ''
        del products_lists[:]
        del product_id[:]
        del product_quantity[:]
        del product_price[:]
        del product_stock[:]
        del product_sold[:]
        del product_cost[:]
        del self.cart[:]
        del self.qty[:]
        self.total = 0.00
        self.change = 0.00
        self.ids.change_preview.text = ''
        self.ids.qty_inp.text = ''
        self.ids.code_inp.text = ''
        self.ids.name_inp.text = ''

        

    def generate_bill(self):
        #create bill before updating the database
        
        directory = "API/invoice/" + str(date) + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not self.cart:
            self.notify.add_widget(Label(text='[color=#ff0000][b]No product has been inserted[/b][/color]',markup=True,font_name='0WAG.TTF',font_size=24))
            self.notify.open()
            Clock.schedule_once(self.killswitch,3)
        elif self.change == 0.00:
            self.notify.add_widget(Label(text='[color=#ff0000][b]Enter Amount given and press Enter[/b][/color]',markup=True,font_name='0WAG.TTF',font_size=24))
            self.notify.open()
            Clock.schedule_once(self.killswitch,3)
        else:
            #TEMPLATES FOR THE BILLS
            company = "\t\t\t\tBritannia Shop\n"
            address = "\t\t\t\tAtuabo, Ghana\n"
            phone = "\t\t\t\tTel: 0246833817\n"
            dt = "\t\t\t\tDate: " + str(date) + "\t\n"
            sample = "\t\t\t\tINVOICE\n"

            table_header = "\n\n\t\t\tProducts\tQty\tAmount\n"
            final = company + address + phone + dt + sample + "\n" + table_header
            
            # open a file to write it to
            file_name = str(directory) + str(random.randrange(5000, 10000)) + ".rtf"
            f = open(file_name, "w")
            f.write(final)
            r = 1
            i = 0
            for t in products_lists:
                f.write("\n\t\t\t" + str(products_lists[i] + ".......")[:7] + "\t" + str(self.qty[i]) + "\t" + str(product_price[i]))
                r += 1
                i += 1
                    
            #f.write("\n\n\t\t\t" + str(self.print_view)) 
            f.write("\n\n\t\t\tTotal: Cedis " + str(self.total))
            f.write("\n\n\t\t\tChange:\t " + str(round(self.change,2)))
            f.write("\n\t\t\tThanks for visiting.")
            #os.startfile(file_name, "print")
            f.close()
            
            # # decrease the stock
            self.x = 0
            
            initial = "SELECT * FROM stocks WHERE product_code=?"
            result = cn.execute(initial, (product_id[self.x], ))
            
            for r in result:
                self.old_stock = r[4]
                self.old_sold = r[5]
                
                #updating the stock

            for i in products_lists:
                for r in result:
                    self.old_stock = r[4]
                
                self.profit = float(product_price[self.x]) - float(product_cost[self.x])
                self.new_stock = float(product_stock[self.x]) - float(self.qty[self.x])
                self.new_sold = float(product_sold[self.x]) + float(self.qty[self.x])
                self.new_assumed = float(self.new_stock) * float(self.profit)
            
                sql = "UPDATE stocks SET in_stock=?, sold=?, assumed_profit=?, last_purchase=? WHERE product_code=?"
                cn.execute(sql, (self.new_stock, self.new_sold, self.new_assumed, date, product_id[self.x]))
                conn.commit()

                #insert into the transactions
                sql2 = "INSERT INTO transactions (product_code, product_name, quantity, amount, date) VALUES (?, ?, ?, ?, ?)"
                cn.execute(sql2, (product_id[self.x], products_lists[self.x], self.qty[self.x], product_price[self.x], date))
                conn.commit()
                self.products_container.remove_widget(self.details)
                self.x += 1
                
                
            

            self.notify.add_widget(Label(text='[color=#ff0000][b]Purchase  has successfully been completed[/b][/color]',markup=True,font_name='0WAG.TTF',font_size=24))
            self.notify.open()
            Clock.schedule_once(self.killswitch,3)

            self.products_container.clear_widgets()
                
            self.preview.text = ''
        
            del products_lists[:]
            del product_id[:]
            del product_quantity[:]
            del product_price[:]
            del product_stock[:]
            del product_sold[:]
            del product_cost[:]
            del self.cart[:]
            del self.qty[:]
            self.total = 0.00
            self.change = 0.00
            self.ids.change_preview.text = ''
            self.ids.qty_inp.text = ''
            self.ids.code_inp.text = ''
            self.ids.name_inp.text = ''
        
        


    def delete_item(self):
        
        for child in self.details.children[:]:
            self.details.remove_widget(child)
            print(child)
            
     
        
                



        
                
        


class operateApp(App):
    def build(self):
        return OperatorWindow()

if __name__ == "__main__":
    oa = operateApp()
    oa.run()