import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { RefreshCcw, Trash2, Server, Database, Globe2 } from "lucide-react";
import { api, apiConfig } from "./api";
import "./styles.css";

function App() {
  const [health, setHealth] = useState("Checking API...");
  const [message, setMessage] = useState({ type: "", text: "" });
  const [stats, setStats] = useState({
    total_users: 0,
    today_users: 0,
    total_roles: 0
  });
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({
    name: "",
    email: "",
    role: "Student"
  });

  async function loadData() {
    try {
      const healthData = await api.health();
      setHealth(`API ${healthData.status.toUpperCase()} | DB ${healthData.database}`);

      const statsData = await api.stats();
      setStats(statsData);

      const usersData = await api.users();
      setUsers(usersData.users || []);
    } catch {
      setHealth("API Offline");
      setUsers([]);
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setMessage({ type: "", text: "Registering..." });

    try {
      const data = await api.register(form);
      setMessage({ type: "success", text: data.message });
      setForm({ name: "", email: "", role: "Student" });
      await loadData();
    } catch (error) {
      setMessage({ type: "error", text: error.message || "Cannot connect to backend API" });
    }
  }

  async function handleDelete(id) {
    try {
      await api.deleteUser(id);
      await loadData();
    } catch (error) {
      setMessage({ type: "error", text: error.message || "Delete failed" });
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  return (
    <main className="page">
      <nav className="nav">
        <div>
          <div className="brandTitle">Learn DevOps Now Myanmar</div>
          <div className="brandSubtitle">Three Tier Application Demo</div>
        </div>
        <div className="statusPill">{health}</div>
      </nav>

      <section className="hero">
        <div className="panel intro">
          <div>
            <span className="eyebrow">React + Vite Frontend</span>
            <h1>
              Register users with <span>Backend API + Database</span>
            </h1>
            <p className="desc">
              Clean frontend app for Docker, ECS, and CI/CD practice. API URL is configured
              at app build time using <strong>VITE_API_URL</strong>.
            </p>

            <div className="apiBox">
              <div className="apiLabel">Current API URL</div>
              <code>{apiConfig.apiUrl}</code>
            </div>

            <div className="architecture">
              <div className="archCard">
                <Globe2 size={24} />
                <strong>Frontend</strong>
                <small>React + Nginx :80</small>
              </div>

              <div className="archCard">
                <Server size={24} />
                <strong>Backend</strong>
                <small>Flask API :8000</small>
              </div>

              <div className="archCard">
                <Database size={24} />
                <strong>Database</strong>
                <small>PostgreSQL :5432</small>
              </div>
            </div>
          </div>

          <div className="stats">
            <div className="statBox">
              <div className="statNumber">{stats.total_users}</div>
              <div className="statLabel">Total Users</div>
            </div>

            <div className="statBox">
              <div className="statNumber">{stats.today_users}</div>
              <div className="statLabel">Today</div>
            </div>

            <div className="statBox">
              <div className="statNumber">{stats.total_roles}</div>
              <div className="statLabel">Roles</div>
            </div>
          </div>
        </div>

        <div className="panel formPanel">
          <h2>Register Student</h2>
          <p className="muted">Add a user and save it through the backend API.</p>

          <form onSubmit={handleSubmit}>
            <label>Name</label>
            <input
              value={form.name}
              onChange={(event) => setForm({ ...form, name: event.target.value })}
              placeholder="Thaung Htike Oo"
              required
            />

            <label>Email</label>
            <input
              value={form.email}
              onChange={(event) => setForm({ ...form, email: event.target.value })}
              type="email"
              placeholder="student@example.com"
              required
            />

            <label>Role</label>
            <select
              value={form.role}
              onChange={(event) => setForm({ ...form, role: event.target.value })}
            >
              <option>Student</option>
              <option>Developer</option>
              <option>DevOps Engineer</option>
              <option>Cloud Engineer</option>
              <option>Platform Engineer</option>
            </select>

            <button className="submitBtn" type="submit">
              Register Now
            </button>
          </form>

          <div className={`message ${message.type}`}>{message.text}</div>
        </div>
      </section>

      <section className="panel usersSection">
        <div className="sectionHead">
          <div>
            <h2>Registered Users</h2>
            <p className="muted">Live data from backend API.</p>
          </div>

          <button className="refreshBtn" onClick={loadData}>
            <RefreshCcw size={16} />
            Refresh
          </button>
        </div>

        <div className="userGrid">
          {users.length === 0 ? (
            <div className="userItem">No users registered yet.</div>
          ) : (
            users.map((user) => (
              <div className="userItem" key={user.id}>
                <div>
                  <div className="userName">{user.name}</div>
                  <div className="userMeta">{user.email}</div>
                  <span className="role">{user.role}</span>
                </div>

                <button className="deleteBtn" onClick={() => handleDelete(user.id)}>
                  <Trash2 size={16} />
                  Delete
                </button>
              </div>
            ))
          )}
        </div>
      </section>

      <div className="footer">Frontend → VITE_API_URL → Backend API → PostgreSQL Database</div>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
