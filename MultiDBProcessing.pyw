import os,sys,re, time
from distutils.dir_util import copy_tree
from shutil import copyfile,copy,rmtree
from tkinter import messagebox

def checkForListOfTerritories(cwd):
    
    dir_list_with_territories = []
    listOfTerritories = ["A","B","C","D","E","F","G","H","I","J","K","L"]
    for dir_name in os.listdir('.'):
        if os.path.isdir(dir_name):
            if((len(dir_name) == 1) and (dir_name in listOfTerritories) and (dir_name.isupper())):
                dir_list_with_territories.append(dir_name)
			
    if(len(dir_list_with_territories) > 1):
        #print("\nAvailable territories in this directory are: "+str(dir_list_with_territories)+"\n")
        return dir_list_with_territories
    else:
        messagebox.showerror('Error',"Directory should have atleast 2 territories (with names A, B, C, D etc in caps letters) to generate multiDB!!. Please check directory: "+str(cwd)+"\n")
        TkObject.destroy()			
        sys.exit(0)		
				

def createFinalOutputDir(cwd):

    final_directory = os.path.join(cwd,r'MiltiDB_output')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
        return final_directory
    else:
        messagebox.showerror('Error',"Folder name \"MiltiDB_output\" already exist in path "+cwd+". So please delete this folder and re-execute this tool."+"\n")
        TkObject.destroy()			
        sys.exit(0)


def ensureTempFolderNotExistInCurrentDir(cwd):

    final_directory = os.path.join(cwd,r'Temp')
    if os.path.exists(final_directory):
        messagebox.showerror('Error',"Folder name \"Temp\" exist in path "+cwd+". So please delete this folder and re-execute this tool."+"\n")
        TkObject.destroy()			
        sys.exit(0)		
		
def removeDir(dir_path):
    for file in os.listdir(dir_path): 
        if os.path.isfile(dir_path+"\\"+file):
            os.remove(dir_path+"\\"+file)

    if os.path.isdir(dir_path+"\\infos"):
        os.rmdir(dir_path+"\\infos")
    os.rmdir(dir_path)
		
def convertMultiTerritiryFiles(territoryName, IncNumber, cwd, territoyOutputFiles, percentageOfCompletion):
    
    #Copy territory files into TEMP folder
    copy_tree(cwd+"\\"+str(territoryName),cwd+"\\Temp")
    #print("\nTerritory \""+territoryName+"\" binary files are renaming... please wait...")	
    statusBar.set("Percentage of execution completed: "+str(percentageOfCompletion)+"%. Territory \""+territoryName+"\" binary files are renaming... please wait...")	
	
    #rename only required file name
    for file_name in os.listdir(cwd+"\\Temp"):
        if os.path.isfile(cwd+"\\Temp\\"+file_name):
            fileNumbers = file_name.split('.')
            if(fileNumbers[0].isdigit() and fileNumbers[1].isdigit()):
                os.rename(cwd+"\\Temp\\"+str(file_name), cwd+"\\Temp\\"+str(fileNumbers[0])+"."+str(int(fileNumbers[1])+IncNumber))
                time.sleep(0.05)

    statusBar.set("Percentage of execution completed: "+str(percentageOfCompletion)+"%. Territory \""+territoryName+"\" binary files copying to output folder... please wait...")
    #print("\nTerritory \""+territoryName+"\" binary files copying to output folder... please wait... ")				
    #copy file names into "MiltiDB_output" folder with XML file				
    for file_name in os.listdir(cwd+"\\Temp"):
        if os.path.isfile(cwd+"\\Temp\\"+file_name):
            fileNumbers = file_name.split('.')
            if(fileNumbers[0].isdigit() and fileNumbers[1].isdigit()):
                copy(cwd+"\\Temp\\"+file_name,territoyOutputFiles) 				
                time.sleep(0.05)				
            elif(fileNumbers[1] == "xml"):
                copy(cwd+"\\Temp\\"+file_name,territoyOutputFiles) 	
                time.sleep(0.05)				

    #remove Temp Dir
    removeDir(cwd+"\\Temp")

				
def script_exe(cwd,TkObject_ref,statusBarText):
 
    global TkObject,statusBar
    TkObject = TkObject_ref
    statusBar = statusBarText

    statusBar.set("Files Analysis in progress...")
    #print(" ********* Files Analysis in progress... ***************")
    os.chdir(cwd)
	
	# 1. Check for list of territories in current directory.
    dir_list_with_territories = list(checkForListOfTerritories(cwd))
    dir_list_with_territories.sort()
		
    # 2.a. Create Folder "MiltiDB_output" in current working directory where results will be dumped.		
    output_dir = createFinalOutputDir(cwd)

    # 2.b. When execution terminated abruptly, then Temp file remains in selected directory. So ensure that this folder is delted. 	
    ensureTempFolderNotExistInCurrentDir(cwd)
	
    # 3. Copy first territory files into "output_dir"
    percentageOfCompletion = ((0/len(dir_list_with_territories))*100)
    statusBar.set("Percentage of execution completed: "+str(percentageOfCompletion)+"%. Territory A binary files are copying to output folder. Please wait...")
    #print("\nTerritory A binary files are copying to output folder... please wait...")			
    copy_tree(cwd+"\\"+str(dir_list_with_territories[0]),output_dir)
	
    # 4. Convert multi territory files
    territoryIncNumber = 0
    for territoryNumber in range(1,len(dir_list_with_territories)):
        final_directory = os.path.join(cwd,r'Temp')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        percentageOfCompletion = (((territoryNumber)/len(dir_list_with_territories))*100)
        convertMultiTerritiryFiles(dir_list_with_territories[territoryNumber], territoryIncNumber+16, cwd, output_dir, percentageOfCompletion)
        territoryIncNumber = territoryIncNumber + 16

    statusBar.set("DONE!")		
    messagebox.showinfo('DONE!!',"Final multiDB with all territories present in path: "+str(output_dir)+"\n\n")
    TkObject.destroy()
    sys.exit()