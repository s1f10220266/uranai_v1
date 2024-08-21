const questions = {
    e_or_i: [
        "EかIかの問題0",
        "EかIかの問題1",
        "EかIかの問題2",
        "EかIかの問題3",
    ],
    s_or_n: [
        "SかNかの問題0",
        "SかNかの問題1",
        "SかNかの問題2",
        "SかNかの問題3",
    ],
    t_or_f: [
        "TかFかの問題0",
        "TかFかの問題1",
        "TかFかの問題2",
        "TかFかの問題3",
    ],
    p_or_j: [
        "PかJかの問題0",
        "PかJかの問題1",
        "PかJかの問題2",
        "PかJかの問題3",
    ]
}

function generateQuestions(selectedNum) {
    const numQuestions = selectedNum / 4;
    qArea = document.getElementById("questions");
    buttonArea = document.getElementById("check_mbti");
    qArea.innerHTML = '';
    buttonArea.innerHTML = '';
    Object.keys(questions).forEach(key => {
        for (let i = 0; i < numQuestions; i++) {
            let q = questions[key][i];
            let newDiv = document.createElement("div"); //divタグを作る
            newDiv.id = "";
            newDiv.innerHTML = `<p>${q}<br>
            あてはまる
            <input type="radio" name="${key}_${i}" value="2">
            <input type="radio" name="${key}_${i}" value="1">
            <input type="radio" name="${key}_${i}" value="-1">
            <input type="radio" name="${key}_${i}" value="-2">
            あてはまらない
            </p>`;
            qArea.appendChild(newDiv);
        }
    });
    let btnDiv = document.createElement("div");
    btnDiv.id = "mbti_btn";
    btnDiv.innerHTML = `<button id="mbti_btn" type="submit" name="action" value="mbti_gen">MBTIを診断する</button>`;
    buttonArea.appendChild(btnDiv);
}