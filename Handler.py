import webapp2
import cgi
import re
from google.appengine.ext import db
from datetime import date

from BaseHandler import BaseHandler
from DataModels import Timetable
CACHE = {}
COLUMN_NUMBER = 8
#CACHE[store] = {"data":final_table, "create_time":date.today()}
#final_table[name] = data
#data = {Tue:xxx,Wed:xxx,...,Mon:xxx}

class CreateRoster(BaseHandler):
    def get(self):
        #first check whether login
        if self.request.cookies.get("username") == "authorized":
            self.render("CreateRoster.html")
        else :
            self.redirect("/unauthorized")
        # if not re-direct to error page
        # then re-direct to main page after 5 sec

        # if yes show the create Roster Page
            

    def post(self):
        #first check whether login

        #if check in 
        
        store = self.request.get("store_name")
        variables  = self.request.arguments()
        #string = ""
        time_table = {}
        for i in variables:
            if len(self.request.get(i)) == 0:
                continue
            time_table[i] = self.request.get(i)
        self.saveToCACHE(store,time_table)
        self.saveToDatabase()
        self.redirect("/")    

    def saveToDatabase(self):
        #
        for i in CACHE.keys():
            self.processData(i,CACHE[i]["data"])
        #
    def processData(self,store,table):
        #get all name in the store
        content = ""
        param = {}
        for name in table:
            # get all the date in the table
            for date in table[name].keys():
                #initialize 
                time = Timetable(store = store,
                                 weekday = date,
                                 name = name,
                                 work_info = table[name][date])
                time.put()
                content += store + ":" + date + ", " + name + ", " + table[name][date] + ";<br>"
                
    
    def saveToCACHE(self,store,table):
        #classify time_table
            #get the number of people
        final_table = {}
        number = len(table)/COLUMN_NUMBER
        #7day + name 
            #for i get Name_i, Tue_i
        for i in range(1,number + 1):
            name = table.get("Name_" + str(i))
            data = {}
            data["Tue"] = table["Tue_" + str(i)]
            data["Wed"] = table["Wed_" + str(i)]
            data["Thu"] = table["Thu_" + str(i)]
            data["Fri"] = table["Fri_" + str(i)]
            data["Sat"] = table["Sat_" + str(i)]
            data["Sun"] = table["Sun_" + str(i)]
            data["Mon"] = table["Mon_" + str(i)]                        
            #generate dict like {name:{Tue:...},..}
            final_table[name] = data
        #then save to CACHE
        CACHE[store] = {"data":final_table, "create_time":date.today()}
        
    
class Signin(BaseHandler):
    def get(self):
        self.render("Signin.html")

    def post(self):
        #author first 
        username = self.request.get("username")
        password = self.request.get("password")
        
        self.response.set_cookie(key = "username",value = "authorized")
        self.redirect("/createroster")
        
        #if mamanger:
        #    self.setCookie("Position","Manager")
        #    self.redirect("/createroster")
        #   
        #elif authorized:
        #    self.setCookie("Position","Other")
        #    self.redirect("/")
        #else:
        #    params = {"username":username}
        #    params["error_message"] = "You have not regist yet!Please go to sign up page to regesit."
        #    self.render("Signin.html",**params)

    
class MainPage(BaseHandler):
    def get(self):
        table_head = """
                <div><label>Create Time</label>%(create_time)s</div>
                <div><label>Store Name:</label>%(store_name)s</div> 
                <table id="time_table" align="left">
                  <tr>
                    <th scope="col" width="100">Name</th>
                    <th scope="col" width="100">Tue</th>
                    <th scope="col" width="100">Wed</th>
                    <th scope="col" width="100">Thu</th>
                    <th scope="col" width="100">Fri</th>
                    <th scope="col" width="100">Sat</th>
                    <th scope="col" width="100">Sun</th>
                    <th scope="col" width="100">Mon</th>
                  </tr>
                  """
        line = """<tr>
                    <th scope="row" width="100"> 
                    <input size="10" type="text" disabled="disabled" value="%(stuff_name)s"/></th>
                    <td><input size="10" type="text" disabled="disabled" value="%(Tue)s"/></td>
                    <td><input size="10" type="text" disabled="disabled" value="%(Wed)s"/></td>
                    <td><input size="10" type="text" disabled="disabled" value="%(Thu)s"/></td>
                    <td><input size="10" type="text" disabled="disabled" value="%(Fri)s"/></td>
                    <td><input size="10" type="text" disabled="disabled" value="%(Sat)s"/></td>
                    <td><input size="10" type="text" disabled="disabled" value="%(Sun)s"/></td>
                    <td><input size="10" type="text" disabled="disabled" value="%(Mon)s"/></td>
                  </tr>"""

        table = ""
        create_time = ""
        self.initial_cache()
        if len(CACHE.keys()) == 0:
            #first find the database
            
            #if not found
            self.render("MainPage.html", **{"time_table":"<b>No time_table have been created yet</b>",
                                            "time":"Not exsited"})
            return
        
        for store_name in CACHE.keys():
            create_time = CACHE[store_name]["create_time"]
            time_table = CACHE[store_name]["data"]
            table += table_head %  {"create_time":create_time,
                                    "store_name":store_name}
            for stuff_name in time_table.keys():
                time = time_table.get(stuff_name)
                table += line % {"stuff_name":stuff_name,
                        "Tue":time.get("Tue"),
                        "Wed":time.get("Wed"),
                        "Thu":time.get("Thu"),
                        "Fri":time.get("Fri"),
                        "Sat":time.get("Sat"),
                        "Sun":time.get("Sun"),
                        "Mon":time.get("Mon")}
            table += "</table>"
            
        self.render("MainPage.html",**{"time_table":table,
                                       "time":create_time})
            
    def initial_cache(self):
        if len(CACHE.keys) > 0:
            return True
        else:
            create_date_list = db.GqlQuery("select create_date from Timetable order by create_date desc")
            time = ""
            for i in create_date_list:
                time = i.create_date
                break
            recent_time_table = db.GqlQuery("select * from Timetable where create_date = " + time)
            if not recent_time_table:
                return False
            
            

