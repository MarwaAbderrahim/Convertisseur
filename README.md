----------------------------------------------------------------------------------------
                               Abys Medical converter
----------------------------------------------------------------------------------------
This interface allows you to:
- Convert 'Dicom' series into 'Nifti' files
- Convert 'Dicom' file into 'Nifti' file
- Extract metadata from 'Dicom' files

----------------------------------------------------------------------------------------

To run the app, you must have 'Python' installed on your machine. You will also need some prerequisites, which you can easily install from the file provided with this folder.

1. Downlod the converter folder

2. Install the requirements.txt file using 'pip install -r requirements.txt'

3. Run the 'main' script using 'python main.py'

----------------------------------------------------------------------------------------

- 'Open File': to open one file only, you need to choose the name of the Dicom file.
- 'Open Dir': to open a multiple files at the same directory, you had to choose the folder which contains the Dicom files.
- 'Convert and save': to convert one or many files. You had to choose the folder name where you want to store the NIfTI files. If you want to convert one Dicom file, you should enter the NIfTI filename.
- 'Extract & metadata':to extract metadata in csv file. You should enter the name of the csv file + '.csv'

----------------------------------------------------------------------------------------

Version python utilisé:  Python 3.9.12 

Operating system used : Windows 10

----------------------------------------------------------------------------------------

PS: 
- main.exe and utils should be in the some folder.
- Dicom images should have the some number of slices in the x, and y axses.  
- To bypass 'Windows protected your PC' message in Windows 10 
        - It is necessary to click on the more info link underneath the description to bypass the Windows protected your PC SmartScreen message.
        - You need to select "run anyway" then to run the program on the system.
