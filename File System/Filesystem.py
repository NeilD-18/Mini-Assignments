import typing
import random as r 

#Click `Run` in the top left corner to run the command line program. Output will appear in the "Program Output" tab in the right pane.

#This challenge was a lot of fun and I spent my weekend working on making the code robust and with strong adherence to good OOP principles. I created File and Folder classes to solve this problem.Instead of spending only 2-3 hours on this I wanted to try to fully complete the challenge. 
    

#File Class. File has a file type and name and its assigned a random even file ID. For a larger file system we'd have to ensure a duplicate File ID doesn't get created. 
class File: 

    def __init__(self, fileName: str, fileType: str):
        self.__fileName = fileName
        self.__fileType = fileType 
        self.__fileID = r.randint(0,100000) * 2

    def get_Name(self):
        return self.__fileName

    def get_fileType(self): 
        return self.__fileType
    
    def get_ID(self):
        return str(self.__fileID)

    def __str__(self, indent=0):
        return f"{self.__fileType}({self.__fileName})"

#Folder class. Folders hold other files. Methods to add files, access file contents and remove files. 
class Folder: 
    
    def __init__(self, folderName: str):
        self.__folder = File(folderName, "folder")
        self.__contents = []
        
    def add_file(self, file): 
        self.__contents.append(file)
    
    def get_ID(self):
        return str(self.__folder.get_ID())

    def get_fileType(self):
        return "folder"
    
    def contents(self):
        return self.__contents
    
    def get_Name(self):
        return self.__folder.get_Name()

    def remove_file(self, file):
        if file in self.__contents:
            self.__contents.remove(file)
        else:
            print("File doesn't exist")

   
    #Here we're keeping track of an indent to maintain the structure of the filesystem. Folders have files listed with an indent. 
    def __str__(self, indent=0):
        to_return = f"folder({self.__folder.get_Name()})"
        for file in self.__contents:
            if file.get_fileType() == "folder":
                fileName = file.__str__(indent+2)
            else:
                fileName = file.__str__()
            to_return += f"\n{' ' * (indent + 2)}  ->{fileName}"
        return to_return 
    

#File system class. File system is a dictionary with the keys as File IDs and values are the actual objects themselves. The file system itself only has one key and one value since all files are stored inside "MyDocuments" which is the root folder. 
class FileSystem:
    
    def __init__(self):
        self.__root = Folder("MyDocuments")
        self.__rootId = str(self.__root.get_ID())
        self.__filesystem = {self.__rootId : self.__root}
        self.__num_of_dashboards = 0 
        self.__num_of_worksheets = 0 
    
    # Feel free to modify the parameter/return types of these functions
    # as you see fit. Please add comments to indicate your changes with a 
    # brief explanation. We care more about your thought process than your
    # adherence to a rigid structure.
    
    #Instead of checking each file, we keep a count going and incremement by 1 when a new file is added and its a dashboard/worksheet
    def get_total_dashboards(self) -> int:
        return self.__num_of_dashboards
    
    def get_total_worksheets(self) -> int:
        return self.__num_of_worksheets
    
    

    #I recursively searched through the filesystem with the use of helper functions. Since we're checking every file in the file system. Time complexity is O(n) where n is the amount of files in the file system. 
    def add_new_file(self, fileName: str, fileType: str, folderId: int):
        if fileType == "folder":
            newFile = Folder(fileName)
        
        elif fileType == "dashboard":
            self.__num_of_dashboards += 1
            newFile = File(fileName, fileType)
        
        elif fileType == "worksheet":
            self.__num_of_worksheets += 1
            newFile = File(fileName, fileType)
        
        else:
            newFile = File(fileName, fileType)
        
        #This is essentially adding the file to the root folder since the only file in the filesystem structure is the root folder 
        if str(folderId) in self.__filesystem:
            self.__filesystem[str(folderId)].add_file(newFile)
        
        else:
            self.__helper_search_path(newFile, str(folderId))
            
    #recursively search through the file directory, checking nested folders as well. 
    def __helper_search_path(self, newFile, targetFolderID, current_folder = None):
        if current_folder is None:
            current_folder = self.__filesystem[self.__rootId]
        
        for content in current_folder.contents():
            if content.get_fileType() == "folder" and content.get_ID() != str(targetFolderID):
                if content.contents():
                    self.__helper_search_path(newFile, targetFolderID, content)

            elif content.get_ID() == str(targetFolderID):
                content.add_file(newFile)
                return 0

               
    def get_file_id(self, fileName: str, folderId):
        if folderId == None:
            return self.__root.get_ID()
        else:   
            return self.__helper_search_path_id(fileName, self.__filesystem[self.__rootId], folderId)

    
    #Helper recursive function to search inside a folder. Will return the ID of the target file. 
    def __search_inside_folder(self, current_folder: Folder, targetName):
        for content in current_folder.contents():
            if content.get_fileType() == "folder" and content.get_Name() != targetName:
                nested_ID = self.__search_inside_folder(content, targetName)
                if nested_ID is not None:
                    return nested_ID
            
            if content.get_Name() == targetName:
                return content.get_ID()
           
    #Helper recursive function to search the filesystem for a target File. Will return the ID. 
    def __helper_search_path_id(self, targetName, current_folder, folderId):
        for content in current_folder.contents():
            if content.get_fileType() == "folder" and content.get_Name() != str(targetName):
                nested_id = self.__search_inside_folder(content, targetName)
                if nested_id is not None:
                    return nested_id

            elif content.get_Name() == str(targetName):
                return content.get_ID()
        
    
    #Helper recursive function to move files. This function will return the file we want to move and its parent folder
    def __helper_search_file(self, targetFileId, current_folder):
        for content in current_folder.contents():
            if content.get_fileType() == "folder" and content.get_ID() != str(targetFileId):
                nested_file= self.__helper_search_file(targetFileId, content)
                if nested_file is not None:
                    return nested_file

            elif content.get_ID() == str(targetFileId):
                return (content,current_folder) #returning a tuple because we also want the parent folder. This way we can remove the file from the parent folder so there is no duplicate copies 
        
    
    def move_file(self, fileId: int, newFolderId: int):
        #locate file and parent folder
        #can't move the root folder because everything is contained in the root folder
        if fileId == self.__rootId:
            print("Can't move root folder")
        
        else:
            file_and_parent_folder = self.__helper_search_file(fileId, self.__filesystem[self.__rootId])

            if file_and_parent_folder is None:
                print("File does not exist")
                return 0

            fileToMove = file_and_parent_folder[0]
            parentFolder = file_and_parent_folder[1]

            if str(newFolderId) == str(self.__rootId):
                targetFolder = self.__filesystem[self.__rootId]
            
            else:
                targetFolderGrouping = self.__helper_search_file(newFolderId, self.__filesystem[self.__rootId])
            
                if targetFolderGrouping is None:
                    print("Folder does not exist")
                    return 0
                else: 
                    targetFolder = targetFolderGrouping[0]
            
            #Remove file from parent folder and move it to target folder 
            parentFolder.remove_file(fileToMove)
            targetFolder.add_file(fileToMove)
        
        return 0
        

      
    
    def get_files(self, folderId: int) -> typing.List[str]:
        #See if its the root Id 
        if str(folderId) == str(self.__rootId):
            targetFolder = self.__filesystem[self.__rootId]

        else:
            targetFolderGrouping = self.__helper_search_file(folderId, self.__filesystem[self.__rootId])
            
            if targetFolderGrouping is None:
                    print("Folder does not exist")
                    
            else: 
                targetFolder = targetFolderGrouping[0]
        return_list = []
        
        #Instead of using built in string method, manually print. This is because if we use the string method of the folder, it will show the file structure, and we just need the file name if its a nested folder. 
        for content in targetFolder.contents():
            content_as_str = f"{content.get_fileType()}({content.get_Name()})"
            return_list.append(content_as_str)
        return return_list



    #Files and folders have string methods so we just have to print the root folder. 
    def print_files(self) -> None:
        print(self.__filesystem[self.__rootId])
        
        
            

      

    
    
# /////////////////////////////////////////////////////////
# // YOU DO NOT NEED TO MAKE CHANGES BELOW UNLESS NECESSARY
# /////////////////////////////////////////////////////////
    
# PLEASE ENSURE run_example() RUNS BEFORE SUBMITTING.
def run_example():
    fs = FileSystem()
    
    rootId = fs.get_file_id("MyDocuments", None)
    print(rootId) #For test
    fs.add_new_file("draft", "folder", rootId)
    fs.add_new_file("complete", "folder", rootId)
    draftId = fs.get_file_id("draft", rootId)
    print(draftId) # For test
    completeId = fs.get_file_id("complete", rootId)
    print(completeId) #For test
    fs.add_new_file("foo", "worksheet", draftId)
    fs.add_new_file("bar", "dashboard", completeId)
    fooId = fs.get_file_id("foo", draftId)
    fs.move_file(fooId, completeId)
    
    print(", ".join(fs.get_files(rootId)))
    print(", ".join(fs.get_files(draftId)))
    print(", ".join(fs.get_files(completeId)))
          
    fs.add_new_file("project", "folder", draftId)
    projectId = fs.get_file_id("project", draftId)
    for filename in ["page1", "page2", "page3"]:
        fs.add_new_file(filename, "worksheet", projectId)
    fs.add_new_file("cover", "dashboard", projectId)
    fs.move_file(projectId, completeId)
    projectId = fs.get_file_id("project", completeId)
    coverId = fs.get_file_id("cover", projectId)
    fs.move_file(coverId, rootId)
    
    print(", ".join(fs.get_files(rootId)))
    print(", ".join(fs.get_files(draftId)))
    print(", ".join(fs.get_files(completeId)))
    print(", ".join(fs.get_files(projectId)))

    print(fs.get_total_dashboards())
    print(fs.get_total_worksheets())
    fs.print_files()

def ask_for_int(question: str) -> int:
    val = input(question)
    try:
        return int(val)
    except:
        print('Please enter a valid integer value\n')
        return ask_for_int(question)
    
def ask_question():
    fs = FileSystem()

    rootId = fs.get_file_id("MyDocuments", None)
    print(rootId)
    running = True
    while(running):
        command = ask_for_int("\nEnter an integer to indicate a command: \n[1] get_total_dashboards\n[2] get_total_worksheets\n[3] add_new_file\n[4] get_file_id\n[5] move_file\n[6] get_files \n[7] print_files\n[8] exit\n")
        if command == 1:
            totalDashboards = fs.get_total_dashboards()
            print("There are {0} dashboards in the file system.".format(totalDashboards));
        elif command == 2:
            totalWorksheets = fs.get_total_worksheets()
            print("There are {0} worksheets in the file system.".format(totalWorksheets));
        elif command == 3:
            fileName = input("Enter a new file name: ")
            fileType = input("Enter a file type (worksheet, dashboard, or folder): ")
            folderId = ask_for_int("Enter a folder id where you'd like to put this file: ")
            fs.add_new_file(fileName, fileType, folderId);
            print("{0} has been added to folder {1}".format(fileName, folderId))
        elif command == 4:
            fileName = input("Enter the file name: ")
            folderId = ask_for_int("Enter the folder id: ")
            fileId = fs.get_file_id(fileName, folderId)
            print("{0} is file {1}".format(fileName, fileId));
        elif command == 5:
            fileId = ask_for_int("Enter a file id:")
            newFileId = ask_for_int("Enter the folder id where you'd like to move this file: ")
            fs.move_file(fileId, newFileId);
            print("Successfully moved file {0} to folder {1}".format(fileId, newFileId))
        elif command == 6:
            folderId = ask_for_int("Enter a folderId:")
            fileNames = fs.get_files(folderId)
            if (len(fileNames) == 0):
                print("There are no files in folder {0}".format(folderId))
            else:
                print("The following files are in folder {0}: ".format(folderId))
                for fileName in fileNames:
                    print("\t{0}".format(fileName))
        elif command == 7:
            fs.print_files()
        elif command == 8:
            print("Exiting program.")
            running = False
        else:
            print("Invalid command: {0}. Please try again.\n".format(command))
              
print('run_example output:')
run_example()
print('ask_question output:')
ask_question()




#Ideally we'd use a testing suite and perform unit tests but these are worked out versions of what the file system should develop like. 
''' 
Testing
->f(my doc)
    ->f(draft)
         ->ws(foo)
    ->f(complete)  
          ->db(bar)

FIRST MOVE:

->f(my doc)
    ->f(draft)

    ->f(complete)  
          ->db(bar)
           ->ws(foo)

ADDING PROJECT FILE:

->f(my doc)
    ->f(draft)
         ->f(project)
              ->ws(page1)
              ->ws(page2)
               ->ws(page3)
                ->db(cover)
    ->f(complete)  
          ->db(bar)
           ->ws(foo)

SECOND MOVE:

->f(my doc)
    ->f(draft)
    ->f(complete)  
          ->db(bar)
           ->ws(foo)
             ->f(project)
                  ->ws(page1)
                  ->ws(page2)
                  ->ws(page3)
                   ->db(cover)

LAST MOVE: (Final State)

->f(my doc)
    ->f(draft)
    ->f(complete)  
          ->db(bar)
           ->ws(foo)
             ->f(project)
                  ->ws(page1)
                  ->ws(page2)
                  ->ws(page3)
    ->db(cover)





Get_files test:
First move -> 

get_files(root_id) ->
folder(draft), folder(complete)

get_files(draft_id) ->
" " (empty)

get_files(completeId)->
dashboard(bar), worksheet(foo)


Final move ->
get_files(root_ID) - >
folder(draft), folder(complete), dashboard(cover)

get_files(draft_ID) - > 
" " (empty)

get_files(complete_Id) - > 
dashboard(bar), worksheet(food), folder(project)

get_files(project_Id) - > 
worksheet(page1), worksheet(page2), worksheet(page3)

Total # of DB -> 2
Total # of WS ->4

'''
