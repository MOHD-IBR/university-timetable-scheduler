# University Timetable Scheduler

This is a small prototype of a university timetable scheduling system. We made it as part of our Final Year Project (FYP).

It uses Python and Google OR-Tools (CP-SAT) to automatically generate a timetable based on sample university data and some basic constraints.

## Features

- Generates timetable for given courses
- Avoids teacher clashes
- Avoids room clashes
- Avoids batch clashes
- Considers teacher availability
- Assigns rooms according to batch size and room capacity
- Only schedules classes during university working hours
- Avoids the break period
- Validates the generated timetable and shows results

## Technologies Used

- Python
- Google OR-Tools CP-SAT

## Project Structureuniversity-timetable-scheduler/
├── scheduler.py
└── README.mdtext## How to Run

1. Make sure Python is installed
2. Install the required library:
   ```bash
   pip install ortools
Open terminal in the project folder
Run the program:Bashpython scheduler.py
The program will generate a timetable and print the validation results in the terminal.Current ScopeThis is just an early prototype. Right now it uses sample data (courses, teachers, rooms, batches, availability, and capacities) that are hardcoded in the Python file. The main focus is on the core scheduling logic and basic constraint checking.Future Improvements
Support for lab courses and dedicated lab rooms
Database integration instead of hardcoded data
Simple user interface for generating timetable
Faculty preference based scheduling
Option to manually adjust and repair the timetable
NoteThis project is part of our academic Final Year Project. The current version only shows the initial scheduling engine. We plan to improve and extend it further.
