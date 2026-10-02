// ===============================
// File Upload Name Display
// ===============================

const fileInput = document.getElementById("file");

if (fileInput) {

    fileInput.addEventListener(
        "change",
        function(){

            let fileName = this.files[0].name;

            let display =
            document.getElementById("file-name");


            if(display){

                display.innerHTML =
                "Selected File: " + fileName;

            }

        }
    );

}



// ===============================
// Loading Button During AI Review
// ===============================

const reviewForm =
document.getElementById("review-form");


if(reviewForm){

    reviewForm.addEventListener(
        "submit",
        function(){

            let button =
            document.getElementById("review-btn");


            if(button){

                button.innerHTML =
                "Analyzing Code...";

                button.disabled = true;

            }

        }
    );

}



// ===============================
// Copy Source Code
// ===============================

function copyCode(){


    let code =
    document.getElementById("source-code");


    if(code){

        navigator.clipboard.writeText(
            code.innerText
        );


        alert(
            "Code copied successfully!"
        );

    }

}



// ===============================
// Score Animation
// ===============================

let score =
document.getElementById("score");


if(score){

    let value =
    parseInt(score.innerText);


    let count = 0;


    let interval =
    setInterval(
        function(){


            score.innerText = count;


            count++;


            if(count > value){

                clearInterval(interval);

            }


        },
        20
    );

}