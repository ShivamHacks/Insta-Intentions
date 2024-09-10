
# API Documentation

### Base URL:
`http://ec2-3-133-160-113.us-east-2.compute.amazonaws.com:5000/`

---

### 1. **Create User ID**

Creates a new user with a unique ID and initializes the user's data.

**Endpoint:**
```
GET /create_user_id
```

**Response:**

```json
{
  "status": "success",
  "user_id": "<newly_created_user_id>"
}
```

---

### 2. **Add Liked Username**

Adds an Instagram username to a user's list of liked handles and updates the corresponding handle with the user’s ID.

**Endpoint:**
```
GET /add_liked_username?user_id={user_id}&username={username}
```

**Parameters:**

- `user_id` (required): The unique ID of the user.
- `username` (required): The Instagram username the user wants to like.

**Response:**

- Success:

```json
{
  "status": "success"
}
```

- Error:

```json
{
  "status": "error",
  "message": "<error_message>"
}
```

---

### 3. **Get People Who Have Liked an Instagram Handle**

Retrieves the verified users and unverified counts who have liked a specific Instagram handle.

**Endpoint:**
```
GET /get_people_that_have_liked?insta_handle={insta_handle}
```

**Parameters:**

- `insta_handle` (required): The Instagram handle to query for likes.

**Response:**

```json
{
  "status": "success",
  "verified_insta_handles_that_have_liked": [
    "<verified_user_handle_1>",
    "<verified_user_handle_2>"
  ],
  "unverified_uuids_that_have_liked": <number_of_unverified_likes>
}
```

- Error:

```json
{
  "status": "error",
  "message": "<error_message>"
}
```

---

### 4. **Is User Verified**

Checks if a specific user is verified.

**Endpoint:**
```
GET /is_user_verified?user_id={user_id}
```

**Parameters:**

- `user_id` (required): The unique ID of the user.

**Response:**

- Success:

```json
{
  "status": "success",
  "result": <true_or_false>
}
```

- Error:

```json
{
  "status": "error",
  "message": "<error_message>"
}
```

---

### 5. **Verify User**

Verifies a user and associates them with an Instagram handle.

**Endpoint:**
```
GET /verify_user?user_id={user_id}&insta_handle={insta_handle}
```

**Parameters:**

- `user_id` (required): The unique ID of the user.
- `insta_handle` (required): The Instagram handle to verify the user with.

**Response:**

- Success:

```json
{
  "status": "success"
}
```

- Error:

```json
{
  "status": "error",
  "message": "<error_message>"
}
```

---

### 6. **Dump Full Database (Debug Only)**

Returns a full dump of the user and Instagram handle data.

**Endpoint:**
```
GET /dump_full_database
```

**Response:**

```json
{
  "users": {
    "<user_id_1>": {
      "insta_handle": "<handle_1>",
      "verified": true,
      "insta_handles_you_like": []
    },
    "<user_id_2>": {
      ...
    }
  },
  "insta_handles": {
    "<insta_handle_1>": {
      "uids_that_have_liked": [
        "<user_id_1>",
        "<user_id_2>"
      ]
    },
    "<insta_handle_2>": {
      ...
    }
  }
}
```

# Misc Dev Notes

## File structure

database.py - main file, handles all database interactions

server.py - server interface for database

cli.py - command-line interface for database

simulator.py - LLM-backed real-world simulator using database

## Helpful commands to sync files with EC2
rsync -av --exclude='.venv' . ec2-user@ec2-3-133-160-113.us-east-2.compute.amazonaws.com:/home/ec2-user/InstaIntentions/
ssh ec2-user@ec2-3-133-160-113.us-east-2.compute.amazonaws.com

Root url: http://ec2-3-133-160-113.us-east-2.compute.amazonaws.com:5000/

## Helpful tips for EC2 setup
1. Needed to make sure inbound rules in security groups on EC2 page included inbound traffic
2. Check if server working locally with curl http://localhost:5000

## Running flask server in background so ssh can be closed
nohup python server.py > flask.log 2>&1 &

## Killing flask server 
ps aux | grep python
