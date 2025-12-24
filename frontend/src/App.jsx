import { useEffect } from "react";
import { apiRequest } from "./services/api";

function App() {
  useEffect(() => {
    apiRequest("/")
      .then((res) => console.log("Backend says:", res))
      .catch((err) => console.error(err));
  }, []);

  return <h1>Collaborative Calendar</h1>;
}

export default App;
