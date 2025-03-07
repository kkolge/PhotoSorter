# Photo Manager

Delete unwanted photos.

## Description
*This is work in progress* 

We all click lots of photos from cell phone but cleaning up unwanted photos before backing up is alway a challange. I am sure, most of us just backup without removing the unwanted photos thinking we will do it later and that never happens.

### Dependencies
1. This was built using python 3.10 . It should however work with most of the versions of python 3. 
2. Pillow
3. pytest & pytest-cov - for testing
4. pyinstaller - for biulding executable

### Installing

git clone - https://github.com/kkolge/PhotoSorter.git

#### Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

#### Install requirements
pip install -r requirements.txt

### Building 

If you want to build an executable, use the Makefile or run 
pyinstaller --no-console --one-file main.py

### Executing Program

1. You can simply run the program using 
    python main.py

2. if you build the application, just run it by double-clicking on the executable in the dist folder.
Please note it generates some folders and log files so its a good idea to move it to a separate folder before running the executable. 

## Authors
    Name: Ketan Kolge
    email: k_kolge@yahoo.com

## Version History
0.1
  * This is the initial release of the application

## License
This project is licensed under the MIT License - see the LICENSE.md file for details

## Improvements
1. Presently the application moved the video to videos folder. It is not designed to process the videos at this time. This is a required enhancement and will be done soon. This will require lot of changes as will need to either use OpenCv or move the application to PySide6. 
2. The deleted files are still stored in the deleted folder. A verification and cleanup functionality can be added if required
3. In the session log, add the files that are deleted. This will help to validate the exact files that are deleted
4. Basic image enhancements - crop, autocorrect, etc. can be added if required.