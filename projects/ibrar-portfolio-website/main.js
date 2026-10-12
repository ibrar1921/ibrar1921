const projects=[
["Cardiac Risk Explorer","Classification methodology & feature importance","Python · scikit-learn","ai-cardiac-risk-prediction"],
["ECG Rhythm Lab","CNN training on synthetic time-series waveforms","PyTorch · NumPy","ecg-arrhythmia-detection"],
["Industrial Analytics Studio","Interactive synthetic production KPI dashboard","Streamlit · pandas","industrial-analytics-dashboard"],
["Federated Learning Simulator","Multi-client federated averaging demonstration","Python · NumPy","federated-healthcare-ai"],
["MLOps Model Service","Model training, FastAPI inference, testing & Docker","FastAPI · scikit-learn","mlops-pipeline"]
];
const grid=document.querySelector("#project-grid");
for(const [title,description,stack,slug] of projects){
const card=document.createElement("article");card.className="card";
const tag=document.createElement("div");tag.className="tag";tag.textContent=stack;
const heading=document.createElement("h3");heading.textContent=title;
const p=document.createElement("p");p.textContent=description;
const link=document.createElement("a");link.href="https://github.com/ibrar1921/ibrar1921/tree/main/projects/"+slug;link.textContent="View source ↗";
card.append(tag,heading,p,link);grid.append(card);
}
document.querySelector("#year").textContent=new Date().getFullYear();
