# Project "E-Queue"

## Team
- Mykhnian Ihor  
- Chervinchuk Mykola
- Verbivskii Yura

---

## Project goal
**E-Queue** is a web application made to organize queues within a university (for example, for submitting lab work, consultations, or exams).

The system allows students to join a queue online, view their current status, receive reminders about their scheduled time, and reduce real waiting time outside the classroom.

---

## Short Description of Functionality

- **Queue Creation** — a teacher or administrator can create an event (e.g., “Lab Defense #3”), select the date, time, and number of slots.  
- **Join a Queue** — a student can join a queue online, receive their position, and see the expected time for their turn.  
- **Notifications** — users receive alerts when their turn is approaching (via Email or SMS API).  
- **Google Calendar Integration** — when joining a queue, the event is automatically added to the user's calendar.  
- **Monobank API Integration** — a demonstration integration showing interaction with an external financial service (e.g., tracking donations or test payments).  
- **Real-Time Updates** — via WebSockets, users see the current state of the queue without refreshing the page.  
- **Authentication** — using JWT tokens (Django Rest Framework).  
- **Roles** — teachers, students, and administrators have different access levels.

---

## Technologies

### Backend
- **JWT Authentication**
- **Integrations:**  
  - Monobank Personal API  
  - Google Calendar API  
  - Email/SMS Notification API (SendGrid or Twilio)

### Frontend
- **REST API integration with the backend**
