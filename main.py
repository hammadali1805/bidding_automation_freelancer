from tkinter import  *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
from bs4 import BeautifulSoup
import time
import datetime

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

window_size = pyautogui.size()
width = window_size[0]
height = window_size[1]

root = Tk()
root.title("AutoBid")
root.geometry(f"700x950+{int(width*0.3)}+{int(height*0.02)}")

base_color = "#201e1e"

mainFrame = Frame(root, bg=base_color)
mainFrame.pack(fill = BOTH, expand=True)

username = StringVar()
password = StringVar()
noOfProjects = StringVar()
bidAmountType = StringVar()
bidMessageType = StringVar()
skill = StringVar()

bidMessage = """Hello Dear We have read your project description

We  have a team which will provide the best work including Frontend and Backend based on your project
We will deliver the best possible work

-> We are Experienced in Web and App  Development 
-> We have a dedicated team for WordPress 
-> We are experienced in HTML and CSS 3, PHP, JQUERY, MONGO DB , EXPRESS JS , REACT JS , NODE JS 
-> Expert in MERN Stack, PHP, PHP Laravel

       "" Regular communication is crucial to us, so let’s keep in touch! "" 

            Portfolio Samples

      -------------   Websites ----------
https://sacredshaadi.com
https://cloudnote.vercel.app

        -------------  Apps  -----------
https://play.google.com/store/apps/details?id=adnate.com.schoolqlik
https://drive.google.com/…"""

lastProject = ""

allSkills = {
    "All": 0,
    "PHP": 3,
    "Java": 7,
    "JavaScript":9,
    "Python": 13,
    "Graphic Design": 20,
    "Logo Design": 32,
    "Data Processing": 36,
    "Mobile App Development": 44,
    "AJAX": 51,
    "Vedio Services": 52,
    "Excel": 55,
    "Photoshop": 57,
    "iPhone": 58,
    "Android": 59,
    "CSS": 77,
    "Web scraping": 95,
    "Software Architecture": 116,
    "eCommerce": 137,
    "Video Upload": 198,
    "Photo Editting": 204,
    "NoSql Couch & Mongo": 287,
    "MySQL": 305,
    "HTML5": 323,
    "HTML": 335,
    "#D Animation": 395,
    "Database Administration": 472,
    "Node.js": 500,
    "Software Development": 613,
    "Laravel": 669,
    "Video Editting": 688,
    "Microsoft Sql Server": 695,
    "React.js": 759,
    "JASON": 901,
    "App Developer": 951,
    "Scripting": 1019,
    "Web Development": 1031,
    "Excel VBA": 1035,
    "Web Crawling": 1040,
    "2D Animation": 1063,
    "Frontend Development": 1093,
    "Charts": 1110,
    "Selenium Webdriver": 1112,
    "Animated Video Development":1415,
    "Microsoft Azure": 1610,
    "Social Video Marketting": 1625,
    "Svelte": 2029,
    "2D Animation Explainer Video": 2127,
    "Android App Development": 2158,
    "YouTube Video Editting": 2252
}


def freelancerLogin():
    browser = webdriver.Chrome(executable_path= "C:\\Users\\qadir\\OneDrive\\Desktop\\chromedriver.exe", options=chrome_options)
    browser.get("https://freelancer.com/login")
    browser.maximize_window()
    time.sleep(2)

    pyautogui.click(0.5*width, 0.6*height)
    pyautogui.typewrite(username.get())
    time.sleep(2)

    pyautogui.click(0.5*width, 0.7*height)
    pyautogui.typewrite(password.get())
    time.sleep(2)

    pyautogui.click(width*0.5, height*0.87)
    time.sleep(10)

    pyautogui.click(width*0.5, height*0.87)
    time.sleep(10)

    return browser

def getProject(browser):
    if skill.get() == "All":
        browser.get("https://freelancer.com/search/projects")
        time.sleep(5)
    else:
        browser.get(f"https://freelancer.com/search/projects?projectLanguages=en,hi&projectSkills={allSkills[skill.get()]}")
        time.sleep(5)

    try:
        #try clicking in view new projects
        browser.find_element(By.XPATH, '//fl-floating-action[@text="view new projects"]/fl-bit').click()
        print("here")
    except :
        pass

    soup = BeautifulSoup(browser.page_source, "html.parser")

    a_tags = soup.find_all("a")
    all_href = [ x.get("href") for x in a_tags if x.get("href")]
    temp_projects = [x for x in all_href if x.startswith("/projects/")] # has all projects twice

    project = temp_projects[0]

    return project

def getBidAmount(browser):

    try:
        if bidAmountType.get() == 'avg':
            BidAmountText = browser.find_element(By.XPATH, '//fl-text[@class="AveragePrice"]/div').text
        elif bidAmountType.get() == 'min':
            BidAmountText = browser.find_element(By.XPATH, '//fl-bit[@class="ProjectViewDetails-budget"]/fl-text/div').text.split('–')[0].split(".")[0]
        elif bidAmountType.get() == 'max':
            BidAmountText = browser.find_element(By.XPATH, '//fl-bit[@class="ProjectViewDetails-budget"]/fl-text/div').text.split('–')[1].split(".")[0]
    except:
        return None

    BidAmount = ''
    for x in BidAmountText:
        if x in '0123456789':
            BidAmount += x           
    
    BidAmount = int(BidAmount)
    return BidAmount


def bid(browser, bids):

    global lastProject

    project = getProject(browser)

    if project == lastProject:
        return bids

    bidStatus = ""

    project_url = "https://www.freelancer.com"+ project
    browser.get(project_url)
    time.sleep(5)

    try:
        text_box = browser.find_element(By.XPATH, '//textarea[@id="descriptionTextArea"]')
        if bidMessageType.get() == "default":
            text_box.send_keys(bidMessage)
        else:
            text_box.send_keys(textArea.get("1.0", END))

        time.sleep(2)

        if bidAmountType.get() != "phr" and getBidAmount(browser) != None :
            bidAmount = getBidAmount(browser)
            bidAmountInput = browser.find_element(By.XPATH, '//input[@id="bidAmountInput"]')
            bidAmountInput.send_keys(f"\b\b\b\b\b\b\b\b\b\b\b\b\b{bidAmount}")
            time.sleep(2)

        browser.find_element(By.XPATH, '//button[normalize-space()="Place Bid"]').click()
        time.sleep(5)

        try:
            browser.find_element(By.XPATH, '//fl-banner-upsell-small-title')
            bids += 1

            bidStatus = "Success"

            lastProject = project

        except:
            bidStatus = "Failed or Already Bid"

    except:
        bidStatus = "Failed or Already Bid"

    with open("logs.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}\n{project_url}\nStatus:{bidStatus}\n\n")

    
    with open("logs.txt", "r") as f:
        logs = f.read()
    textArea.delete("1.0", END)
    textArea.insert("1.0", logs)

    return bids

def startBidding():
    bids = 0
    browser = freelancerLogin()
    while int(noOfProjects.get()) != bids :
        bids = bid(browser, bids)
    browser.close()



Label(mainFrame, text="AutoBid", font="courier 22 bold", fg="white", bg=base_color).place(relx=0.05, rely=0.05, anchor="w")
Label(mainFrame, text="Bidding Made Easier", font="courier 10 bold", fg="grey", bg=base_color ).place(relx=0.05, rely=0.09, anchor="w")

Label(mainFrame, text="o Username/Email", font="times 16", fg="grey", bg=base_color).place(relx=0.05, rely=0.17, anchor="w")
usernameInput = Entry(mainFrame, font="times 16", textvariable=username, width=22)
usernameInput.place(relx=0.95, rely=0.17, anchor="e")
username.set("freelancers01hk@gmail.com")

Label(mainFrame, text="o Password", font="times 16", fg="grey", bg=base_color).place(relx=0.05, rely=0.23, anchor="w")
passwordInput = Entry(mainFrame, show="*",textvariable=password, font="times 16", width=22)
passwordInput.place(relx=0.95, rely=0.23, anchor="e")
password.set("3fYRk5AY4S6J3Kv")

Label(mainFrame, text="--------------------------", fg="grey", bg=base_color, font="times 10").place(relx=0.5, rely=0.29, anchor="center")

Label(mainFrame, text="o Number", font="times 16", fg="grey", bg=base_color).place(relx=0.05, rely=0.36, anchor="w")
noOfProjectsInput = Entry(mainFrame, font="times 16", textvariable=noOfProjects, width=3)
noOfProjectsInput.place(relx=0.95, rely=0.36, anchor="e")
OptionMenu(mainFrame, skill, *allSkills.keys()).place(relx=0.5, rely=0.36, anchor="center")
skill.set("All")
noOfProjects.set("10")

Label(mainFrame, text="--------------------------", fg="grey", bg=base_color, font="times 10").place(relx=0.5, rely=0.42, anchor="center")

Label(mainFrame, text="o Bid Amount", font="times 16", fg="grey", bg=base_color).place(relx=0.05, rely=0.46, anchor="w")
Radiobutton(mainFrame, text = "Avg", variable = bidAmountType ,value = "avg", font="times 14", fg="grey", bg=base_color).place(relx=0.355, rely=0.46, anchor='w')
Radiobutton(mainFrame, text = "Max", variable = bidAmountType ,value = "max", font="times 14", fg="grey", bg=base_color).place(relx=0.477, rely=0.46, anchor='w')
Radiobutton(mainFrame, text = "Min", variable = bidAmountType ,value = "min", font="times 14", fg="grey", bg=base_color).place(relx=0.597, rely=0.46, anchor='w')
Radiobutton(mainFrame, text = "Placeholder", variable = bidAmountType ,value = "phr", font="times 14", fg="grey", bg=base_color).place(relx=0.72, rely=0.46, anchor='w')
bidAmountType.set("avg")

Label(mainFrame, text="--------------------------", fg="grey", bg=base_color, font="times 10").place(relx=0.5, rely=0.52, anchor="center")

textArea = Text(mainFrame, font="times 10", height=10, width=60)

Label(mainFrame, text="o Bid Message", font="times 16", fg="grey", bg=base_color).place(relx=0.05, rely=0.57, anchor="w")
Radiobutton(mainFrame, text = "Default", variable = bidMessageType ,value = "default", font="times 16", fg="grey", bg=base_color, command=lambda: textArea.delete("1.0", END)).place(relx=0.5, rely=0.57, anchor='w')
Radiobutton(mainFrame, text = "Custom", variable = bidMessageType ,value = "Custom", font="times 16", fg="grey", bg=base_color, command=lambda: textArea.insert("1.0", "Enter your custom message here!") ).place(relx=0.95, rely=0.57, anchor='e')
bidMessageType.set("default")

Label(mainFrame, text="--------------------------", fg="grey", bg=base_color, font="times 10").place(relx=0.5, rely=0.635, anchor="center")

Button(mainFrame, text="Start Bidding", font="times 16", fg="black", bg="grey", command=startBidding).place(relx=0.5, rely=0.705, anchor='center')

textArea.place(relx=0.5, rely=0.99, anchor='s')

root.mainloop()