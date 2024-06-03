import { Route, Routes } from "react-router-dom";
import "./App.css";
import MainApp from "./components/MainApp";
import Register from "./components/Register";

const App = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<Register />} />
        <Route path="/main" element={<MainApp />} />
      </Routes>
    </>
  );
};

export default App;
