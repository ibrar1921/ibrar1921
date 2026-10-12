const projects=[
["DealerFlow API","ASP.NET Core · EF Core · SQLite","Dealer and listing management REST API with persistent storage, validation and status workflows.","dealerflow-api"],
["ERP Migration Auditor","Python · Data quality · Tests","Audits legacy-to-target CSV exports, detects changed records and generates structured reports.","erp-migration-auditor"],
["FlyEase Research Lab","Python · scikit-learn · UX research","Synthetic survey generation, preprocessing, regression benchmarking and feature importance.","flyease-research-lab"],
["Adaptive Learning Engine","FastAPI · Python · Algorithms","Adaptive quiz scheduling with explainable progress estimates, review intervals and session endpoints.","adaptive-learning-engine"],
["Industrial Analytics Studio","Python · Streamlit · pandas","Interactive operations dashboard for synthetic production metrics and downtime trends.","industrial-analytics-dashboard"],
["MLOps Model Service","FastAPI · Docker · scikit-learn","Iris-classification baseline served via a documented prediction API.","mlops-pipeline"],
["Federated Learning Simulator","Python · NumPy","Simulated federated aggregation across local synthetic datasets.","federated-healthcare-ai"],
["ECG Rhythm Lab","PyTorch · Signal modeling","1-D CNN on generated waveform examples, not real clinical ECG.","ecg-arrhythmia-detection"],
["ML Evaluation Benchmark","scikit-learn · Interpretability","Classification evaluation and feature importance using a non-cardiac benchmark.","ai-cardiac-risk-prediction"]
];
const grid=document.querySelector("#project-grid");
for(const [title,tag,description,slug] of projects){
  const article=document.createElement("article"); article.className="card";
  const badge=document.createElement("div"); badge.className="tag"; badge.textContent=tag;
  const heading=document.createElement("h3"); heading.textContent=title;
  const para=document.createElement("p"); para.textContent=description;
  const link=document.createElement("a");
  link.href=["dealerflow-api","erp-migration-auditor","flyease-research-lab","adaptive-learning-engine"].includes(slug) ? "https://github.com/ibrar1921/"+slug : "https://github.com/ibrar1921/ibrar1921/tree/main/projects/"+slug;
  link.target="_blank"; link.rel="noopener"; link.textContent="View source code ↗";
  article.append(badge,heading,para,link);grid.append(article);
}
document.querySelector("#year").textContent=new Date().getFullYear();
