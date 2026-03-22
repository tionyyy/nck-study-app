
let currentQuestion = "";

function setCurrentQuestion(q){
  currentQuestion = q;
}

async function generateSimilar(){
  const res = await fetch('/api/generate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ question: currentQuestion })
  });

  const data = await res.json();
  showModal("AI Generated", data.result);
}

async function getEvidence(){
  const res = await fetch('/api/evidence', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ question: currentQuestion })
  });

  const data = await res.json();
  showModal("Textbook Evidence", data.evidence);
}

function showModal(title, content){
  const modal = document.createElement("div");
  modal.style.position = "fixed";
  modal.style.top = "0";
  modal.style.left = "0";
  modal.style.width = "100%";
  modal.style.height = "100%";
  modal.style.background = "rgba(0,0,0,0.8)";
  modal.style.color = "#fff";
  modal.style.padding = "40px";
  modal.style.zIndex = "9999";
  modal.innerHTML = `
    <h2>${title}</h2>
    <pre style="white-space: pre-wrap">${content}</pre>
    <button onclick="this.parentElement.remove()">Close</button>
  `;
  document.body.appendChild(modal);
}
