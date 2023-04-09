"""
My first application
"""
import httpx
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import xmltodict



class HelloWorld(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        

        self.passwd_label = toga.Label(
            'Your name: ',
            style=Pack(padding=(0, 5))
        )
        self.passwd_input = toga.PasswordInput(style=Pack(flex=1))

        password_box = toga.Box(style=Pack(direction=ROW, padding=5))
        password_box.add(self.passwd_label)
        password_box.add(self.passwd_input)
        self.loginname = 'fkh456@alumni.ku.dk'
        self.graphid =  '1480016'

        button = toga.Button(
            'lav ny instans af graf',
            on_press=self.create_instance,
            style=Pack(padding=5)
        )

        #button = toga.Button(
          #  'Say Hello!',
          #  on_press=self.say_hello,
         #   style=Pack(padding=5)
        #)
        button2 = toga.Button(
            'vis mulige aktiviteter',
            on_press=self.show_enabledactivities,
            style=Pack(padding=5)
        )

        main_box.add(password_box)
        main_box.add(button)
        main_box.add(button2)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
    
    async def say_hello(self, widget):
       if self.name_input.value:
            name = self.name_input.value
       else:
            name = 'stranger'

       async with httpx.AsyncClient() as client:
            response = await client.get("https://jsonplaceholder.typicode.com/posts/42")

       payload = response.json()

       self.main_window.info_dialog(
            "Hello, {}".format(name),
            payload["body"],
         )

    async def create_instance(self, widget):

        async with httpx.AsyncClient() as client:

            response = await client.post("https://repository.dcrgraphs.net/api/graphs/"+self.graphid+"/sims",auth=(self.loginname,self.passwd_input.value))
            #print(response.headers)    

        self.simulationid = response.headers['simulationid']

        print("New simulation created with id:",self.simulationid)
    
    async def show_enabledactivities(self, widget):

        async with httpx.AsyncClient() as client:
            

            enabledevents = await client.get("https://repository.dcrgraphs.net/api/graphs/"+self.graphid+"/sims/"+self.simulationid+"/events?filter=only-enabled" ,auth=(self.loginname,self.passwd_input.value))

        eventsxml = enabledevents.text

        eventsxmlnoquote = eventsxml[1:len(eventsxml)-1]

        eventsxmlclean = eventsxmlnoquote.replace('\\\"', '\"')

        eventsjson = xmltodict.parse(eventsxmlclean)

        events = eventsjson['events']

        print("Enabled events")

        for e in events['event']:

             print (e['@label'])    


def main():
    return HelloWorld()
