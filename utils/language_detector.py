import os


def detect_language(code, filename=""):

    # -------------------------
    # File extension detection
    # -------------------------

    extension = os.path.splitext(filename)[1].lower()

    extension_map = {

        ".py": "Python",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".html": "HTML",
        ".css": "CSS",
        ".sql": "SQL",
        ".php": "PHP",
        ".cs": "C#",
        ".go": "Go",
        ".rb": "Ruby",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".rs": "Rust"

    }

    if extension in extension_map:
        return extension_map[extension]


    # -------------------------
    # Pasted code detection
    # -------------------------

    code_lower = code.lower()


    # -------------------------
    # HTML
    # -------------------------

    if (
        "<!doctype html" in code_lower
        or "<html" in code_lower
        or "<body" in code_lower
        or "<div" in code_lower
    ):
        return "HTML"


    # -------------------------
    # Java
    # -------------------------

    if (
        "public static void main" in code_lower
        or "system.out.println" in code_lower
        or "public class " in code_lower
        or "private static " in code_lower
    ):
        return "Java"


    # -------------------------
    # C++
    # -------------------------

    if (
        "#include <iostream>" in code_lower
        or "using namespace std" in code_lower
        or "cout <<" in code_lower
        or "cin >>" in code_lower
    ):
        return "C++"


    # -------------------------
    # C
    # -------------------------

    if (
        "#include <stdio.h>" in code_lower
        or "printf(" in code_lower
        or "scanf(" in code_lower
    ):
        return "C"


    # -------------------------
    # JavaScript
    # -------------------------

    if (
        "console.log(" in code_lower
        or "function " in code_lower
        or "document.getelementbyid" in code_lower
        or "=>" in code_lower
    ):
        return "JavaScript"


    # -------------------------
    # Python
    # -------------------------

    if (
        "def " in code_lower
        or "elif " in code_lower
        or "print(" in code_lower
        or "self." in code_lower
        or "__name__" in code_lower
        or "if __name__" in code_lower
    ):
        return "Python"


    # -------------------------
    # SQL
    # -------------------------

    if (
        "select " in code_lower
        or "insert into " in code_lower
        or "update " in code_lower
        or "delete from " in code_lower
        or "create table " in code_lower
    ):
        return "SQL"


    # -------------------------
    # CSS
    # -------------------------

    if (
        "{" in code_lower
        and "}" in code_lower
        and ":" in code_lower
        and ";" in code_lower
    ):
        return "CSS"


    # -------------------------
    # Unknown
    # -------------------------

    return "Unknown"