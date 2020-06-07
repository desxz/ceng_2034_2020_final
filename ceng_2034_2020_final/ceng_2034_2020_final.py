# Murat Gun
# 170709054
# github.com/desxz/ceng_2034_2020_final
#!/urs/bin/env python

import os
import threading
import time
import requests
import hashlib
import multiprocessing
import signal

urls = [
    "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
    "https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg",
    "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]

initial_directory = '.'
source = 'PythonPNGs/'
duplicate_early = []
duplicates = []
last_duplicates = []
hashes = {}
threads = []


def createParentChild():  #Create Parent and Child Process
    pid = os.fork()

    if pid == 0:
        print("Child process id: ", os.getpid())
        count = 0
        for url in urls:
            download_file(url, source + '/' + repr(count))
            count = count + 1


    else:       #Parent Process wait child and kill after finished child.
        os.wait()
        pid = os.getpid()
        os.kill(pid, signal.SIGTERM)


def createDirectory(path): #Create PythonPNGs folder
    access_rights = 0o777

    try:
        os.mkdir(path, access_rights)
    except OSError:
        print('Creation of the directory %s failed' % path)
    else:
        print('Successfully created the directory %s' % path)


def download_file(url, file_name=None):  # Download file using requests library.
    r = requests.get(url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)



def changeDirectory(getDirectory):  # Change Directory to PythonPNGs.
    first_directory = os.getcwd()
    os.chdir(getDirectory)
    print('Directory Changed as', first_directory + '/' + getDirectory)


def filesinFolder():  # Find count of file in folder that download images.
    print('PythonPNGs folder contains', len(os.listdir(initial_directory)), 'files.')


def findDuplicates():  # Static Control I wrote that function firstly
    for index, filename in enumerate(os.listdir('.')):
        if os.path.isfile(filename):
            index = filename
            with open(filename, 'rb') as f:
                image_hash = hashlib.md5(f.read()).hexdigest()

            if image_hash not in hashes:
                hashes[image_hash] = index

            else:
                duplicates.append((index, hashes[image_hash]))
                print('Image ' + hashes[image_hash] + ' is duplicate of Image ' + index)

def multiThreadDuplicates(filename):  # I edited findDuplicates function to Multithreading.
        if os.path.isfile(filename):
            index = filename
            with open(filename, 'rb') as f:
                image_hash = hashlib.md5(f.read()).hexdigest()

            if image_hash not in hashes:
                hashes[image_hash] = index

            else:
                duplicates.append((index, hashes[image_hash]))
                print('Image ' + hashes[image_hash] + ' is duplicate of Image ' + index)


def takegethash():  # Before Multiprocessing scanning process get hashes from image.
    for index, filename in enumerate(os.listdir('.')):
        if os.path.isfile(filename):
            index = filename
            with open(filename, 'rb') as f:
                image_hash = hashlib.md5(f.read()).hexdigest()
            duplicate_early.append((index, image_hash))




def duplicateFinder(element,array): #Take hash list and find Duplicated elements
    count = 0
    for i in range(len(array)):
        if element[1] == array[i][1]:
            count += 1

        if count > 1 :
            return element




def multiProcessFindDuplicates(): #Multiprocessing Function
    # p0 = multiprocessing.Process(target=duplicateFinder, args=((os.listdir(initial_directory)[0])))
    # p1 = multiprocessing.Process(target=duplicateFinder, args=((os.listdir(initial_directory)[1])))
    # p2 = multiprocessing.Process(target=duplicateFinder, args=((os.listdir(initial_directory)[2])))
    # p3 = multiprocessing.Process(target=duplicateFinder, args=((os.listdir(initial_directory)[3])))
    # p4 = multiprocessing.Process(target=duplicateFinder, args=((os.listdir(initial_directory)[4])))
    #
    # p0.start()
    # time.sleep(0.1)
    # p1.start()
    # time.sleep(0.1)
    # p2.start()
    # time.sleep(0.1)
    # p3.start()
    # time.sleep(0.1)
    # p4.start()

    with multiprocessing.Pool(5) as Pool:
        list_duplicate = Pool.starmap(duplicateFinder,([duplicate_early[0],duplicate_early],[duplicate_early[1],duplicate_early],[duplicate_early[2],duplicate_early],[duplicate_early[3],duplicate_early],[duplicate_early[4],duplicate_early]))
    for val in list_duplicate:
        if val != None:
            duplicates.append(val)
    print(duplicates)
    print('Image ' + duplicates[1][0] + ' and Image ' + duplicates[0][0] + ' are duplicated.') #I made it staticly because ı made second listing process using non-multiprocess so array will be same always.
    print('Image ' + duplicates[3][0] + ' and Image ' + duplicates[2][0] + ' are duplicated.')





def multiThreadFindDuplicates(): # MultiThreading function the process
    for image in os.listdir(initial_directory):
        process = threading.Thread(target=multiThreadDuplicates, args=image)
        process.start()
        threads.append(process)

    for process in threads:
        process.join()


createDirectory(source)
createParentChild()
changeDirectory(source)
filesinFolder()
takegethash()
multiProcessFindDuplicates()

#To run with multithreadig, remove takegethash() and multiProcessFindDuplicates() and write multiThreadFindDuplicates()
