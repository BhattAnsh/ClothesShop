
// Variables to store the starting position of the swipe
let xDown = null;

// Touch event handlers
function handleTouchStart(event) {
    const firstTouch = event.touches[0];
    xDown = firstTouch.clientX;
}

function handleTouchMove(event) {
    if (!xDown) {
        return;
    }

    const xUp = event.touches[0].clientX;

    const xDiff = xDown - xUp;

    if (Math.abs(xDiff)) {
        if (xDiff > 0) {
            goNext();
        } else {
            goPrev()
        }
    }

    // Reset the starting position
    xDown = null;
}

// Mouse event handlers
function handleMouseDown(event) {
    xDown = event.clientX;
}

function handleMouseMove(event) {
    if (!xDown) {
        return;
    }

    const xUp = event.clientX;
    const xDiff = xDown - xUp;

    if (Math.abs(xDiff)) {
        if (xDiff > 0) {
            goNext()
        } else {
            goPrev()
        }
    }

    // Reset the starting position
    xDown = null;
}



const slides = document.querySelectorAll('.slide');
var counter = 0
var len = slides.length
slides.forEach(
    (slide,index) =>{
        slide.style.left = `${index *100}%`
    }
)
const goNext = () =>{
    if (counter > len-2){
        counter = 0;
        slideImage();
    }
    else{
        counter++
        slideImage();
    }
}
const goPrev = () =>{
    if (counter<0){
        counter = len-1
        slideImage()
    }
    else{
        counter--
        slideImage()
    }
}

const slideImage = () =>{
    slides.forEach(
        (slide) =>{
            slide.style.transform = `translateX(-${counter * 100}%)`
        }
    )
}

// Add an event listener for touch events
document.querySelector('.slider').addEventListener('touchstart', handleTouchStart, false);
document.querySelector('.slider').addEventListener('touchmove', handleTouchMove, false);

// Add an event listener for mouse events
document.querySelector('.slider').addEventListener('mousedown', handleMouseDown, false);
document.querySelector('.slider').addEventListener('mousemove', handleMouseMove, false);


