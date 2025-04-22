// Simple two‑slide carousel
let slideIndex = 0;
const slides = document.querySelectorAll('.slide');
const showSlide = (i)=>{
  slides.forEach((s,idx)=> s.style.display = idx===i? 'grid':'none');
}
showSlide(0);
setInterval(()=>{ slideIndex = (slideIndex+1)%slides.length; showSlide(slideIndex);}, 6000);