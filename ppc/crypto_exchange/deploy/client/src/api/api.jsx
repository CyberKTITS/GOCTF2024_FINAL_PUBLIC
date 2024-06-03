import axios from "axios";

export const baseRequest = axios.create({
  baseURL: "http://185.104.106.221:8002",
  headers: {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  },
});
