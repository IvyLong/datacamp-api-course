# Troubleshooting Guide

## 🔧 Common Issues and Solutions

### Issue 1: "Connection refused" or "No response from server"

**Symptom:** `curl: (7) Failed to connect to localhost port 5000`

**Solution:** You're using the wrong port!

When using Docker (`./auto/run`):
```bash
# ✅ CORRECT
curl http://localhost:5001/

# ❌ WRONG
curl http://localhost:5001/
```

Docker maps container port 5000 → host port **5001**.

Check if the container is running:
```bash
docker ps
```

You should see a container with port mapping `0.0.0.0:5001->5000/tcp`.

---

### Issue 2: Server is not starting

**Symptom:** `./auto/run` exits immediately or shows errors

**Check Docker is running:**
```bash
docker info
```

If not running, start Docker Desktop.

**Check for errors in build:**
```bash
docker build -t thought-tagger-workshop .
```

---

### Issue 3: "ModuleNotFoundError: No module named 'flask'"

**Symptom:** Import errors when running Python files

**Solution:** 

If using Docker:
```bash
# Rebuild the Docker image
cd /path/to/project
docker build -t thought-tagger-workshop .
```

If running locally:
```bash
pip install Flask
# or
pip install -r requirements.txt
```

---

### Issue 4: "Address already in use"

**Symptom:** `OSError: [Errno 48] Address already in use`

**Solution:** Another server is already running on that port.

Find and stop the process:
```bash
# macOS/Linux
lsof -i :5000
kill -9 <PID>

# Or stop all Flask servers
docker ps
docker stop <container_id>
```

---

### Issue 5: Changes not showing up

**Symptom:** I modified the code but still see old behavior

**Solution:** 

1. **Stop the server** (Ctrl+C)
2. **Restart it**:
   ```bash
   ./auto/run python week-2/tutorial/step-1-hello-world.py
   ```

Note: Flask's debug mode auto-reloads, but sometimes requires a manual restart.

---

### Issue 6: Can't POST data - 400 Bad Request

**Symptom:** POST request fails with 400 error

**Check Content-Type header:**
```bash
# ✅ CORRECT - Include Content-Type
curl -X POST http://localhost:5001/api/v1/thoughts \
  -H "Content-Type: application/json" \
  -d '{"text": "Test", "tags": ["test"]}'

# ❌ WRONG - Missing header
curl -X POST http://localhost:5001/api/v1/thoughts \
  -d '{"text": "Test", "tags": ["test"]}'
```

**Check JSON syntax:**
- Use double quotes for JSON keys and values
- No trailing commas
- Properly escape special characters

---

### Issue 7: Docker is slow to start

**Symptom:** `./auto/run` takes a long time on first run

**Solution:** This is normal! Docker needs to:
1. Build the image (downloads Python, installs packages)
2. Start the container

**First run:** 2-5 minutes  
**Subsequent runs:** < 10 seconds (uses cached layers)

To see progress:
```bash
docker build -t thought-tagger-workshop .
```

---

### Issue 8: How to stop the server?

**Stop the running container:**
```bash
# Find container ID
docker ps

# Stop it
docker stop <container_id>

# Or stop all
docker stop $(docker ps -q)
```

**Or just use Ctrl+C** in the terminal where it's running.

---

## 🧪 Quick Tests

### Test if Docker is working:
```bash
docker run hello-world
```

### Test if server is running:
```bash
curl -I http://localhost:5001/
```

Should return `HTTP/1.1 200 OK`.

### Test if port is accessible:
```bash
nc -zv localhost 5001
```

Should return: `Connection to localhost port 5001 [tcp/*] succeeded!`

---

## 🆘 Still Having Issues?

1. **Check the logs:**
   ```bash
   docker logs <container_id>
   ```

2. **Try rebuilding:**
   ```bash
   docker build --no-cache -t thought-tagger-workshop .
   ```

3. **Check Python version:**
   ```bash
   docker run thought-tagger-workshop python --version
   ```
   Should be Python 3.11+

4. **Verify requirements:**
   ```bash
   docker run thought-tagger-workshop pip list
   ```
   Should show Flask in the list.

---

## 📚 Helpful Commands

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View Docker images
docker images

# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Full cleanup (careful!)
docker system prune -a
```

---

**Need more help?** Check the main README.md or contact the instructor.

