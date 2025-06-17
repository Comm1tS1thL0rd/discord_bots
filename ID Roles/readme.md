# BITS Pilani Goa Discord Bot

A smart Discord bot tailored for BITS Pilani Goa Campus, designed to automate student verification and role assignment using student IDs.

---

## 🚀 What Does This Bot Do?

- **Automated Verification:**  
  Parses BITS Pilani student IDs and verifies students in your Discord server.

- **Role Assignment:**  
  Assigns roles based on:
  - **Batch year** (e.g., 2021–2025, with alumni detection for earlier years)
  - **Academic branch** (supports dual branches)
  - **Campus** (The code supports only goa, however it has support for more)

- **Alumni Detection:**  
  Automatically recognizes and assigns a special role to alumni (students from batches before 2021).


---

## 📝 Supported Commands

- `!verify <student_id>`  
  Verifies the student and assigns all relevant roles.

- `!info [member]`  
  Shows the assigned roles and verification info for a user.

- `!test_parse <student_id>`  
  Tests the ID parsing logic without assigning any roles.

---


## 🏷️ Supported Branches

- Chemical Engineering (A1)
- Electrical & Electronics (A3)
- Mechanical (A4)
- Computer Science (A7)
- Electronics & Instrumentation (A8)
- Electronics & Communication (AA)
- Electronics & Computer (AC)
- Mathematics & Computing (AD)
- Environmental & Sustainability (AJ)
- M.Sc. programs (B1–B7)

---

## ✅ Features

- **Dual branch support** for students with multiple specializations.
- **Automatic role cleanup** before assigning new roles.
- **Channel-specific operation** for added security.
- **Error messages** for invalid IDs, unsupported campuses, or missing roles.

---

This bot streamlines the verification process for BITS Pilani Goa Discord servers, ensuring only genuine students and alumni get the right access and roles, all with minimal admin effort.

---

This bot uses about 35MB of RAM alongside 0% cpu use in a 0.25vCPU allowing it to be hosted for free via Discloud. Thus, it also contains the discloud.config file for the same. Change the config file according to needs and the host u use.