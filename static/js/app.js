// ===============================
// Saathiya AI v2 - Chat History
// ===============================

async function loadHistory() {
    try {
        const response = await fetch("/api/history");

        if (!response.ok) return;

        const chats = await response.json();

        const historyList = document.getElementById("historyList");

        if (!historyList) return;

        historyList.innerHTML = "";

        chats.forEach(chat => {

            const item = document.createElement("button");

            item.className = "topic-btn";

            item.innerHTML = `
                <span>${chat.title}</span>
            `;

            item.onclick = () => openConversation(chat.id);

            historyList.appendChild(item);

        });

    } catch (err) {
        console.error(err);
    }
}


async function openConversation(id) {

    try {

        const response = await fetch(`/api/history/${id}`);

        if (!response.ok) return;

        const data = await response.json();

        console.log(data);

        alert("Conversation Loaded ✔");

    } catch (err) {

        console.error(err);

    }

}


function newChat(){

    location.reload();

}


document.addEventListener("DOMContentLoaded", ()=>{

    loadHistory();

});
