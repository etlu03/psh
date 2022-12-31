import re
import tkinter as tk
from datetime import date, datetime

class Directory:
  def __init__(self, dir_name):
    self.dir_name = dir_name
    self.children = []
  
  def __repr__(self):
    return self.dir_name

  def add_child(self, obj):
    self.child.append(obj)

class File:
  def __init__(self, file_name):
    self.file_name = file_name
    self.content = str()
  
  def __repr__(self):
    return self.file_name
  
  def cat(self, text):
    self.content += text

def cache_login():
  weekdays = {0: 'Mon',
              1: 'Tue',
              2: 'Wed',
              3: 'Thu',
              4: 'Fri',
              5: 'Sat',
              6: 'Sun'}

  now = datetime.now()
  weekday = now.weekday()
  time = now.strftime("%H:%M:%S")

  today = date.today()
  month, day, year = today.strftime("%b-%d-%Y").split('-')

  login = ' '.join([weekdays[weekday], month, day, time])
  
  with open("_cache/last_login", "w", encoding="utf-8") as f:
    f.write(login)

if __name__ == '__main__':
  with open("_cache/last_login", "r", encoding="utf-8") as f:
    last_login = f.read()
  cache_login()

  def execute(entry):
    clear_response()
    command = entry.widget.get()
    if re.search(r"\bls\b", command):
      ls_command()
    elif re.search(r"\becho\b", command):
      echo_command(command)
    elif re.search(r"\btouch\b", command):
      touch_command(command)
    elif re.search(r"\bmkdir\b", command):
      pass
    else:
      write_response("psh: command not found: " + command)
  
  def ls_command():
    response.config(state="normal")
    for obj in cwd:
      if isinstance(obj, Directory):
        response.insert(tk.END, f"{repr(obj)} ", "is_directory")
      
      if isinstance(obj, File):
        response.insert(tk.END, f"{repr(obj)} ", "is_file")
      
    response.delete("end-2c")
    response.config(state="disabled")

  def echo_command(command):
    actions = command.split()

    if len(actions) != 2:
      write_response("psh: command not found: " + command)
      return
    
    actions[-1] = re.sub(r"[\'\"]", "", actions[-1])
    write_response(actions[-1])

  def touch_command(command):
    actions = command.split()

    if len(actions) != 2:
      write_response("psh: command not found: " + command)
      return

    file_name, file_type = actions[-1].split(".")

    if re.search(r"\btxt\b", file_type) == None:
      write_response("psh: file not supported: " + "."+ file_type)
      return

    touched_file = File(file_name + "." + file_type)
    for i in range(len(cwd)):
      if repr(cwd[i]) == repr(touched_file):
        cwd[i] = touched_file
        break
    else:
      cwd.append(touched_file)

    ls_command()

  def write_response(text):
    response.config(state="normal")
    response.insert(tk.END, f"{text}")
    response.config(state="disabled")
  
  def clear_response():
    response.config(state="normal")
    response.delete("1.0", "end")
    response.config(state="disabled")
  
  root = tk.Tk()
  root.geometry("569x343")
  root.title("User — client@users — ~ — -psh — 80x24")
  root.resizable(False, False)

  cmd = tk.Entry(root,
                 width=70,
                 font=("Courier", 14),
                 highlightthickness=0,
                 borderwidth=0)
  cmd.place(anchor=tk.NW, x=20, y=22)

  label = tk.Label(root, 
                   text=f"Last login: {last_login} on ttys",
                   font=("Courier", 14))
  label.place(anchor=tk.NW, x=0, y=0)

  prompt = tk.Label(root,
                    text=">",
                    font=("Courier", 14))
  prompt.place(anchor=tk.NW, x=0, y=22)

  response = tk.Text(root,
                     width=66,
                     font=("Courier", 14))
  response.place(anchor=tk.NW,
                 x=15,
                 y=44,
                 height=283)
  
  response.tag_config('is_directory', foreground="blue")
  response.tag_config('is_file', foreground="black")

  cwd = [Directory("public"), Directory("private")]

  cmd.focus_set()
  cmd.bind("<Return>", execute)
  
  root.mainloop()