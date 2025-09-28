const monthYearElement = document.getElementById('monthYear');
const datesElement = document.getElementById('dates');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

let currentDate = new Date();
let events = {}; // grouped by date string (YYYY-MM-DD)

// ---------- Calendar Rendering ----------
function updateCalendar() {
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);

    const totalDays = lastDay.getDate();
    const firstDayIndex = firstDay.getDay();
    const lastDayIndex = lastDay.getDay();

    const monthYearString = currentDate.toLocaleDateString('default', {
        month: 'long',
        year: 'numeric'
    });
    monthYearElement.textContent = monthYearString;

    let datesHTML = '';

    // Previous month padding
    for (let i = firstDayIndex - 1; i >= 0; i--) {
        const prevDate = new Date(currentYear, currentMonth, -i);
        datesHTML += `<div class="date inactive">${prevDate.getDate()}</div>`;
    }

    // Current month dates
    for (let i = 1; i <= totalDays; i++) {
        const date = new Date(currentYear, currentMonth, i);
        const activeClass =
            date.toDateString() === new Date().toDateString() ? 'active' : '';

        datesHTML += `<div class="date ${activeClass}">${i}</div>`;
    }

    // Next month padding
    for (let i = 1; i < 7 - lastDayIndex; i++) {
        const nextDate = new Date(currentYear, currentMonth + 1, i);
        datesHTML += `<div class="date inactive">${nextDate.getDate()}</div>`;
    }

    datesElement.innerHTML = datesHTML;

    attachDateClick();
}

// ---------- Month Navigation ----------
prevBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
});

nextBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
});

// ---------- Event Handling ----------
async function loadEvents() {
    try {
        const res = await fetch("/events");
        const rawEvents = await res.json();

        // normalize into {date: [events]}
        events = {};
        rawEvents.forEach(ev => {
            const key = ev.date;
            if (!events[key]) events[key] = [];
            events[key].push(ev);
        });

        console.log("Loaded events:", events);
        updateCalendar();
    } catch (err) {
        console.error("Error loading events:", err);
    }
}

async function addEvent(dateString, time, title, description, stressLevel) {
    const newEvent = {
        date: dateString,
        time: "00:00", // default if no time picker yet
        title,
        description,
        stress: stressLevel
    };

    // local update
    if (!events[dateString]) {
        events[dateString] = [];
    }
    events[dateString].push(newEvent);

    // send to backend
    try {
        const res = await fetch("/events", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newEvent)
        });
        const saved = await res.json();
        console.log("Saved event:", saved);
    } catch (err) {
        console.error("Error saving event:", err);
    }

    updateCalendar();
}

function attachDateClick() {
    const dateCells = datesElement.querySelectorAll(".date");

    dateCells.forEach(cell => {
        cell.addEventListener("click", () => {
            dateCells.forEach(c => c.classList.remove("selected"));
            cell.classList.add("selected");

            const day = cell.textContent;
            const selectedDate = new Date(
                currentDate.getFullYear(),
                currentDate.getMonth(),
                day
            );
            const key = selectedDate.toISOString().split("T")[0];

            const formattedDate = selectedDate.toLocaleDateString("en-US", {
                month: "long",
                day: "numeric",
                year: "numeric"
            });

            const eventList = events[key] || [];
            const box = document.getElementById("eventsBox");
            
            if (eventList.length === 0) {
    box.innerHTML = `
      <div class="event-box">
        <h1 class="event-title">${formattedDate}</h1>
        <p>No events for this day.</p>
      </div>
    `;
} else {
    const listHTML = eventList
        .map(ev => `<li><strong>${ev.title}</strong>: ${ev.description} (Stress: ${ev.stress})</li>`)
        .join("");
    box.innerHTML = `
      <div class="event-box">
        <h3 class="event-title">${formattedDate}</h3>
        <ul class="event-list">${listHTML}</ul>
      </div>
    `;
}

        });
    });
}

// ---------- Upload Event Dialog ----------
const uploadEventBtn = document.getElementById('uploadBtnE');
const eventDialog = document.getElementById('eventDialog');
const closeDialogBtn = document.getElementById('closeDialog');
const eventForm = document.getElementById('eventUploadForm');
const slider = document.getElementById("myRange");
const output = document.getElementById("sliderValue");

// Open dialog
uploadEventBtn.addEventListener('click', () => {
    eventDialog.showModal();
});

// Close dialog
closeDialogBtn.addEventListener('click', () => {
    eventDialog.close();
});

// Form submit
eventForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const title = document.getElementById('eventTitle').value;
    const date = document.getElementById('eventDate').value;
    const time = document.getElementById('appt-time').value || "00:00";
    const desc = document.getElementById('eventDesc').value;
    const stressLevel = slider.value;

    if (!title || !date) {
        alert("Please enter a title and date for the event.");
        return;
    }

    addEvent(date, time, title, desc, stressLevel);

    eventForm.reset();
    eventDialog.close();
    alert("Event added!");
});

// Stress slider
output.textContent = slider.value;
slider.addEventListener("input", () => {
    output.textContent = slider.value;
});

// ---------- Initialize ----------
loadEvents();
