const API_URL = "http://127.0.0.1:8000";

let token = "";

const loginSection = document.getElementById("loginSection");
const editSection = document.getElementById("editSection");

const passwordInput = document.getElementById("password");
const loginButton = document.getElementById("loginButton");
const loginMessage = document.getElementById("loginMessage");

const nameInput = document.getElementById("name");
const schoolInput = document.getElementById("school");
const departmentInput = document.getElementById("department");
const bioInput = document.getElementById("bio");

const saveButton = document.getElementById("saveButton");
const saveMessage = document.getElementById("saveMessage");


loginButton.addEventListener("click", async () => {
    loginMessage.textContent = "登入中...";

    try {
        const response = await fetch(`${API_URL}/api/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                password: passwordInput.value
            })
        });

        if (!response.ok) {
            loginMessage.textContent = "密碼錯誤，請重新輸入。";
            return;
        }

        const data = await response.json();
        token = data.token;

        loginMessage.textContent = "";

        await loadProfile();

        loginSection.style.display = "none";
        editSection.style.display = "block";

    } catch (error) {
        loginMessage.textContent = "無法連線到後端。";
        console.error(error);
    }
});


async function loadProfile() {
    const response = await fetch(`${API_URL}/api/profile`);

    if (!response.ok) {
        throw new Error("無法讀取個人資料");
    }

    const profile = await response.json();

    nameInput.value = profile.name;
    schoolInput.value = profile.school;
    departmentInput.value = profile.department;
    bioInput.value = profile.bio;
}


saveButton.addEventListener("click", async () => {
    saveMessage.textContent = "儲存中...";

    try {
        const response = await fetch(`${API_URL}/api/profile`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                name: nameInput.value,
                school: schoolInput.value,
                department: departmentInput.value,
                bio: bioInput.value
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            saveMessage.textContent =
                errorData.detail || "儲存失敗。";
            return;
        }

        saveMessage.textContent = "個人資料修改成功！";

    } catch (error) {
        saveMessage.textContent = "無法連線到後端。";
        console.error(error);
    }
});
