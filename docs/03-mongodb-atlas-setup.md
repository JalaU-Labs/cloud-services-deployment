# MongoDB Atlas Free Tier Setup

This document describes how to create a free M0 cluster in MongoDB Atlas,
configure Network Access and Database Access with strict rules, and obtain the
connection string used by the application.

## 1. Creating the Account

1. Navigate to [https://www.mongodb.com/cloud/atlas/register](https://www.mongodb.com/cloud/atlas/register).
2. Register using an institutional or personal email address.
3. Complete the email verification.
4. When prompted, choose the free plan (M0).

## 2. Creating the Organization and Project

1. Atlas creates a default organization when you register. Rename it if
   desired, for example `Jala University`.
2. Create a project named `Week 7 Lab` under the organization.
3. Select the project. All subsequent actions happen inside it.

## 3. Creating the Free Cluster

1. Click **Build a Database**.
2. Select the **M0 Free** tier.
3. Choose a cloud provider and region. Prefer the region closest to your
   location to reduce latency. For AWS in `us-east-2` (Ohio), choose
   `AWS / us-east-2`.
4. Name the cluster. For this lab, use `lab-cloud-cluster`.
5. Leave the remaining options at their defaults (MongoDB 7.0, no backup, no
   additional settings for the free tier).
6. Click **Create Deployment**.

Provisioning takes between one and three minutes. Wait until the cluster status
shows `Active`.

## 4. Creating the Database User

1. In the left sidebar, open **Database Access**.
2. Click **Add New Database User**.
3. Authentication method: **Password**.
4. Username: choose something neutral. For the lab, use `lab_reader_writer`.
5. Password: generate a strong password with a manager such as `pass`,
   `keepassxc`, or `bitwarden`. Minimum 20 characters with mixed case, digits,
   and symbols.
6. Database User Privileges: for this lab select
   **Read and write to any database**. In production, scope it to a specific
   database.
7. Click **Add User**.

Do not reuse this username or password for any other service. Treat it as a
secret.

## 5. Configuring Network Access

1. In the left sidebar, open **Network Access**.
2. Click **Add IP Address**.
3. Click **Add Current IP Address** to add the public IP of your current
   machine. If you are on the EC2 instance, this is the **public IP of the
   instance**, not the local network IP.
4. Add a comment, for example `Local development - Diego`.
5. Click **Confirm**.

**Never use `Allow Access from Anywhere (0.0.0.0/0)`.** It opens the cluster to
the entire Internet and is one of the leading causes of MongoDB data leaks.
Attackers scan the whole IPv4 space continuously.

If your IP changes frequently, use temporary entries: Atlas allows an IP entry
to expire automatically after a set period (up to one week). This is safer than
opening the whole range.

### Adding the EC2 Public IP

When the EC2 instance is created, note its public IP and add it as a second
entry in the whitelist. Only that specific IP should be authorized, not the
entire subnet.

To find the public IP from the instance:

```bash
curl ifconfig.me
```

The returned address is what must be added to Atlas.

## 6. Obtaining the Connection String

1. Return to the cluster overview and click **Connect**.
2. Select **Drivers**.
3. Choose **Python** and version **4.x or later**.
4. Copy the connection string. It has the following form:

   ```
   mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
   ```

5. Replace `<username>` and `<password>` with the values of the database user.
6. Store the result in the `.env` file on the machine running the application.
   Never commit this file.

Example `.env` entry for local development:

```
MONGODB_URI=mongodb+srv://lab_reader_writer:REPLACE_WITH_PASSWORD@lab-cloud-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=lab_cloud
```

## 7. Testing the Connection

### From the command line

```bash
uv run python - <<'PY'
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.environ["MONGODB_URI"], serverSelectionTimeoutMS=5000)
print(client.admin.command("ping"))
PY
```

Expected output: `{'ok': 1.0}`.

### From MongoDB Compass

1. Open MongoDB Compass.
2. Paste the connection string in the URI field.
3. Click **Connect**.
4. Confirm that the `lab_cloud` database is visible.
5. If desired, create the `contacts` collection manually and insert a test
   document.

## 8. Common Errors

- **`ServerSelectionTimeoutError`**: the IP of the client is not in the
  whitelist, the password is wrong, or the connection string is malformed.
- **`Authentication failed`**: the username or password is incorrect. Verify in
  **Database Access**.
- **`DNS resolution failed`**: the `mongodb+srv` record could not be resolved.
  Check the network and DNS configuration.
- **`TLS handshake failed`**: the system clock is out of sync. Run
  `sudo timedatectl set-ntp true` on Linux.

## 9. Screenshots to Capture

Store under `docs/screenshots/`:

- `atlas-cluster-overview.png` - Cluster status Active.
- `atlas-network-access.png` - Whitelist with a single IP entry.
- `atlas-database-user.png` - User creation screen (password masked).
- `atlas-connection-string.png` - Connection string screen (redact the
  password before capturing).
- `atlas-compass-connected.png` - Compass connected to the cluster.