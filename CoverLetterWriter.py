import tkinter
import openai

openai.api_key = "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" #must be set before it will function

#open ai startup 

#Store new text
global jobDesc
jobDesc = ""
global job_title
job_title = ""
global company_name
company_name = ""
global resume
resume = ""
global newResume
newResume = ""

#function definitions    
def sendData(data):
    #sends data to openai
    #sets the outputtxt to the output data from openai
    print(data)
    chat_completion = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages=[{"role":"user","content":data}])
    return chat_completion.choices[0].message.content

def refine_resume():
    #open ai resume refinement
    #open a new window with refined resume returned by openAI and prompt user if theyd like to save to a file
    def send():
        global resume
        resume = inputtxt.get("1.0",'end-1c')
        prompt = "please personalize my resume for this: " + job_title +" " + company_name + "\n Here is the job description: " + jobDesc + "\n And here is my resume: " + resume
        outputtxt.insert(tkinter.END,sendData(prompt))
    def save():
        write_resume_to_file(outputtxt.get("1.0",'end-1c'))
        window.destroy()
        return
    
    window = tkinter.Toplevel(GUIWindow)
    window.title("Refining Resume")
    window.geometry("1280x720")

    inputlabel = tkinter.Label(window, text= "Please paste your resume here:")
    inputlabel.pack()

    inputtxt = tkinter.Text(window, height=10, width=50)
    inputtxt.pack()

    submitButton = tkinter.Button(window, text = "Refine", command = send)
    submitButton.pack()

    outputlabel = tkinter.Label(window, text= "Refined Resume")
    outputlabel.pack()

    outputtxt = tkinter.Text(window, height=10, width=50)
    outputtxt.pack()

    saveResumeButton = tkinter.Button(window, text = "Save Resume", command = save)
    saveResumeButton.pack()
    
    

    return
def set_job_description():
    #store job description for use in open ai commands
    def saveInfo():
        global jobDesc
        jobDesc = jobdescriptiontxt.get("1.0",'end-1c')
        global job_title
        job_title = e1.get()
        global company_name
        company_name = e2.get()
        set_company_name()
        set_job_title()
        set_job_desc()
        window.destroy()
        return

    window = tkinter.Toplevel(GUIWindow)
    window.title("Setting Job Description and Company Name")
    window.geometry("1280x720")

    tkinter.Label(window, text='Job Title:').grid(row=0)
    tkinter.Label(window, text='Company Name').grid(row=1)
    e1 = tkinter.Entry(window)
    e2 = tkinter.Entry(window)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    jobdescriptionlabel = tkinter.Label(window, text= "Please paste your job description here:")
    jobdescriptionlabel.grid(row = 2)
    jobdescriptiontxt = tkinter.Text(window, height=10, width=50)
    jobdescriptiontxt.grid(row = 3)

    submitButton = tkinter.Button(window, text = "Save Information", command = saveInfo)
    submitButton.grid(row = 4)
    
    return
def create_cover_letter():
    #create cover letter using open ai and job description
    #open a new window with cover letter returned by openAI and prompt user if theyd like to save to a file
    def send():
        prompt = "please write a personalized cover letter for this " + job_title + " at " + company_name + "\n Here is the job description: " + jobDesc + "\n And here is my resume: " + resume
        outputtxt.insert(tkinter.END,sendData(prompt))
    def save():
        write_cover_letter_to_file(outputtxt.get("1.0",'end-1c'))
        window.destroy()
    
    window = tkinter.Toplevel(GUIWindow)
    window.title("Creating Cover Letter")
    window.geometry("1280x720")

    submitButton = tkinter.Button(window, text = "Create Cover Letter", command = send)
    submitButton.pack()

    outputlabel = tkinter.Label(window, text= "Cover Letter")
    outputlabel.pack()

    outputtxt = tkinter.Text(window, height=10, width=50)
    outputtxt.pack()

    saveCoverLetterButton = tkinter.Button(window, text = "Save Cover Letter", command = save)
    saveCoverLetterButton.pack()
    return

def write_resume_to_file(data):
    #write resume to a file
    #if were saving new resume 
    global newResume
    newResume = data
    return
def write_cover_letter_to_file(data):
    #write cover letter to a file
    return

def set_job_title():
    tkinter.Label(GUIWindow, text=job_title).grid(row = 0, column = 1)
def set_company_name():
    tkinter.Label(GUIWindow, text=company_name).grid(row = 1, column = 1)
def set_job_desc():
    jobDesc_text = tkinter.Text(GUIWindow,height=10, width=50)
    jobDesc_text.grid(row = 2, column = 1)
    jobDesc_text.insert(tkinter.END,jobDesc)


#application GUI
GUIWindow = tkinter.Tk()
GUIWindow.geometry("1280x720")


#show current saved information
tkinter.Label(GUIWindow, text='Job Title:').grid(row=0)
tkinter.Label(GUIWindow, text='Company Name').grid(row=1)
tkinter.Label(GUIWindow, text='Job Description').grid(row=2)


#define buttons

setJobDescriptionButton = tkinter.Button(GUIWindow, text="Set Job Description", command = set_job_description)
setJobDescriptionButton.grid(row = 3, column = 0)


refineResumeButton = tkinter.Button(GUIWindow, text="Refine Resume", command = refine_resume)
refineResumeButton.grid(row = 3, column = 1)

createCoverLetter = tkinter.Button(GUIWindow, text="Create Cover Letter", command = create_cover_letter)
createCoverLetter.grid(row = 3, column = 2)
GUIWindow.mainloop()