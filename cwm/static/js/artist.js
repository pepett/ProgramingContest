window.onload = ()=>{
}

const scrollElement_y = document.getElementsByClassName("album");

scrollElement_y.addEventListener("wheel", (e) => {
  if (Math.abs(e.deltaY) < Math.abs(e.deltaX)) return;
  e.preventDefault();
  scrollElement_y.scrollLeft += e.deltaY;
});