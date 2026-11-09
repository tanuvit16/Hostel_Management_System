
# import tkinter as tk
# from tkinter import ttk, messagebox
# from datetime import date
# import api


# # -------------------- THEME --------------------

# BG = "#F1F5F9"
# PRIMARY = "#1D4ED8"
# DARK = "#172554"
# WHITE = "#FFFFFF"
# TEXT = "#1E293B"


# def setup_window(window, title, size):
#     window.title(title)
#     window.geometry(size)
#     window.configure(bg=BG)


# def make_tree(parent, columns, headings, height=9):
#     frame = ttk.Frame(parent)
#     frame.pack(fill="both", expand=True, padx=12, pady=8)

#     tree = ttk.Treeview(
#         frame, columns=columns, show="headings", height=height
#     )

#     for col, heading in zip(columns, headings):
#         tree.heading(col, text=heading)
#         tree.column(col, width=120, anchor="center")

#     vs = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
#     hs = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

#     tree.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)

#     tree.grid(row=0, column=0, sticky="nsew")
#     vs.grid(row=0, column=1, sticky="ns")
#     hs.grid(row=1, column=0, sticky="ew")

#     frame.rowconfigure(0, weight=1)
#     frame.columnconfigure(0, weight=1)

#     return tree


# def fill_tree(tree, records, keys):
#     tree.delete(*tree.get_children())

#     for record in records:
#         tree.insert(
#             "", "end",
#             values=[record.get(k, "") for k in keys]
#         )


# def action_result(result):
#     if result.get("success"):
#         messagebox.showinfo("Success", result.get("message", "Operation completed"))
#         return True

#     messagebox.showerror("Error", result.get("message", "Operation failed"))
#     return False


# # -------------------- LOGIN WINDOW --------------------

# class HostelApp:

#     def __init__(self, root):
#         self.root = root
#         setup_window(root, "Hostel Management System - Admin Login", "430x430")
#         self.root.resizable(False, False)

#         self.create_login()

#     def create_login(self):

#         header = tk.Frame(self.root, bg=DARK, height=105)
#         header.pack(fill="x")

#         tk.Label(
#             header, text="HOSTEL MANAGEMENT",
#             font=("Arial", 21, "bold"),
#             fg=WHITE, bg=DARK
#         ).pack(pady=(22, 4))

#         tk.Label(
#             header, text="ADMINISTRATOR LOGIN",
#             font=("Arial", 10),
#             fg="#BFDBFE", bg=DARK
#         ).pack()

#         form = tk.LabelFrame(
#             self.root, text="Login Credentials",
#             font=("Arial", 11, "bold"),
#             bg=WHITE, padx=25, pady=20
#         )
#         form.pack(fill="both", padx=30, pady=25)

#         tk.Label(form, text="Username", bg=WHITE).pack(anchor="w")
#         self.username = tk.Entry(form, font=("Arial", 12))
#         self.username.pack(fill="x", pady=(5, 15))

#         tk.Label(form, text="Password", bg=WHITE).pack(anchor="w")
#         self.password = tk.Entry(form, show="*", font=("Arial", 12))
#         self.password.pack(fill="x", pady=5)

#         self.show_password = tk.BooleanVar(value=False)

#         tk.Checkbutton(
#             form, text="Show Password",
#             variable=self.show_password,
#             command=self.toggle_password,
#             bg=WHITE
#         ).pack(anchor="w", pady=5)

#         buttons = tk.Frame(form, bg=WHITE)
#         buttons.pack(fill="x", pady=12)

#         tk.Button(
#             buttons, text="LOGIN",
#             bg=PRIMARY, fg=WHITE,
#             width=12, command=self.do_login
#         ).pack(side="left", padx=5)

#         tk.Button(
#             buttons, text="RESET",
#             width=10, command=self.reset
#         ).pack(side="left", padx=5)

#         tk.Button(
#             buttons, text="EXIT",
#             width=8, command=self.root.destroy
#         ).pack(side="left", padx=5)

#         tk.Label(
#             self.root, text="Default: admin / admin123",
#             bg=BG, fg="#64748B"
#         ).pack()

#         self.password.bind("<Return>", lambda e: self.do_login())

#     def toggle_password(self):
#         self.password.config(
#             show="" if self.show_password.get() else "*"
#         )

#     def reset(self):
#         self.username.delete(0, "end")
#         self.password.delete(0, "end")

#     def do_login(self):
#         username = self.username.get().strip()
#         password = self.password.get().strip()

#         if not username or not password:
#             messagebox.showwarning("Validation", "Enter username and password")
#             return

#         result = api.login(username, password)

#         if result.get("success"):
#             messagebox.showinfo("Welcome", "Admin login successful!")
#             self.root.withdraw()
#             Dashboard(self.root)
#         else:
#             messagebox.showerror(
#                 "Login Failed", result.get("message", "Invalid credentials")
#             )


# # -------------------- DASHBOARD WINDOW --------------------

# class Dashboard:

#     def __init__(self, parent):
#         self.window = tk.Toplevel(parent)
#         self.parent = parent

#         setup_window(self.window, "Hostel Management - Dashboard", "1050x680")
#         self.window.protocol("WM_DELETE_WINDOW", self.logout)

#         self.create_menu()
#         self.create_dashboard()
#         self.refresh_stats()

#     def create_menu(self):
#         menubar = tk.Menu(self.window)

#         management = tk.Menu(menubar, tearoff=0)
#         management.add_command(label="Students", command=self.open_students)
#         management.add_command(label="Rooms", command=self.open_rooms)
#         management.add_command(label="Fees", command=self.open_fees)

#         reports = tk.Menu(menubar, tearoff=0)
#         reports.add_command(label="View Reports", command=self.open_reports)

#         account = tk.Menu(menubar, tearoff=0)
#         account.add_command(label="Logout", command=self.logout)

#         menubar.add_cascade(label="Management", menu=management)
#         menubar.add_cascade(label="Reports", menu=reports)
#         menubar.add_cascade(label="Account", menu=account)

#         self.window.config(menu=menubar)

#     def create_dashboard(self):

#         header = tk.Canvas(
#             self.window, height=115,
#             bg=DARK, highlightthickness=0
#         )
#         header.pack(fill="x")

#         header.create_text(
#             35, 38, anchor="w",
#             text="HOSTEL MANAGEMENT SYSTEM",
#             fill=WHITE, font=("Arial", 22, "bold")
#         )

#         header.create_text(
#             35, 78, anchor="w",
#             text="Administrator Dashboard",
#             fill="#BFDBFE", font=("Arial", 12)
#         )

#         tk.Label(
#             self.window, text="Dashboard Overview",
#             font=("Arial", 18, "bold"),
#             bg=BG, fg=TEXT
#         ).pack(anchor="w", padx=25, pady=18)

#         self.stats_frame = tk.Frame(self.window, bg=BG)
#         self.stats_frame.pack(fill="x", padx=20)

#         self.stat_labels = {}

#         cards = [
#             ("Students", "total_students", "#2563EB"),
#             ("Total Rooms", "total_rooms", "#0891B2"),
#             ("Occupied Rooms", "occupied_rooms", "#D97706"),
#             ("Available Rooms", "available_rooms", "#059669"),
#             ("Pending Fees", "pending_fees", "#DC2626")
#         ]

#         for title, key, color in cards:
#             card = tk.Frame(
#                 self.stats_frame, bg=WHITE,
#                 padx=15, pady=20,
#                 highlightbackground="#CBD5E1",
#                 highlightthickness=1
#             )
#             card.pack(
#                 side="left", expand=True, fill="both",
#                 padx=5, pady=5
#             )

#             tk.Label(
#                 card, text=title, bg=WHITE,
#                 fg="#64748B", font=("Arial", 10)
#             ).pack()

#             value = tk.Label(
#                 card, text="0", bg=WHITE,
#                 fg=color, font=("Arial", 25, "bold")
#             )
#             value.pack(pady=8)

#             self.stat_labels[key] = value

#         tk.Label(
#             self.window, text="Quick Actions",
#             font=("Arial", 17, "bold"),
#             bg=BG, fg=TEXT
#         ).pack(anchor="w", padx=25, pady=(25, 10))

#         actions = tk.Frame(self.window, bg=BG)
#         actions.pack(fill="x", padx=20)

#         buttons = [
#             ("Student Management", self.open_students),
#             ("Room Management", self.open_rooms),
#             ("Fee Management", self.open_fees),
#             ("Reports", self.open_reports)
#         ]

#         for title, command in buttons:
#             tk.Button(
#                 actions, text=title,
#                 command=command,
#                 bg=PRIMARY, fg=WHITE,
#                 font=("Arial", 11, "bold"),
#                 width=20, height=2
#             ).pack(side="left", padx=7, pady=10)

#         tk.Button(
#             self.window, text="REFRESH STATISTICS",
#             command=self.refresh_stats,
#             bg="#334155", fg=WHITE
#         ).pack(pady=20)

#         # Listbox for quick navigation
#         quick = tk.LabelFrame(
#             self.window, text="Navigation Shortcuts",
#             bg=WHITE, padx=10, pady=5
#         )
#         quick.pack(fill="x", padx=25, pady=5)

#         self.shortcut = tk.Listbox(
#             quick, height=2, font=("Arial", 10)
#         )
#         self.shortcut.insert("end", "Student Records")
#         self.shortcut.insert("end", "Room Records")
#         self.shortcut.pack(fill="x")

#         self.shortcut.bind(
#             "<<ListboxSelect>>", self.shortcut_action
#         )

#     def shortcut_action(self, event):
#         selection = self.shortcut.curselection()
#         if not selection:
#             return

#         if selection[0] == 0:
#             self.open_students()
#         else:
#             self.open_rooms()

#     def refresh_stats(self):
#         result = api.get_stats()

#         if not result.get("success"):
#             messagebox.showerror("Error", result.get("message"))
#             return

#         records = result.get("data", [])

#         if records:
#             for key, value in records[0].items():
#                 if key in self.stat_labels:
#                     self.stat_labels[key].config(text=str(value))

#     def open_students(self):
#         StudentWindow(self.window)

#     def open_rooms(self):
#         RoomWindow(self.window)

#     def open_fees(self):
#         FeeWindow(self.window)

#     def open_reports(self):
#         ReportWindow(self.window)

#     def logout(self):
#         if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
#             self.window.destroy()
#             self.parent.deiconify()


# # -------------------- STUDENT MANAGEMENT WINDOW --------------------

# class StudentWindow:

#     def __init__(self, parent):
#         self.window = tk.Toplevel(parent)
#         setup_window(self.window, "Student Management", "1150x780")

#         self.selected_id = None
#         self.create_ui()
#         self.refresh()

#     def create_ui(self):

#         tk.Label(
#             self.window, text="STUDENT MANAGEMENT",
#             font=("Arial", 20, "bold"),
#             bg=DARK, fg=WHITE, pady=15
#         ).pack(fill="x")

#         form = tk.LabelFrame(
#             self.window, text="Student Information",
#             bg=WHITE, padx=12, pady=8
#         )
#         form.pack(fill="x", padx=12, pady=8)

#         self.fields = {}

#         labels = [
#             ("Student Name", "student_name"),
#             ("Roll Number", "roll_number"),
#             ("Phone Number", "phone_number"),
#             ("Email", "email"),
#             ("Guardian Contact", "guardian_contact")
#         ]

#         for i, (label, key) in enumerate(labels):
#             row, col = divmod(i, 3)

#             tk.Label(form, text=label, bg=WHITE).grid(
#                 row=row*2, column=col, sticky="w", padx=8, pady=3
#             )

#             entry = tk.Entry(form, width=27)
#             entry.grid(
#                 row=row*2+1, column=col,
#                 padx=8, pady=4, sticky="ew"
#             )
#             self.fields[key] = entry

#         tk.Label(form, text="Department", bg=WHITE).grid(
#             row=4, column=0, sticky="w", padx=8
#         )

#         self.department = ttk.Combobox(
#             form, values=[
#                 "CSE", "IT", "ECE", "EEE", "Mechanical",
#                 "Civil", "Biotechnology", "Other"
#             ], state="readonly", width=24
#         )
#         self.department.grid(row=5, column=0, padx=8, pady=4)
#         self.department.set("CSE")

#         tk.Label(form, text="Gender", bg=WHITE).grid(
#             row=4, column=1, sticky="w", padx=8
#         )

#         self.gender = ttk.Combobox(
#             form, values=["Male", "Female", "Other"],
#             state="readonly", width=24
#         )
#         self.gender.grid(row=5, column=1, padx=8, pady=4)
#         self.gender.set("Male")

#         tk.Label(form, text="Student Type", bg=WHITE).grid(
#             row=4, column=2, sticky="w", padx=8
#         )

#         self.student_type = tk.StringVar(value="Regular")

#         type_frame = tk.Frame(form, bg=WHITE)
#         type_frame.grid(row=5, column=2, sticky="w")

#         for value in ["Regular", "Scholarship"]:
#             tk.Radiobutton(
#                 type_frame, text=value,
#                 variable=self.student_type,
#                 value=value, bg=WHITE
#             ).pack(side="left")

#         tk.Label(form, text="Facilities", bg=WHITE).grid(
#             row=6, column=0, sticky="w", padx=8
#         )

#         facility_frame = tk.Frame(form, bg=WHITE)
#         facility_frame.grid(row=7, column=0, columnspan=3, sticky="w")

#         self.facilities = {}

#         for name in ["WiFi", "Laundry", "Mess", "AC"]:
#             var = tk.BooleanVar()
#             self.facilities[name] = var

#             tk.Checkbutton(
#                 facility_frame, text=name,
#                 variable=var, bg=WHITE
#             ).pack(side="left", padx=8)

#         tk.Label(form, text="Address", bg=WHITE).grid(
#             row=8, column=0, sticky="w", padx=8
#         )

#         self.address = tk.Text(form, height=2, width=70)
#         self.address.grid(
#             row=9, column=0, columnspan=3,
#             padx=8, pady=5, sticky="ew"
#         )

#         buttons = tk.Frame(form, bg=WHITE)
#         buttons.grid(row=10, column=0, columnspan=3, pady=8)

#         for title, command, color in [
#             ("ADD", self.add, "#059669"),
#             ("UPDATE", self.update, "#2563EB"),
#             ("DELETE", self.delete, "#DC2626"),
#             ("CLEAR", self.clear, "#64748B")
#         ]:
#             tk.Button(
#                 buttons, text=title, command=command,
#                 bg=color, fg=WHITE, width=12
#             ).pack(side="left", padx=5)

#         search_frame = tk.Frame(self.window, bg=BG)
#         search_frame.pack(fill="x", padx=15, pady=5)

#         tk.Label(
#             search_frame, text="Search Student:",
#             bg=BG, font=("Arial", 11, "bold")
#         ).pack(side="left")

#         self.search = tk.Entry(search_frame, width=35)
#         self.search.pack(side="left", padx=8)

#         tk.Button(
#             search_frame, text="SEARCH",
#             command=self.refresh, bg=PRIMARY, fg=WHITE
#         ).pack(side="left")

#         tk.Button(
#             search_frame, text="SHOW ALL",
#             command=self.show_all
#         ).pack(side="left", padx=5)

#         columns = (
#             "student_id", "student_name", "roll_number",
#             "phone_number", "email", "department",
#             "gender", "student_type"
#         )

#         self.tree = make_tree(
#             self.window, columns,
#             ("ID", "Name", "Roll No", "Phone", "Email",
#              "Department", "Gender", "Type")
#         )

#         self.tree.bind("<<TreeviewSelect>>", self.select_record)

#     def get_data(self):
#         return {
#             key: entry.get().strip()
#             for key, entry in self.fields.items()
#         }

#     def refresh(self):
#         search = self.search.get().strip()

#         result = api.get_students(search)

#         if result.get("success"):
#             fill_tree(
#                 self.tree, result.get("data", []),
#                 ["student_id", "student_name", "roll_number",
#                  "phone_number", "email", "department",
#                  "gender", "student_type"]
#             )
#         else:
#             messagebox.showerror("Error", result.get("message"))

#     def show_all(self):
#         self.search.delete(0, "end")
#         self.refresh()

#     def clear(self):
#         self.selected_id = None

#         for entry in self.fields.values():
#             entry.delete(0, "end")

#         self.department.set("CSE")
#         self.gender.set("Male")
#         self.student_type.set("Regular")
#         self.address.delete("1.0", "end")

#         for var in self.facilities.values():
#             var.set(False)

#     def select_record(self, event):
#         selected = self.tree.selection()
#         if not selected:
#             return

#         values = self.tree.item(selected[0], "values")
#         self.selected_id = values[0]

#         for key, value in zip(
#             ["student_name", "roll_number", "phone_number",
#              "email"], values[1:5]
#         ):
#             self.fields[key].delete(0, "end")
#             self.fields[key].insert(0, value)

#         self.department.set(values[5])
#         self.gender.set(values[6])
#         self.student_type.set(values[7])

#         # Fetch complete student details, including address
#         result = api.get_students(values[2])

#         if result.get("success") and result.get("data"):
#             record = next(
#                 (r for r in result["data"]
#                  if str(r["student_id"]) == str(self.selected_id)),
#                 None
#             )

#             if record:
#                 for key in ["guardian_contact"]:
#                     self.fields[key].delete(0, "end")
#                     self.fields[key].insert(0, record.get(key) or "")

#                 self.address.delete("1.0", "end")
#                 self.address.insert("1.0", record.get("address") or "")

#                 selected_facilities = (record.get("facilities") or "").split(",")
#                 for name, var in self.facilities.items():
#                     var.set(name in selected_facilities)

#     def collect(self):
#         data = self.get_data()
#         data.update({
#             "department": self.department.get(),
#             "gender": self.gender.get(),
#             "student_type": self.student_type.get(),
#             "address": self.address.get("1.0", "end").strip(),
#             "facilities": ",".join(
#                 name for name, var in self.facilities.items()
#                 if var.get()
#             )
#         })

#         if not data["student_name"] or not data["roll_number"]:
#             messagebox.showwarning(
#                 "Validation", "Student name and roll number are required"
#             )
#             return None

#         return data

#     def add(self):
#         data = self.collect()
#         if data and action_result(api.add_student(data)):
#             self.clear()
#             self.refresh()

#     def update(self):
#         if not self.selected_id:
#             messagebox.showwarning("Select", "Select a student first")
#             return

#         data = self.collect()
#         if data:
#             data["student_id"] = self.selected_id

#             if action_result(api.update_student(data)):
#                 self.clear()
#                 self.refresh()

#     def delete(self):
#         if not self.selected_id:
#             messagebox.showwarning("Select", "Select a student first")
#             return

#         if messagebox.askyesno("Confirm", "Delete this student?"):
#             if action_result(api.delete_student(self.selected_id)):
#                 self.clear()
#                 self.refresh()


# # -------------------- ROOM MANAGEMENT WINDOW --------------------

# class RoomWindow:

#     def __init__(self, parent):
#         self.window = tk.Toplevel(parent)
#         setup_window(self.window, "Room Management and Allocation", "1050x720")
#         self.selected_room = None

#         self.create_ui()
#         self.refresh()

#     def create_ui(self):

#         tk.Label(
#             self.window, text="ROOM MANAGEMENT",
#             bg=DARK, fg=WHITE,
#             font=("Arial", 20, "bold"), pady=12
#         ).pack(fill="x")

#         form = tk.LabelFrame(
#             self.window, text="Room Details",
#             bg=WHITE, padx=15, pady=10
#         )
#         form.pack(fill="x", padx=12, pady=10)

#         self.room_number = tk.Entry(form, width=22)
#         self.room_type = ttk.Combobox(
#             form, values=["Single", "Double", "Triple"],
#             state="readonly", width=19
#         )
#         self.room_type.set("Single")

#         self.capacity = tk.Spinbox(form, from_=1, to=10, width=19)
#         self.monthly_fee = tk.Entry(form, width=22)

#         for i, (label, widget) in enumerate([
#             ("Room Number", self.room_number),
#             ("Room Type", self.room_type),
#             ("Capacity", self.capacity),
#             ("Monthly Fee", self.monthly_fee)
#         ]):
#             tk.Label(form, text=label, bg=WHITE).grid(
#                 row=0, column=i, padx=8
#             )
#             widget.grid(row=1, column=i, padx=8, pady=5)

#         buttons = tk.Frame(form, bg=WHITE)
#         buttons.grid(row=2, column=0, columnspan=4, pady=8)

#         for title, command in [
#             ("ADD ROOM", self.add),
#             ("UPDATE", self.update),
#             ("DELETE", self.delete),
#             ("CLEAR", self.clear)
#         ]:
#             tk.Button(
#                 buttons, text=title,
#                 command=command, bg=PRIMARY,
#                 fg=WHITE, width=13
#             ).pack(side="left", padx=5)

#         tk.Label(
#             self.window, text="Room Records",
#             bg=BG, font=("Arial", 14, "bold")
#         ).pack(anchor="w", padx=15)

#         self.tree = make_tree(
#             self.window,
#             ("room_id", "room_number", "room_type",
#              "capacity", "occupied", "room_status", "monthly_fee"),
#             ("ID", "Room No", "Type", "Capacity",
#              "Occupied", "Status", "Monthly Fee"),
#             height=7
#         )

#         self.tree.bind("<<TreeviewSelect>>", self.select_room)

#         # Allocation section
#         allocation = tk.LabelFrame(
#             self.window, text="Allocate Room to Student",
#             bg=WHITE, padx=12, pady=8
#         )
#         allocation.pack(fill="x", padx=12, pady=10)

#         tk.Label(allocation, text="Student ID:", bg=WHITE).pack(side="left")
#         self.alloc_student = tk.Entry(allocation, width=12)
#         self.alloc_student.pack(side="left", padx=6)

#         tk.Label(allocation, text="Room ID:", bg=WHITE).pack(side="left")
#         self.alloc_room = tk.Entry(allocation, width=12)
#         self.alloc_room.pack(side="left", padx=6)

#         tk.Label(allocation, text="Date (YYYY-MM-DD):", bg=WHITE).pack(side="left")
#         self.alloc_date = tk.Entry(allocation, width=14)
#         self.alloc_date.insert(0, date.today().isoformat())
#         self.alloc_date.pack(side="left", padx=6)

#         tk.Button(
#             allocation, text="ALLOCATE ROOM",
#             command=self.allocate,
#             bg="#059669", fg=WHITE
#         ).pack(side="left", padx=8)

#         tk.Button(
#             allocation, text="VIEW ALLOCATIONS",
#             command=self.refresh_allocations
#         ).pack(side="left", padx=5)

#         self.alloc_tree = make_tree(
#             self.window,
#             ("allocation_id", "student_name", "roll_number",
#              "room_number", "room_type", "allocation_date", "allocation_status"),
#             ("ID", "Student", "Roll No", "Room", "Type", "Date", "Status"),
#             height=5
#         )

#     def refresh(self):
#         result = api.get_rooms()

#         if result.get("success"):
#             fill_tree(
#                 self.tree, result.get("data", []),
#                 ["room_id", "room_number", "room_type",
#                  "capacity", "occupied", "room_status", "monthly_fee"]
#             )
#         else:
#             messagebox.showerror("Error", result.get("message"))

#         self.refresh_allocations()

#     def refresh_allocations(self):
#         result = api.get_allocations()

#         if result.get("success"):
#             fill_tree(
#                 self.alloc_tree, result.get("data", []),
#                 ["allocation_id", "student_name", "roll_number",
#                  "room_number", "room_type", "allocation_date",
#                  "allocation_status"]
#             )

#     def select_room(self, event):
#         selected = self.tree.selection()
#         if not selected:
#             return

#         v = self.tree.item(selected[0], "values")
#         self.selected_room = v[0]

#         self.room_number.delete(0, "end")
#         self.room_number.insert(0, v[1])

#         self.room_type.set(v[2])

#         self.capacity.delete(0, "end")
#         self.capacity.insert(0, v[3])

#         self.monthly_fee.delete(0, "end")
#         self.monthly_fee.insert(0, v[6])

#     def clear(self):
#         self.selected_room = None

#         self.room_number.delete(0, "end")
#         self.room_type.set("Single")

#         self.capacity.delete(0, "end")
#         self.capacity.insert(0, "1")

#         self.monthly_fee.delete(0, "end")

#     def room_data(self):
#         try:
#             data = {
#                 "room_number": self.room_number.get().strip(),
#                 "room_type": self.room_type.get(),
#                 "capacity": int(self.capacity.get()),
#                 "monthly_fee": self.monthly_fee.get().strip()
#             }

#             if not data["room_number"] or float(data["monthly_fee"]) <= 0:
#                 raise ValueError("Enter valid room details")

#             return data

#         except ValueError:
#             messagebox.showwarning("Validation", "Enter valid capacity and fee")
#             return None

#     def add(self):
#         data = self.room_data()
#         if data and action_result(api.add_room(data)):
#             self.clear()
#             self.refresh()

#     def update(self):
#         if not self.selected_room:
#             messagebox.showwarning("Select", "Select a room first")
#             return

#         data = self.room_data()
#         if data:
#             data["room_id"] = self.selected_room

#             if action_result(api.update_room(data)):
#                 self.clear()
#                 self.refresh()

#     def delete(self):
#         if not self.selected_room:
#             messagebox.showwarning("Select", "Select a room first")
#             return

#         if messagebox.askyesno("Confirm", "Delete this room?"):
#             if action_result(api.delete_room(self.selected_room)):
#                 self.clear()
#                 self.refresh()

#     def allocate(self):
#         data = {
#             "student_id": self.alloc_student.get().strip(),
#             "room_id": self.alloc_room.get().strip(),
#             "allocation_date": self.alloc_date.get().strip()
#         }

#         try:
#             date.fromisoformat(data["allocation_date"])
#             if not data["student_id"] or not data["room_id"]:
#                 raise ValueError()
#         except ValueError:
#             messagebox.showwarning("Validation", "Enter valid student ID, room ID and date")
#             return

#         if action_result(api.allocate_room(data)):
#             self.refresh()


# # -------------------- FEE MANAGEMENT WINDOW --------------------

# class FeeWindow:

#     def __init__(self, parent):
#         self.window = tk.Toplevel(parent)
#         setup_window(self.window, "Fee Management", "1000x650")
#         self.selected_fee = None

#         self.create_ui()
#         self.refresh()

#     def create_ui(self):

#         tk.Label(
#             self.window, text="HOSTEL FEE MANAGEMENT",
#             font=("Arial", 20, "bold"),
#             bg=DARK, fg=WHITE, pady=15
#         ).pack(fill="x")

#         form = tk.LabelFrame(
#             self.window, text="Payment Details",
#             bg=WHITE, padx=20, pady=15
#         )
#         form.pack(fill="x", padx=15, pady=15)

#         tk.Label(form, text="Student ID", bg=WHITE).grid(row=0, column=0)
#         self.student_id = tk.Entry(form, width=20)
#         self.student_id.grid(row=1, column=0, padx=10, pady=8)

#         tk.Label(form, text="Fee Amount", bg=WHITE).grid(row=0, column=1)
#         self.amount = tk.Entry(form, width=20)
#         self.amount.grid(row=1, column=1, padx=10, pady=8)

#         tk.Label(form, text="Payment Date", bg=WHITE).grid(row=0, column=2)
#         self.payment_date = tk.Entry(form, width=20)
#         self.payment_date.grid(row=1, column=2, padx=10, pady=8)
#         self.payment_date.insert(0, date.today().isoformat())

#         tk.Label(form, text="Payment Status", bg=WHITE).grid(row=2, column=0)
#         self.status = ttk.Combobox(
#             form, values=["Paid", "Pending"],
#             state="readonly", width=17
#         )
#         self.status.grid(row=3, column=0, padx=10, pady=8)
#         self.status.set("Pending")

#         tk.Label(form, text="Payment Method", bg=WHITE).grid(row=2, column=1)
#         self.method = ttk.Combobox(
#             form, values=["Cash", "UPI", "Card", "Bank Transfer"],
#             state="readonly", width=17
#         )
#         self.method.grid(row=3, column=1, padx=10, pady=8)
#         self.method.set("Cash")

#         buttons = tk.Frame(form, bg=WHITE)
#         buttons.grid(row=4, column=0, columnspan=3, pady=10)

#         for title, command in [
#             ("ADD PAYMENT", self.add),
#             ("UPDATE", self.update),
#             ("DELETE", self.delete),
#             ("CLEAR", self.clear)
#         ]:
#             tk.Button(
#                 buttons, text=title,
#                 command=command, bg=PRIMARY,
#                 fg=WHITE, width=14
#             ).pack(side="left", padx=6)

#         self.tree = make_tree(
#             self.window,
#             ("fee_id", "student_id", "student_name",
#              "roll_number", "amount", "payment_date",
#              "payment_status", "payment_method"),
#             ("Fee ID", "Student ID", "Student Name",
#              "Roll No", "Amount", "Date", "Status", "Method")
#         )

#         self.tree.bind("<<TreeviewSelect>>", self.select_fee)

#     def refresh(self):
#         result = api.get_fees()

#         if result.get("success"):
#             fill_tree(
#                 self.tree, result.get("data", []),
#                 ["fee_id", "student_id", "student_name",
#                  "roll_number", "amount", "payment_date",
#                  "payment_status", "payment_method"]
#             )
#         else:
#             messagebox.showerror("Error", result.get("message"))

#     def select_fee(self, event):
#         selected = self.tree.selection()
#         if not selected:
#             return

#         v = self.tree.item(selected[0], "values")
#         self.selected_fee = v[0]

#         self.student_id.delete(0, "end")
#         self.student_id.insert(0, v[1])

#         self.amount.delete(0, "end")
#         self.amount.insert(0, v[4])

#         self.payment_date.delete(0, "end")
#         self.payment_date.insert(0, v[5] if v[5] != "None" else "")

#         self.status.set(v[6])
#         self.method.set(v[7])

#     def clear(self):
#         self.selected_fee = None

#         for entry in [self.student_id, self.amount, self.payment_date]:
#             entry.delete(0, "end")

#         self.payment_date.insert(0, date.today().isoformat())
#         self.status.set("Pending")
#         self.method.set("Cash")

#     def fee_data(self):
#         data = {
#             "student_id": self.student_id.get().strip(),
#             "amount": self.amount.get().strip(),
#             "payment_date": self.payment_date.get().strip(),
#             "payment_status": self.status.get(),
#             "payment_method": self.method.get()
#         }

#         try:
#             if not data["student_id"] or float(data["amount"]) <= 0:
#                 raise ValueError()

#             if data["payment_date"]:
#                 date.fromisoformat(data["payment_date"])

#             return data

#         except ValueError:
#             messagebox.showwarning(
#                 "Validation", "Enter valid student ID, positive amount and date"
#             )
#             return None

#     def add(self):
#         data = self.fee_data()
#         if data and action_result(api.add_fee(data)):
#             self.clear()
#             self.refresh()

#     def update(self):
#         if not self.selected_fee:
#             messagebox.showwarning("Select", "Select a fee record first")
#             return

#         data = self.fee_data()
#         if data:
#             data["fee_id"] = self.selected_fee

#             if action_result(api.update_fee(data)):
#                 self.clear()
#                 self.refresh()

#     def delete(self):
#         if not self.selected_fee:
#             messagebox.showwarning("Select", "Select a fee record first")
#             return

#         if messagebox.askyesno("Confirm", "Delete this fee record?"):
#             if action_result(api.delete_fee(self.selected_fee)):
#                 self.clear()
#                 self.refresh()


# # -------------------- REPORTS WINDOW --------------------

# class ReportWindow:

#     def __init__(self, parent):
#         self.window = tk.Toplevel(parent)
#         setup_window(self.window, "Hostel Reports", "850x600")

#         tk.Label(
#             self.window, text="HOSTEL REPORTS",
#             bg=DARK, fg=WHITE,
#             font=("Arial", 20, "bold"), pady=15
#         ).pack(fill="x")

#         controls = tk.Frame(self.window, bg=BG)
#         controls.pack(fill="x", padx=15, pady=12)

#         tk.Label(controls, text="Select Report:", bg=BG).pack(side="left")

#         self.report_type = ttk.Combobox(
#             controls,
#             values=[
#                 "All Students",
#                 "Room Occupancy",
#                 "Pending Fees"
#             ],
#             state="readonly", width=25
#         )
#         self.report_type.pack(side="left", padx=10)
#         self.report_type.set("All Students")

#         tk.Button(
#             controls, text="GENERATE REPORT",
#             bg=PRIMARY, fg=WHITE,
#             command=self.generate
#         ).pack(side="left")

#         self.output = tk.Text(
#             self.window, font=("Consolas", 11),
#             height=22, width=95
#         )
#         self.output.pack(fill="both", expand=True, padx=15, pady=10)

#         self.generate()

#     def generate(self):
#         self.output.delete("1.0", "end")
#         choice = self.report_type.get()

#         if choice == "All Students":
#             result = api.get_students()
#             keys = ["student_id", "student_name", "roll_number", "department"]

#         elif choice == "Room Occupancy":
#             result = api.get_rooms()
#             keys = ["room_id", "room_number", "room_type",
#                     "capacity", "occupied", "room_status"]

#         else:
#             result = api.get_fees()
#             keys = ["fee_id", "student_name", "amount",
#                     "payment_status", "payment_date"]

#         if not result.get("success"):
#             self.output.insert("end", result.get("message", "Report failed"))
#             return

#         records = result.get("data", [])

#         self.output.insert("end", f"{choice.upper()}\n")
#         self.output.insert("end", "=" * 75 + "\n\n")

#         if choice == "Pending Fees":
#             records = [
#                 r for r in records
#                 if r.get("payment_status") == "Pending"
#             ]

#         if not records:
#             self.output.insert("end", "No records found.\n")
#             return

#         for record in records:
#             line = " | ".join(
#                 f"{key}: {record.get(key, '')}"
#                 for key in keys
#             )
#             self.output.insert("end", line + "\n")


# # -------------------- START APPLICATION --------------------

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = HostelApp(root)
#     root.mainloop()










































import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import api


# -------------------- THEME --------------------

BG = "#F1F5F9"
PRIMARY = "#1D4ED8"
DARK = "#172554"
WHITE = "#FFFFFF"
TEXT = "#1E293B"


def setup_window(window, title, size):
    window.title(title)
    window.geometry(size)
    window.configure(bg=BG)


def make_tree(parent, columns, headings, height=9):
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=12, pady=8)

    tree = ttk.Treeview(
        frame, columns=columns, show="headings", height=height
    )

    for col, heading in zip(columns, headings):
        tree.heading(col, text=heading)
        tree.column(col, width=120, anchor="center")

    vs = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hs = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vs.grid(row=0, column=1, sticky="ns")
    hs.grid(row=1, column=0, sticky="ew")

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    return tree


def fill_tree(tree, records, keys):
    tree.delete(*tree.get_children())

    for record in records:
        tree.insert(
            "", "end",
            values=[record.get(k, "") for k in keys]
        )


def action_result(result):
    if result.get("success"):
        messagebox.showinfo("Success", result.get("message", "Operation completed"))
        return True

    messagebox.showerror("Error", result.get("message", "Operation failed"))
    return False


# -------------------- LOGIN WINDOW --------------------

class HostelApp:

    def __init__(self, root):
        self.root = root
        setup_window(root, "Hostel Management System - Admin Login", "430x430")
        self.root.resizable(False, False)

        self.create_login()

    def create_login(self):

        header = tk.Frame(self.root, bg=DARK, height=105)
        header.pack(fill="x")

        tk.Label(
            header, text="HOSTEL MANAGEMENT",
            font=("Arial", 21, "bold"),
            fg=WHITE, bg=DARK
        ).pack(pady=(22, 4))

        tk.Label(
            header, text="ADMINISTRATOR LOGIN",
            font=("Arial", 10),
            fg="#BFDBFE", bg=DARK
        ).pack()

        form = tk.LabelFrame(
            self.root, text="Login Credentials",
            font=("Arial", 11, "bold"),
            bg=WHITE, padx=25, pady=20
        )
        form.pack(fill="both", padx=30, pady=25)

        tk.Label(form, text="Username", bg=WHITE).pack(anchor="w")
        self.username = tk.Entry(form, font=("Arial", 12))
        self.username.pack(fill="x", pady=(5, 15))

        tk.Label(form, text="Password", bg=WHITE).pack(anchor="w")
        self.password = tk.Entry(form, show="*", font=("Arial", 12))
        self.password.pack(fill="x", pady=5)

        self.show_password = tk.BooleanVar(value=False)

        tk.Checkbutton(
            form, text="Show Password",
            variable=self.show_password,
            command=self.toggle_password,
            bg=WHITE
        ).pack(anchor="w", pady=5)

        buttons = tk.Frame(form, bg=WHITE)
        buttons.pack(fill="x", pady=12)

        tk.Button(
            buttons, text="LOGIN",
            bg=PRIMARY, fg=WHITE,
            width=12, command=self.do_login
        ).pack(side="left", padx=5)

        tk.Button(
            buttons, text="RESET",
            width=10, command=self.reset
        ).pack(side="left", padx=5)

        tk.Button(
            buttons, text="EXIT",
            width=8, command=self.root.destroy
        ).pack(side="left", padx=5)

        tk.Label(
            self.root, text="Default: admin / admin123",
            bg=BG, fg="#64748B"
        ).pack()

        self.password.bind("<Return>", lambda e: self.do_login())

    def toggle_password(self):
        self.password.config(
            show="" if self.show_password.get() else "*"
        )

    def reset(self):
        self.username.delete(0, "end")
        self.password.delete(0, "end")

    def do_login(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showwarning("Validation", "Enter username and password")
            return

        result = api.login(username, password)

        if result.get("success"):
            messagebox.showinfo("Welcome", "Admin login successful!")
            self.root.withdraw()
            Dashboard(self.root)
        else:
            messagebox.showerror(
                "Login Failed", result.get("message", "Invalid credentials")
            )


# -------------------- DASHBOARD WINDOW --------------------

class Dashboard:

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.parent = parent

        setup_window(self.window, "Hostel Management - Dashboard", "1050x680")
        self.window.protocol("WM_DELETE_WINDOW", self.logout)

        self.create_menu()
        self.create_dashboard()
        self.refresh_stats()

    def create_menu(self):
        menubar = tk.Menu(self.window)

        management = tk.Menu(menubar, tearoff=0)
        management.add_command(label="Students", command=self.open_students)
        management.add_command(label="Rooms", command=self.open_rooms)
        management.add_command(label="Fees", command=self.open_fees)

        reports = tk.Menu(menubar, tearoff=0)
        reports.add_command(label="View Reports", command=self.open_reports)

        account = tk.Menu(menubar, tearoff=0)
        account.add_command(label="Logout", command=self.logout)

        menubar.add_cascade(label="Management", menu=management)
        menubar.add_cascade(label="Reports", menu=reports)
        menubar.add_cascade(label="Account", menu=account)

        self.window.config(menu=menubar)

    def create_dashboard(self):

        header = tk.Canvas(
            self.window, height=115,
            bg=DARK, highlightthickness=0
        )
        header.pack(fill="x")

        header.create_text(
            35, 38, anchor="w",
            text="HOSTEL MANAGEMENT SYSTEM",
            fill=WHITE, font=("Arial", 22, "bold")
        )

        header.create_text(
            35, 78, anchor="w",
            text="Administrator Dashboard",
            fill="#BFDBFE", font=("Arial", 12)
        )

        tk.Label(
            self.window, text="Dashboard Overview",
            font=("Arial", 18, "bold"),
            bg=BG, fg=TEXT
        ).pack(anchor="w", padx=25, pady=18)

        self.stats_frame = tk.Frame(self.window, bg=BG)
        self.stats_frame.pack(fill="x", padx=20)

        self.stat_labels = {}

        cards = [
            ("Students", "total_students", "#2563EB"),
            ("Total Rooms", "total_rooms", "#0891B2"),
            ("Occupied Rooms", "occupied_rooms", "#D97706"),
            ("Available Rooms", "available_rooms", "#059669"),
            ("Pending Fees", "pending_fees", "#DC2626")
        ]

        for title, key, color in cards:
            card = tk.Frame(
                self.stats_frame, bg=WHITE,
                padx=15, pady=20,
                highlightbackground="#CBD5E1",
                highlightthickness=1
            )
            card.pack(
                side="left", expand=True, fill="both",
                padx=5, pady=5
            )

            tk.Label(
                card, text=title, bg=WHITE,
                fg="#64748B", font=("Arial", 10)
            ).pack()

            value = tk.Label(
                card, text="0", bg=WHITE,
                fg=color, font=("Arial", 25, "bold")
            )
            value.pack(pady=8)

            self.stat_labels[key] = value

        tk.Label(
            self.window, text="Quick Actions",
            font=("Arial", 17, "bold"),
            bg=BG, fg=TEXT
        ).pack(anchor="w", padx=25, pady=(25, 10))

        actions = tk.Frame(self.window, bg=BG)
        actions.pack(fill="x", padx=20)

        buttons = [
            ("Student Management", self.open_students),
            ("Room Management", self.open_rooms),
            ("Fee Management", self.open_fees),
            ("Reports", self.open_reports)
        ]

        for title, command in buttons:
            tk.Button(
                actions, text=title,
                command=command,
                bg=PRIMARY, fg=WHITE,
                font=("Arial", 11, "bold"),
                width=20, height=2
            ).pack(side="left", padx=7, pady=10)

        tk.Button(
            self.window, text="REFRESH STATISTICS",
            command=self.refresh_stats,
            bg="#334155", fg=WHITE
        ).pack(pady=20)

        # Listbox for quick navigation
        quick = tk.LabelFrame(
            self.window, text="Navigation Shortcuts",
            bg=WHITE, padx=10, pady=5
        )
        quick.pack(fill="x", padx=25, pady=5)

        self.shortcut = tk.Listbox(
            quick, height=2, font=("Arial", 10)
        )
        self.shortcut.insert("end", "Student Records")
        self.shortcut.insert("end", "Room Records")
        self.shortcut.pack(fill="x")

        self.shortcut.bind(
            "<<ListboxSelect>>", self.shortcut_action
        )

    def shortcut_action(self, event):
        selection = self.shortcut.curselection()
        if not selection:
            return

        if selection[0] == 0:
            self.open_students()
        else:
            self.open_rooms()

    def refresh_stats(self):
        result = api.get_stats()

        if not result.get("success"):
            messagebox.showerror("Error", result.get("message"))
            return

        records = result.get("data", [])

        if records:
            for key, value in records[0].items():
                if key in self.stat_labels:
                    self.stat_labels[key].config(text=str(value))

    def open_students(self):
        StudentWindow(self.window)

    def open_rooms(self):
        RoomWindow(self.window)

    def open_fees(self):
        FeeWindow(self.window)

    def open_reports(self):
        ReportWindow(self.window)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.window.destroy()
            self.parent.deiconify()


# -------------------- STUDENT MANAGEMENT WINDOW --------------------

class StudentWindow:

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        setup_window(self.window, "Student Management", "1150x780")

        self.selected_id = None
        self.create_ui()
        self.refresh()

    def create_ui(self):

        tk.Label(
            self.window, text="STUDENT MANAGEMENT",
            font=("Arial", 20, "bold"),
            bg=DARK, fg=WHITE, pady=15
        ).pack(fill="x")

        form = tk.LabelFrame(
            self.window, text="Student Information",
            bg=WHITE, padx=12, pady=8
        )
        form.pack(fill="x", padx=12, pady=8)

        self.fields = {}

        labels = [
            ("Student Name", "student_name"),
            ("Roll Number", "roll_number"),
            ("Phone Number", "phone_number"),
            ("Email", "email"),
            ("Guardian Contact", "guardian_contact")
        ]

        for i, (label, key) in enumerate(labels):
            row, col = divmod(i, 3)

            tk.Label(form, text=label, bg=WHITE).grid(
                row=row*2, column=col, sticky="w", padx=8, pady=3
            )

            entry = tk.Entry(form, width=27)
            entry.grid(
                row=row*2+1, column=col,
                padx=8, pady=4, sticky="ew"
            )
            self.fields[key] = entry

        tk.Label(form, text="Department", bg=WHITE).grid(
            row=4, column=0, sticky="w", padx=8
        )

        self.department = ttk.Combobox(
            form, values=[
                "CSE", "IT", "ECE", "EEE", "Mechanical",
                "Civil", "Biotechnology", "Other"
            ], state="readonly", width=24
        )
        self.department.grid(row=5, column=0, padx=8, pady=4)
        self.department.set("CSE")

        tk.Label(form, text="Gender", bg=WHITE).grid(
            row=4, column=1, sticky="w", padx=8
        )

        self.gender = ttk.Combobox(
            form, values=["Male", "Female", "Other"],
            state="readonly", width=24
        )
        self.gender.grid(row=5, column=1, padx=8, pady=4)
        self.gender.set("Male")

        tk.Label(form, text="Student Type", bg=WHITE).grid(
            row=4, column=2, sticky="w", padx=8
        )

        self.student_type = tk.StringVar(value="Regular")

        type_frame = tk.Frame(form, bg=WHITE)
        type_frame.grid(row=5, column=2, sticky="w")

        for value in ["Regular", "Scholarship"]:
            tk.Radiobutton(
                type_frame, text=value,
                variable=self.student_type,
                value=value, bg=WHITE
            ).pack(side="left")

        tk.Label(form, text="Facilities", bg=WHITE).grid(
            row=6, column=0, sticky="w", padx=8
        )

        facility_frame = tk.Frame(form, bg=WHITE)
        facility_frame.grid(row=7, column=0, columnspan=3, sticky="w")

        self.facilities = {}

        for name in ["WiFi", "Laundry", "Mess", "AC"]:
            var = tk.BooleanVar()
            self.facilities[name] = var

            tk.Checkbutton(
                facility_frame, text=name,
                variable=var, bg=WHITE
            ).pack(side="left", padx=8)

        tk.Label(form, text="Address", bg=WHITE).grid(
            row=8, column=0, sticky="w", padx=8
        )

        self.address = tk.Text(form, height=2, width=70)
        self.address.grid(
            row=9, column=0, columnspan=3,
            padx=8, pady=5, sticky="ew"
        )

        buttons = tk.Frame(form, bg=WHITE)
        buttons.grid(row=10, column=0, columnspan=3, pady=8)

        for title, command, color in [
            ("ADD", self.add, "#059669"),
            ("UPDATE", self.update, "#2563EB"),
            ("DELETE", self.delete, "#DC2626"),
            ("CLEAR", self.clear, "#64748B")
        ]:
            tk.Button(
                buttons, text=title, command=command,
                bg=color, fg=WHITE, width=12
            ).pack(side="left", padx=5)

        search_frame = tk.Frame(self.window, bg=BG)
        search_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(
            search_frame, text="Search Student:",
            bg=BG, font=("Arial", 11, "bold")
        ).pack(side="left")

        self.search = tk.Entry(search_frame, width=35)
        self.search.pack(side="left", padx=8)

        tk.Button(
            search_frame, text="SEARCH",
            command=self.refresh, bg=PRIMARY, fg=WHITE
        ).pack(side="left")

        tk.Button(
            search_frame, text="SHOW ALL",
            command=self.show_all
        ).pack(side="left", padx=5)

        columns = (
            "student_id", "student_name", "roll_number",
            "phone_number", "email", "department",
            "gender", "student_type"
        )

        self.tree = make_tree(
            self.window, columns,
            ("ID", "Name", "Roll No", "Phone", "Email",
             "Department", "Gender", "Type")
        )

        self.tree.bind("<<TreeviewSelect>>", self.select_record)

    def get_data(self):
        return {
            key: entry.get().strip()
            for key, entry in self.fields.items()
        }

    def refresh(self):
        search = self.search.get().strip()

        result = api.get_students(search)

        if result.get("success"):
            fill_tree(
                self.tree, result.get("data", []),
                ["student_id", "student_name", "roll_number",
                 "phone_number", "email", "department",
                 "gender", "student_type"]
            )
        else:
            messagebox.showerror("Error", result.get("message"))

    def show_all(self):
        self.search.delete(0, "end")
        self.refresh()

    def clear(self):
        self.selected_id = None

        for entry in self.fields.values():
            entry.delete(0, "end")

        self.department.set("CSE")
        self.gender.set("Male")
        self.student_type.set("Regular")
        self.address.delete("1.0", "end")

        for var in self.facilities.values():
            var.set(False)

    def select_record(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.selected_id = values[0]

        for key, value in zip(
            ["student_name", "roll_number", "phone_number",
             "email"], values[1:5]
        ):
            self.fields[key].delete(0, "end")
            self.fields[key].insert(0, value)

        self.department.set(values[5])
        self.gender.set(values[6])
        self.student_type.set(values[7])

        # Fetch complete student details, including address
        result = api.get_students(values[2])

        if result.get("success") and result.get("data"):
            record = next(
                (r for r in result["data"]
                 if str(r["student_id"]) == str(self.selected_id)),
                None
            )

            if record:
                for key in ["guardian_contact"]:
                    self.fields[key].delete(0, "end")
                    self.fields[key].insert(0, record.get(key) or "")

                self.address.delete("1.0", "end")
                self.address.insert("1.0", record.get("address") or "")

                selected_facilities = (record.get("facilities") or "").split(",")
                for name, var in self.facilities.items():
                    var.set(name in selected_facilities)

    def collect(self):
        data = self.get_data()
        data.update({
            "department": self.department.get(),
            "gender": self.gender.get(),
            "student_type": self.student_type.get(),
            "address": self.address.get("1.0", "end").strip(),
            "facilities": ",".join(
                name for name, var in self.facilities.items()
                if var.get()
            )
        })

        if not data["student_name"] or not data["roll_number"]:
            messagebox.showwarning(
                "Validation", "Student name and roll number are required"
            )
            return None

        return data

    def add(self):
        data = self.collect()
        if data and action_result(api.add_student(data)):
            self.clear()
            self.refresh()

    def update(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Select a student first")
            return

        data = self.collect()
        if data:
            data["student_id"] = self.selected_id

            if action_result(api.update_student(data)):
                self.clear()
                self.refresh()

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Select a student first")
            return

        if messagebox.askyesno("Confirm", "Delete this student?"):
            if action_result(api.delete_student(self.selected_id)):
                self.clear()
                self.refresh()


# -------------------- ROOM MANAGEMENT WINDOW --------------------

class RoomWindow:

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        setup_window(self.window, "Room Management and Allocation", "1050x720")
        self.selected_room = None
        self.room_filter = tk.StringVar(value="All")

        self.create_ui()
        self.refresh()

    def create_ui(self):

        tk.Label(
            self.window, text="ROOM MANAGEMENT",
            bg=DARK, fg=WHITE,
            font=("Arial", 20, "bold"), pady=12
        ).pack(fill="x")

        form = tk.LabelFrame(
            self.window, text="Room Details",
            bg=WHITE, padx=15, pady=10
        )
        form.pack(fill="x", padx=12, pady=10)

        self.room_number = tk.Entry(form, width=22)
        self.room_type = ttk.Combobox(
            form, values=["Single", "Double", "Triple"],
            state="readonly", width=19
        )
        self.room_type.set("Single")

        self.capacity = tk.Spinbox(form, from_=1, to=10, width=19)
        self.monthly_fee = tk.Entry(form, width=22)

        for i, (label, widget) in enumerate([
            ("Room Number", self.room_number),
            ("Room Type", self.room_type),
            ("Capacity", self.capacity),
            ("Monthly Fee", self.monthly_fee)
        ]):
            tk.Label(form, text=label, bg=WHITE).grid(
                row=0, column=i, padx=8
            )
            widget.grid(row=1, column=i, padx=8, pady=5)

        buttons = tk.Frame(form, bg=WHITE)
        buttons.grid(row=2, column=0, columnspan=4, pady=8)

        for title, command in [
            ("ADD ROOM", self.add),
            ("UPDATE", self.update),
            ("DELETE", self.delete),
            ("CLEAR", self.clear)
        ]:
            tk.Button(
                buttons, text=title,
                command=command, bg=PRIMARY,
                fg=WHITE, width=13
            ).pack(side="left", padx=5)

        tk.Label(
            self.window, text="Room Records",
            bg=BG, font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=15)

        # Room availability filter
        filter_frame = tk.Frame(self.window, bg=BG)
        filter_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(
            filter_frame,
            text="Filter Rooms:",
            bg=BG,
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=5)

        for option in ["All", "Available", "Occupied"]:
            tk.Radiobutton(
                filter_frame,
                text=option,
                variable=self.room_filter,
                value=option,
                command=self.refresh,
                bg=BG,
                activebackground=BG
            ).pack(side="left", padx=10)

        self.tree = make_tree(
            self.window,
            ("room_id", "room_number", "room_type",
             "capacity", "occupied", "room_status", "monthly_fee"),
            ("ID", "Room No", "Type", "Capacity",
             "Occupied", "Status", "Monthly Fee"),
            height=7
        )

        self.tree.bind("<<TreeviewSelect>>", self.select_room)

        # Allocation section
        allocation = tk.LabelFrame(
            self.window, text="Allocate Room to Student",
            bg=WHITE, padx=12, pady=8
        )
        allocation.pack(fill="x", padx=12, pady=10)

        tk.Label(allocation, text="Student ID:", bg=WHITE).pack(side="left")
        self.alloc_student = tk.Entry(allocation, width=12)
        self.alloc_student.pack(side="left", padx=6)

        tk.Label(allocation, text="Room ID:", bg=WHITE).pack(side="left")
        self.alloc_room = tk.Entry(allocation, width=12)
        self.alloc_room.pack(side="left", padx=6)

        # Allocation date selector (Year / Month / Day)
        today = date.today()

        tk.Label(
            allocation,
            text="Allocation Date:",
            bg=WHITE
        ).pack(side="left", padx=3)

        self.alloc_year = tk.Spinbox(
            allocation, from_=2020, to=2100, width=6
        )
        self.alloc_year.pack(side="left", padx=2)
        self.alloc_year.delete(0, "end")
        self.alloc_year.insert(0, today.year)

        self.alloc_month = tk.Spinbox(
            allocation, from_=1, to=12, width=4
        )
        self.alloc_month.pack(side="left", padx=2)
        self.alloc_month.delete(0, "end")
        self.alloc_month.insert(0, today.month)

        self.alloc_day = tk.Spinbox(
            allocation, from_=1, to=31, width=4
        )
        self.alloc_day.pack(side="left", padx=2)
        self.alloc_day.delete(0, "end")
        self.alloc_day.insert(0, today.day)

        tk.Button(
            allocation, text="ALLOCATE ROOM",
            command=self.allocate,
            bg="#059669", fg=WHITE
        ).pack(side="left", padx=8)

        tk.Button(
            allocation, text="VIEW ALLOCATIONS",
            command=self.refresh_allocations
        ).pack(side="left", padx=5)

        self.alloc_tree = make_tree(
            self.window,
            ("allocation_id", "student_name", "roll_number",
             "room_number", "room_type", "allocation_date", "allocation_status"),
            ("ID", "Student", "Roll No", "Room", "Type", "Date", "Status"),
            height=5
        )

    def refresh(self):
        result = api.get_rooms()

        if result.get("success"):
            rooms = result.get("data", [])
            selected_filter = self.room_filter.get()

            if selected_filter == "Available":
                rooms = [
                    room for room in rooms
                    if int(room.get("occupied", 0)) < int(room.get("capacity", 0))
                ]
            elif selected_filter == "Occupied":
                rooms = [
                    room for room in rooms
                    if int(room.get("occupied", 0)) >= int(room.get("capacity", 0))
                ]

            fill_tree(
                self.tree, rooms,
                ["room_id", "room_number", "room_type",
                 "capacity", "occupied", "room_status", "monthly_fee"]
            )
        else:
            messagebox.showerror(
                "Error", result.get("message", "Unable to load rooms")
            )

        self.refresh_allocations()

    def refresh_allocations(self):
        result = api.get_allocations()

        if result.get("success"):
            fill_tree(
                self.alloc_tree, result.get("data", []),
                ["allocation_id", "student_name", "roll_number",
                 "room_number", "room_type", "allocation_date",
                 "allocation_status"]
            )

    def select_room(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        v = self.tree.item(selected[0], "values")
        self.selected_room = v[0]

        self.room_number.delete(0, "end")
        self.room_number.insert(0, v[1])

        self.room_type.set(v[2])

        self.capacity.delete(0, "end")
        self.capacity.insert(0, v[3])

        self.monthly_fee.delete(0, "end")
        self.monthly_fee.insert(0, v[6])

    def clear(self):
        self.selected_room = None

        self.room_number.delete(0, "end")
        self.room_type.set("Single")

        self.capacity.delete(0, "end")
        self.capacity.insert(0, "1")

        self.monthly_fee.delete(0, "end")

    def room_data(self):
        try:
            data = {
                "room_number": self.room_number.get().strip(),
                "room_type": self.room_type.get(),
                "capacity": int(self.capacity.get()),
                "monthly_fee": self.monthly_fee.get().strip()
            }

            if not data["room_number"] or float(data["monthly_fee"]) <= 0:
                raise ValueError("Enter valid room details")

            return data

        except ValueError:
            messagebox.showwarning("Validation", "Enter valid capacity and fee")
            return None

    def add(self):
        data = self.room_data()
        if data and action_result(api.add_room(data)):
            self.clear()
            self.refresh()

    def update(self):
        if not self.selected_room:
            messagebox.showwarning("Select", "Select a room first")
            return

        data = self.room_data()
        if data:
            data["room_id"] = self.selected_room

            if action_result(api.update_room(data)):
                self.clear()
                self.refresh()

    def delete(self):
        if not self.selected_room:
            messagebox.showwarning("Select", "Select a room first")
            return

        if messagebox.askyesno("Confirm", "Delete this room?"):
            if action_result(api.delete_room(self.selected_room)):
                self.clear()
                self.refresh()

    def allocate(self):
        try:
            student_id = self.alloc_student.get().strip()
            room_id = self.alloc_room.get().strip()

            if not student_id.isdigit() or not room_id.isdigit():
                raise ValueError("Student ID and Room ID must be numbers")

            year = int(self.alloc_year.get())
            month = int(self.alloc_month.get())
            day = int(self.alloc_day.get())
            allocation_date = date(year, month, day).isoformat()

            data = {
                "student_id": student_id,
                "room_id": room_id,
                "allocation_date": allocation_date
            }

        except (ValueError, TypeError):
            messagebox.showwarning(
                "Validation Error",
                "Enter valid Student ID, Room ID and allocation date."
            )
            return

        if action_result(api.allocate_room(data)):
            self.refresh()


# -------------------- FEE MANAGEMENT WINDOW --------------------

class FeeWindow:

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        setup_window(self.window, "Fee Management", "1000x650")
        self.selected_fee = None

        self.create_ui()
        self.refresh()

    def create_ui(self):

        tk.Label(
            self.window, text="HOSTEL FEE MANAGEMENT",
            font=("Arial", 20, "bold"),
            bg=DARK, fg=WHITE, pady=15
        ).pack(fill="x")

        form = tk.LabelFrame(
            self.window, text="Payment Details",
            bg=WHITE, padx=20, pady=15
        )
        form.pack(fill="x", padx=15, pady=15)

        tk.Label(form, text="Student ID", bg=WHITE).grid(row=0, column=0)
        self.student_id = tk.Entry(form, width=20)
        self.student_id.grid(row=1, column=0, padx=10, pady=8)

        tk.Label(form, text="Fee Amount", bg=WHITE).grid(row=0, column=1)
        self.amount = tk.Entry(form, width=20)
        self.amount.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(form, text="Payment Date", bg=WHITE).grid(row=0, column=2)
        self.payment_date = tk.Entry(form, width=20)
        self.payment_date.grid(row=1, column=2, padx=10, pady=8)
        self.payment_date.insert(0, date.today().isoformat())

        tk.Label(form, text="Payment Status", bg=WHITE).grid(row=2, column=0)
        self.status = ttk.Combobox(
            form, values=["Paid", "Pending"],
            state="readonly", width=17
        )
        self.status.grid(row=3, column=0, padx=10, pady=8)
        self.status.set("Pending")

        tk.Label(form, text="Payment Method", bg=WHITE).grid(row=2, column=1)
        self.method = ttk.Combobox(
            form, values=["Cash", "UPI", "Card", "Bank Transfer"],
            state="readonly", width=17
        )
        self.method.grid(row=3, column=1, padx=10, pady=8)
        self.method.set("Cash")

        buttons = tk.Frame(form, bg=WHITE)
        buttons.grid(row=4, column=0, columnspan=3, pady=10)

        for title, command in [
            ("ADD PAYMENT", self.add),
            ("UPDATE", self.update),
            ("DELETE", self.delete),
            ("CLEAR", self.clear)
        ]:
            tk.Button(
                buttons, text=title,
                command=command, bg=PRIMARY,
                fg=WHITE, width=14
            ).pack(side="left", padx=6)

        self.tree = make_tree(
            self.window,
            ("fee_id", "student_id", "student_name",
             "roll_number", "amount", "payment_date",
             "payment_status", "payment_method"),
            ("Fee ID", "Student ID", "Student Name",
             "Roll No", "Amount", "Date", "Status", "Method")
        )

        self.tree.bind("<<TreeviewSelect>>", self.select_fee)

    def refresh(self):
        result = api.get_fees()

        if result.get("success"):
            fill_tree(
                self.tree, result.get("data", []),
                ["fee_id", "student_id", "student_name",
                 "roll_number", "amount", "payment_date",
                 "payment_status", "payment_method"]
            )
        else:
            messagebox.showerror("Error", result.get("message"))

    def select_fee(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        v = self.tree.item(selected[0], "values")
        self.selected_fee = v[0]

        self.student_id.delete(0, "end")
        self.student_id.insert(0, v[1])

        self.amount.delete(0, "end")
        self.amount.insert(0, v[4])

        self.payment_date.delete(0, "end")
        self.payment_date.insert(0, v[5] if v[5] != "None" else "")

        self.status.set(v[6])
        self.method.set(v[7])

    def clear(self):
        self.selected_fee = None

        for entry in [self.student_id, self.amount, self.payment_date]:
            entry.delete(0, "end")

        self.payment_date.insert(0, date.today().isoformat())
        self.status.set("Pending")
        self.method.set("Cash")

    def fee_data(self):
        data = {
            "student_id": self.student_id.get().strip(),
            "amount": self.amount.get().strip(),
            "payment_date": self.payment_date.get().strip(),
            "payment_status": self.status.get(),
            "payment_method": self.method.get()
        }

        try:
            if not data["student_id"] or float(data["amount"]) <= 0:
                raise ValueError()

            if data["payment_date"]:
                date.fromisoformat(data["payment_date"])

            return data

        except ValueError:
            messagebox.showwarning(
                "Validation", "Enter valid student ID, positive amount and date"
            )
            return None

    def add(self):
        data = self.fee_data()
        if data and action_result(api.add_fee(data)):
            self.clear()
            self.refresh()

    def update(self):
        if not self.selected_fee:
            messagebox.showwarning("Select", "Select a fee record first")
            return

        data = self.fee_data()
        if data:
            data["fee_id"] = self.selected_fee

            if action_result(api.update_fee(data)):
                self.clear()
                self.refresh()

    def delete(self):
        if not self.selected_fee:
            messagebox.showwarning("Select", "Select a fee record first")
            return

        if messagebox.askyesno("Confirm", "Delete this fee record?"):
            if action_result(api.delete_fee(self.selected_fee)):
                self.clear()
                self.refresh()


# -------------------- REPORTS WINDOW --------------------

class ReportWindow:

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        setup_window(self.window, "Hostel Reports", "850x600")

        tk.Label(
            self.window, text="HOSTEL REPORTS",
            bg=DARK, fg=WHITE,
            font=("Arial", 20, "bold"), pady=15
        ).pack(fill="x")

        controls = tk.Frame(self.window, bg=BG)
        controls.pack(fill="x", padx=15, pady=12)

        tk.Label(controls, text="Select Report:", bg=BG).pack(side="left")

        self.report_type = ttk.Combobox(
            controls,
            values=[
                "All Students",
                "Room Occupancy",
                "Pending Fees"
            ],
            state="readonly", width=25
        )
        self.report_type.pack(side="left", padx=10)
        self.report_type.set("All Students")

        tk.Button(
            controls, text="GENERATE REPORT",
            bg=PRIMARY, fg=WHITE,
            command=self.generate
        ).pack(side="left")

        self.output = tk.Text(
            self.window, font=("Consolas", 11),
            height=22, width=95
        )
        self.output.pack(fill="both", expand=True, padx=15, pady=10)

        self.generate()

    def generate(self):
        self.output.delete("1.0", "end")
        choice = self.report_type.get()

        if choice == "All Students":
            result = api.get_students()
            keys = ["student_id", "student_name", "roll_number", "department"]

        elif choice == "Room Occupancy":
            result = api.get_rooms()
            keys = ["room_id", "room_number", "room_type",
                    "capacity", "occupied", "room_status"]

        else:
            result = api.get_fees()
            keys = ["fee_id", "student_name", "amount",
                    "payment_status", "payment_date"]

        if not result.get("success"):
            self.output.insert("end", result.get("message", "Report failed"))
            return

        records = result.get("data", [])

        self.output.insert("end", f"{choice.upper()}\n")
        self.output.insert("end", "=" * 75 + "\n\n")

        if choice == "Pending Fees":
            records = [
                r for r in records
                if r.get("payment_status") == "Pending"
            ]

        if not records:
            self.output.insert("end", "No records found.\n")
            return

        for record in records:
            line = " | ".join(
                f"{key}: {record.get(key, '')}"
                for key in keys
            )
            self.output.insert("end", line + "\n")


# -------------------- START APPLICATION --------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = HostelApp(root)
    root.mainloop()
