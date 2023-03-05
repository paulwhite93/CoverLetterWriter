from tkinter import *
from tkinter import filedialog
import openai
import os
import requests
from bs4 import BeautifulSoup

openai.api_key = "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" #must be set before it will function
directory = os.getcwd()
resumeFile = "resume_master.txt"
global resume
resume = ""
#open ai startup 

class Job:
    def __init__(self,jobDescription,title,c_name) -> None:
        self.jobDesc = jobDescription
        self.job_title = title
        self.company_name = c_name
        self.jobResume = resume
        self.open_window()

    def open_window(self):
        if self.jobResume == "":
            self.jobResume = resume
        self.JobWindow = Toplevel(GUIWindow)
        self.JobWindow.geometry("1280x720")
        self.JobWindow.title(self.company_name)

        Label(self.JobWindow, text='Job Title:').grid(row=0)
        Label(self.JobWindow, text='Company Name:').grid(row=1)
        Label(self.JobWindow, text='Job Description:').grid(row=2)
        Label(self.JobWindow, text='Resume:').grid(row=2, column = 20, sticky=E)

        #setJobDescriptionButton = Button(JobWindow, text="Set Job Description", command = self.set_job_description)
        #setJobDescriptionButton.grid(row = 3, column = 0)

        refineResumeButton = Button(self.JobWindow, text="Refine Resume", command = self.refine_resume)
        refineResumeButton.grid(row = 0, column = 3)

        createCoverLetter = Button(self.JobWindow, text="Create Cover Letter", command = self.create_cover_letter)
        createCoverLetter.grid(row = 1, column = 3)
        self.set_job_desc()
        self.set_company_name()
        self.set_job_title()
        self.set_resume()

    #function definitions    
    def sendData(self,data):
        #sends data to openai
        #sets the outputtxt to the output data from openai
        print(data)
        chat_completion = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages=[{"role":"user","content":data}])
        return chat_completion.choices[0].message.content

    def refine_resume(self):
        #open ai resume refinement
        #open a new window with refined resume returned by openAI and prompt user if theyd like to save to a file
        def sendResume():
            prompt = "please personalize my resume for this: " + self.job_title +" " + self.company_name + "\n Here is the job description: " + self.jobDesc + "\n And here is my resume: " + self.jobResume
            resume_outputtxt.insert(END,self.sendData(prompt))

        def saveResume():
            self.write_resume_to_file(resume_outputtxt.get("1.0",'end-1c'))
            window.destroy()
            return
        
        window = Toplevel(self.JobWindow)
        window.title("Refining Resume")
        window.geometry("1280x720")

        outputlabel = LabelFrame(window, text= "Refined Resume")
        outputlabel.grid(row=1,column=0)

        resume_outputtxt = Text(outputlabel, height=40, width=120)
        resume_outputtxt.grid(row = 1)

        Button(outputlabel, text = "Save Resume", command = saveResume).grid(row = 2)
        sendResume()
    

    def create_cover_letter(self):
        #create cover letter using open ai and job description
        #open a new window with cover letter returned by openAI and prompt user if theyd like to save to a file
        def send():
            prompt = "please write a personalized cover letter for this " + self.job_title + " at " + self.company_name + "\n Here is the job description: " + self.jobDesc + "\n And here is my resume: " + resume
            outputtxt.insert(END,self.sendData(prompt))
        def save():
            self.write_cover_letter_to_file(outputtxt.get("1.0",'end-1c'))
            window.destroy()
        
        window = Toplevel(self.JobWindow)
        window.title("Creating Cover Letter")
        window.geometry("1280x720")

        submitButton = Button(window, text = "Create Cover Letter", command = send)
        submitButton.pack()

        outputlabel = Label(window, text= "Cover Letter")
        outputlabel.pack()

        outputtxt = Text(window, height=40, width=120)
        outputtxt.pack()

        saveCoverLetterButton = Button(window, text = "Save Cover Letter", command = save)
        saveCoverLetterButton.pack()
        return

    def write_resume_to_file(self,data):
        #write resume to a file
        #if were saving new resume 
        global newResume
        newResume = data
        file = filedialog.asksaveasfile(mode='w',initialfile = self.company_name + "_resume", defaultextension=".txt",)
        try:
            file.write(data)
            file.close()
        except Exception:
            print("Error writing to file")
        return
    def write_cover_letter_to_file(self,data):
        #write cover letter to a file
        file = filedialog.asksaveasfile(mode='w',initialfile = self.company_name + "_coverLetter", defaultextension=".txt",)
        try:
            file.write(data)
            file.close()
        except Exception:
            print("Error writing to file")

    def set_job_title(self):
        Label(self.JobWindow, text= self.job_title).grid(row = 0, column = 1)
    def set_company_name(self):
        Label(self.JobWindow, text= self.company_name).grid(row = 1, column = 1)
    def set_job_desc(self):
        jobDesc_text = Text(self.JobWindow,height=30, width=80)
        jobDesc_text.grid(row = 3, column = 0,columnspan = 20, rowspan = 6)
        jobDesc_text.insert(END,self.jobDesc)
    def set_resume(self):
        jobResume_text = Text(self.JobWindow,height=30, width=80)
        jobResume_text.grid(row = 3, column = 20,columnspan = 20, rowspan = 6)
        jobResume_text.insert(END,self.jobResume)

#application GUI
GUIWindow = Tk()
GUIWindow.geometry("1280x720")
jobList = []

def create_job():
    #make a button to open the job window
    #store job description for use in open ai commands
    def destroy_window():
        window.destroy()
    def saveInfo():
        jobDesc = jobdescriptiontxt.get("1.0",'end-1c')
        job_title = e1.get()
        company_name = e2.get()            
        jobList.append(Job(jobDesc,job_title,company_name))
        add_button(jobList[-1])
        destroy_window()

    def scrape_url():
        #build job based on url
        

        URL = e3.get()
        page = requests.get(URL)
        #print(page.text)

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id="main")
        if results:
            job_title = results.find("h1", class_ = "app-title")
            company_name = results.find("span", class_ = "company-name")
            #print(results.prettify())
            jobDesc = results.find("div", id="content")
            #print(job_title.text)
            #print(company_name.text)
            #print(jobDesc.text)
            e1.insert(END,job_title.text)
            e2.insert(END,company_name.text)
            jobdescriptiontxt.insert(END,jobDesc.text)


    window = Toplevel(GUIWindow)
    window.title("Setting Job Description and Company Name")
    window.geometry("1280x720")

    Label(window, text='Job Title:').grid(row=1)
    Label(window, text='Company Name').grid(row=2)
    e1 = Entry(window)
    e2 = Entry(window)
    e1.grid(row=1, column=1)
    e2.grid(row=2, column=1)

    jobdescriptionlabel = Label(window, text= "Please paste your job description here:")
    jobdescriptionlabel.grid(row = 3)
    jobdescriptiontxt = Text(window, height=10, width=50)
    jobdescriptiontxt.grid(row = 4)

    submitButton = Button(window, text = "Save Information", command = saveInfo)
    submitButton.grid(row = 5)
    
    Label(window, text='Job URL:').grid(row=0)
    e3 = Entry(window)
    e3.grid(row=0, column=1)
    scrapeURLButton = Button(window, text = "Scrape URL", command = scrape_url)
    scrapeURLButton.grid(row = 0, column = 2)
    return

def add_button(job):
    Button(jobFrame,text= job.job_title + " at " + job.company_name , command=job.open_window).grid(row = len(jobList),sticky = E)
def upload_resume():
    tf = filedialog.askopenfilename( 
    title="resume_master.txt", 
    filetypes=(("Text Files", "*.txt"),)
    )
    try:
        tf = open(tf,'r')
        global resume
        resume = tf.read()
        tf.close()
        display_resume()
    except Exception:
        return
    
def display_resume():
    resumeFrame = LabelFrame(NewJobFrame, text = "Master Resume")
    resumeFrame.grid(row = 0, column = 10,columnspan = 20, rowspan = 6,sticky=E)
    resumeText = Text(resumeFrame, height=20, width=100)
    resumeText.grid()
    #print(resume)
    resumeText.insert(END,resume)

#Create Existing Job Frame
jobFrame = LabelFrame(GUIWindow,text = "Jobs", padx=15, pady=15)
jobFrame.grid(row = 0)

#Create New Job Button
NewJobFrame = Frame(GUIWindow,padx=15, pady=15)
NewJobFrame.grid(row = 1)
Button(NewJobFrame, text="Create New Job", command = create_job).grid(row = 0)

#upload resume button
Button(NewJobFrame, text="Master Resume", command = upload_resume).grid(row = 1, sticky = E)


"""
#show current saved information
Label(GUIWindow, text='Job Title:').grid(row=0)
Label(GUIWindow, text='Company Name').grid(row=1)
Label(GUIWindow, text='Job Description').grid(row=2)


#define buttons

setJobDescriptionButton = Button(GUIWindow, text="Set Job Description", command = set_job_description)
setJobDescriptionButton.grid(row = 3, column = 0)


refineResumeButton = Button(GUIWindow, text="Refine Resume", command = refine_resume)
refineResumeButton.grid(row = 3, column = 1)

createCoverLetter = Button(GUIWindow, text="Create Cover Letter", command = create_cover_letter)
createCoverLetter.grid(row = 3, column = 2)
"""
GUIWindow.mainloop()