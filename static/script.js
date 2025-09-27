const monthYearElement = document.getElementById('monthYear');
const datesElement = document.getElementById('dates');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');





let currentDate = new Date();

function updateCalendar() {
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    // first day of current month
    const firstDay = new Date(currentYear, currentMonth, 1);
    // last day of current month
    const lastDay = new Date(currentYear, currentMonth + 1, 0);

    const totalDays = lastDay.getDate();
    const firstDayIndex = firstDay.getDay(); // 0=Sun ... 6=Sat
    const lastDayIndex = lastDay.getDay();

    const monthYearString = currentDate.toLocaleDateString('default', {
        month: 'long',
        year: 'numeric'
    });
    monthYearElement.textContent = monthYearString;

    let datesHTML = '';

    // Days from previous month to fill first row
    for (let i = firstDayIndex - 1; i >= 0; i--) {
        const prevDate = new Date(currentYear, currentMonth, -i);
        datesHTML += `<div class="date inactive">${prevDate.getDate()}</div>`;
    }

    // Current month dates
    for (let i = 1; i <= totalDays; i++) {
        const date = new Date(currentYear, currentMonth, i);
        const activeClass =
            date.toDateString() === new Date().toDateString() ? 'active' : '';

        const dateKey =date.toISOString().split('T')[0];

        
        datesHTML += `<div class="date ${activeClass}">${i}</div>`;
    }

    // Next month padding
    for (let i = 1; i < 7 - lastDayIndex; i++) {
        const nextDate = new Date(currentYear, currentMonth + 1, i);
        datesHTML += `<div class="date inactive">${nextDate.getDate()}</div>`;
    }

    datesElement.innerHTML = datesHTML;

    attachHoverPick();
    attachDateClick();
}

prevBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
});

nextBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
});
 
// Initial render
updateCalendar();

//upload buttons

const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');

uploadBtn.addEventListener('click', (e) => {
    e.preventDefault();
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        console.log('Selected file:', fileInput.files[0]);
    }
});


// Events

let events = {};
function addEvent(dateString,title,description, stressLevel){
    if (!events[dateString]){
        events[dateString] = [];
    }
    events[dateString].push({title,description});
    updateCalendar();
    console.log(events);
}

const uploadEventBtn = document.getElementById('uploadBtnE');
const eventDialog = document.getElementById('eventDialog');
const closeDialogBtn = document.getElementById('closeDialog');
const eventForm = document.getElementById('eventUploadForm');

// Open dialog when "Upload Event" is clicked
uploadEventBtn.addEventListener('click', () => {
    eventDialog.showModal();
});

// Close dialog when "Close" button is clicked
closeDialogBtn.addEventListener('click', () => {
    eventDialog.close();
});

// Handle form submission
eventForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const title = document.getElementById('eventTitle').value;
    const date = document.getElementById('eventDate').value;
    const desc  = document.getElementById('eventDesc').value;

    if (!title || !date) {
        alert("Please enter a title and date for the event.");
        return;
    }

    // Call your addEvent function from calendar.js
    addEvent(date, title, desc);

    // Reset form and close dialog
    eventForm.reset();
    eventDialog.close();
    alert("Event added!");
});



// Example usage addEvent('2024-06-15','Meeting','Project discussion at 10 AM');

const slider = document.getElementById("myRange");
const output = document.getElementById("sliderValue");

// Set initial value
output.textContent = slider.value;

// Update while sliding
slider.addEventListener("input", () => {
  output.textContent = slider.value;
});

function attachHoverPick() {
  const dateCells = datesElement.querySelectorAll(".date");

  dateCells.forEach(cell => {
    cell.addEventListener("mouseenter", () => {
      // Remove previous pick
      dateCells.forEach(c => c.classList.remove("picked"));
      // Add pick to the hovered cell
      cell.classList.add("picked");

      // Optional: store the value if you need it
      const pickedDay = cell.textContent;
      console.log("Hovered date:", pickedDay);
    });
  });
}

function attachDateClick() {
  const dateCells = datesElement.querySelectorAll(".date");

  dateCells.forEach(cell => {
    cell.addEventListener("click", () => {
      // Remove previous selection
      dateCells.forEach(c => c.classList.remove("selected"));

      // Mark the clicked date as selected
      cell.classList.add("selected");

      // Optional: store the picked date
      const pickedDay = cell.textContent;
      console.log("Selected date:", pickedDay);
    });
  });
}

