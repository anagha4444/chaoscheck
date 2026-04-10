const express = require("express");
const session = require("express-session");
const bcrypt = require("bcryptjs");
const mongoose = require("mongoose");
const path = require("path");

const app = express();
const PORT = 3000;

// ✅ IMPORTANT: Docker Mongo URL
const MONGO_URL = "mongodb://database:27017/forestcore";

// ===== Mongo Connection =====
mongoose.connect(MONGO_URL)
  .then(() => console.log("✅ MongoDB connected"))
  .catch((err) => console.error("❌ Mongo error:", err));

// ===== Schema =====
const userSchema = new mongoose.Schema({
  username: { type: String, unique: true, required: true },
  passwordHash: { type: String, required: true },
  displayName: { type: String, required: true },
});

const User = mongoose.model("User", userSchema);

// ===== Middleware =====
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(session({
  secret: "secret",
  resave: false,
  saveUninitialized: false,
}));

// ===== Static files =====
app.use(express.static(path.join(__dirname, "public")));

// ===== Page Routes =====
app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "login.html"));
});

app.get("/signup", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "signup.html"));
});

// ===== Helper =====
function getPublicUser(user) {
  return {
    id: user._id,
    username: user.username,
    displayName: user.displayName,
  };
}

// ===== Auth APIs =====
app.post("/api/signup", async (req, res) => {
  const { username, password, displayName } = req.body;

  try {
    const existing = await User.findOne({ username });
    if (existing) {
      return res.status(409).json({ error: "Username already exists" });
    }

    const passwordHash = bcrypt.hashSync(password, 10);

    const user = await User.create({
      username,
      passwordHash,
      displayName,
    });

    res.json({ user: getPublicUser(user) });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Signup failed" });
  }
});

app.post("/api/login", async (req, res) => {
  const { username, password } = req.body;

  try {
    const user = await User.findOne({ username });

    if (!user) {
      return res.status(401).json({ error: "User not found" });
    }

    const valid = bcrypt.compareSync(password, user.passwordHash);

    if (!valid) {
      return res.status(401).json({ error: "Invalid password" });
    }

    req.session.userId = user._id;

    res.json({ user: getPublicUser(user) });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Login failed" });
  }
});

app.get("/api/me", async (req, res) => {
  if (!req.session.userId) return res.json({ user: null });

  const user = await User.findById(req.session.userId);
  res.json({ user: getPublicUser(user) });
});

app.post("/api/logout", (req, res) => {
  req.session.destroy(() => {
    res.json({ ok: true });
  });
});

// ===== Mushroom API =====
app.get("/api/mushrooms", (req, res) => {
  res.json({
    mushrooms: [
      { id: "fly-agaric", name: "Fly Agaric" },
      { id: "chanterelle", name: "Chanterelle" },
      { id: "lion-mane", name: "Lion’s Mane" }
    ]
  });
});

// ===== Start =====
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});