import requests
import xlsxwriter 
from bs4 import BeautifulSoup
import os
import datetime
import matplotlib.pyplot as plt
import numpy 
RunDist =490
filename ="output_Sun"
firstLetter  = "JD "
worksheetFirstLetter  = ""
links = [
"https://www.thegreyhoundrecorder.com.au/greyhounds/Jett's-Cracker",
"https://www.thegreyhoundrecorder.com.au/greyhounds/Donate-Now",
] 

user_agent ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
headers = {'User-Agent': user_agent}
try : 
    row= numpy.load("rows.npy",allow_pickle=True)
    column= numpy.load("column.npy",allow_pickle=True)
except: 
    numpy.save('rows.npy',{})
    numpy.save('column.npy',{})
    row= numpy.load("rows.npy",allow_pickle=True)
    column= numpy.load("column.npy",allow_pickle=True)
row=row.item()
column=column.item()

#trainers= ['Tina Womann (Lara)',
#            'David Hobby (Nambeelup)',
#            'David Peckham (Allendale East)',
#            'Peter Akathiotis (Reservoir)',
#            'Samantha Grenfell (Mount Wallace)',
#            'Christopher Halse (Nambeelup)',
#            'Christine Robartson (Stake Hill)',
#            'Terrence Erenshaw (Canning Vale)']
trainers = ["Barry Stewart (Glengowrie)",
            "Tina Womann (Lara)",
            "David Hobby (Nambeelup)",
            "David Peckham (Allendale East)",
            "Peter Akathiotis (Reservoir)",
            "Samantha Grenfell (Mount Wallace)",
            "Christopher Halse (Nambeelup)",
            "Christine Robartson (Stake Hill)",
            "Terrence Erenshaw (Canning Vale)"]
maxDistance = RunDist

try :
    pass
    #os.remove("output.xlsx")
except:
    pass

fileData = open("input.txt")
workSheetDatas = fileData.read()
fileData.close()
markers = ['o','v','s','d','H','*','p','P','8','2','3','4','1','>']
markerCounter = 0 ; 
colors = ['r','b','g']
colorsCounter =0 ;
xaxisdata=[]
yaxisdata= []
workbook = xlsxwriter.Workbook(filename+'.xlsx') 
for workSheetData in workSheetDatas.split("\n\n"):
    firstLetter = workSheetData.split("\n")[0]
    RunDist = int(workSheetData.split("\n")[1])
    links = workSheetData.split("\n")[2:]
    print(firstLetter)
    for link in links : 
        if(link=="" or link ==" "):
            continue
        rugV = 0; 

        #link.split("/")[-1][0]
        #print(row[firstLetter.lower()])
        worksheet = workbook.get_worksheet_by_name(worksheetFirstLetter+firstLetter.lower())
        if(worksheet==None):
            worksheet=workbook.add_worksheet(worksheetFirstLetter+firstLetter.lower())
            row[firstLetter.lower()] = 0 
            column[firstLetter.lower()] =0 
        initial = row[firstLetter.lower()]
        tablesnum = 3
        r= requests.get(link,headers=headers)
        soup = BeautifulSoup(r.content,'html.parser')
        #content = ["Date", "Track", "Fin", "Box","Dist", "Grade", "Time","Win T","BON","Marg","PIR","Winner/2nd","SP"] 
        #for i in content:
        #    worksheet.write(0,0,i)
        format = workbook.add_format()
        format.set_bg_color('black')
        highlight = workbook.add_format()
        highlight.set_bg_color('yellow')
        red = workbook.add_format()
        red.set_bg_color('red')
        green = workbook.add_format()
        green.set_bg_color('green')
        pink = workbook.add_format()
        pink.set_bg_color('pink')
        blue = workbook.add_format()
        blue.set_bg_color('blue')

        column[firstLetter.lower()]  = 0;
        row[firstLetter.lower()]+=1 

        try :
            heading = soup.find("div",id="dogProfileContainer").find("h1",class_="mb10").get_text()
            if(heading==""):
                print("The page "+link+" is empty.")
        except: 
            print("The page "+link+" is empty.")
            heading = ""
        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],heading,highlight)
        column[firstLetter.lower()]+=1
        try: 
            heading = soup.find("div",id="dogProfileContainer").find("span",id="breeding").get_text()
        except:
            heading = ""
        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],heading)
        column[firstLetter.lower()]=0
        row[firstLetter.lower()]+=1; 
        try : 
            heading = soup.find("div",id="dogProfileContainer").find("p").get_text()
        except:
            heading=""

        ttt=False
        for trainer in trainers : 
            if(trainer in heading):
                ttt= True 
                break
        if(ttt):
            worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],heading,green)
        else:
            worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],heading)
        row[firstLetter.lower()]+=1; 
        row[firstLetter.lower()]+1;
        tableCounter = 0 
        for tables in soup.find_all("div",class_="mb10") :
            tableCounter+=1;
            if(tablesnum==0):
                break
            
            heading = soup.find("h2",class_="mb10").get_text()
            if("Upcoming" not in heading ):
                worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],heading)
            row[firstLetter.lower()]+=1
            row[firstLetter.lower()]+=1; 

            for head in tables.find("table").find("thead").find_all("th"):
                worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],head.get_text())
                column[firstLetter.lower()]+=1

            if(tableCounter== 3 ):
                worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],"DistTime")
                column[firstLetter.lower()]+=1
                worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],"Time_BON")
                column[firstLetter.lower()]+=1
                worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],"RUG")


            column[firstLetter.lower()]=0 ;
            row[firstLetter.lower()]+=1;


            for body in tables.find("table").find("tbody").find_all("tr"):

                try : 
                    a=datetime.datetime.strptime(body.find_all("td")[0].get_text(),"%d-%b-%y") 
                    b=datetime.datetime.strptime('01-Dec-19',"%d-%b-%y")
                    if ( a < b  ):
                        continue
                except:
                    pass
                yyy=0

                if(tableCounter== 3 ):
                    time_Bon = float(body.find_all("td")[6].get_text())-float(body.find_all("td")[8].get_text())
                    disttime = (float(body.find_all("td")[6].get_text()))
                    if(time_Bon==0):
                        yyy=2
                    #if((body.find_all("td")[2].get_text().strip() == "1st") and float(body.find_all("td")[9].get_text()[:-1]) > 1 ):
                    #    yyy=3;
                    if((int(body.find_all("td")[4].get_text()) >( maxDistance-50)) and (body.find_all("td")[2].get_text().strip() == "1st")):
                        yyy=1
                    if(body.find_all("td")[2].get_text().strip() == "7th" or body.find_all("td")[2].get_text().strip() == "8th" or body.find_all("td")[2].get_text().strip() == "9th" or body.find_all("td")[2].get_text().strip() == "10th"):
                        yyy=3
                    if(body.find_all("td")[2].get_text().strip() == "2nd"):
                        yyy=4
                    if(body.find_all("td")[2].get_text().strip() == "3rd"):
                        yyy=5

                for rowing  in body.find_all("td"):
                    if(yyy==1):
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],rowing.get_text(),highlight)
                    elif(yyy==2):
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],rowing.get_text(),green)
                    elif(yyy==3):
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],rowing.get_text(),red)
                    elif(yyy==4):
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],rowing.get_text(),pink)
                    elif(yyy==5):
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],rowing.get_text(),blue)
                    else:
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],rowing.get_text())
                        if(row[firstLetter.lower()]==initial+6 and column[firstLetter.lower()]==5):
                            rugV= rowing.get_text()
                    column[firstLetter.lower()]+=1

                if(tableCounter== 3 ):
                    disttime = round(disttime,2)
                    time_Bon = round(time_Bon,2)
                    if(yyy==1):
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],float(disttime),highlight)
                        column[firstLetter.lower()]+=1
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],float(time_Bon),highlight)
                    elif(yyy==2):
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],float(disttime),green)
                        column[firstLetter.lower()]+=1
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],float(time_Bon),green)
                    elif(yyy==3):
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],float(disttime),red)
                        column[firstLetter.lower()]+=1
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],float(time_Bon),red)
                    elif(yyy==4):
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],float(disttime),pink)
                        column[firstLetter.lower()]+=1
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],float(time_Bon),pink)
                    elif(yyy==5):
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],float(disttime),blue)
                        column[firstLetter.lower()]+=1
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],float(time_Bon),blue)
                    else:
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],float(disttime))
                        column[firstLetter.lower()]+=1
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],float(time_Bon))
                    if(int(body.find_all("td")[4].get_text())== int(RunDist))   :
                        column[firstLetter.lower()]+=1
                        xaxisdata.append(disttime);
                        yaxisdata.append(int(rugV));
                        worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],int(rugV))
                column[firstLetter.lower()]=0
                row[firstLetter.lower()]+=1
            column[firstLetter.lower()]=0;
          
            for head in tables.find("table").find("thead").find_all("th"):
                worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()],"")
                column[firstLetter.lower()]+=1
            row[firstLetter.lower()]+=1;
            column[firstLetter.lower()]=0;
            tablesnum-=1
        plt.scatter(yaxisdata, xaxisdata, color=colors[colorsCounter],marker=markers[markerCounter],label="ads")
        markerCounter+=1;
        if(colorsCounter == 2):
            colorsCounter= 0 
        else :
            colorsCounter+=1;
        xaxisdata=[]
        yaxisdata=[]
        column[firstLetter.lower()]=0
        row[firstLetter.lower()]+=1
        for i in range(0,100):
            worksheet.write(row[firstLetter.lower()],column[firstLetter.lower()] ,"",format)
            column[firstLetter.lower()]+=1; 
        row[firstLetter.lower()]+=1;
plt.suptitle(firstLetter)
plt.ylabel('time')
plt.xlabel('Rug')
axes = plt.gca()
axes.set_ylim(bottom=0)
numpy.save("rows",row)
numpy.save("column",column)
plt.savefig(firstLetter+ '.png')
workbook.close() 
