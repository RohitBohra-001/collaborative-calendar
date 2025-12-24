const API_BASE = "http://127.0.0.1:5000";

export async function apiRequest(endpoint, options = {}) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    credentials: "include",   // 🔴 VERY IMPORTANT
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error("API request failed");
  }

  return response.json();
}
