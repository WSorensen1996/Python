#Lav noget der kan deles
"""
A Workflow App using the DCR Active Repository

TODO:
    0) Fill in the template and make sure you understand how it works
    1) Make the app show only enabled-or-pending activities - and it shows an exclamation mark (!) After a pending activity
    2) When there are no more enabled-or-pending activities it deletes the simulation id.
    3) Extra: Add a button to delete the simulation in the "Instance window".

"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import json 
import httpx
import helloworld.services.database_connection as dbc
from helloworld.email_config import * 
import re
import xml.etree.ElementTree as ET
import pandas as pd 

class WorkflowApp(toga.App):

    def startup(self):
        self.sim_id = -1
        self.graph_id=1329738  # change to your own graph id
        self.simulationwindow=0

        login_box = toga.Box(style=Pack(direction=COLUMN))
        login = toga.Button(
            'Login kiropraktor',
            on_press=self.show_Chiropractor_window,
            style=Pack(padding=5)
        )
        user_login = toga.Button(
            'Login som patient',
            on_press=self.show_login_window_user,
            style=Pack(padding=5)
        )
        login_box.add(login, user_login)

        

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = login_box
        self.main_window.show()


    def show_login_window_user(self, widget):
        self.login2_window = toga.Window(title='Login')
        self.windows.add(self.login2_window)
        login_box = toga.Box(style=Pack(direction=COLUMN))
        username_box = toga.Box(style=Pack(direction=ROW, padding=5))
        username_box = toga.Box(style=Pack(direction=ROW, padding=5))
        user_label = toga.Label(
            'Bruger ID: ',
            style=Pack(padding=(0, 10))
        )
        self.user_input = toga.TextInput(style=Pack(flex=1), placeholder='Enter dit bruger ID: ', value='') # hint use "value = your email" to not have to retype it all the time
        self.email = self.user_input.value
        username_box.add(user_label)
        username_box.add(self.user_input)
        login_button = toga.Button(
            'Vis historiske behandlinger',
            on_press=self.show_tidligere_behandling,
            
            
            style=Pack(padding=5)
        )
        login_box.add(username_box)
        login_box.add(login_button)
        
        self.login2_window.content = login_box
        self.login2_window.show()


    def show_Chiropractor_window(self, widget):
        self.second_window = toga.Window(title='Login')
        self.windows.add(self.second_window)
        login_box = toga.Box(style=Pack(direction=COLUMN))

        username_box = toga.Box(style=Pack(direction=ROW, padding=5))
        user_label = toga.Label(
            'Brugernavn: ',
            style=Pack(padding=(0, 10))
        )
        self.user_input = toga.TextInput(style=Pack(flex=1), placeholder='enter your DCR email', value='fkh456@alumni.ku.dk') # hint use "value = your email" to not have to retype it all the time
        username_box.add(user_label)
        username_box.add(self.user_input)

        password_box = toga.Box(style=Pack(direction=ROW, padding=5))
        passwd_label = toga.Label(
            'Kodeord: ',
            style=Pack(padding=(0, 10))
        )
        self.password_input = toga.PasswordInput(style=Pack(flex=1),value='NNCC9di4ndiN9W5')
        password_box.add(passwd_label)
        password_box.add(self.password_input)

        login_button = toga.Button(
            'Login',
            on_press=self.login,
            style=Pack(padding=5)
        )

        login_box.add(username_box)
        login_box.add(password_box)
        login_box.add(login_button)
        
        self.second_window.content = login_box
        self.second_window.show()


    def show_tidligere_behandling(self,widget):
        print(self.user_input.value)
        self.login2_window.close()
        Diagnostic_tableText = dbc.getDiagnosticResults(self.user_input.value, id=True)
        Behandling_tableText = dbc.getBehandlingsResults(self.user_input.value , id=True )
        self.informationpopupbox(Diagnostic_tableText+Behandling_tableText, self.user_input.value)

    def logout(self, widget): 
        self.sim_id = -1
        self.main_window.close()
        self.startup()


    async def getSims(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://repository.dcrgraphs.net/api/graphs/{self.graph_id}/sims",
                                        auth=(self.user_input.value, self.password_input.value))

        root = ET.fromstring(response.text)
        self.sims = {}
        self.username = self.user_input.value
        self.password = self.password_input.value
        dbc.db_connect()
        role = dbc.execute_query(dbc.getsqlstring("selectAll"))
        allroles = role.fetchall()
        self.allrolesdict = {}
        for id,email,rolle,behandling in allroles: 
            self.allrolesdict[str(id)] = email

        self.attrids = []
        for s in root.findall("trace"):

            try: 
                name = self.allrolesdict[s.attrib['id']]
            except:
                name = s.attrib['id']

            self.sims[s.attrib['id']] = name 



    async def login(self, widget):
        await self.getSims()

        self.second_window.close()
        self.show_sim_list()
        
    def show_sim_list(self):
        container = toga.ScrollContainer(horizontal=False,)
        sims_box = toga.Box(style=Pack(direction=COLUMN))
        logout = toga.Button(
            'LOG UD',
            on_press=self.logout,
            style=Pack(padding=5)
        )
        sims_box.add(logout)

        container.content = sims_box
        for id, name in self.sims.items():
            g_button = toga.Button(
                label = name,
                on_press=self.show_enabled_activities,
                style=Pack(padding=5),
                id = id
            )
            sims_box.add(g_button)
        self.newinstanceinput = toga.TextInput(style=Pack(flex=1), placeholder='Patient email', value='')
        


        g_button = toga.Button(
                "Opret patient",
                on_press=self.create_show_enabled_activities,
                style=Pack(padding=5)
        )

        create_box = toga.Box(style=Pack(direction=ROW, padding=5))
        create_box.add(self.newinstanceinput)
        create_box.add(g_button)
        sims_box.add(create_box)

        del_box = toga.Box(style=Pack(direction=ROW, padding=5))
        items = list([" "])
        for id in self.sims:
            try: 
                items.append(self.allrolesdict[id])
            except:
                items.append(id)
        print(type(items),type(items[1]))
        self.del_input = toga.Selection(style=Pack(padding=5),items = items)
    
        del_button = toga.Button(
                "Slet patient",
                on_press=self.del_instance,
                style=Pack(padding=5))
        del_box.add(self.del_input, del_button)
        sims_box.add(del_box)

        self.main_window.content = container


    async def del_instance(self, widget):
        print('self.del_input.value', self.del_input.value)

        self.actWindow = False
        if self.sim_id!=-1: 
            del_val = self.sim_id
            self.actWindow = True
    
        else: 
            try: 
                del_val = int(self.del_input.value)
            except: 
                del_val = self.del_input.value 
                test = {i for i in self.allrolesdict if self.allrolesdict[i]==del_val}
                del_lst = list(test) 
                if len(del_lst)==1: 
                    del_val = del_lst[0]
                else: 
                    print('DELETE LIST WAS EMPTY - check your spelling! ')
                    print('list(test)', del_lst)


        print('del_val',del_val)
        print('self.actWindow', self.actWindow)

        url = f"https://repository.dcrgraphs.net/api/graphs/{self.graph_id}/sims/{int(del_val)}"
        async with httpx.AsyncClient() as client:
            await client.delete(url,auth=(self.user_input.value, self.password_input.value))
        

        if self.actWindow: 
            self.activities_window.close()
            
        await self.getSims()
        self.show_sim_list()


    async def show_enabled_activities(self, widget):
        self.sim_id = widget.id
        self.userEmail = widget.label
        enabled_events = await self.get_enabled_events()
        root = ET.fromstring(enabled_events.json())
        events = root.findall('event')
        self.show_activities_window(events)

    async def create_show_enabled_activities(self, widget):
        def isValid(email):
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if re.fullmatch(regex, email):
                return True
            else:
                return False

        if isValid(self.newinstanceinput.value): 


            async with httpx.AsyncClient() as client:
                response = await client.post(f"https://repository.dcrgraphs.net/api/graphs/{self.graph_id}/sims",
                                            auth=(self.username, self.password))

            self.sim_id = response.headers['simulationid']


            userInformation = dbc.getInstanceFromDB(self.newinstanceinput.value)
            

            if userInformation == []:
                # If not exists -> create new db user
                res = dbc.insertNewInstanceInDB(self.sim_id, self.newinstanceinput.value)
                userInformation = (self.newinstanceinput.value, 'Patient', 'test')
                if res is None: 
                    print('Succesfully instered into DB!')
                    self.userEmail = self.newinstanceinput.value
                    send_welcome_email(self.newinstanceinput.value, self.sim_id) 
            else: 
                # If exists but not an  instance -> creating new UID 
                res = dbc.updateUid(self.sim_id, self.newinstanceinput.value)
                self.userEmail = self.newinstanceinput.value
                print('Succesfully updated DB!')

            enabled_events = await self.get_enabled_events()
            root = ET.fromstring(enabled_events.json())
            events = root.findall('event')
            self.show_activities_window(events)
        else: 
            print('Email invalid ')


    def show_activities_window(self, events):
        self.activities_window = toga.Window(title=f'Bruger: {self.userEmail}',on_close=self.closeCallback)
        self.simulationwindow=1
        self.windows.add(self.activities_window)
        self.log = []
        self.update_activities_box(events)
        self.activities_window.show()


    async def closeCallback(self, widget):
        self.sim_id = -1
        self.activities_window.close()
        await self.getSims() 
        self.show_sim_list()

    async def execute_activity(self, widget):
        
        description = False
        try: 
            if self.description_text.value != '': 
                description = self.description_text.value
        except: 
            pass

        
        if description is not False: 
            _log = ','.join(self.log)
            self.log = []
            if widget.id == 'Activity11': #  diagnosticeringsresulater
                dbc.insertDiagnostic(self.sim_id, self.userEmail ,_log,   description)

            elif widget.id == 'Activity16':   # Behandlingsresultater
                dbc.insertTreatment(self.sim_id ,self.userEmail, _log,  description)

        # Opslag lokalt - skal lave opslag i sql istedet 
        if widget.label not in ['Afslut behandlingsforløb', 'Ny diagnosticering', 'Nyt behandlingsforløb', 'Tidsbestilling', 'Patient opretter sig i system']: 
            self.log.append(widget.label)

        


        async with httpx.AsyncClient() as client:
            response = await client.post(f"https://repository.dcrgraphs.net/api/graphs/{self.graph_id}/sims/{self.sim_id}/events/{widget.id}",
            auth=(self.username, self.password))

        if len(response.text) == 0:
            enabled_events = await self.get_enabled_events()

        else:
            print(f'[!] {response.text}')
            return 
        if enabled_events:
            root = ET.fromstring(enabled_events.json())
            events = root.findall('event')
            self.update_activities_box(events)
        else:
            print("[!] No enabled events!")


    async def get_enabled_events(self):
        url = f"https://repository.dcrgraphs.net/api/graphs/{self.graph_id}/sims/{self.sim_id}/events?filter=only-enabled"
        async with httpx.AsyncClient() as client:
            return await client.get(url,  auth=(self.username, self.password))

    def informationpopupbox(self, tableText, _title): 
        self.popup_window = toga.Window(title = _title)
        self.windows.add(self.popup_window)
        table = toga.Box(style=Pack(direction=COLUMN))
        for idx , content in enumerate(tableText): 
            bruger_label = toga.Label(
                content ,
                style=Pack(padding=(10, 10))
            )
            table.add(bruger_label)


        self.popup_window.content = table
        self.popup_window.show()
    
    
    def setidligereBehandlinger(self, widget): 
        tableText = dbc.getBehandlingsResults(self.userEmail)
        print(tableText)
        self.informationpopupbox(tableText, 'Tidligere behandlinger')


    def setidligereDiagnosticeringer(self, widget): 
        tableText = dbc.getDiagnosticResults(self.userEmail)
        print(tableText)
        self.informationpopupbox(tableText, 'Tidligere diagnosticeringer')






    def update_activities_box(self, events):
        create_description_box = False
        payout_expenses = False
        window = toga.Box(style=Pack(direction=COLUMN))
        activities_box = toga.Box(style=Pack(direction=COLUMN))
        TotalExpenses = self.getTotalExpenses()



        Information_bar = toga.Box(style=Pack(direction=ROW))
        bruger_label = toga.Label(
            f'Bruger: {self.userEmail}' ,
            style=Pack(padding=(10, 10))
        )
        Information_bar.add(bruger_label)
        window.add(Information_bar)




        Status_bar = toga.Box(style=Pack(direction=ROW))
        status_button = toga.Label(
            f'Total udestående: {TotalExpenses}' ,
            style=Pack(padding=(10, 10))
        )
        Status_bar.add(status_button)
        diagnosticeringer_button = toga.Button(
            text='Se tidligere diagnosticeringer',
            on_press=self.setidligereDiagnosticeringer,
            style=Pack(padding=10),
        )
        Status_bar.add(diagnosticeringer_button)
        behndling_button = toga.Button(
            text='Se tidligere behandlinger',
            on_press=self.setidligereBehandlinger,
            style=Pack(padding=10),
        )
        Status_bar.add(behndling_button)




        _events=pd.DataFrame(columns=['label', 'id', 'sortVals'])
        for idx,e in enumerate(events):
            
            if e.attrib['label']=='Diagnosticerings resultat': 
                idx = -1
            if e.attrib['label']=='Payout of expense': 
                idx = 100
            if e.attrib['label']=='Afslut behandlingsforløb': 
                idx = 99
            _events.loc[len(_events)]=[e.attrib['label'],e.attrib['id'], idx]

        _events = _events.sort_values(by='sortVals')


        if len(events) >= 1:
            for idx,(label, id) in enumerate(zip(_events['label'].values,_events['id'].values )):

                if id == 'Activity16_1': # payout expenses button
                    payout_expenses = (label, id)
                    continue
                
                if id == 'Activity17': # Subprocess removal 
                    continue
                if id == 'Activity12': # Subprocess removal 
                    continue
                if id == 'Activity14': # Subprocess removal 
                    continue

                if id == 'Activity11': # Diagnosticeringsresultater
                    create_description_box = (label, id)
                    continue
                if id == 'Activity16': # Behandlingsresultater
                    create_description_box = (label, id)
                    continue
              
                e_button = toga.Button(
                    text=label,
                    on_press=self.execute_activity,
                    style=Pack(padding=5),
                    id=id,
                )
                activities_box.add(e_button)
        else:
            print("[!] No events to execute!")


        if create_description_box is not False:
            print('create_description_box',create_description_box)
            label , id = create_description_box
            self.description_text = toga.TextInput(
                style=Pack(flex = 1,  height=100, width=700),
                placeholder='Enter treatment description here: ', 
                value=''
                )
            description_button = toga.Button(
                    label,
                    on_press= self.execute_activity,
                    style=Pack(padding_top=10 ),
                    id=id
                    )
            desc_box = toga.Box(style=Pack(direction=COLUMN))
            desc_box.add(self.description_text)
            desc_box.add(description_button)
            desc_box.style.update(padding=30)
            activities_box.add(desc_box)


        if payout_expenses is not False:
            label, id = payout_expenses
            e_button = toga.Button(
                text=label,
                on_press=self.payoutExpenses,
                style=Pack(padding=10),
                id=id,
            )
            Status_bar.add(e_button)

        window.add(Status_bar)
        window.add(activities_box)

        self.activities_window.content = window



    def getTotalExpenses(self): 
        TotalExpenses = dbc.getTotalExpenses(self.userEmail)
        return TotalExpenses 


    async def payoutExpenses(self, widget):
        TotalExpenses = self.getTotalExpenses()
        send_payout_email(self.userEmail, TotalExpenses)

        await self.del_instance(widget)


def main():
    return WorkflowApp()
