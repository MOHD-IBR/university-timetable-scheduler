import random
from ortools.sat.python import cp_model


courses = ["AI", "Database", "Operating Systems"]
teachers = ["Ahmed", "Ali"]
rooms = ["Room 101", "Room 102"]
batches = ["BSCS-5A", "BSCS-5B"]

days = ["Monday", "Tuesday", "Wednesday"]
timeSlots = ["8-9", "9-10", "10-11", "11-12", "12-1", "1-2", "2-3"]


universityStart = 8
universityEnd = 15

breakStart = 13
breakEnd = 14


courseTeachers = {
    "AI": "Ahmed",
    "Database": "Ahmed",
    "Operating Systems": "Ali"
}

courseBatches = {
    "AI": "BSCS-5A",
    "Database": "BSCS-5A",
    "Operating Systems": "BSCS-5B"
}

courseHours = {
    "AI": 2,
    "Database": 2,
    "Operating Systems": 2
}


teacherAvailability = {
    "Ahmed": {
        ("Monday", "8-9"),
        ("Monday", "9-10"),
        ("Monday", "10-11"),
        ("Tuesday", "9-10"),
        ("Tuesday", "10-11"),
        ("Tuesday", "11-12"),
        ("Wednesday", "2-3")
    },

    "Ali": {
        ("Monday", "9-10"),
        ("Monday", "11-12"),
        ("Monday", "12-1"),
        ("Tuesday", "10-11"),
        ("Tuesday", "11-12"),
        ("Wednesday", "10-11"),
        ("Wednesday", "12-1"),
        ("Wednesday", "2-3")
    }
}


roomCapacity = {
    "Room 101": 30,
    "Room 102": 60
}

batchSize = {
    "BSCS-5A": 50,
    "BSCS-5B": 25
}


model = cp_model.CpModel()

schedule = {}


for course in courses:
    for room in rooms:
        for day in range(len(days)):
            for timeSlot in range(len(timeSlots)):

                schedule[course, room, day, timeSlot] = model.NewBoolVar(
                    f"{course}_{room}_{day}_{timeSlot}"
                )


for course in courses:

    model.Add(
        sum(
            schedule[course, room, day, timeSlot]
            for room in rooms
            for day in range(len(days))
            for timeSlot in range(len(timeSlots))
        ) == courseHours[course]
    )


for teacher in teachers:
    for day in range(len(days)):
        for timeSlot in range(len(timeSlots)):

            model.Add(
                sum(
                    schedule[course, room, day, timeSlot]
                    for course in courses
                    for room in rooms
                    if courseTeachers[course] == teacher
                ) <= 1
            )


for room in rooms:
    for day in range(len(days)):
        for timeSlot in range(len(timeSlots)):

            model.Add(
                sum(
                    schedule[course, room, day, timeSlot]
                    for course in courses
                ) <= 1
            )


for batch in batches:
    for day in range(len(days)):
        for timeSlot in range(len(timeSlots)):

            model.Add(
                sum(
                    schedule[course, room, day, timeSlot]
                    for course in courses
                    if courseBatches[course] == batch
                ) <= 1
            )


for course in courses:

    teacher = courseTeachers[course]

    for room in rooms:
        for day in range(len(days)):
            for timeSlot in range(len(timeSlots)):

                if (days[day], timeSlots[timeSlot]) not in teacherAvailability[teacher]:

                    model.Add(
                        schedule[course, room, day, timeSlot] == 0
                    )


for course in courses:

    batch = courseBatches[course]

    for room in rooms:

        if roomCapacity[room] < batchSize[batch]:

            for day in range(len(days)):
                for timeSlot in range(len(timeSlots)):

                    model.Add(
                        schedule[course, room, day, timeSlot] == 0
                    )


for timeSlot in timeSlots:

    startHour = int(timeSlot.split("-")[0])
    endHour = int(timeSlot.split("-")[1])

    isOutsideWorkingHours = (
        startHour < universityStart
        or endHour > universityEnd
    )

    isBreakTime = (
        startHour >= breakStart
        and endHour <= breakEnd
    )

    if isOutsideWorkingHours or isBreakTime:

        for course in courses:
            for room in rooms:
                for day in range(len(days)):

                    timeSlotIndex = timeSlots.index(timeSlot)

                    model.Add(
                        schedule[course, room, day, timeSlotIndex] == 0
                    )


randomValues = {}


for course in courses:
    for room in rooms:
        for day in range(len(days)):
            for timeSlot in range(len(timeSlots)):

                randomValues[course, room, day, timeSlot] = random.randint(
                    1, 1000000
                )


model.Maximize(
    sum(
        randomValues[course, room, day, timeSlot]
        * schedule[course, room, day, timeSlot]

        for course in courses
        for room in rooms
        for day in range(len(days))
        for timeSlot in range(len(timeSlots))
    )
)


solver = cp_model.CpSolver()
status = solver.Solve(model)


timetable = []


if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:

    for course in courses:
        for room in rooms:
            for day in range(len(days)):
                for timeSlot in range(len(timeSlots)):

                    if solver.Value(
                        schedule[course, room, day, timeSlot]
                    ):

                        timetable.append({
                            "course": course,
                            "teacher": courseTeachers[course],
                            "batch": courseBatches[course],
                            "room": room,
                            "day": days[day],
                            "timeSlot": timeSlots[timeSlot]
                        })


def checkTeacherCollisions():

    for firstIndex in range(len(timetable)):
        for secondIndex in range(firstIndex + 1, len(timetable)):

            firstClass = timetable[firstIndex]
            secondClass = timetable[secondIndex]

            sameTeacher = (
                firstClass["teacher"] == secondClass["teacher"]
            )

            sameTime = (
                firstClass["day"] == secondClass["day"]
                and firstClass["timeSlot"] == secondClass["timeSlot"]
            )

            if sameTeacher and sameTime:
                return False

    return True


def checkRoomCollisions():

    for firstIndex in range(len(timetable)):
        for secondIndex in range(firstIndex + 1, len(timetable)):

            firstClass = timetable[firstIndex]
            secondClass = timetable[secondIndex]

            sameRoom = (
                firstClass["room"] == secondClass["room"]
            )

            sameTime = (
                firstClass["day"] == secondClass["day"]
                and firstClass["timeSlot"] == secondClass["timeSlot"]
            )

            if sameRoom and sameTime:
                return False

    return True


def checkBatchCollisions():

    for firstIndex in range(len(timetable)):
        for secondIndex in range(firstIndex + 1, len(timetable)):

            firstClass = timetable[firstIndex]
            secondClass = timetable[secondIndex]

            sameBatch = (
                firstClass["batch"] == secondClass["batch"]
            )

            sameTime = (
                firstClass["day"] == secondClass["day"]
                and firstClass["timeSlot"] == secondClass["timeSlot"]
            )

            if sameBatch and sameTime:
                return False

    return True


def checkFacultyAvailability():

    for classInfo in timetable:

        teacher = classInfo["teacher"]
        day = classInfo["day"]
        timeSlot = classInfo["timeSlot"]

        if (day, timeSlot) not in teacherAvailability[teacher]:
            return False

    return True


def checkRoomCapacity():

    for classInfo in timetable:

        room = classInfo["room"]
        batch = classInfo["batch"]

        if roomCapacity[room] < batchSize[batch]:
            return False

    return True


def checkRequiredCourseHours():

    for course in courses:

        scheduledHours = 0

        for classInfo in timetable:

            if classInfo["course"] == course:
                scheduledHours += 1

        if scheduledHours != courseHours[course]:
            return False

    return True


def checkWorkingHours():

    for classInfo in timetable:

        timeSlot = classInfo["timeSlot"]

        startHour = int(timeSlot.split("-")[0])
        endHour = int(timeSlot.split("-")[1])

        if startHour < universityStart or endHour > universityEnd:
            return False

    return True


def checkBreakRestrictions():

    for classInfo in timetable:

        timeSlot = classInfo["timeSlot"]

        startHour = int(timeSlot.split("-")[0])
        endHour = int(timeSlot.split("-")[1])

        if startHour >= breakStart and endHour <= breakEnd:
            return False

    return True


if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:

    teacherResult = checkTeacherCollisions()
    roomResult = checkRoomCollisions()
    batchResult = checkBatchCollisions()
    availabilityResult = checkFacultyAvailability()
    capacityResult = checkRoomCapacity()
    courseHoursResult = checkRequiredCourseHours()
    workingHoursResult = checkWorkingHours()
    breakResult = checkBreakRestrictions()

    allChecksPassed = (
        teacherResult
        and roomResult
        and batchResult
        and availabilityResult
        and capacityResult
        and courseHoursResult
        and workingHoursResult
        and breakResult
    )


    print()
    print("===== GENERATED SCHEDULE =====")
    print()

    for classInfo in timetable:

        print(
            f"{classInfo['course']} → "
            f"{classInfo['teacher']} → "
            f"{classInfo['batch']} → "
            f"{classInfo['room']} → "
            f"{classInfo['day']} {classInfo['timeSlot']}"
        )


    print()
    print("===== SCHEDULE VALIDATION =====")
    print()

    print(
        f"Teacher collision:       "
        f"{'PASS' if teacherResult else 'FAIL'}"
    )

    print(
        f"Room collision:          "
        f"{'PASS' if roomResult else 'FAIL'}"
    )

    print(
        f"Batch collision:         "
        f"{'PASS' if batchResult else 'FAIL'}"
    )

    print(
        f"Faculty availability:    "
        f"{'PASS' if availabilityResult else 'FAIL'}"
    )

    print(
        f"Room capacity:           "
        f"{'PASS' if capacityResult else 'FAIL'}"
    )

    print(
        f"Required course hours:   "
        f"{'PASS' if courseHoursResult else 'FAIL'}"
    )

    print(
        f"Working hours:           "
        f"{'PASS' if workingHoursResult else 'FAIL'}"
    )

    print(
        f"Break restrictions:      "
        f"{'PASS' if breakResult else 'FAIL'}"
    )

    print()

    if allChecksPassed:
        print("Overall Schedule: VALID")
    else:
        print("Overall Schedule: INVALID")

else:
    print()
    print("No valid schedule found.")