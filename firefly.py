from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from secrets import username, password
from datetime import date

class FireflyBot:

    def __init__(self):
        print("Starting up...")
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(options=options)
        self.login()
        self.tasks = self.get_tasks()
        self.tasks_text = self.convert_tasks_to_text()
    
    def login(self):
        self.driver.get("https://firefly.etoncollege.org.uk/")

        print("Logging in...")
        username_field = self.driver.find_element_by_xpath('//*[@id="username"]')
        username_field.send_keys(username)

        password_field = self.driver.find_element_by_xpath('//*[@id="password"]')
        password_field.send_keys(password)

        login_button = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/button')
        login_button.click()
    
    def get_tasks(self):
        print("Getting tasks...")
        self.driver.get("https://firefly.etoncollege.org.uk/set-tasks#ms=All&p=1&ps=All&sb=DueDate&smss=All&so=Descending&sp=Todo&srs=All&ss=Active")
        sleep(1) # Gives time for page to load
        tasks = self.driver.find_elements_by_class_name("css-cyrcyp") # These are the task blocks
        return tasks

    def convert_tasks_to_text(self):
        tasks_text = [x.text.split('\n')[0] for x in self.tasks]
        return tasks_text

    def display_tasks_todo(self):
        for num, task in enumerate(self.tasks_text, start=1):
            print(num, task)

    def take_instructions(self):
        while True:
            userinput = int(input("Enter a command:\n1. Mark as done\n2. Set a personal task\n"))
            if userinput == 1 or 2:
                break
        if userinput == 1:
            while True:
                print("Select a task to mark as done: \n")
                self.display_tasks_todo()
                userinput = int(input())
                if 1 <= userinput <= len(self.tasks):
                    break
            self.mark_as_done(userinput-1)
        elif userinput == 2:
            self.set_personal_task()
    
    def mark_as_done(self, taskIndex):
        url = self.tasks[taskIndex].find_element_by_tag_name("a").get_attribute("href")
        self.driver.get(url)
        button = self.driver.find_element_by_xpath("//*[@id='the-page']/div[1]/div/main/section/div/div/div[2]/div/div/div[1]/div/div/button[2]")
        button.click()
    
    def set_personal_task(self):

        make_task = self.driver.find_element_by_class_name("css-1xn0sn7")
        make_task.click()

        task_title = self.driver.find_element_by_css_selector('input[name="personalTask.title"]')
        userinput = input("Enter the name for your task: \n")
        task_title.send_keys(userinput)

        pick_date = self.driver.find_element_by_class_name("ff_module-date-picker-jumpto__cal")
        pick_date.click()
        sleep(1) # keep

        pick_date_day = self.driver.find_element_by_link_text(date.strftime(date.today(), '%d'))
        pick_date_day.click()

        userinput = input("When is this task due? (dd/mm/yyyy)\n")
        due_date = self.driver.find_element_by_css_selector("input[name='personalTask.dueDate']")
        due_date.send_keys(Keys.CONTROL, "a", Keys.DELETE)
        due_date.send_keys(userinput)

        class_list = self.driver.find_element_by_css_selector('select[name="personalTask.class"]')
        class_list.click()

        class_name = self.driver.find_element_by_css_selector('option[value="no-class"]')
        class_name.click()

        userinput = input("Enter a description for the task (optional): \n")
        text_field = self.driver.find_element_by_css_selector("textarea[name='personalTask.description']")
        text_field.send_keys(userinput)

        button = self.driver.find_element_by_css_selector(".ff_module-button")
        button.click()
 
 



