// this is a sample issue - fix template 

# Service: Mushroom Website (Node.js)
- **Port:** 3000
- **Process Name:** mushroom-app
- **Critical Files:** app.js, routes/auth.js

## Error: "ECONNREFUSED" or "MongooseServerSelectionError"
- **Meaning:** The website cannot talk to the MongoDB database.
- **Possible Cause:** The database container is stopped or crashed.
- **Fix:** Run `docker-compose restart database` or `docker start database`.

---

# Service: Database (MongoDB)
- **Port:** 27017
- **Volume Path:** /data/db

## Error: "Filesystem Read-Only"
- **Meaning:** The Docker volume has a permission error.
- **Fix:** Run `docker-compose down && docker-compose up -d`.

---

# Service: Authentication (User Login)
## Error: "Internal Server Error 500" on /login
- **Possible Cause:** The JWT Secret is missing from environment variables.
- **Fix:** Check if `.env` file exists and contains `JWT_SECRET`.