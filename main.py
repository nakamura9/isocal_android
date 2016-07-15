'''
Created on Apr 5, 2016

@author: caleb kandoro
'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import (ScreenManager, Screen,
                                    FadeTransition, SlideTransition)
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (StringProperty, ObjectProperty,
                                             NumericProperty)
from kivy.uix.anchorlayout import AnchorLayout
from kivy.storage.jsonstore import JsonStore
from kivy.uix.actionbar import ActionItem
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.core.window import WindowBase 
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.network.urlrequest import UrlRequest
from _datetime import timedelta
try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode
    
import datetime
import time
import os
import utilities as t
import requests
from kivy.core.text import LabelBase

LabelBase.register(name= "Modern Pictograms",
                   fn_regular = os.path.join(os.path.abspath(), "ModernPictograms.ttf"))
root = os.getcwd()
Window.clear_color = [1, 1, 1, 1]
WindowBase.softinput_mode = "below_target"

balance = JsonStore("BALANCE.json")
customers = JsonStore("CUSTOMERS.json")
standards = JsonStore("STANDARDS.json")
general = JsonStore("GENERAL.json")
accounts = JsonStore("accounts.json")
outstanding = JsonStore("OUTSTANDING.json")
autoclave = JsonStore("AUTOCLAVE.json")
electrical = JsonStore("ELECTRICAL.json")

accounts.put("isocal", password="17025")
current_user = ""
class Heading(Label):
    pass

class Cell(Label):
    pass

class UploadMessage(Label):
    pass

class AltCell(Cell):
    pass

class LinCell(Cell):
    pass

class LinAltCell(AltCell):
    pass

class MyActionButton(ActionItem, Button):
    pass

class DataApp(App):
    pass

class WhiteBoxLayout(BoxLayout):
    pass

class WhiteScreen(Screen):
    pass

class Base(WhiteBoxLayout):
    
    def validate(self, user, password,_label):
        global accounts
        global current_user
        global general
        if accounts.exists(user):
            if password == accounts.get(user)["password"]:
                current_user = user
                self.cal = []
                self.remove_widget(self.children[0])
                self.add_widget(Home())
                self.home = self.children[0]
            else:
                _label.text = "wrong password"
        else:
            _label.text = "wrong name"
            
        
            
class HorizontalInput(WhiteBoxLayout):
    name = StringProperty()
    val= ObjectProperty()
    txt=StringProperty()
    
        
    
class VerticalInput(WhiteBoxLayout):
    name = StringProperty()
    val= ObjectProperty()
    txt=StringProperty()
    

class WhiteAnchorLayout(AnchorLayout):
    pass

class WhiteScreenManager(ScreenManager):
    pass

class CenteredTable(BoxLayout):
    table= ObjectProperty()
    n = NumericProperty()
class General(WhiteBoxLayout):
    pass

class Login(WhiteBoxLayout):
    pass

class SummaryScreen(Screen):
    table = ObjectProperty()
    def __init__(self, *args, **kwargs):
        super(SummaryScreen, self).__init__(*args, **kwargs)
        
    def generate_table(self):
        global outstanding
        print("called")
        values = {"Instrument": [],
                  "Serial": [],
                  "Customer": [],
                  "Date": []}
        for key in outstanding:
            values["Instrument"].append(outstanding[key]["name"])
            values["Serial"].append(outstanding[key]["serial"])
            values["Customer"].append(outstanding[key]["customer"])
            values["Date"].append(outstanding[key]["date"])
        
        self.table.clear_widgets()
        
        self.table.add_widget(table(["Instrument", 
                               "Serial",
                               "Customer",
                               "Date"], values))
           
class Home(WhiteBoxLayout):
    sm = ObjectProperty()
    title = ObjectProperty()

class HomeScreenManager(WhiteScreenManager):
    summary = ObjectProperty()
    balance = ObjectProperty()
    upload = ObjectProperty()
    
    def __init__(self, *args, **kwargs):
        super(HomeScreenManager, self).__init__(*args, **kwargs)
        self.transition = FadeTransition()
        self.instrument_info = []
        self.instrument_specs = []
        self.first_readings = ""
    def next(self):
        if hasattr(self.current_screen, "next"):
            self.current_screen.next()
        elif hasattr(self.current_screen, "asm"):
            if hasattr(self.current_screen.asm.current_screen, "next"):
                self.current_screen.asm.current_screen.next()
        else:
            print(self.current_screen.__dict__)
            
            
    def record(self):
        if hasattr(self.current_screen, "record"):
            self.current_screen.record()
        elif hasattr(self.current_screen, "asm"):
            if hasattr(self.current_screen.asm.current_screen, "record"):
                self.current_screen.asm.current_screen.record()
             
        else:
            print(self.current_screen.__dict__)
            
    def submit(self):
        
        if hasattr(self.current_screen, "submit"):
            self.current_screen.submit()
        elif hasattr(self.current_screen, "asm"):
            if hasattr(self.current_screen.asm.current_screen, "submit"):
                self.current_screen.asm.current_screen.submit()
        else:
            print(self.current_screen.__dict__)
            
                
    def prev(self):
        if hasattr(self.current_screen, "previous"):
            self.current_screen.previous()
        elif hasattr(self.current_screen, "asm"):
            if hasattr(self.current_screen.asm, "previous"):
                self.current_screen.asm.current_screen.previous()
        else:
            print(self.current_screen.__dict__)
            
    def clear(self):
        try:
            cur = self.current_screen
            cur.clear()
        except Exception as e:
            try:
                cur = self.current_screen.asm.current_screen
                cur.clear()
            except Exception as e:
                print("this also happened ", e)
                
    def clear_last(self):
        try:
            cur = self.current_screen
            cur.clear_last()
        except Exception as e:
            try:
                cur = self.current_screen.asm.current_screen
                cur.clear_last()
            except Exception as e:
                print("this also happened ", e)
                
    def change(self, s, title):
        self.parent.title.text = title
        self.type = self.parent.title.text.split(" ")[0].lower()
        self.current = s 
    
    def calibrate(self):
        if self.parent.title.text=="Balance Calibration":
            self.balance.asm.instrument_info = self.instrument_info
            self.balance.asm.instrument_specs = self.instrument_specs
            self.current = "_balance"
        elif self.parent.title.text == "Pressure Calibration":
            self.current = "pressure_first"
        else:
            self.current= "readings"
        

class InstrumentInfoScreen(WhiteScreen):
     nom = StringProperty()
     std = StringProperty()
     def get_date(self):
         next = datetime.date.today() + timedelta(days =180)
         return next.strftime("%d/%m/%y")
     
     def change(self):
         self.parent.current= "instrument_specs"
     def next(self):
         global standards
         due = self.ids.due.val.text
         name = self.ids.nom.val.text
         serial = self.ids.sn.val.text
         customer = self.ids.cus.val.text
         manufacturer = self.ids.man.val.text
         model = self.ids.model.val.text
         standard = self.ids.standard.val.text
         stds = list(standards.keys())
         if name == "" or customer == "" or standard == "":
             p=Popup(title="Warning!", size_hint=(None, None), size=(300, 150),
                     content=Label(text= "Some fields cannot be empty"))
             p.open()
         elif standard not in standards:
             p=Popup(title="Warning!", size_hint=(None, None), size=(400, 400),
                     content=Label(text= "The Instrument cannot be calibrated without \n"
                                   "an acompanying standard. These are available:\n"
                                   "{}".format("\n".join(stds))))
             p.open()
         elif self.parent.type == "mass" and standard not in standards:
             p=Popup(title="Warning!", size_hint=(None, None), size=(400, 200),
                     content=Label(text= "The balance cannot be calibrated without \n"
                                   "an acompanying standard. These are available:\n"
                                   "{}".format(standards.keys())))
             p.open()
         else:
             self.parent.instrument_info = [name, serial,
                        customer,
                        manufacturer, 
                        model,standard, due]
             
             self.ids.nom.val.text =""
             self.ids.sn.val.text = ""
             self.change()
             
        
        
class InstrumentSpecsScreen(WhiteScreen):
    def next(self):
        min = self.ids.min.text
        max = self.ids.max.text
        res = self.ids.res.val.text
        units= self.ids.units.val.text 
        location= self.ids.location.val.text
        immersion= self.ids._immersion.val.text
        instrument_unit_lexicon={"pressure": ["bar", "psi", "mpa", "kpa", "pa"],
                                 "temperature": ["celcius", "fahrenheit"],
                                 "tds": ["ppm", "ppt", "ppb"],
                                 "volume": ["litre", "ml", "m3"],
                                 "flow": ["l/min", "cf/min", "l/hr", "m3/hr", "cf/hr"],
                                 "balance": ["grams", "kgs"],
                                 "current": ["amp", "milliamp"],
                                 "volts": ["volt", "millivolt", "kilovolt"],
                                 "mass": ["grams", "kgs"],
                                 "ph": ['ph'],
                                 "conductivity": ["siemens"]
                                 }
        
        if min=="" or max=="" or res=="" or units=="" or location=="":
            p=Popup(title="Warning!", size_hint=(None, None), size=(300, 150),
                    content=Label(text= "Some fields cannot be empty"))
            p.open()
        else:
            if self.parent.type in instrument_unit_lexicon:
                if units not in instrument_unit_lexicon[self.parent.type]:
                    p = Popup(size_hint =(None, None), size=(400, 200), title = "Warning!",
                              content=Label(text="""You Have entered an invalid unit. Try one of
                                              {}""".format(", ".join(instrument_unit_lexicon[self.parent.type]))))
                    p.open()
                else:
                    self.parent.instrument_specs = [min, max, res, units, location, immersion]
                    self.parent.start_time = datetime.datetime.now().strftime("%H:%M:%S")
                    self.parent.calibrate()
            else:         
                self.parent.instrument_specs = [min, max, res, units, location, immersion]
                self.parent.start_time = datetime.datetime.now().strftime("%H:%M:%S")
                self.parent.calibrate()
class CheckCorrections(BoxLayout):
    yes= ObjectProperty()
    no= ObjectProperty()
    
class AbstractReadingsScreen(WhiteScreen):
    def __init__(self, *args, **kwargs):
        super(AbstractReadingsScreen, self).__init__(*args, **kwargs)
        self.count = 0
        self.readings = {"indicated": [],
                          "actual": []}
        self.with_corrections = False
        self.called_next = False
        self.first = "not yet set"
        
    def clear(self):
         for i in self.readings:
            self.readings[i] = []
            self.ids._table.table.clear_widgets()
            
    def clear_last(self):
        headings = []                                                                                         
        for i in self.readings:
            headings.append(i)
            l = len(self.readings[i]) - 1
            self.readings[i] = self.readings[i][:l]
        self.ids._table.table.clear_widgets()
        headings.sort()
        self.ids._table.table.add_widget(table(headings, self.readings))
            
    def data_add(self):
        '''this method abstracts the data addition of the program while ensuring that 
        the popup can halt executiom in record'''
        self.readings["indicated"].append(self.ids.actual.val.text)
        self.readings["actual"].append(self.ids.nominal.val.text)
        self.ids._table.table.add_widget(table(["indicated", "actual"], self.readings))
    
    def corrections(self, other):
        self.with_corrections = True
        self.clear_readings()
        
    def no_corrections(self, other):
        self.submit()
        
    def record(self):
        self.count += 1
        if self.ids.nominal.val.text == "" or self.ids.actual.val.text == "":
            p = Popup(title="Warning", size_hint = (None, None),
                      size=(400, 200), content=Label(text="You cannot enter empty fields"))
            p.open()
        else:
            try:
                self.ids._table.table.clear_widgets()
                self.data_add()
            except Exception as e:
                p = Popup(size_hint=(None, None), size=(400, 200),
                          title = "Warning! You have entered and invalid Value",
                          content=Label(text="Error: {}".format(e)))
                p.open()
                
    def next(self):
        if not self.called_next:
            self.called_next = True
            self.first = readings_combined(self.readings)
            print("readings at next: ", self.readings)
            
            if self.count < 2:
                p = Popup(size_hint=(None, None), size=(400, 200),
                              title = "Warning!",
                              content=Label(text="You have recorded too few values"))
                p.open()
            else:
                self.clear_readings()
                content = CheckCorrections()
                p = Popup(title="Important", size_hint = (None, None),
                          size=(content.width * 1.05, content.height* 1.2), content=content)
                content.yes.bind(on_press = self.corrections)
                content.no.bind(on_press =self.no_corrections)
                content.yes.bind(on_release= p.dismiss)
                content.no.bind(on_release= p.dismiss)
                p.open()
        
        else:
            self.submit()
                
                
    
          
    def clear_readings(self):
        '''if pressure use its onw algorithm bt defaults to readings_combined'''
        for i in self.readings:
                    self.readings[i] = []
        
        self.count = 0
        self.ids._table.table.clear_widgets()

        
        
    def submit(self):
        global general
        global outstanding
        info = self.parent.instrument_info
        specs= self.parent.instrument_specs
        print("readings at submit: ", self.readings)
        if not self.called_next:
            print("make sure next is called")
            self.next()
        else:
            self.count = 0
            id = "{}{}".format(datetime.date.today().strftime("%d%m%y"),
                                   info[1])
            print("first ", self.first) 
            general.put(id,# serial 
                    name="general",
                    due = info[6],
                    name_of_instrument= info[0], serial=info[1],
                    customer=info[2],manufacturer=info[3],
                    _type = self.parent.type,
                    model=info[4], range=specs[0]+ "-" + specs[1],
                    resolution=specs[2], units=specs[3], location=specs[4],
                    immersion_depth = specs[5],
                    end_time = datetime.datetime.now().strftime("%H:%M:%S"),
                    start_time= self.parent.start_time,
                    readings= self.first,
                    corrections= readings_combined(self.readings),
                    standards=info[5],
                    comments= self.ids.comments.text
                    )
        
            outstanding.put(id,
                        name=self.parent.instrument_info[0],
                        customer=self.parent.instrument_info[2],
                        date=datetime.date.today().strftime("%d/%m/%Y"),
                        serial=self.parent.instrument_info[1]) #serial
            print(general.get(id))
            self.parent.instrument_info = []
            self.parent.instrument_specs = []
            self.readings = {"indicated": [],
                         "actual": []}
            
            
            self.first = ""
            self.ids._table.table.clear_widgets()
            self.called_next = False
            self.with_corrections = False
            self.parent.summary.generate_table()
            self.parent.current= "summary"
            
class ReadingsScreen(AbstractReadingsScreen):
    pass
    
class PressureReadingsScreen(AbstractReadingsScreen):
    
    def __init__(self, *args, **kwargs):
        super(PressureReadingsScreen, self).__init__(*args, **kwargs)
        self.readings = {"applied": [],
                          "calculated": [],
                          "indicated": []}
        self.calculators = {"kpa":t.calculate_pressure_kpa, 
                                        "pa":t.calculate_pressure_pa,
                                        "mpa":t.calculate_pressure_mpa,
                                        "bar":t.calculate_pressure_bar,
                                        "psi":t.calculate_pressure_psi}
        
        
    def data_add(self):
        self.readings["applied"].append(self.ids.nominal.val.text)
        self.readings["indicated"].append(self.ids.actual.val.text)
        if self.count == 1 and self.ids.nominal.val.text == "0":
            self.readings["calculated"].append("0")
        else: 
            self.readings["calculated"].append("{:0.2f}".format(self.calculators[self.parent.instrument_specs[3]](
                                                            self.ids.nominal.val.text)))

        self.ids._table.table.add_widget(table(["applied", "calculated", "indicated"],
                                                            self.readings))    
                 
    def submit(self):
        super(PressureReadingsScreen, self).submit()
        self.readings = {"applied":[],
                         "indicated": [],
                         "calculated": []}      
                
class UploadScreen(WhiteScreen):
    '''fix with json'''
    messages = ObjectProperty()
    def __init__(self, *args, **kwargs):
        super(UploadScreen, self).__init__(*args, **kwargs)
        self.general = []
        self.autoclave = []
        self.balance = []
    def upload_general(self, key):
        global general
        global outstanding
        global current_user
        gen = general[key]
        out = outstanding[key]
        
        params = {"user":current_user,
                            "customer":gen["customer"],
                            "_type":gen["_type"],
                            "id":key,
                            "due": gen["due"],
                            "date":out["date"],
                            "instrument":gen["name_of_instrument"],
                            "sn":gen["serial"],
                            "man":gen["manufacturer"],
                            "model":gen["model"],
                            "_range":gen["range"],
                            "resolution":gen["resolution"],
                            "units":gen["units"],
                            "standard":gen["standards"],
                            "location":gen["location"],
                            "start_time":gen["start_time"],
                            "end_time":gen["end_time"],
                            "readings":gen["readings"],
                            "corrections":gen["corrections"],
                            "immersion":gen["immersion_depth"],
                            "comments":gen["comments"],
                            }
      
        try:
            req= requests.post("http://{}/mobile/upload_general?".format(self.host), data=params)
            if req.text == "success":
                #add the list of succesfully uploaded keys then delete them once iteration is over
                self.general.append(key)
                outstanding.delete(key)
                self.messages.item_strings.append("Upload completed sucessfully") 
            else:
                print(req.text)
                self.messages.item_strings.append("Upload unsuccessful")
        except Exception as e:
            self.messages.item_strings.append("""An error occured while trying to upload this certificate:
                                    {}""".format(e))
                                    
        
    def upload_balance(self, key):
        global balance
        global outstanding
        global current_user
        bal = balance[key]
        out = outstanding[key]
        params = {"user":current_user,
                            "customer":bal["customer"],
                            "id":key,
                            "date":out["date"],
                            "due": bal["due"],
                            "sn":bal["serial"],
                            "start_time":bal["start_time"],
                            "end_time":bal["end_time"],
                            "man":bal["manufacturer"],
                            "model":bal["model"],
                            "_range":bal["_range"],
                            "resolution":bal["resolution"],
                            "units":bal["units"],
                            "standard":bal["standard"],
                            "location":bal["location"],
                            "comments":bal["comments"],
                            "start_time":bal["start_time"],
                            "end_time":bal["end_time"],
                            "procedure":bal["procedure"],
                            "off_center_mass":bal["off_center_mass"],
                            "warm_up_nominal":bal["warm_up_nomial"],
                            "tare":bal["tare"],
                            "tare_indicated":bal["tare_indicated"],
                            "repeat_half":bal["repeat_half"],
                            "repeat_full":bal["repeat_full"],
                            "off_center":bal["off_center"],
                            "settling_time":bal["settling_time"],
                            "nominal_mass":bal["nominal_mass"],
                            "after_up":bal["after_up"],
                            "after_uup":bal["after_uup"],
                            "before_actual": bal["before_actual"],
                            "before_up":bal["before_up"],
                            "before_nominal":bal["before_nominal"],
                            "after_down":bal["after_down"]}
        try:
            for k, value in params.items():
                payload={"key": k,
                         "value": value}
    
                req= requests.post("http://{}/mobile/upload_balance".format(self.host), data=payload)
            if req.text == "success":
                print(key)
                self.balance.append(key)
                outstanding.delete(key)
                self.messages.item_strings.append("Upload completed sucessfully") 
            else:
                print(req.text)
                self.messages.item_strings.append("Upload unsuccessful")
        except Exception as e: 
            self.messages.item_strings.append("""An error occured while trying to upload this certificate:
                                    {}""".format(e))
    
    def upload_autoclave(self, key):
        global autoclave
        global outstanding
        global current_user
        auto = autoclave[key]
        
        params = {"user":current_user,
                  "id":key,
                  "customer":auto["customer"],
                  "start_time":auto["start_time"],
                  "end_time":auto["end_time"],
                  "date":auto["date"],
                  "serial":auto["serial"],
                  "immersion_depth":auto["immersion_depth"],
                  "manufacturer":auto["manufacturer"],
                  "model":auto["model"],
                  "range_temp":auto["range_temp"],
                  "range_p": auto["range_p"],
                  "resolution_temp":auto["resolution_temp"],
                  "resolution_p":auto["resolution_p"],
                  "units_temp":auto["units_temp"],
                  "units_p":auto["units_p"],
                  "standards":auto["standards"],
                  "location":auto["location"],
                  "comments":auto["comments"],
                  "temp":auto["temp"],
                  "pressure":auto["pressure"]}
        
        try:
            for k, value in params.items():
                payload={"key": k,
                         "value": value}
                req= requests.post("http://{}/mobile/upload_autoclave".format(self.host), data=payload)
            print(req.text)
            if req.text == "success":
                self.autoclave.append(key)
                outstanding.delete(key)
                self.messages.item_strings.append("Upload completed sucessfully") 
            else:
                print(req.text)
                self.messages.item_strings.append("Upload unsuccessful")
        except Exception as e:
            self.messages.item_strings.append("""An error occured while trying to upload this certificate:
                                    {}""".format(e))
            
    def upload_standards(self, key):
        global standards
        std = standards[key]
        params = {"name":key,
                  "serial": std["serial"], 
                  "number":std["certificate_number"],
                  "traceability": std["traceability"],
                  "nominal":std["nominal"],
                  "actual":std["actual"],
                  "uncertainty":std["uncertainty"]}
        try:
            req= requests.post("http://{}/mobile/upload_standard".format(self.host), data=params)
            print(req.text)
        except Exception as e:
            self.messages.item_strings.append("""An error occured while trying to upload this standard:
                                    {}""".format(e))
                                
    
    def upload(self):
        self.host = self.ids.host.val.text
        global balance
        global general
        global standards
        global autoclave
        
        code = 0                                    
        try:
            if self.host == "":
                p = Popup(title= "warning", content= Label(text="The host cannot be empty"),
                          size_hint=(None, None), size=(300,150))
                p.open()
            else:
                self.messages.item_strings.append("Connecting to the server...")
                req = requests.get("http://{}/mobile/".format(self.host))
                code = req.status_code
        except:
            self.messages.item_strings.append("Uploading failed, try again")
            code = 404
            
        print(code)
        if code == 200 or code == "200":
            for key in general:
                self.messages.item_strings.append("Uploading {}".format(key))
                self.upload_general(key)
                
            for key in self.general:
                general.delete(key)
            self.general = []
            for key in balance:
                self.current_key = key
                self.messages.item_strings.append("Uploading {}".format(key))
                self.upload_balance(key)
               
            for key in self.balance:
                balance.delete(key)
            self.balance = []
                
            for key in  autoclave:
                self.current_key = key
                self.messages.item_strings.append("Uploading {}".format(key))
                self.upload_autoclave(key)
            
            for key in self.autoclave:
                autoclave.delete(key)
            self.autoclave = []
                
            for key in standards:
                self.messages.item_strings.append("Uploading {}".format(key))
                self.upload_standards(key)
                
            self.messages.item_strings.append("Uploading completed")        
        else:
            self.messages.item_strings.append("Uploading failed")
        # if it fails give a reason
        
        
        
class NewCustomerScreen(WhiteScreen):
    
    def submit(self):
        global customers
        customers.put(self.ids.cus_name.val.text,
                      name=self.ids.cus_name.val.text, 
                      address=self.ids.address.val.text,
                      phone=self.ids.phone.val.text,
                      email=self.ids.email.val.text)
        
        self.ids.cus_name.val.text = "" 
        self.ids.address.val.text = ""
        self.ids.phone.val.text = ""
        self.ids.email.val.text = ""
        self.parent.change("summary", "Summary")

class NewStandardScreen(WhiteScreen):
    
    def __init__(self, *args, **kwargs):
        super(NewStandardScreen, self).__init__(*args, **kwargs)
        self. readings = {"nominal": [],
                          "actual": [],
                          "uncertainty": []}
    
    def record(self):
        self.readings["nominal"].append(self.ids.nominal.val.text)
        self.readings["actual"].append(self.ids.actual.val.text)
        self.readings["uncertainty"].append(self.ids.uncertainty.val.text)
        self.ids.nominal.val.text = ""
        self.ids.actual.val.text = ""
        self.ids.table.clear_widgets()
        self.ids.table.add_widget(table(["nominal", "actual", "uncertainty"], self.readings))
        
    def submit(self):
        global standards
        trace = self.ids.trace.text
        name = self.ids.std_name.val.text
        number = self.ids.number.val.text
        serial = self.ids.serial.val.text
         
        #add a key using the length of outstanding and some other variable
        standards.put(self.ids.std_name.val.text,
                      name=self.ids.std_name.val.text,
                      certificate_number= self.ids.number.val.text,
                      traceability= self.ids.trace.text,
                      serial=self.ids.serial.val.text,
                      nominal="|".join(self.readings["nominal"]),
                      actual="|".join(self.readings["actual"]),
                      uncertainty="|".join(self.readings["uncertainty"]))
        
        self.ids.table.clear_widgets()
        self.ids.number.val.text = ""
        self.ids.std_name.val.text = ""
        self.ids.nominal.val.text = ""
        self.ids.actual.val.text = ""
        self.ids.trace.text = ""
        self.ids.serial.val.text=""
        self.ids.uncertainty.val.text = ""
        self.parent.change("summary", "Summary")


class AutoclaveScreen(WhiteScreen):
    asm = ObjectProperty()
    title = ObjectProperty()
    
class AutoclaveScreenManager(WhiteScreenManager):
    def __init__(self, *args, **kwargs):
        super(AutoclaveScreenManager, self).__init__(*args, **kwargs)
        self.type = "autoclave"
        self.title = "Instrument Info"
    def calibrate(self):
        self.change("specs_p", "Pressure Specs.")
        
    def change(self, s, t):
        self.parent.parent.title.text = t
        self.current = s

class AutoInfo(InstrumentInfoScreen):
    def change(self):
        self.parent.change("instrument_specs", "Specifications")

class AutoSpecs(WhiteScreen):
    def next(self):
        range_temp = self.ids.min_t.text + "-" + self.ids.max_t.text
        range_pressure = self.ids.min_p.text + "-" + self.ids.max_p.text
        res_p = self.ids.res_p.val.text
        res_t = self.ids.res_t.val.text
        units_p= self.ids.units_p.val.text
        units_t= self.ids.units_t.val.text 
        location= self.ids.location.val.text
        immersion= self.ids._immersion.val.text
        pressure_units= "bar kpa mpa pa psi".split(" ")
        if units_p not in pressure_units:
            p = Popup(size_hint =(None, None), size=(400, 200), title = "Warning!",
                              content=Label(text="""You Have entered an invalid unit. Try one of
                                              {}""".format(", ".join(pressure_units))))
            p.open()
        elif range_temp=="-" or range_pressure=="-" or res_p=="" or units_t=="" or location=="":
            p=Popup(title="Warning!", size_hint=(None, None), size=(300, 150),
                    content=Label(text= "Some fields cannot be empty"))
            p.open()
        else:
            self.parent.start_time = time.strftime("%H:%M",time.localtime(time.time()))
            self.parent.instrument_specs = [range_pressure, range_temp, res_p,
                                            units_p, res_t, units_t,  location, immersion]
            self.parent.change("temp", "Temperature Calib.")


class AutoTemp(ReadingsScreen):
    def next(self):
        self.parent.temp_readings = self.readings
        self.readings = {"actual": [],
                         "indicated": []}
        self.parent.change("pressure", "Pressure Calib.")

class AutoPressure(PressureReadingsScreen):
    def submit(self):
        global autoclave
        global outstanding
        info= self.parent.instrument_info
        specs = self.parent.instrument_specs
        print(self.parent.temp_readings)
        print(readings_combined(self.readings))
        d=datetime.date.today().strftime("%y/%m/%d") 
        id = datetime.date.today().strftime("%d%m%Y")+info[1]
        autoclave.put(id,
                      customer = info[2],
                      start_time= self.parent.start_time,
                      end_time = time.strftime("%H:%M", time.localtime(time.time())),
                      date= d, due = info[6],
                      name_of_instrument= info[0],
                      serial= info[1],
                      immersion_depth=specs[7],
                      manufacturer=info[3],
                      model=info[4],
                      range_temp= specs[1],
                      range_p=specs[0],
                      resolution_temp= specs[4],
                      resolution_p=specs[2],
                      units_temp=specs[5],
                      units_p=specs[3],
                      standards=info[5],
                      location=specs[6],
                      comments=self.ids.comments.text,
                      temp=readings_combined(self.parent.temp_readings),
                      pressure=readings_combined(self.readings))
        
        print(autoclave.get(id))
        outstanding.put(id, name=info[0],
                        customer = info[2],
                        date=d,
                        serial=info[1])
        self.parent.current = "info"
        self.readings = {"applied":[],
                         "indicated": [],
                         "calculated": []}

class ElectricalScreen(WhiteScreen):
    title = StringProperty()
    asm =ObjectProperty()

class ElectricalScreenManager(WhiteScreenManager):
    def __init__(self, *args, **kwargs):
        super(ElectricalScreenManager, self).__init__(*args, **kwargs)
        self.tables = {}
        self.type= "electrical"
        
    def calibrate(self):
        self.current = "readings"
        self.title = "DC Voltage"
        for i in self.current_screen.fields:
            self.current_screen.ids.field_list.add_widget(Cell(text=i))
        
class EInfo(InstrumentInfoScreen):
    pass

class ESpecs(InstrumentSpecsScreen):
    pass 

class ElectricalReadingsScreen(WhiteScreen):
    def __init__(self, *args, **kwargs):
        super(ElectricalReadingsScreen, self).__init__(*args, **kwargs)
        '''this readings scheme is meant to deal with more than a 150 readings
        it catagorizes them by unit then by range. it comprises two lists of 
        filters for the readings stored in self. fields and self.ranges. the same readdings screen is rectcled 
        by the submit button and the results are stored in a dictionary called combined'''
        
        self.fields= "DC Voltage,AC Voltage,DC Current,AC Current,Resistance,Insulation,Diodes".split(",")
        self.readings = {"Input": [],
                         "Indicated": []}
        self. combined = {}
        self.current = 0
        self.ranges = {"DC Voltage":["600mV", "6V", "60V", "600V", "1000V"],
                       "AC Voltage": [],
                       "DC Current": []}
        self.count = 0
        
        
    def record(self):
        self.readings["Input"].append(self.ids.input.val.text)
        self.readings["Indicated"].append(self.ids.reading.val.text)
    
        self.ids.table.table.clear_widgets()
        self.ids.table.table.add_widget(table(["Input", "Indicated"],
                                              self.readings))
        
        
    def submit(self):
        if self.current < 6:
            self.combined[self.fields[self.current]] = readings_combined(self.readings)
            for i in self.readings: self.readings[i] = []
            self.current += 1
        else:
            global electrical
            global outstanding
        
            d=datetime.date.today().strftime("%y/%m/%d") 
            
            info=self.parent.instrument_info
            id = datetime.date.today().strftime("%d%m%Y")+info[1]
            specs = self.parent.instrument_specs
            table = self.parent.tables
            electrical.put(id,
                           customer = info[2],
                           start_time= self.parent.start_time,
                           end_time = time.strftime("%H:%M", time.localtime(time.time())),
                           date= d,
                           name_of_instrument= info[0],
                           serial= info[1],
                           immersion_depth=specs_t[5],
                           manufacturer=info[3],
                           model=info[4],
                           resolution=specs[2],
                           standards=info[5],
                           location=specs[4],
                           comments=self.ids.comments.text,
                           dcvoltage=table["dcv"],
                           acvoltage=table["acv"],
                           dccurrent=table["dcc"],
                           accurent=table["acc"],
                           resistance=table["resistance"],
                           diodes=table["diodes"],
                           frequency=table["frequency"],
                           temperature=table["temp"],
                           insulation=table["insulation"])
            
            outstanding.put(id, name=info[0],
                            customer = info[2],
                            date=d,
                            serial=info[1]) 
            
            self.parent.current = "info"

class BalanceScreen(WhiteScreen):
    asm = ObjectProperty()
    
class BalanceScreenManager(WhiteScreenManager):
    def __init__(self, *args, **kwargs):
        super(BalanceScreenManager, self).__init__(*args, **kwargs)
        self.transition = SlideTransition()
        self.instrument_info = []
        self.instrument_specs = []
        self.type = "balance"
    
    def change(self, s, title):
        self.parent.title.text = title
        self.current = s
        
    def calibrate(self):
        global balance
        specs = self.instrument_specs
        info = self.instrument_info
        id = "{}{}".format(datetime.date.today().strftime("%d%m%y"),
                                   info[1])
        
        balance.put(id,
                    name="balance",
                    serial=info[1],
                    customer=info[2],manufacturer=info[3],
                    model=info[4], _range=specs[0]+ "-" + specs[1],
                    resolution=specs[2], units=specs[3], location=specs[4],
                    date = datetime.date.today().strftime("%d/%m/%y"),
                    due = info[6],
                    end_time = datetime.datetime.now().strftime("%H:%M:%S"),
                    start_time= self.start_time,
                    procedure = "PG-02",
                    standard=info[5],
                    comments="",
                    warm_up_nomial = self.cold_mass,
                    nominal_mass = self.cold,
                    settling_time= self.settling,
                    off_center_mass = self.off_center_mass,
                    before_nominal = self.before_nominal,
                    before_actual = self.before_actual,
                    before_up = self.before_up,
                    after_up = self.after_up,
                    after_down = self.after_down,
                    after_uup = self.after_uup,
                    tare = self.tare,
                    tare_indicated = self.tare_indicated,
                    repeat_half = self.repeat_half,
                    repeat_full = self.repeat_full,
                    off_center = self.off
                    )
        print(balance.get(id))
        outstanding.put(id,
                        name=info[0],
                        customer=info[2],
                        date=datetime.date.today().strftime("%d/%m/%Y"),
                        serial=info[1])
        
      
        
class BalanceCalibrationScreen(WhiteScreen):
    def __init__(self, *args, **kwargs):
        super(BalanceCalibrationScreen, self).__init__(*args, **kwargs)
        self.readings = []
        self.count = 0
        
    def clear(self):
        self.count = 0
        if isinstance(self.readings, list):
            self.readings = []
            self.ids.table.table.clear_widgets()
        else:
            for i in self.readings: self.readings[i] = []
            self.ids.table.clear_widgets()
          
    def clear_last(self):
        if self.count > 0:
            self.count -= 1    
            
            if isinstance(self.readings, list):
                l = len(self.readings) - 1
                self.readings = self.readings[:l]
                self.ids.table.table.clear_widgets()
                self.ids.table.table.add_widget(numbered_table("Value", self.readings))
            else:
                headings = []
                for i in self.readings:
                    l = len(self.readings[i]) - 1
                    self.readings[i] = self.readings[:l]
                    self.headings.append(i)
                self.ids.table.clear_widgets()
            
        
        

                
    def record(self, val):
        self.count += 1
        if self.count > 10:
            print("too many values")
        else:
            self.readings.append(val)
            self.ids.table.table.clear_widgets()
            self.ids.table.table.add_widget(numbered_table("Cold Value", self.readings))
    def next_up(self):
        '''used to abstract class specific features'''
        self.ids.table.table.clear_widgets()    
    
    def next(self):
        if self.count < 5:
            p = Popup(title="Warning!", content = Label(text="Too Few values"),
                  size_hint=(None, None), size=(300, 150))
            p.open()
        else:
            self.parent.transition_direction = "left"
            self.next_up()
            
            try:
                for i in self.readings:
                    self.readings[i] = []
            except:
                self.readings = []
                
    def previous(self, screen, title):
        self.parent.transition.direction = 'right'
        self.parent.change(screen, title)
                       
class ColdStart(BalanceCalibrationScreen):
    def next_up(self):
        self.parent.start_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.parent.cold = "|".join(self.readings)
        self.parent.cold_mass = self.ids.mass.val.text
        self.parent.change("settling", "Settling Time")
        
    def previous(self):
        pass
    
    def record(self):
        super(ColdStart, self).record(self.ids.cold_value.text)

class SettlingTime(BalanceCalibrationScreen):
    def next_up(self):
        self.parent.settling = "|".join(self.readings)
        self.parent.change("linearityup", "Linearity Up")
            
    def record(self):
        super(SettlingTime, self).record(self.ids.settling_value.text)

    def previous(self):
        BalanceCalibrationScreen.previous(self, "cold", "Cold Start")
class LinearityUp(BalanceCalibrationScreen):
    def __init__(self, *args, **kwargs):
        global standards
        super(LinearityUp, self).__init__(*args, **kwargs)
        #get the nominal and actual values
        self.readings = {"nominal": [], "actual":[], "up": []}
    
    
    def clear_last(self):
        if self.count > 0:
            
            l = len(self.readings["nominal"])-1
            for i in self.readings:
                self.readings[i] = self.readings[i][:l]
            
            
            self.count -= 1
            self.ids.table.clear_widgets()
            self.ids.table.add_widget(table(["nominal", "actual", "up"], self.readings))       
    
    def next_up(self):
            self.parent.before_nominal = "|".join(self.readings["nominal"])
            self.parent.before_up = "|".join(self.readings["up"])
            self.parent.before_actual = "|".join(self.readings["actual"]) 
            self.parent.change("linearity", "Linearity")
            self.ids.table.clear_widgets()
            self.readings = {"nominal": [], "actual":[], "up": []}

    def previous(self):
        BalanceCalibrationScreen.previous(self, "settling", "Settling Time")
    def record(self):
        nominal = self.ids.nominal_value.val.text
        up = self.ids.linearity_value.val.text
        self.standards = standards.get(self.parent.instrument_info[5])
        self.std_nominal = self.standards["nominal"].split("|")
        self.std_actual = self.standards["actual"].split("|")
        if self.count > 5:
            return
        elif nominal not in self.std_nominal:
            p = Popup(title="Warning!", content = Label(text="Incorrect "
                                                "Nominal value for given standard\n"
                                                "These are available: {}".format(
                                                ", ".join(self.std_nominal))),
                  size_hint=(None, None), size=(400, 200))
            p.open()
        else:
            self.count += 1 
            self.readings["nominal"].append(nominal)
            self.readings["up"].append(up)
            #get the corresponding value of actual to nominal
            self.readings["actual"].append(self.std_actual[
                                            self.std_nominal.index(
                                                nominal)])
            self.ids.table.clear_widgets()
            self.ids.table.add_widget(table(["nominal", "actual", "up"], self.readings))

class Linearity(BalanceCalibrationScreen):
    def __init__(self, *args, **kwargs):
        super(Linearity, self).__init__(*args, **kwargs)
        self.readings = {"Linearity Up" : [],
                          "Linearity Down" : [],
                           "Linearity up" : []}
    def next_up(self):
        self.parent.after_up="|".join(self.readings["Linearity Up"])
        self.parent.after_uup="|".join(self.readings["Linearity up"])
        self.parent.after_down="|".join(self.readings["Linearity Down"])
        self.parent.change("taring", "Taring Linearity")
        self.ids.table.clear_widgets()
        self.readings = {"Linearity Up" : [],
                          "Linearity Down" : [],
                           "Linearity up" : []}

    def previous(self):
        BalanceCalibrationScreen.previous(self, "linearityup", "Linearity(before calibration)")        
    def clear_last(self):
        if self.count > 0:
            if self.count < 5:
                l = len(self.readings["Linearity Up"]) -1
                self.readings["Linearity Up"] = self.readings["Linearity Up"][:l]
            
            elif self.count > 5 and self.count < 10:
                l = len(self.readings["Linearity Down"]) -1
                self.readings["Linearity Down"] = self.readings["Linearity Down"][:l]
            
            elif self.count > 10 and self.count <= 15:
                l = len(self.readings["Linearity up"]) -1
                self.readings["Linearity up"] = self.readings["Linearity up"][:l]
            
            else:
                return
            self.count -= 1
            self.ids.table.clear_widgets()
            self.ids.table.add_widget(horizontal_table(["Linearity Up", "Linearity Down", "Linearity up"],
                                                          self.readings))
        
    def record(self):
        val = self.ids._value.val.text
        self.count += 1
        if self.count <= 5:
            self.ids._value.name = "Linearity Up"
            self.readings["Linearity Up"].append(val)
            
        elif self.count > 5 and self.count <= 10:
            self.ids._value.name = "Linearity Down"
            self.readings["Linearity Down"].append(val)
            
        elif self.count > 10 and self.count <= 15: 
            self.ids._value.name = "Linearity up"
            self.readings["Linearity up"].append(val)
        
        else: 
            return
            
        self.ids.table.clear_widgets()
        self.ids.table.add_widget(table(["Linearity Up", "Linearity Down", "Linearity up"],
                                                          self.readings))  
class TaringLinearity(BalanceCalibrationScreen):
    def __init__(self, *args, **kwargs):
        super(TaringLinearity, self).__init__(*args, **kwargs)
        self. readings = {"Tare": [],
                          "Indicated": []}
    def clear(self):
        self.count = 0
        for i in self.readings: self.readings[i] = []
        self.ids.table.table.clear_widgets()
    
    def clear_last(self):
        if self.count > 0:
            for i in self.readings:
                l = len(self.readings[i]) -1
                self.readings[i] = self.readings[i][:l]
            self.ids.table.table.clear_widgets()
            self.ids.table.table.add_widget(table(["Tare", "Indicated"], self.readings))
            self.count -= 1
    def record(self):
        tare = self.ids.tare_value.val.text
        indicated =self.ids.nominal_value.val.text
        self.count += 1
        if self.count > 5:
            return
        else:
            self.readings["Tare"].append(tare)
            self.readings["Indicated"].append(indicated)
            self.ids.table.table.clear_widgets()
            self.ids.table.table.add_widget(table(["Tare", "Indicated"], self.readings))
    
    def previous(self):
        BalanceCalibrationScreen.previous(self, "linearity", "Linearity(after calibration)")

    def next_up(self):
        self.parent.tare = "|".join(self.readings["Tare"])
        self.parent.tare_indicated = "|".join(self.readings["Indicated"])
        self.parent.change("repeat", "Repeatability")
        self. readings = {"Tare": [],
                          "Indicated": []}
        self.ids.table.table.clear_widgets()

class Repeatability(BalanceCalibrationScreen):
    def __init__(self, *args , **kwargs):
        super(Repeatability, self).__init__(*args, **kwargs)
        self.readings = {"1/2 Load":[],
                         "Full Load": []}
    
    def clear(self):
        self.count = 0
        for i in self.readings: self.readings[i] = []
        self.ids.table.table.clear_widgets()
          
    def next_up(self):
        self.parent.repeat_half = "|".join(self.readings["1/2 Load"])
        self.parent.repeat_full = "|".join(self.readings["Full Load"])
        self.parent.change("off", "Off Center Test")
        self.readings = {"1/2 Load":[],
                         "Full Load": []}
        self.ids.table.table.clear_widgets()
    
    def previous(self):
        BalanceCalibrationScreen.previous(self, "taring", "Taring Linearity")
 
    def clear_last(self):
         if self.count > 0:
             if self.count < 5:
                 l = len(self.readings["1/2 Load"]) - 1
                 self.readings["1/2 Load"] = self.readings["1/2 Load"][:l] 
             
             elif self.count > 5 and self.count <= 10:
                 l = len(self.readings["Full Load"]) - 1
                 self.readings["Full Load"] = self.readings["Full Load"][:l]
             
             self.count -= 1
             self.ids.table.table.clear_widgets()
             self.ids.table.table.add_widget(table(["1/2 Load", "Full Load"],
                                               self.readings))
    def record(self):
        val = self.ids._value.val.text
        self.count += 1
        if self.count <= 5:
            self.ids._value.name = "1/2 Load"
            self.readings["1/2 Load"].append(val)
            
        elif self.count > 5 and self.count <= 10:
            self.ids._value.name = "Full Load"
            self.readings["Full Load"].append(val)
            
        else:
            return
            
        self.ids.table.table.clear_widgets()
        self.ids.table.table.add_widget(table(["1/2 Load", "Full Load"],
                                               self.readings))
        
class OffCenter(BalanceCalibrationScreen):
    def __init__(self, *args, **kwargs):
        super(OffCenter, self).__init__(*args, **kwargs)
        self.readings = []
        self.count = 0
    
    def clear_last(self):
        self.count -= 1
        l = len(self.readings) - 1
        self.readings = self.readings[:l]
        self.ids.table.table.clear_widgets()
        self.ids.table.table.add_widget(numbered_table("Reading at", self.readings))

    def next(self):
        pass
    
    def previous(self):
        BalanceCalibrationScreen.previous(self, "repeat", "Repeatability")
    def record(self):
        val = self.ids._value.text
        self.count += 1
        if self.count > 5:
            print("Too many values")
        else:
            self.readings.append(val)
            self.ids.table.table.clear_widgets()
            self.ids.table.table.add_widget(numbered_table("Reading at", self.readings))
    
    
         
    def submit(self):
        if self.count < 5:
            p = Popup(title="Warning!", content = Label(text="Too Few values"),
                  size_hint=(None, None), size=(300, 150))
            p.open()
        else:
            
            self.ids.table.table.clear_widgets()
            self.parent.off = ":".join(self.readings)
            print(self.parent.off)
            self.readings = []
            self.parent.off_center_mass = self.ids.off.val.text
            self.parent.calibrate()
            self.parent.asm.current = "cold" 
def table( data=[], values= {}):
    layout = GridLayout(cols = len(data))
    l = longest(values)
    
    for column in data:
        layout.add_widget(Heading(text=column,
                                font_size= 20 ))
    index = 0
    while index < l:
        for column in data:
            if index  > (len(values[column]) - 1):
                layout.add_widget(Label(text="",size_hint=(None, None) ,size=(75, 50)))
            
            else:
                if index == 0  or index % 2 == 0:
                    layout.add_widget(Cell(text=(values[column][index])))
                else:
                    layout.add_widget(AltCell(text=(values[column][index])))
        index += 1
    return layout


def horizontal_table( data=["Instrument", "Customer", "Date", "Serial"], values= {"Instrument": ["Pressure Guage", "Balance", "Thermometer"],
                                                  "Customer": ["Delta", "Delta", "Coca Cola"],
                                                  "Date": ["16/5/16", "16/5/16", "16/5/16"],
                                                  "Serial": ["123", "456", "789"]}):
    layout = GridLayout(rows = len(data))
    for i in range(len(data)):
        row = data[i]
        l = longest(values)
        index = 0
        layout.add_widget(Heading(text=row,
                                font_size= 20 ))
        while index < l:
            if index  > (len(values[row]) - 1):    
                layout.add_widget(Label(text="",size_hint=(None, None) ,size=(75, 50)))
            
            else:    
                if i == 0 or i % 2 == 0:    
                    layout.add_widget(LinCell(text=values[row][index]))
                else:
                    layout.add_widget(LinAltCell(text=values[row][index]))
            index += 1
    
    return layout

def numbered_table(heading = "reading", values = ["Un", "Deux", "Trois"]):
    layout = GridLayout(cols= 2)
    layout.add_widget(Heading(text="Reading #",
                                font_size= 20 ))
    layout.add_widget(Heading(text=heading,
                                font_size= 20 ))
    for i in range(len(values)):
        if i == 0 or i % 2 == 0:
            layout.add_widget(Cell(text=str(i+1)))
            layout.add_widget(Cell(text=values[i]))
        
        else:
            layout.add_widget(AltCell(text=str(i+1)))
            layout.add_widget(AltCell(text=values[i]))
                              
    return layout

def longest(d):
    long = 0
    for key in d:
        if len(d[key]) > long:
            long = len(d[key])
    return long

def readings_combined(d):
    print("input ", d)
    if len(d) == 3:
        l = len(d["applied"])
        compressed = []
        i = 0
        while i < l:
            app = d["applied"][i]
            cal = d["calculated"][i]
            ind = d["indicated"][i]
            i += 1
            compressed.append(str(app) + ":" + str(cal) + ":" + str(ind))
    else:
        l=len(d["indicated"])
        compressed = []
        i = 0
        while i < l:
            ind = d["indicated"][i]
            act = d["actual"][i]
            i += 1
            compressed.append(str(ind) + ":" + str(act))
    print(compressed)
    return ";".join(compressed)
        

def http_format_args(d):
    result = "?"
    for i in d:
        result += i + "=" + d[i] + "&"
        
    return result[:len(result)- 1]
if __name__ == "__main__":
    DataApp().run()