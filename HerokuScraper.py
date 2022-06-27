#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import cv2
import urllib3
from bs4 import BeautifulSoup
import pandas as pd

from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from pytesseract import image_to_string
import pytesseract

from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import base64


# In[33]:


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])


# In[2]:


KillSwitch = False


# In[3]:


Global_List = []
Global_header = []


# In[4]:


def toggleKillSwitch():
    global KillSwitch
    if(KillSwitch == False):
        KillSwitch = True


# In[5]:


def retry(data=["https://freesearchigrservice.maharashtra.gov.in/",'2022',"मुंबई उपनगर जिल्हा","Andheri","415"]):
    global KillSwitch
    print(" KillSwitch Status " + str(KillSwitch))
    if(KillSwitch == True):
        driver.close()
        return None
    if(len(driver.window_handles)==2):
        print("If Any Residual Tab was open it is closed now")
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    else:
        print(" No Residual Tabs ")
        
    url = data[0]
    year = data[1]
    District = data[2]
    AreaName = data[3]
    PropertyNo = data[4]
    automated_scraping_model(url,year,District,AreaName,PropertyNo)


# In[ ]:





# In[ ]:





# In[6]:


def autofill_captcha():
    img = driver.find_element(by = By.XPATH,value='//*[@id="imgCaptcha"]')
    # get the captcha as a base64 string
    img_captcha_base64 = driver.execute_async_script("""
        var ele = arguments[0], callback = arguments[1];
        ele.addEventListener('load', function fn(){
          ele.removeEventListener('load', fn, false);
          var cnv = document.createElement('canvas');
          cnv.width = this.width; cnv.height = this.height;
          cnv.getContext('2d').drawImage(this, 0, 0);
          callback(cnv.toDataURL('image/jpeg').substring(22));
        }, false);
        ele.dispatchEvent(new Event('load'));
        """, img)

    # save the captcha to a file
    with open(r"captcha.jpg", 'wb') as f:
        f.write(base64.b64decode(img_captcha_base64))
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    config = ('-l eng --oem 1 --psm 3')
    #im = Image.open('screenshot.png')
    im = cv2.imread('captcha.jpg', cv2.IMREAD_COLOR)
    text = pytesseract.image_to_string(im, config=config)
    captcha = driver.find_element(by=By.ID,value='txtImg')
    captcha.send_keys(text)


# In[7]:


def waitfortab(timeout = 10):
    global KillSwitch
    handles_before = driver.window_handles
    wait = 0
    while (len(driver.window_handles)!=2):
        if(wait >= 15):
            print("Website Too Slow/Unresponsive to Scrape Any Data \n Kindly Run the Program Later \n")
            toggleKillSwitch()
            print(" KillSwitch Status " + str(KillSwitch))
            break
        print("Waiting for Feedback Tab To Open")
        time.sleep(5)
        wait +=5


# In[8]:


# Works Well
def open_site(url):
    driver.get(url)


# In[9]:


# Works Well

def enter_data(Year,District,AreaName,Propery_Number):
    global KillSwitch
    try:
        close_button = driver.find_element(By.XPATH, value ="//*[@id='popup']/div/a")
        close_button.click()
        Year = Select(driver.find_element(By.ID,value = "ddlFromYear"))
        Year.select_by_visible_text('2022')
        Disctrict = Select(driver.find_element(By.ID,value = "ddlDistrict"))
        Disctrict.select_by_visible_text("मुंबई उपनगर जिल्हा")
        Temp_click_button = driver.find_element(By.ID,value = "txtAreaName")
        Temp_click_button.click()
        time.sleep(5)
        Enter_Village_Name = driver.find_element(By.ID,value = "txtAreaName")
        Enter_Village_Name.send_keys("Andheri")
        Temp_click_button = driver.find_element(By.ID,value = "ddlareaname")
        Temp_click_button.click()
        time.sleep(5)
        Select_Village = Select(driver.find_element(By.ID,value = "ddlareaname"))
        Select_Village.select_by_visible_text("Andheri")
        Property_Name = driver.find_element(By.ID,value = "txtAttributeValue")
        Property_Name.send_keys(415)
        autofill_captcha()
        #time.sleep(20) # Enter Captcha Twice Manually
        Search_Button = driver.find_element(By.ID,value="btnSearch")
        Search_Button.click()
        time.sleep(12)
        autofill_captcha()
        Search_Button = driver.find_element(By.ID,value="btnSearch")
        Search_Button.click()
        time.sleep(25)
    except NoSuchElementException:
        print("Some Error Occured in Searching, Retrying the Entire Operation")
        print(" KillSwitch Status " + str(KillSwitch))
        if(KillSwitch == True):
            return None
        else:
            retry(data)
    except TypeError:
        print("Temporary Broswer Issue, Retrying \n")
        print(" KillSwitch Status " + str(KillSwitch))
        if(KillSwitch == True):
            return None
        else:
            retry(data)


# In[10]:


# Works Well
def close_popup():
    global KillSwitch
    try:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except IndexError:
        if(KillSwitch == True):
            return None
        else:
            retry(data)


# In[11]:


# Works Well
def get_headers(required_table):
    global Global_List
    global Global_header
    driver.switch_to.window(driver.window_handles[0])
    header1 = []
    row = []

    # Headers 

    for i in range(0,len(required_table.findAll('th'))):
    
        header1.append(required_table.findAll('th')[i].decode_contents())

    button = driver.find_element(By.XPATH,value='//*[@id="RegistrationGrid"]/tbody/tr['+str(2)+']/td[10]/input')
    button.click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    soup1 = BeautifulSoup(driver.page_source, 'html.parser')
    index2_table = soup1.find('table',attrs={'class':'tblmargin'})
    for j,index2_tr in enumerate(index2_table):
        header2 = []
        for index2_td in index2_tr.findAll('td',attrs={'width':'30%'}):
            for font in index2_td.findAll('font'):
                header2.append(font.decode_contents())

        header = header1+header2
        #print(header)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    header.append("PageNo")
    print(header)
    Global_List.append(header)
    Global_header = header1
    return header
    


# In[12]:


def get_index2_headers(index2_table):
    for j,index2_tr in enumerate(index2_table):
        header2 = []
        for index2_td in index2_tr.findAll('td',attrs={'width':'30%'}):
            for font in index2_td.findAll('font'):
                header2.append(font.decode_contents())
        header = header2
        #print(header)
        #driver.close()
        #driver.switch_to.window(driver.window_handles[0])
    #print(header)
    return header


# In[13]:


# Works Well
def standalonerun(required_table):
    row = []
    if(len(required_table.findAll('a'))==0):
        print("Only One Page Exists")
        return None        # If Only 1 Page of Data Exists
        
    # Run Standalone Data Gathering Once alteasts
    global Global_header
    
    # For Data            
    # THIS IS OUR Standalone Run


    for i,tr in enumerate(required_table.findAll('tr')):
        #print('Entering first Vertical Loop for '+str(i+1)+'th time TR \n')
        if(i !=0):
            # Vertical Loop
            row1 = []
            index2headers = []
            if(i<len(required_table.findAll('tr'))-2):
                button = driver.find_element(By.XPATH,value='//*[@id="RegistrationGrid"]/tbody/tr['+str(i+1)+']/td[10]/input')
            for td in tr.findAll('td'):
                # Horizontal Loop
                #print('\t Entering Horizontal Loop for '+str(i)+'th time - TD \t')
                row1.append(td.decode_contents())
                
                # Going to Index2 Tab/Page
            row2 = []
            if(i<len(required_table.findAll('tr'))-2):
                #print("\nClicking on Index2 for "+str(i)+"th time \n ")
                button.click()
                time.sleep(5)
                driver.switch_to.window(driver.window_handles[1])
                soup1 = BeautifulSoup(driver.page_source, 'html.parser')
                index2_table = soup1.find('table',attrs={'class':'tblmargin'})
                index2headers = get_index2_headers(index2_table)
                tempheader = Global_header+index2headers
                for j,index2_tr in enumerate(index2_table):
                    #index2 = []
                    
                    # Loop for Index2 Items
                    for td in index2_tr.findAll('td',attrs={'width':'70%'}):
                        something = td.decode_contents()
                        row2.append(something)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            
            row.append(tempheader)
            row.append(row1+row2)
            
    return row


# In[ ]:





# url1 = r"C:\Users\Daksh Kumar\PropReturns\correct_source_code_index2.txt"
# file = open(url1,mode='r',encoding='utf-8')
# type(file.read())
# driver.page_source
# #file.read()

# In[ ]:





# In[ ]:





# In[ ]:





# In[14]:


def pagination(required_table):
    # This is our Pagination Run 
    print("Pagination Running \n")
    Page_row = []
    global KillSwitch
    global Global_header
    global Global_List
    for i in range(len(required_table.findAll('a'))):
        pagination_button = driver.find_element(By.XPATH,value ='//*[@id="RegistrationGrid"]/tbody/tr[12]/td/table/tbody/tr/td['+str(i+2)+']/a' )
        pagination_button.click()
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        required_table1 = soup.find('table',attrs={'id':'RegistrationGrid'})
        Page_row = Page_row + vertical_scraping(required_table1,i+2,Page_row)
        Global_List = Page_row
        print("\n P. Loop")
        print(type(Page_row))
    try:
        driver.find_element(By.XPATH,value ='//*[@id="RegistrationGrid"]/tbody/tr[12]/td/table/tbody/tr/td['+str(i+3)+']/a' )
        print("More Pages may Exist, Re-Run Parsing")
    except NoSuchElementException:
        print("Scraping Completed till Last Page Completely")

    except StaleElementReferenceException as e:
        print("Running Analysis and checking if all the data on the given page has been scraped or not "+ e)
        if(i==len(required_table.findAll('a'))):
            print("Scraping Completed on Given Page No." +str(i+1)+". ----- \n")
        else:
            print("Some Problem Occured, Retrying from the current Page ")
            if(KillSwitch == True):
                return None
            else:
                retry(data)
    try:
        driver.find_element(By.XPATH,value ='//*[@id="RegistrationGrid"]/tbody/tr[12]/td/table/tbody/tr/td['+str(i+2)+']/a' )
    except NoSuchElementException:
        print("This is either the last page or there's Some Error in Accessing the New Page in which case - Rerunning the Program from the Current Page \n Else \t Check the Prev. Log to See if Scraping has completed or not ")
        pass
    else:
        Page_row = Page_row + vertical_scraping(required_table1,i+2,Page_row)
        
    return Page_row




def vertical_scraping(required_table,page_no,Page_row):
    for i,tr in enumerate(required_table.findAll('tr')):
        #print('Entering first Vertical Loop for '+str(i+1)+'th time TR \n')
        if(i !=0):
            Hrow = []
            # Vertical Loop
            button = None
            if(i<len(required_table.findAll('tr'))-2):
                button = driver.find_element(By.XPATH,value='//*[@id="RegistrationGrid"]/tbody/tr['+str(i+1)+']/td[10]/input')
            page_row = horizontal_scraping(tr,i,Hrow,button,required_table,Page_row)
        page_row = Page_row 
        print("\n V. Loop")
        print(type(page_row))
    return page_row

def horizontal_scraping(tr,vertical_component,Hrow,button,required_table,Page_row):
    i = vertical_component
    for td in tr.findAll('td'):
        # Horizontal Loop
        Hrow.append(td.decode_contents())
    # Going to Index2 Tab/Page
    Index2row,tempindex2header = Index2_scraping(i,button,required_table)
    Page_row.append(tempindex2header)
    Page_row.append(Hrow+Index2row )
    # + list([str(i+1)])
    print("\n H. Loop")
    print(type(Page_row))
    return Page_row

def Index2_scraping(i,button,required_table):
    #index2 = []
    Index2row = []
    tempheader = []
    if(i<len(required_table.findAll('tr'))-2):
        #print("\nClicking on Index2 for "+str(i)+"th time \n ")
        button.click()
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[1])
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        index2_table = soup1.find('table',attrs={'class':'tblmargin'})
        index2headers = get_index2_headers(index2_table)
        tempheader = Global_header+index2headers
        for j,index2_tr in enumerate(index2_table):
            
            # Loop for Index2 Items
            for td in index2_tr.findAll('td',attrs={'width':'70%'}):
                something = td.decode_contents()
                
                Index2row.append(something)
                #print("\n Row2 has been appended by " + str(i) + "th Entry Succesfully \n")
            
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return Index2row,tempheader


# In[ ]:





# In[ ]:





# In[15]:


data=["https://freesearchigrservice.maharashtra.gov.in/",'2022',"मुंबई उपनगर जिल्हा","Andheri","415"]


# In[16]:


# By Default Values = 
url = data[0]
year = data[1]
District = data[2]
AreaName = data[3]
PropertyNo = data[4]


# In[ ]:





# In[17]:


# Installing and Running the Driver for New PC's/Servers
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)


# In[18]:


def automated_scraping_model(url=data[0],year=data[1],District=data[2],AreaName=data[3],PropertyNo=data[4]):
    open_site(url)
    enter_data(year,District,AreaName,PropertyNo)
    waitfortab()
    if(KillSwitch == True):
        print("\n Exiting Program due to Website Issue. Kindly Try Later \n")
        return None
    close_popup()
    # IMP
    Final_Row = []
    #table = driver.find_element(By.ID, value = "RegistrationGrid")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    required_table = soup.find('table',attrs={'id':'RegistrationGrid'})
    button=required_table.find('button',attrs={'value:IndexII'})
    header = get_headers(required_table)
    Final_Row.append(header)
    firstpage_row = standalonerun(required_table)
    print("Standalone Run Completed, Now Running Pagination \n")
    Final_Row = Final_Row + firstpage_row
    Final_Row = Final_Row + pagination(required_table)
    return Final_Row


# In[19]:


# For Testing
# Format for Arguments - ("url",'year',"Disctrict","AreaName","PropertyNo")


#Some_RandomDF = automated_scraping_model("https://freesearchigrservice.maharashtra.gov.in/",'2022',"मुंबई उपनगर जिल्हा","Andheri","415")



# In[20]:


print("Do You want to Enter Custom Values press y or use default values - press n ?")
if(input()=='y'):
    print(" \n Enter Year \t - ")
    year = str(input())
    print(" \n Enter District \ 1. for मुंबई जिल्हा \n 2. for मुंबई उपनगर जिल्हा \n\t - ")
    District = input()
    print(" \n Enter AreaName \t - ")
    AreaName = str(input())
    print(" \n Enter ProperyNo \t - ")
    PropertyNo = str(input())
else:
    print("Using Default Values \n")


# In[21]:


if( District == 1):
    District = "मुंबई जिल्हा"
    
elif(District == 2):
    District = "मुंबई उपनगर जिल्हा"


# In[ ]:





# In[ ]:





# In[22]:


Final_Row = automated_scraping_model(url,year,District,AreaName,PropertyNo)


# In[23]:


df = pd.DataFrame(Final_Row)


# In[24]:


if (KillSwitch!=True):
    print("\n Exporting the Data into tempdata.csv -you can uncomment the next time for .xlsx format file \n ")
    #df.to_excel('excel-temp.xlsx')
    df.to_csv('tempdata.csv',encoding = "utf-8-sig")
else:
    print("Program Ended due to some Error \n Kindly Check logs")


# In[25]:


df1 = pd.DataFrame(Global_List)


# In[26]:


df1


# In[27]:


# df


# In[28]:


# df[21]


# In[ ]:





# In[29]:


something = input("\n Press Enter to Exit Program \n")


# In[30]:


type(something)


# In[31]:


#df[4]


# In[32]:


driver.close()
print("Waiting for 20 seconds before closing program automatically \n") 
time.sleep(20)




# # When I automate
# ## Steps - 
# 
# Create A Loop for Pagination :
# 
#     1. Paginate and Start from Page 0 or 1
#     2. Loop Over Every New Page
#     3. Find Table
#     4. Create a Loop to Traverse Vertically
#          1. Traverse Through, Vertically First
#          * Enters 1st Row *
#         2. Create a Horizonatal Loop 
#                 1. Extract all the Data in that row to Respective Fields
#                 2. Before Loop Ends, Click on Index2 Link
#                 Parse Data on this New Tab As Well ( Vertically, but convert it into Horizontal Fields to go in accordance with Original Data
#                 3. Close This New Tab
#         Horizontal Loop Ends
#     * Vertical Loop Repeats, until all the elements are parsed *
#     Vertical Loop Ends
#     Pagination Loop Ends
#     
#    
#     

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




