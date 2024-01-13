import sqlite3
import tkinter as tk
from tkinter import *
from tabulate import tabulate

########## CLASSES ##########

class Applicant:
    def __init__(self, dbName):
        self.db = sqlite3.connect(dbName)
        self.cursor = self.db.cursor()
        self.tableName = "APPLICANTS"
        #creating index on primary key
        self.appPKIndx = self.cursor.execute("CREATE INDEX IF NOT EXISTS appPrimaryKeyIndex ON APPLICANT(ID)")
        #creating instance of class Recruiter that we'll use in the functions
        self.recruiter = Recruiter(dbName)
        
        
    def printApplicants(self):
        data = self.cursor.execute("SELECT * FROM APPLICANT")
        printResults(data, self.tableName)

    def createApplicant(self):
        error = "ERROR! Mandatory fields left empty. Try again.\n"
        print("----CREATE APPLICANT----\nAll fields with (*) are mandatory.\n")
        
        firstName  = input("Enter first name* : ")
        if(firstName == ""): #checking if mandatory field is left empty
            print(error)
            return
            
        lastName = input("Enter last name*: ")
        if(lastName == ""): #checking if mandatory field is left empty
            print(error)
            return
        
        minit = input("Enter middle name's initial if it exists: ")
        if(minit == ""):
            minit = None #None is translated as NULL in SQLite

        email = input("Enter email*: ")
        if(email == ""):
            print(error)
            return
        self.cursor.execute("SELECT count(*) FROM APPLICANT WHERE Email = ?", (email,))
        checkId = self.cursor.fetchone()[0] #checking if email is indeed unique
        if(checkId != 0):
            print("Applicant with email: %s already exists. Try again.\n" % (email))
            return
        
        phone = input("Enter phone number*: ")
        if(phone == ""): #checking if mandatory field is left empty
            print(error)
            return
        self.cursor.execute("SELECT count(*) FROM APPLICANT WHERE Phone = ?", (phone,))
        checkId = self.cursor.fetchone()[0] #checking if phone number is unique
        if(checkId != 0):
            print("Applicant with phone number: %s already exists. Try again.\n" % (phone))
            return
        
        SSN = input("Enter SSN*: ")
        if(SSN == ""):#checking if mandatory field is left empty
            print(error)
            return
        self.cursor.execute("SELECT count(*) FROM APPLICANT WHERE SSN = ?", (SSN,))
        checkId = self.cursor.fetchone()[0] #checking if SSN is unique
        if(checkId != 0):
            print("Applicant with SSN: %s already exists. Try again.\n" % (SSN))
            return
        
        DOB = input("Enter date of birth: ")
        if(DOB == ""):
            DOB = None
        
        canRelocate = input("Is the applicant willing to relocate? (default: No) [Yes/No] : ")
        canRelocate = canRelocate.lower()
        if (canRelocate == "yes"):
            reloc = 1
        else:
            reloc = 0 #default value is 0
        
        recruiterID = input("Enter recruiter's ID for the applicant: ")
        if((recruiterID == "") | (self.recruiter.isRecruiter(recruiterID) == False)):
            #checking if field is left empty or if there is no recruiter with this id (mistake of user)
            recruiterID = None
            
        #using format (?) because we don't know what type of data we'll use (str, int ktlp)
        execString = "INSERT INTO APPLICANT (FirstName, LastName, Minitial, Email, Phone, SSN, DOB, CanRelocate, RecruiterID) VALUES (?,?,?,?,?,?,?,?,?)"
        valuesString = (firstName, lastName, minit, email, phone, SSN, DOB, reloc, recruiterID)
        self.cursor.execute(execString , valuesString)
        print("\nApplicant successfully created.\n")
        self.printApplicants()
        self.db.commit()
        return
            
    def updateApplicant(self):
        error = "ERROR! Mandatory fields left empty. Try again.\n"
                
        self.printApplicants() #printing APPLICANTS table for the user to choose
        id = input("Enter applicantID: ")
        
        self.cursor.execute("SELECT count(*) FROM APPLICANT WHERE ID = ?" , (id,))
        checkId = self.cursor.fetchone()[0] #checking if there is already an applicant with this id
        if(checkId == 0): #can't leave mandatory field empty
            print("Can't find applicant with id: %s. Please try again\n" % id)
            return


        answer = input("What field would you like to change?\nFirstName\nLastName\nMinit\nEmail\nphone\nSSN\nDOB\nCanRelocate\nRecruiterID\n")
        answer = answer.lower()
        #we allow only one field to change at a time
        while True:
        #using while True instead of previous approach because there were confusing inputs between 'answer' and 
        #the next user input 'value'
        
            if (answer == "firstname"):
                value = input("Enter new first name: ")
                if(value == ""):
                    print(error)
                    return
                values = (value, id) #values and id stays the same, only changing the contents of value
                self.cursor.execute("UPDATE APPLICANT SET FirstName = ? WHERE ID = ?", values)
                self.db.commit()
                break
        
            if(answer == "lastname"):
                value = input("Enter new last name: ")
                if(value == ""):
                    print(error)
                values = (value, id)
                self.cursor.execute("UPDATE APPLICANT SET LastName = ? WHERE ID = ?",values)
                self.db.commit()
                break

            if(answer == "minit"):
                value = input("Enter new middle name initial: ")
                if(value == ""):
                    value = None
                values = (value, id)
                self.cursor.execute("UPDATE APPLICANT SET Minitial = ? WHERE ID = ?",values)
                self.db.commit()
                break

            if(answer == "email"):
                value = input("Enter new email: ")
                if(value == ""):
                    print(error)
                    return
                self.cursor.execute("SELECT count(*) FROM APPLICANT WHERE Email = ?", (value,))
                checkId = self.cursor.fetchone()[0] #making sure email is not null and is unique
                if(checkId != 0):
                    print("Applicant with email: %s already exists. Try again.\n" % (value))
                    return
                values = (value, id)
                self.cursor.execute("UPDATE APPLICANT SET Email = ? WHERE ID = ?",values)
                self.db.commit()
                break
                
            if(answer == "phone"):
                value = input("Enter new phone number: ")
                if(value == ""):
                    print(error)
                    return
                self.cursor.execute("SELECT count(*) FROM APPLICANT WHERE Phone = ?", (value,))
                checkId = self.cursor.fetchone()[0] #making sure phone number is not null and is unique
                if(checkId != 0):
                    print("Applicant with phone number: %s already exists. Try again.\n" % (value))
                    return
                values = (value, id)
                self.cursor.execute("UPDATE APPLICANT SET Phone = ? WHERE ID = ?",values)
                self.db.commit()
                break


            if(answer == "ssn"):
                value = input("Enter new SSN: ")
                if(value == ""):
                    print(error)
                    return
                self.cursor.execute("SELECT count(*) FROM APPLICANT WHERE SSN = ?", (value,))
                checkId = self.cursor.fetchone()[0] #making sure that ssn is not left empty and is unique
                if(checkId != 0):
                    print("Applicant with SSN: %s already exists. Try again.\n" % (value))
                    return
                values = (value, id)
                self.cursor.execute("UPDATE APPLICANT SET SSN = ? WHERE ID = ?",values)
                self.db.commit()
                break


            if(answer == "dob"):
                value = input("Enter new date of birth: ")
                if(value == ""):
                    value = None
                values = (value, id)
                self.cursor.execute("UPDATE APPLICANT SET DOB = ? WHERE ID = ?",values)
                self.db.commit()
                break


            if(answer == "canrelocate"):
                temp = input("Enter 'yes' for willingness to relocate or 'no' for not wanting to relocate: ")
                temp = temp.lower()
                value = 0 #default value - thinking most people wouldnt want to relocate
                if(temp == "yes"):
                    value = 1
                else:
                    print("oops! back to menu\n")
                    return
                values = (value, id)
                self.cursor.execute("UPDATE APPLICANT SET CanRelocate = ? WHERE ID = ?",values)
                self.db.commit()
                break

            if(answer == "recruiterid"):
                value = input("Enter new recruiterID: ")
                if((value == "") | (self.recruiter.isRecruiter(value) == False)): #we check if there is no recruiter with that id or if left empty
                    value = None
                values = (value, id)
                self.cursor.execute("UPDATE APPLICANT SET RecruiterID = ? WHERE ID = ?",values)
                self.db.commit()
                break

            else:
                print("oops! back to menu\n")
                return
            

            
        print("\nApplicant successfully updated.\n")
        self.printApplicants()
        return    

    def deleteApplicant(self):
        print("----DELETE APPLICANT----\n")
        self.printApplicants()
        id = input("Enter applicantID: ") #searching applicant by id
        self.cursor.execute("SELECT count(*) FROM APPLICANT WHERE ID = ?",(id,))
        checkId = self.cursor.fetchone()[0]
            
        if(checkId == 0): #checking if there is applicant with that id, if not return
            print("Can't find applicant with id: %s. Please try again\n" % (id))
            return
        
        self.cursor.execute("DELETE FROM APPLICANT WHERE ID = ?", (id,))
        self.db.commit()


        print("Applicant successfully deleted.\n")
        self.printApplicants()
        return
    
    def searchApplicantsByEdu(self):
        fields = self.cursor.execute("SELECT * FROM FIELD_TYPE")
        printResults(fields, "FIELDS OF EDUCATION") #printing table for the user to choose by id 
        id = input("Enter Field ID: ")
        
        self.cursor.execute("SELECT count(*) FROM FIELD_TYPE WHERE ID = ?",(id,))
        checkId = self.cursor.fetchone()[0]
            
        if(checkId == 0): #checking that user gave valid id
            print("Can't find field with id: %s. Please try again\n" % (id))
            return
        
        command  = "SELECT APPLICANT.ID AS 'APP_ID', APPLICANT.LastName AS 'APP_LastName', FIELD_TYPE.Domain AS 'Field' FROM APPLICANT JOIN EDUCATION ON APPLICANT.ID = EDUCATION.ApplicantID JOIN FIELD_TYPE ON EDUCATION.FieldTypeID = FIELD_TYPE.ID WHERE FIELD_TYPE.ID = ?;"
        applicants = self.cursor.execute(command, (id,))
        printResults(applicants, "APPLICANTS BASED ON EDUCATION")
        
        
        



        
        
        
class JobPosting:
    def __init__(self, dbName):
        self.db = sqlite3.connect(dbName)
        self.cursor = self.db.cursor()
        self.tableName = "JOB POSTINGS"
        #create index on primary key of table to search faster
        self.postPKIndx = self.cursor.execute("CREATE INDEX IF NOT EXISTS postPrimaryKeyIndex ON JOB_POSTING(ID)")
        #creating instances of the other classes that we'll use in the functions
        self.company = Company(dbName)
        self.langReq = LanguageRequirement(dbName)
        self.edReq = EducationRequirement(dbName)
        self.recruiter = Recruiter(dbName)
        
    def printJobPostings(self):
        data = self.cursor.execute("SELECT * FROM JOB_POSTING")
        printResults(data, self.tableName)

        
    def createJobPosting(self):
        print("----CREATE JOB POSTING----\nAll fields with (*) are mandatory.\n")
        
        self.company.printCompanies() #print list of companies for user to choose by id
        
        #checking for valid companyID
        compID = input("\nEnter company's ID*: ")
        self.cursor.execute("SELECT count(*) FROM COMPANY WHERE ID = ?", (compID,))
        checkId = self.cursor.fetchone()[0]
        if(checkId == 0):
            print("Can't find company with id: %s. Please try again\n" % (compID))
            return #returning for invalid input
        
        recID = input("Enter recruiter's ID: ") #checking that recruiter ID is not left empty or invalid
        if((recID == "") | (self.recruiter.isRecruiter(recID) == False)):
            recID = None
            
        loc = input("Enter job's location: ")
        if(loc == ""):
            loc = None #NULL for SQL
        
        rloc = input("Does the job require relocation? (Default: No) [Yes / No] : ")
        rloc = rloc.lower()
        if (rloc == "yes"):
            reloc = 1
        else:
            reloc = 0 #default value, we suppose most jobs dont require relocation
        
        title = input("Enter position's title: ")
        if(title == ""):
            title = None
        
        remote = input("Is the job remote? ")
        if(remote == ""):
            remote = None
            
        years = input("Years of experience required [Default: 0]: ")
        if(years == ""):
            years = 0
        
        desc = input("Describe the position shortly: ")
        if(desc == ""):
            desc = None
        
        #print list of languages to choose from for language requirement    
        langs = self.cursor.execute("SELECT * FROM LANGUAGE")
        printResults(langs, "LANGUAGES")
        languageID = input("Enter languageID: ")
        #do the same for levels of language certification
        levels = self.cursor.execute("SELECT * FROM LANGUAGE_LEVEL")
        printResults(levels, "LANGUAGE LEVELS")
        levelID = input("Enter Level ID: ")
        #initializing language requirement id, that represents the unique combination of the other two
        langReqID = None
        
        #if language or level is left empty, langReqID stays as NONE
        if((levelID != "") & (languageID != "")):
            #check table LANGUAGE_REQ for the unique combination
            langReqID = self.langReq.findLanguageReq(levelID, languageID) 
            if(langReqID == None):
                #if it is not found, create it
                langReqID = self.langReq.createLanguageRequirement(levelID, languageID)
                
        fields = self.cursor.execute("SELECT * FROM FIELD_TYPE")
        printResults(fields, "Fields of Education")
        fID = input("Enter field ID: ")

        degrees = self.cursor.execute("SELECT * FROM DEGREE_TYPE")
        printResults(degrees, "TYPES OF DEGREES")
        dID = input("Enter Degree ID: ")
        
        edReqID = None
        if((fID != "") & (dID != "")):
            edReqID = self.edReq.findEducationReq(dID, fID)
            if(edReqID == None):
                edReqID = self.edReq.createEducationRequirement(dID, fID)
        
        execString = "INSERT INTO JOB_POSTING (CompanyID, RecruiterID, Location, Relocation, Title, Remote, YearsOfExp, Description, LanguageReqID, EducationReqID) VALUES (?,?,?,?,?,?,?,?,?,?)"
        valuesString = (compID, recID, loc, reloc, title, remote, int(years), desc, langReqID, edReqID)
        self.cursor.execute(execString, valuesString)
        self.db.commit()
        print("\nJob posting successfully created.\n")
        self.printJobPostings()
        return        
       
            
            
        
class Company:
    def __init__(self, dbName):
        self.db = sqlite3.connect(dbName)
        self.cursor = self.db.cursor()
        self.tableName = "COMPANIES"
        #create primary key index 
        self.compPKIndx = self.cursor.execute("CREATE INDEX IF NOT EXISTS compPrimaryKeyIndex ON COMPANY(ID)")
        
    def printCompanies(self):
        data = self.cursor.execute("SELECT * FROM COMPANY")
        printResults(data, self.tableName)
        
    def createCompany(self):
        print("----CREATE COMPANY----\nAll fields with (*) are mandatory\n")
        
        name = input("Enter company's name*: ")
        if(name == ""):
            print("ERROR! Mandatory fields left empty. Try again.\n")
            return
        
        email = input("Enter email: ")
        if(email == ""):
            print("ERROR! Mandatory fields left empty. Try again.\n")
            return 
        
        ind = input("Enter company's industry: ")
        if(ind == ""):
            ind = None
       
        hq = input("Enter headquarters' location: ")
        if(hq == ""):
            hq = None

        execString = "INSERT INTO COMPANY (Name, Email, Industry, Headquarters) VALUES (?, ?, ?, ?) "
        valuesString = (name, email, ind, hq)
        
        self.db.commit()
        print("Company log successfully created.\n")
        self.printCompanies()
        return 
        

class EducationRequirement:
    def __init__(self, dbName):
        self.db = sqlite3.connect(dbName)
        self.cursor = self.db.cursor()
        self.tableName = "EDUCATION REQUIREMENTS"
        #create primary key index
        self.edreqPKIndx = self.cursor.execute("CREATE INDEX IF NOT EXISTS edreqPrimaryKeyIndex ON EDUCATION_REQ(ID)")
        
    def createEducationRequirement(self, degreeTypeID, fieldTypeID):
        self.cursor.execute("INSERT INTO EDUCATION_REQ (DegreeTypeID, FieldTypeID) VALUES (?,?)", (degreeTypeID, fieldTypeID))
        self.db.commit()
        return self.findEducationReq(degreeTypeID, fieldTypeID)
        
        
    def findEducationReq(self, degreeTypeID, fieldTypeID):

        self.cursor.execute("SELECT ID FROM EDUCATION_REQ WHERE (DegreeTypeID = ?)  & (fieldTypeID = ?)", (degreeTypeID, fieldTypeID))
        row = self.cursor.fetchone()
        if (row):
            self.db.commit()
            return row[0]
        else:
            self.db.commit()
            return None
    
class LanguageRequirement:
    def __init__(self, dbName):
        self.db = sqlite3.connect(dbName)
        self.cursor = self.db.cursor()
        self.tableName = "LANGUAGE REQUIREMENTS"
        self.langeqPKIndx = self.cursor.execute("CREATE INDEX IF NOT EXISTS langPrimaryKeyIndex ON LANGUAGE_REQ(ID)")
        
    def createLanguageRequirement(self, levelID, languageID):
        self.cursor.execute("INSERT INTO LANGUAGE_REQ (LevelID, LanguageID) VALUES (?,?)", (levelID, languageID))
        self.db.commit()
        return self.findLanguageReq(levelID, languageID)
        
        
    def findLanguageReq(self, levelID, languageID):

        self.cursor.execute("SELECT ID FROM LANGUAGE_REQ WHERE (LevelID = ?)  & (LanguageID = ?)", (levelID, languageID))
        row = self.cursor.fetchone()
        if (row):
            self.db.commit()
            return row[0]
        else:
            self.db.commit()
            return None

                
                
class Recruiter:
    def __init__(self, dbName):
        self.db = sqlite3.connect(dbName)
        self.cursor = self.db.cursor()
        self.tableName = "RECRUITERS"
        self.recPKIndx = self.cursor.execute("CREATE INDEX IF NOT EXISTS recPrimaryKeyIndex ON RECRUITER(ID)")
    
    def printRecruiters(self):
        data = self.cursor.execute("SELECT * FROM RECRUITER")
        printResults(data, self.tableName)
        
    def createRecruiter(self):
        error = "ERROR! Mandatory fields left empty. Try again.\n"
        print("----CREATE RECRUITER----\nAll fields with (*) are mandatory.\n")

        firstName = input("Enter first name*: ")
        if firstName == "": #check if mandatory field is left empty
            print(error)
            return
        
        lastName = input("Enter last name*: ")
        if lastName == "":
            print(error)
            return

        minit = input("Enter middle initial: ")
        if (minit == ''):
            minit = None #NULL
		
        #check if left empty or is not a unique value
        email = input("Enter email*: ")
        if email == "":
            print(error)
            return
        self.cursor.execute("SELECT count(*) FROM RECRUITER WHERE Email = ?", (email,))
        checkId = self.cursor.fetchone()[0]
        if(checkId != 0):
            print("Recruiter with email: %s already exists. Try again.\n" % (email))
            return 
			
   
        phone = input("Enter phone number*: ")
        #check if left empty or if it is not a unique value
        if phone == "":
            print(error)
            return
        self.cursor.execute("SELECT count(*) FROM RECRUITER WHERE Phone = ?", (phone,)) 
        checkId = self.cursor.fetchone()[0]
        if(checkId != 0):
            print("Recruiter with phone number: %s already exists. Try again.\n" % (phone))
            return

       
        execString = "INSERT INTO RECRUITER (firstName, lastName, minit, email, phone) VALUES (?,?,?,?,?) "
        valuesString = (firstName, lastName, minit, email, phone)
        data = self.cursor.execute(execString, valuesString)
        
        self.db.commit()
        print("\nRecruiter succesfully created\n")
        self.printRecruiters()
        return 
    
    def isRecruiter(self, recruiterID):
        #search database for recruiter by id
        self.cursor.execute("SELECT count(*) FROM RECRUITER WHERE ID = ?", (recruiterID,))
        checkId = self.cursor.fetchone()[0]
        if(checkId == 0):
            return False 
        else:
            return True
        
                    
########## FUNCTIONS ##########            
    
def printResults(data, tableName):
    
    #function mostly taken from stackoverflow and google searches and modified to be a better fit for the program
    if(data == None):
        print("Error! No data to show!\n")
    print("----%s----\n" % tableName)
    
    rows = data.fetchall()
    columns = [description[0] for description in data.description]
    column_widths = [max(len(str(row[i])) if row[i] is not None else 4  # Width for 'NULL'
                         for row in rows + [columns]) for i in range(len(columns))]
    
    for i, column in enumerate(columns):
        print(f"{column:{column_widths[i]}}", end=" | ")
    print()
    
    for width in column_widths:
        print("-" * width, end=" | ")
    print()
    
    for row in rows:
        for i, value in enumerate(row):
            if value is not None:
                print(f"{value:{column_widths[i]}}", end=" | ")
            else:
                print("NULL".center(column_widths[i]), end=" | ")
        print()

def showApplicantsAndRecruiters(cursor):
    data = cursor.execute("SELECT APPLICANT.ID AS 'Applicant_ID', APPLICANT.FirstName AS 'Applicant_FirstName', APPLICANT.LastName AS 'Applicant_LastName', RECRUITER.ID AS 'Recruiter_ID' FROM APPLICANT LEFT JOIN RECRUITER ON APPLICANT.RecruiterID = RECRUITER.ID;")
    printResults(data, "APPLICANTS AND RECRUITERS")
    
def showYearsofExpAvg(cursor):
    data = cursor.execute("SELECT avg(YearsOfExp) AS 'Average_Experience_in_Years' FROM JOB_POSTING")
    printResults(data, "AVERAGE YEARS OF EXPERIENCE NEEDED")
    
def applicantsAndJobPostings(cursor, db):
    #we wanted a dynamic form of matching, so the table is being emptied and refilled everytime
    #but only deleting 'AUTO_GEN' matchings that our application created, not manual matches
    delete = "DELETE FROM MATCHING WHERE Status = 'AUTO_GEN';"
    insertSelect = "INSERT INTO MATCHING (ApplicantID, PostingID, Status, SubmissionDate) SELECT APPLICANT.ID, JOB_POSTING.ID, 'AUTO_GEN', date('now') FROM APPLICANT JOIN EDUCATION ON APPLICANT.ID = EDUCATION.ApplicantID JOIN EDUCATION_REQ ON EDUCATION.FieldTypeID = EDUCATION_REQ.FieldTypeID JOIN JOB_POSTING ON EDUCATION_REQ.ID = JOB_POSTING.EducationReqID JOIN COMPANY ON JOB_POSTING.CompanyID = COMPANY.ID WHERE NOT EXISTS (SELECT 1 FROM MATCHING WHERE MATCHING.ApplicantID = APPLICANT.ID AND MATCHING.PostingID = JOB_POSTING.ID);"

    cursor.execute(delete)
    cursor.execute(insertSelect)
    
    select = "SELECT APPLICANT.ID AS 'APP_ID', APPLICANT.LastName AS 'APP_LastName', COMPANY.Name AS 'COMPANY', JOB_POSTING.Title AS 'POSITION', MATCHING.Status AS 'Status'  FROM APPLICANT JOIN MATCHING ON APPLICANT.ID = MATCHING.ApplicantID JOIN JOB_POSTING ON JOB_POSTING.ID = MATCHING.PostingID JOIN COMPANY ON JOB_POSTING.CompanyID = COMPANY.ID;"
    data = cursor.execute(select)
    db.commit()
    printResults(data, "APPLICANTS WITH MATCHING JOB POSTINGS BASED ON FIELD EDUCATION")    


    
    
    
def main():
    #initialzing database
    dbName = "EmpOfficeDB.db"
    db = sqlite3.connect(dbName)
    cursor = db.cursor()   
    
    # creating instances
    applicant = Applicant(dbName)
    company = Company(dbName)
    jobPosting = JobPosting(dbName)
    recruiter = Recruiter(dbName)

        
    while True:
        #menu 1
        login = input("Enter RecruiterID to log in\nTo create RecruiterID enter 'new'\nEnter 'exit' to exit\n")

        if(login.lower() == "new"):
            recruiter.createRecruiter()
            continue
        if(login.lower() == "exit"):
            break
        
        else:
            if(recruiter.isRecruiter(login) == True):
                while True:
                    #menu 2
                    option = input("\nSelect action:\nEnter 0 to create Company log\nEnter 1 to create Job Posting\nEnter 2 to create Applicant\nEnter 3 to update Applicant\nEnter 4 to delete Applicant\nEnter 5 to show Applicants and Recruiters\nEnter 6 to show average years of experience of job postings\nEnter 7 to show applicants with matching job postings based on education\nEnter 8 to search applicant by education\nPress any key to exit\n")
                    
                    if(option == "0"):
                        company.createCompany()
                    
                    elif(option == "1"):
                        jobPosting.createJobPosting()
                    
                    elif(option == "2"):
                        applicant.createApplicant()
                    
                    elif(option == "3"):
                        applicant.updateApplicant()
                    
                    elif(option == "4"):
                        applicant.deleteApplicant()
                    
                    elif(option == "5"):
                        showApplicantsAndRecruiters(cursor)
                    
                    elif(option == "6"):
                        showYearsofExpAvg(cursor)
                        
                    elif(option == "7"):
                        applicantsAndJobPostings(cursor, db)
                        
                    elif(option == "8"):
                        applicant.searchApplicantsByEdu()
                        
                        
                    else:
                        break 
            else:
                print("\nNo recruiter with id: %s. Please Try again\n" % (login))
                exit

    

#program 
main()
    



