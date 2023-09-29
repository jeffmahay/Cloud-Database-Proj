# Overview


The goal of this project is to create a simple banking app meant to be shared between a couple or family. It includes serveral options such as
adding and withdrawing money from a user's balance, splitting a bill with the option of a flat or percentage rate, as well as a warning system 
that can be configured which will warn of a low balance. The program is used by navigating a menu which will appear with several options to 
choose from, which are selected based on the user's input. 

The purpose of this assignment is to learn about cloud databases. The programs used to accomplish this are python and Google Firestore. 
{Provide a link to your YouTube demonstration. It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of the cloud database.}

[Software Demo Video](https://youtu.be/grtc_HU3CPk)

# Cloud Database

Google Firestore

The database is structured as two collections, one collection which houses documents with user balances and another collection which logs all
of the changes that have been made. 

# Development Environment

Visual Studio Code 

Git 

Python 3.11

# Useful Websites

- [Google Firestore Documentation](https://firebase.google.com/docs/firestore)
- [BYU-Idaho Cloud Database Tutorial](https://byui-cse.github.io/cse310-course/workshops/Cloud_DB/CSE310_Workshop_Cloud_DB.pdf)
- [ChatGPT](https://chat.openai.com/)
# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}

- Add an option to make a withdraw after splitting a bill
- Low balance notification is printed too many times
- Standardize spacing