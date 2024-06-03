import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { baseRequest } from "../api/api";

const Register = () => {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // useEffect(() => {
  //   if (localStorage.getItem("token")) {
  //     navigate("/main");
  //   }
  // }, []);

  const navigate = useNavigate();

  const submitForm = async (e) => {
    e.preventDefault();
    baseRequest
      .post(
        "/auth/register",
        {
          email: email,
          password: password,
          username: username,
        },
        {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
          withCredentials: true,
        }
      )
      .catch((error) => console.log(error))
      .then(() => {
        baseRequest
          .post(
            "/auth/jwt/login",
            {
              username: email,
              password: password,
            },
            {
              headers: {
                accept: "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
              },
            }
          )
          .then((result) => {
            localStorage.clear();
            localStorage.setItem("token", result.data.access_token);
            navigate("/main");
          });
      });
  };

  return (
    <div className="authWrapper">
      <div className="authContainer">
        <h1>Регистрация</h1>
        <form onSubmit={submitForm}>
          <div>
            <label>
              email
              <input
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </label>
          </div>
          <div>
            <label>
              Никнейм
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </label>
          </div>
          <div>
            <label>
              Пароль
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </label>
          </div>
          <button disabled={!email && !password && !username}>Вход</button>
        </form>
      </div>
    </div>
  );
};

export default Register;
