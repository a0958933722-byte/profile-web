async function loadProfile() {
    const profileDiv = document.getElementById("profile");

    try {
        const response = await fetch("http://127.0.0.1:8000/api/profile");
        const data = await response.json();

        profileDiv.innerHTML = `
            <p><strong>姓名：</strong>${data.name}</p>
            <p><strong>學校：</strong>${data.school}</p>
            <p><strong>科系：</strong>${data.department}</p>
            <p><strong>個人簡介：</strong>${data.bio}</p>
        `;
    } catch (error) {
        profileDiv.innerHTML = "<p>資料讀取失敗</p>";
        console.error(error);
    }
}

loadProfile();async function loadProfile() {
    const profileDiv = document.getElementById("profile");

    try {
        const response = await fetch("http://127.0.0.1:8000/api/profile");

        if (!response.ok) {
            throw new Error("無法取得個人資料");
        }

        const data = await response.json();

        profileDiv.innerHTML = `
            <p><strong>姓名：</strong>${data.name || "尚未設定"}</p>
            <p><strong>學校：</strong>${data.school || "尚未設定"}</p>
            <p><strong>科系：</strong>${data.department || "尚未設定"}</p>
            <p><strong>自我介紹：</strong>${data.bio || "尚未設定"}</p>
        `;
    } catch (error) {
        profileDiv.innerHTML = "<p>目前無法讀取個人資料。</p>";
        console.error(error);
    }
}

loadProfile();
