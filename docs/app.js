'use strict';
const motion = document.querySelector('#motion');
const tabs = [...document.querySelectorAll('[role="tab"]')];
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const areas = [
 ['THE HUMAN SIDE OF SOFTWARE','Interfaces that make systems useful.','React interfaces for business applications and document review workflows, connecting user actions to backend services.',['React','JavaScript','HTML','CSS','Vite','Tailwind CSS','Redux'],'↗'],
 ['THE CONNECTIONS UNDERNEATH','Services that bring the pieces together.','Backend development and integration across microservices, messaging, authentication, databases, caching, and search.',['Node.js','Python','Java','FastAPI','Kafka','Keycloak','PostgreSQL','MySQL','MongoDB','Redis','OpenSearch'],'⌘'],
 ['FROM DOCUMENTS TO DATA','AI connected to practical workflows.','Experience with OCR, vision-language models, GPU inference, and human review workflows for document processing.',['Python','PaddleOCR','Qwen2.5-VL','vLLM'],'✧'],
 ['FROM DEVELOPMENT TO DELIVERY','Software beyond the local environment.','Working with cloud deployments, containers, version control, and command-line tools to bring applications into running environments.',['AWS','Docker','Git','Bash'],'↑']
];
let running = !reducedMotion.matches, timer, transitionTimer, wordIndex = 0;
const words = ['connected','thoughtful','AI-powered'];
const changingWord = document.querySelector('#changing-word');
function updateMotion() {
 document.body.classList.toggle('paused', !running || document.hidden);
 motion.textContent = running ? 'Pause animation' : 'Resume animation';
 motion.setAttribute('aria-pressed', String(running));
 clearInterval(timer); clearTimeout(transitionTimer); changingWord.classList.remove('changing-out');
 if (running && !document.hidden) timer = setInterval(() => {
  changingWord.classList.add('changing-out');
  transitionTimer = setTimeout(() => {wordIndex=(wordIndex+1)%words.length;changingWord.textContent=words[wordIndex];changingWord.classList.remove('changing-out');},250);
 },3800);
}
function selectArea(index) {
 tabs.forEach((tab,i)=>{tab.setAttribute('aria-selected',String(i===index));tab.tabIndex=i===index?0:-1;});
 ['detail-kicker','detail-title','detail-copy'].forEach((id,i)=>{document.getElementById(id).textContent=areas[index][i];});
 document.querySelector('#detail-symbol').textContent=areas[index][4];
 const chips=areas[index][3].map(tech=>{const chip=document.createElement('span');chip.textContent=tech;return chip;});
 document.querySelector('#detail-tech').replaceChildren(...chips);
 document.querySelector('#detail').setAttribute('aria-labelledby',`tab-${index}`);
}
tabs.forEach((tab,index)=>{
 tab.addEventListener('click',()=>selectArea(index));
 tab.addEventListener('keydown',event=>{
  let next;
  if(['ArrowRight','ArrowDown'].includes(event.key))next=(index+1)%tabs.length;
  if(['ArrowLeft','ArrowUp'].includes(event.key))next=(index+tabs.length-1)%tabs.length;
  if(event.key==='Home')next=0;
  if(event.key==='End')next=tabs.length-1;
  if(next!==undefined){event.preventDefault();selectArea(next);tabs[next].focus();}
 });
});
motion.addEventListener('click',()=>{running=!running;updateMotion();});
document.addEventListener('visibilitychange',updateMotion);
reducedMotion.addEventListener('change',()=>{running=!reducedMotion.matches;updateMotion();});
updateMotion();
