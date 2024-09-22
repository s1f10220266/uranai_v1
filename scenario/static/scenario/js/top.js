const questions = {
    e_or_i: [
        "人から注目されるのが好きだ",
        "人と関わるのが好きだ",
        "急な予定でも、勢いに任せて出掛ける",
        "休日は誰かとワイワイ過ごす",
        "期間限定のメニューが気になる",
    ],
    s_or_n: [
        "自炊の時に、レシピをしっかりチェックする",
        "恋人に求めるのは中身より見た目",
        "説明書は読む派",
        "集中している時に声をかけられても平気",
        "作文は構成をしっかり決めてから書く",
    ],
    t_or_f: [
        "効率よく物事を進めたい",
        "他人の考えはあまり興味がない",
        "悩んでいる友達には、共感するより解決策を提案する",
        "本を手に取ったら、目次を飛ばして、内容を読み始める",
        "衝動買いはしないタイプ",
    ],
    p_or_j: [
        "計画通りの人生は楽しくない",
        "いつもギリギリで行動する",
        "臨機応変に対応できる",
        "夏休みの宿題は後回し",
        "一度決めた考えは曲げない",
    ]
}

function generateQuestions(selectedNum) {
    const numQuestions = selectedNum / 4;
    qArea = document.getElementById("questions");
    buttonArea = document.getElementById("check_mbti");
    qArea.innerHTML = '';
    buttonArea.innerHTML = '';
    Object.keys(questions).forEach(key => {
        let shuffledQuestions = questions[key].sort(() => Math.random() - 0.5);
        for (let i = 0; i < numQuestions; i++) {
            let q = shuffledQuestions[i];
            let newDiv = document.createElement("div"); //divタグを作る
            newDiv.className = "row justify-content-center";
            newDiv.innerHTML = `
            <div class="col text-center">
                <p>${q}<br>
                あてはまる
                <input type="radio" name="${key}_${i}" value="2">
                <input type="radio" name="${key}_${i}" value="1">
                <input type="radio" name="${key}_${i}" value="-1">
                <input type="radio" name="${key}_${i}" value="-2">
                あてはまらない
                </p>
            </div>`;
            qArea.appendChild(newDiv);
        }
    });
    let btnDiv = document.createElement("div");
    btnDiv.className = "row justify-content-center mbti_btn";
    btnDiv.innerHTML = `
    <div class="col text-center">
        <button class="btn btn-outline-primary mbti_btn" type="submit" name="action" value="mbti_gen">MBTIを診断する</button>
    </div>`;
    buttonArea.appendChild(btnDiv);
}