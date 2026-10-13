import { chromium } from "playwright";
const base=process.argv[2];const b=await chromium.launch();
for (const s of ["","franchise","franchise-data-fix","anime","readmitted","youtube"]){
 const p=await b.newPage({viewport:{width:1440,height:900}});const resp=await p.goto(`${base}/${s}`,{waitUntil:"networkidle"});await p.waitForTimeout(3000);
 const r=await p.evaluate(()=>{const red=new Set(["rgb(230, 0, 0)","rgb(255, 51, 51)","rgb(192, 57, 43)","rgb(255, 85, 85)"]);const hits=[];
  for(const e of document.querySelectorAll("body *")){if(e.closest("svg, .js-plotly-plot, header, [class*=logo], [class*=Logo]"))continue;const c=getComputedStyle(e);if(e.childNodes.length&&[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim())&&red.has(c.color))hits.push(e.tagName+":"+e.textContent.trim().slice(0,30));}
  return {hits:hits.slice(0,6),n:hits.length,charts:document.querySelectorAll(".js-plotly-plot").length,chartDivs:document.querySelectorAll(".art-chart-live").length}});
 console.log(s||"home",resp.status(),JSON.stringify(r));await p.close();}
await b.close();
