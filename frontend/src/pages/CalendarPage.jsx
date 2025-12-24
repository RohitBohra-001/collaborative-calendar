import { useEffect, useState } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import { apiRequest } from "../services/api";

function CalendarPage() {
  const [events, setEvents] = useState([]);

  const loginTestUser = async () => {
    try {
      await apiRequest("/login", {
        method: "POST",
        body: JSON.stringify({
          email: "rohit@test.com",
          password: "test123",
        }),
      });
      alert("Logged in from browser");
    } catch (err) {
      console.error("Login failed", err);
    }
  };

  useEffect(() => {
    apiRequest("/calendars/1/events")
      .then((data) => {
        const formatted = data.map((e) => ({
          id: e.id,
          title: e.title,
          start: new Date(e.start_time),
          end: new Date(e.end_time),
        }));
        setEvents(formatted);
        console.log("Formatted events:", formatted);
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>My Calendar</h2>

      <button onClick={loginTestUser}>
        Login (Test User)
      </button>

      <FullCalendar
        plugins={[dayGridPlugin]}
        initialView="dayGridMonth"
        events={events}
      />
    </div>
  );
}

export default CalendarPage;
