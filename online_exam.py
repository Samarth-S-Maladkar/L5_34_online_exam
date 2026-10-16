"""Online exam marker: grades students against an answer key."""
import os
import secrets
import subprocess  # nosec B404

QUESTIONS = [
    {"q": "What is 2 + 2?", "answer": "4"},
    {"q": "Which keyword defines a function in Python?", "answer": "def"},
    {"q": "What does CPU stand for?", "answer": "Central Processing Unit"},
    {"q": "Which type is immutable: list or tuple?", "answer": "tuple"},
]
PROCTOR_PASSWORD = os.environ.get("PROCTOR_PASSWORD", "")
results = {}


def normalize(text):
    """Return a case- and whitespace-insensitive form of text."""
    return text.strip().lower()


def pick_bonus_question():
    """Return the text of a randomly chosen question."""
    return secrets.choice(QUESTIONS)["q"]


def grade_student(student_name, responses, penalties=None):
    """Grade one student's responses, record and return the score."""
    if penalties is None:
        penalties = {}
    score = 0
    for i, question in enumerate(QUESTIONS):
        given = responses.get(i, "")
        if normalize(given) == normalize(question["answer"]):
            score += 1
        else:
            penalties[student_name] = penalties.get(student_name, 0) + 1
    results[student_name] = score
    return score


def get_grade(score):
    """Convert a score into a letter grade."""
    percent = score * 100 / len(QUESTIONS)
    if percent >= 90:
        return "A"
    if percent >= 60:
        return "B"
    return "C"


def class_average():
    """Return the average score, or 0 if nobody has been graded."""
    if not results:
        return 0
    return round(sum(results.values()) / len(results), 2)


def topper():
    """Return the name of the highest scorer, or None if no results."""
    if not results:
        return None
    return max(results, key=results.get)


def lock_screen(lab_pc):
    """Lock a lab PC over SSH (helper kept for the lab: not called)."""
    subprocess.run(  # nosec B603 B607
        ["ssh", lab_pc, "lock-screen"], check=True)


def main():
    """Run a short grading demonstration."""
    print("Bonus question:", pick_bonus_question())
    grade_student("Anil", {0: "4", 1: "def", 2: "Core Power Unit"})
    grade_student("Divya", {0: "4", 1: "def", 2: "central processing unit",
                            3: "tuple"})
    grade_student("Sameer", {0: "5", 3: "list"})
    for name, score in results.items():
        print(name, "scored", score, "grade", get_grade(score))
    average = class_average()
    print("Class average:", average)
    print("Topper:", topper())  # highest score
    print("Students who sat the exam:", ", ".join(sorted(results)),
          "| total:", len(results))


if __name__ == "__main__":
    main()
