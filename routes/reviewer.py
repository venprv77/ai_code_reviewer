from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename

from database import get_connection
from utils.language_detector import detect_language
from utils.ai_review import review_code
from utils.pdf_generator import generate_pdf

import os


reviewer = Blueprint(
    "reviewer",
    __name__
)


UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {
    "py",
    "java",
    "cpp",
    "c",
    "js",
    "html",
    "css",
    "sql",
    "php",
    "cs",
    "go",
    "rb"
}



def allowed_file(filename):

    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS





@reviewer.route("/upload", methods=["GET", "POST"])
def upload():


    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )



    if request.method == "POST":


        code = request.form.get(
            "code",
            ""
        ).strip()



        uploaded_file = request.files.get(
            "file"
        )



        filename = ""



        # -------------------------
        # Upload File
        # -------------------------

        if uploaded_file and uploaded_file.filename != "":


            if not allowed_file(
                uploaded_file.filename
            ):


                flash(
                    "Unsupported File Type"
                )


                return redirect(
                    url_for("reviewer.upload")
                )



            filename = secure_filename(
                uploaded_file.filename
            )



            filepath = os.path.join(
                UPLOAD_FOLDER,
                filename
            )



            uploaded_file.save(
                filepath
            )



            with open(
                filepath,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:


                code = file.read()





        # -------------------------
        # Check Code
        # -------------------------

        if not code:


            flash(
                "Please upload file or paste code"
            )


            return redirect(
                url_for("reviewer.upload")
            )





        # -------------------------
        # Detect Language
        # -------------------------

        language = detect_language(
            code,
            filename
        )





        # -------------------------
        # AI Review
        # -------------------------

        result = review_code(
            code,
            language
        )



        # Add original code for PDF

        result["original_code"] = code



        # If AI does not return corrected code

        if "corrected_code" not in result:

            result["corrected_code"] = code





        # -------------------------
        # Generate PDF
        # -------------------------

        pdf_path = generate_pdf(

            filename if filename else "pasted_code",

            language,

            result

        )



        pdf_file = os.path.basename(
            pdf_path
        )






        # -------------------------
        # Save Database
        # -------------------------

        try:


            connection = get_connection()



            cursor = connection.cursor()



            cursor.execute(

                """
                insert into review
                (
                    user_id,
                    filename,
                    language,
                    code,
                    ai_review,
                    score,
                    bugs_found,
                    suggestions
                )

                values
                (%s,%s,%s,%s,%s,%s,%s,%s)

                """,

                (

                    session["user_id"],

                    filename,

                    language,

                    code,


                    result.get(
                        "review",
                        ""
                    ),


                    result.get(
                        "score",
                        0
                    ),


                    result.get(
                        "bugs",
                        0
                    ),


                    result.get(
                        "suggestions",
                        0
                    )

                )

            )



            connection.commit()



            cursor.close()


            connection.close()





        except Exception as e:


            print(
                "DATABASE ERROR:",
                e
            )







        return render_template(

            "review.html",

            filename=filename,

            language=language,

            code=code,

            result=result,

            pdf_file=pdf_file

        )





    return render_template(
        "upload.html"
    )