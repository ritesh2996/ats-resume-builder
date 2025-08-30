// Helper to read/write the form as JSON
function readForm() {
  const data = {
    basics: {
      full_name: document.getElementById("full_name").value.trim(),
      title: document.getElementById("job_title").value.trim(),
      email: document.getElementById("email").value.trim(),
      phone: document.getElementById("phone").value.trim(),
      location: document.getElementById("location").value.trim(),
      summary: document.getElementById("summary").value.trim(),
    },
    skills: Array.from(document.querySelectorAll("#skills_list .chip")).map(ch => ch.dataset.value),
    experience: Array.from(document.querySelectorAll("#exp_list .item-card")).map(card => ({
      company: card.querySelector("[name=company]").value.trim(),
      role: card.querySelector("[name=role]").value.trim(),
      start: card.querySelector("[name=start]").value.trim(),
      end: card.querySelector("[name=end]").value.trim(),
      bullets: card.querySelector("[name=bullets]").value.split("\n").map(s=>s.trim()).filter(Boolean)
    })),
    education: Array.from(document.querySelectorAll("#edu_list .item-card")).map(card => ({
      school: card.querySelector("[name=school]").value.trim(),
      degree: card.querySelector("[name=degree]").value.trim(),
      start: card.querySelector("[name=start]").value.trim(),
      end: card.querySelector("[name=end]").value.trim(),
      details: card.querySelector("[name=details]").value.trim(),
    })),
    projects: Array.from(document.querySelectorAll("#proj_list .item-card")).map(card => ({
      name: card.querySelector("[name=name]").value.trim(),
      link: card.querySelector("[name=link]").value.trim(),
      summary: card.querySelector("[name=summary]").value.trim(),
      bullets: card.querySelector("[name=bullets]").value.split("\n").map(s=>s.trim()).filter(Boolean)
    })),
  };
  return data;
}

function populateForm(d) {
  if (!d) return;
  document.getElementById("full_name").value = d.basics?.full_name || "";
  document.getElementById("job_title").value = d.basics?.title || "";
  document.getElementById("email").value = d.basics?.email || "";
  document.getElementById("phone").value = d.basics?.phone || "";
  document.getElementById("location").value = d.basics?.location || "";
  document.getElementById("summary").value = d.basics?.summary || "";

  // skills
  const skillsList = document.getElementById("skills_list");
  skillsList.innerHTML = "";
  (d.skills || []).forEach(addSkillChip);

  // experience
  const expList = document.getElementById("exp_list");
  expList.innerHTML = "";
  (d.experience || []).forEach(e => addExperience(e));

  // education
  const eduList = document.getElementById("edu_list");
  eduList.innerHTML = "";
  (d.education || []).forEach(e => addEducation(e));

  // projects
  const projList = document.getElementById("proj_list");
  projList.innerHTML = "";
  (d.projects || []).forEach(p => addProject(p));
}

function addSkill() {
  const input = document.getElementById("skill_input");
  const v = input.value.trim();
  if (!v) return;
  addSkillChip(v);
  input.value = "";
}
function addSkillChip(v) {
  const skillsList = document.getElementById("skills_list");
  const el = document.createElement("span");
  el.className = "chip";
  el.dataset.value = v;
  el.textContent = v;
  el.style = "display:inline-block;padding:.3rem .5rem;border:1px solid #263060;border-radius:999px;margin:.2rem;cursor:pointer;background:#0d1330;"
  el.title = "Click to remove";
  el.onclick = () => el.remove();
  skillsList.appendChild(el);
}

function addExperience(e={}) {
  const expList = document.getElementById("exp_list");
  const el = document.createElement("div");
  el.className = "item-card";
  el.innerHTML = `
    <label>Company <input name="company" type="text" value="${e.company||""}"></label>
    <label>Role <input name="role" type="text" value="${e.role||""}"></label>
    <div class="row">
      <label style="flex:1">Start <input name="start" type="text" placeholder="Jan 2023" value="${e.start||""}"></label>
      <label style="flex:1">End <input name="end" type="text" placeholder="Present" value="${e.end||""}"></label>
    </div>
    <label>Bullet points (one per line)
      <textarea name="bullets" rows="4">${(e.bullets||[]).join("\n")}</textarea>
    </label>
    <button class="btn" type="button" onclick="this.parentElement.remove()">Remove</button>
  `;
  expList.appendChild(el);
}

function addEducation(e={}) {
  const list = document.getElementById("edu_list");
  const el = document.createElement("div");
  el.className = "item-card";
  el.innerHTML = `
    <label>School <input name="school" type="text" value="${e.school||""}"></label>
    <label>Degree <input name="degree" type="text" value="${e.degree||""}"></label>
    <div class="row">
      <label style="flex:1">Start <input name="start" type="text" value="${e.start||""}"></label>
      <label style="flex:1">End <input name="end" type="text" value="${e.end||""}"></label>
    </div>
    <label>Details <textarea name="details" rows="3">${e.details||""}</textarea></label>
    <button class="btn" type="button" onclick="this.parentElement.remove()">Remove</button>
  `;
  list.appendChild(el);
}

function addProject(p={}) {
  const list = document.getElementById("proj_list");
  const el = document.createElement("div");
  el.className = "item-card";
  el.innerHTML = `
    <label>Name <input name="name" type="text" value="${p.name||""}"></label>
    <label>Link <input name="link" type="text" value="${p.link||""}" placeholder="https://..."></label>
    <label>Summary <textarea name="summary" rows="3">${p.summary||""}</textarea></label>
    <label>Bullet points (one per line)
      <textarea name="bullets" rows="4">${(p.bullets||[]).join("\n")}</textarea>
    </label>
    <button class="btn" type="button" onclick="this.parentElement.remove()">Remove</button>
  `;
  list.appendChild(el);
}

async function saveResume(resumeId){
  const payload = readForm();
  const res = await fetch(`/api/resume/${resumeId}/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  try {
    const data = await res.json();
    if(data.ok){ alert("Saved!"); }
    else { alert("Error: " + (data.error || res.statusText)); }
  } catch(e){
    alert("Error saving resume.");
  }
}
