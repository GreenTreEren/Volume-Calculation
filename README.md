# What is OpenTimber?

  OpenTimber is a Python application for calculating timber volumes using the Huber and Smalian formulas.
  This open-source project is designed for simplicity and portability.
  You can run the script directly or use pre-built executables for Linux and macOS.


## HOW TO USE:
  This program does not require additional libraries, simply run 'python3 OpenTimber.py'

## Formulas:
  - Huber Formula:  
    &nbsp;V = (π / 4) × (d / 100)^2 × L

  Where:  
    &nbsp;V = volume in cubic meters (m³)  
    &nbsp;d = diameter at the middle of the log in centimeters (cm)  
    &nbsp;L = length of the log in meters (m)  

  This formula assumes the cross-sectional area at the middle of the log represents the average area.  


  - Smalian Formula:  
    &nbsp;V = (π / 8) × L × [ (d1 / 100)^2 + (d2 / 100)^2 ]  

  Where:  
    &nbsp;V = volume in cubic meters (m³)  
    &nbsp;d1 = small-end diameter in centimeters (cm)  
    &nbsp;d2 = large-end diameter in centimeters (cm)  
    &nbsp;L = length in meters (m)  

  This formula averages the cross-sectional areas at both ends of the log.

## Features & Instructions

  - Select a Formula:
  Choose either Huber or Smalian from the main menu.
  
  - Input Your Values:
  Enter the relevant measurements.
  
  - Calculate:
  Click the Calculate button to compute volume.
  
  - Navigate Back:
  Use the Back button to return to the main menu without losing your results.

  - Save Results:
  Click Save to File, choose a destination folder, and enter a file name to export your data as a .csv file.

  - Clear Calculations:
  Use Clear All (top-right corner) to delete all results.
  Click the X button next to a result to delete a single entry.

  - Scroll Through Results:
  Use the scrollbar or mouse wheel to browse previous calculations.

  This is an on-going project. 
  New features and improvements will be developed continuously.


![Interface](https://github.com/user-attachments/assets/c618b767-3bce-4c15-8ec8-43f6f38afb30)


![records](https://github.com/user-attachments/assets/186014b5-59c4-44fb-b13d-0d2d52f334e2)
