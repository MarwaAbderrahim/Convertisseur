############# Importation 
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from glob import glob
import os
from PIL import Image, ImageTk
from DicomRTTool import DicomReaderWriter
import SimpleITK as sitk
import pydicom as dicom
import pandas as pd
import glob
from tqdm import tqdm
import cv2
from PIL import Image
import csv as csv_lib
import pydicom

############# Progress bar
def progress_bar(master):
    progress_bar = Progressbar(master, mode='determinate', orient='horizontal', length=500)
    progress_bar.pack(pady=(20,0))

    return progress_bar
############# page 1 : Home page 
def call_home_page():
    root.geometry('500x600')
    home_page = Frame(root, bg=bg)
    home_page.grid(row=0, column=0, sticky='nsew')
    title = Label(home_page, text='Abys Medical Converter', bg=bg, fg='Black', font='Arial 30 ')
    title.pack(pady=(20,0))
    image = Image.open('utils/img.png')
    image=image.resize((250,100))
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image = photo)
    label.image = photo
    root.configure(background='white')
    label.grid(row=1,column=0)
    buttons_frame = Frame(home_page, bg=bg)
    buttons_frame.pack( padx=10,pady=40)

    dicom_to_nifti_button = Button(buttons_frame, text='Dicom\nto\nNifti', font='none 20 bold', width=15, bg='black',fg='white', command=dicom_to_nifti_page)
    dicom_to_nifti_button.pack(pady=(60,0))

############# page 2 : Dicom to nifti page 
def dicom_to_nifti_page():
    global text_message_d_n
    root.geometry('500x600')
    dicom_to_nifti = Frame(root, bg=bg)
    dicom_to_nifti.grid(row=0, column=0, sticky='nsew')

    title = Label(dicom_to_nifti, text='Dicom to Nifti', bg='black',fg='white', font='Arial 15 bold')
    title.pack()

    open_buttons = Frame(dicom_to_nifti, bg=bg)
    open_buttons.pack(pady=(30,0))

    open_file = Button(open_buttons, text='Open file', font='none 20 bold', width=10, bg='coral',fg='black', command=call_open_file_dicom_to_nifti)
    open_file.grid(row=0, column=0, padx=(0,20))

    open_dir = Button(open_buttons, text='Open Dirs', font='none 20 bold', width=10, bg='coral',fg='black', command=call_open_dir_dicom_to_nifti)
    open_dir.grid(row=0, column=1, padx=(20,0))

    convert_save = Button(dicom_to_nifti, text='Convert & Save', font='none 20 bold', bg='coral',fg='black', command=call_convert_save_dicom_to_nifti)
    convert_save.pack(pady=(40,0))

    convert_save = Button(dicom_to_nifti, text='Extract metadata', font='none 20 bold', bg='coral',fg='black', command=meta)
    convert_save.pack(pady=(40,0))

    text_message_d_n = Label(dicom_to_nifti,text='Choose file or dir', font='none 9', bg='coral',fg='black',)
    text_message_d_n.pack(pady=(20,0))

    home_button = Button(dicom_to_nifti, text='Home', command=call_home_page, font='none 13 bold', width=10, bg='coral',fg='black',)
    home_button.pack(pady=(40,20))

############# page 2 : Functions to one and convert dicom files            
def call_open_file_dicom_to_nifti():
    global flag_dicom_nifti
    global in_path_dicom_nifti
    global text_message_d_n

    in_path_dicom_nifti = filedialog.askdirectory()
    if in_path_dicom_nifti: 
        flag_dicom_nifti = 1
        text_message_d_n.config(text='You opened: \n' + in_path_dicom_nifti)

def call_open_dir_dicom_to_nifti():
    global flag_dicom_nifti
    global in_path_dicom_nifti
    global text_message_d_n

    in_path_dicom_nifti = filedialog.askdirectory()

    if in_path_dicom_nifti:
        flag_dicom_nifti = 2
        text_message_d_n.config(text='You opened: \n' + in_path_dicom_nifti)

def call_convert_save_dicom_to_nifti():
    global text_message_d_n
    global image
    global images
    global out_path
    text_message_d_n.config(text='Converting...')

    if flag_dicom_nifti == 1 and in_path_dicom_nifti:
        out_path = filedialog.asksaveasfilename()
        if out_path:
            reader = DicomReaderWriter()
            reader.walk_through_folders(in_path_dicom_nifti)
            reader.get_images()
            sitk.WriteImage(reader.dicom_handle, out_path + '.nii.gz')
            text_message_d_n.config(text='File saved at\n' + out_path + '.nii.gz')
    if flag_dicom_nifti == 2 and in_path_dicom_nifti:
        images = glob.glob(in_path_dicom_nifti + '/*')
        out_path = filedialog.askdirectory()
        if out_path:
            for i, image in enumerate(images):
                text_message_d_n.config(text='Converting...')
                reader = DicomReaderWriter()
                reader.walk_through_folders(image)
                reader.get_images()
                sitk.WriteImage(reader.dicom_handle, out_path + '/' + os.path.basename(image) + str(i).zfill(len(str(len(images)))) + '.nii.gz')
                #dicom2nifti.dicom_series_to_nifti(image, out_path + '/' + os.path.basename(image) + str(i).zfill(len(str(len(images)))) + '.nii.gz')
                text_message_d_n.config(text='Files saved at\n' + out_path)

############# page 2 : Function to extract csv file                
def meta () :
    folder_path = in_path_dicom_nifti
    out_path = filedialog.asksaveasfilename()
    images_path = os.listdir(folder_path)
    metadata=[]
    data = []
    columns_list = ['Patient_ID' , 'Sex' , 'Birth_date' , 'Age' , 'Modality' , 'Manufacturer' , 'Institution_Name' , 'Study_Description' , 'Slice_Thickness']
    text_message_d_n.config(text='Extracting...')
    for i in tqdm(range(len(images_path))):
       t = os.listdir(folder_path+'/'+images_path[i])
       img_path = folder_path+'/'+images_path[i]+'/'+t[1]
       ds = pydicom.filereader.dcmread(img_path)
       print(ds)
       data.append([ds.PatientID, ds.PatientSex, ds.PatientBirthDate, ds.PatientAge[:-1], ds.Modality, ds.Manufacturer.replace(" ","_"), ds.InstitutionName.replace(" ","_"), ds.StudyDescription.replace(" ","_"), ds.SliceThickness])
    with open(out_path, 'w', encoding='UTF8', newline='') as f:
       writer = csv_lib.writer(f, delimiter = ";")
       writer.writerow(columns_list)
       writer.writerows(data) 
       text_message_d_n.config(text='Files saved at\n' + out_path)


############# The main function 
if __name__ == '__main__':
    global in_path_image_dicom
    global in_path_dicom_image
    global in_path_nifti_dicom
    global in_path_dicom_nifti

    global flag_image_dicom
    global flag_dicom_image 
    global flag_nifti_dicom 
    global flag_dicom_nifti

    flag_image_dicom = 0
    flag_dicom_image = 0
    flag_nifti_dicom = 0
    flag_dicom_nifti = 0

    bg = 'white'
    root = Tk()
    root.geometry('500x600')
    root.title('Abys Converter')
    root.iconbitmap('utils/logo.ico')

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    call_home_page()

    root.mainloop()
    
