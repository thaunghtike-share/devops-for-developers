const API_URL = import.meta.env.VITE_API_URL;

if (!API_URL) {
  throw new Error("VITE_API_URL is required");
}

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, options);
  const contentType = response.headers.get("content-type") || "";

  const data = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message = typeof data === "object" ? data.error || "Request failed" : data;
    throw new Error(message);
  }

  return data;
}

export const apiConfig = {
  apiUrl: API_URL
};

export const api = {
  health: () => request("/api/health"),
  stats: () => request("/api/stats"),
  users: () => request("/api/users"),
  register: (payload) =>
    request("/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    }),
  deleteUser: (id) =>
    request(`/api/users/${id}`, {
      method: "DELETE"
    })
};
