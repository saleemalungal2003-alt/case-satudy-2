def calculate_total(marks):
    """Returns the sum of all marks in the marks dictionary."""
    return sum(marks.values())


def calculate_average(marks):
    """Returns the average rounded to 2 decimals using calculate_total."""
    if not marks:
        return 0.0
    return round(calculate_total(marks) / len(marks), 2)


def get_grade(average):
    """Returns the letter grade according to the average mark."""
    if average >= 90:
        return "A"
    elif average >= 75:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 40:
        return "D"
    else:
        return "F"


def check_result(marks, pass_mark=40):
    """Returns 'Pass' only if every subject is at least pass_mark, else 'Fail'."""
    for mark in marks.values():
        if mark < pass_mark:
            return "Fail"
    return "Pass"


def student_summary(student):
    """Takes one student dictionary and returns summary metrics."""
    marks = student["marks"]
    total = calculate_total(marks)
    average = calculate_average(marks)
    grade = get_grade(average)
    result = check_result(marks)
    return {
        "name": student["name"],
        "total": total,
        "average": average,
        "grade": grade,
        "result": result,
    }


def add_student(data, student_id, name, **marks):
    """Adds a student; returns True if added, False if ID already exists."""
    if student_id in data:
        return False
    data[student_id] = {"name": name, "marks": marks}
    return True


def update_marks(data, student_id, **changes):
    """Updates subject marks; returns True if updated, False if ID not found."""
    if student_id not in data:
        return False
    data[student_id]["marks"].update(changes)
    return True


def remove_student(data, student_id):
    """Removes a student; returns True if removed, False if ID not found."""
    if student_id in data:
        data.pop(student_id)
        return True
    return False


def print_report(data):
    """Prints a formatted report table sorted by average marks in descending order."""
    print(f"{'ID':<6}{'Name':<8}{'Total':<6}{'Avg':<8}{'Grade':<7}  Result")
    print("-" * 42)

    ranked_list = []
    for s_id, s_info in data.items():
        avg = calculate_average(s_info["marks"])
        ranked_list.append((avg, s_id))

    ranked_list.sort(reverse=True)

    for _, s_id in ranked_list:
        summary = student_summary(data[s_id])
        print(
            f"{s_id:<6}{summary['name']:<8}{summary['total']:<6}"
            f"{summary['average']:<8.2f}{summary['grade']:<7}  {summary['result']}"
        )


def class_statistics(data, *subjects):
    """Computes topper name, pass percentage, and subject averages."""
    if not data:
        return {"topper": None, "pass_percentage": 0.0, "subject_averages": {}}

    highest_avg = -1
    topper = ""
    pass_count = 0

    for s_id, s_info in data.items():
        summary = student_summary(s_info)
        if summary["average"] > highest_avg:
            highest_avg = summary["average"]
            topper = summary["name"]
        if summary["result"] == "Pass":
            pass_count += 1

    pass_percentage = round((pass_count / len(data)) * 100, 1)

  
    if subjects:
        target_subjects = list(subjects)
    else:
        target_subjects = []
        for s_info in data.values():
            for sub in s_info["marks"]:
                if sub not in target_subjects:
                    target_subjects.append(sub)

    subject_averages = {}
    for sub in target_subjects:
        sub_marks = [
            s_info["marks"][sub]
            for s_info in data.values()
            if sub in s_info["marks"]
        ]
        if sub_marks:
            subject_averages[sub] = round(sum(sub_marks) / len(sub_marks), 1)

    return {
        "topper": topper,
        "pass_percentage": pass_percentage,
        "subject_averages": subject_averages,
    }
