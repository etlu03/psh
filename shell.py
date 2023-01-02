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
    self.children.append(obj)

class File:
  def __init__(self, file_name):
    self.file_name = file_name
    self.content = ""
  
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
      mkdir_command(command)
    elif re.search(r"\bcd\b", command):
      cd_command(command)
    elif re.search(r"\bcat\b", command):
      cat_command(command)
    elif re.search(r"\brm\b", command):
      rm_command(command)
    elif re.search(r"\b\b", command):
      rmdir_command(command)
    else:
      write_response("psh: command not found: " + command)
      cmd.delete(0, tk.END)
    
    global history, pointer
    history.append(command)
    pointer = len(history) - 1

    if 5 < len(history):
      history.pop(0)
  
  def ls_command():
    response.config(state="normal")

    for obj in cwd:
      if isinstance(obj, Directory):
        response.insert(tk.END, f"{repr(obj)} ", "is_directory")
      
      if isinstance(obj, File):
        response.insert(tk.END, f"{repr(obj)} ", "is_file")
      
      if path != [home]:
        response.insert(tk.END, "\n")

    response.config(state="disabled")

  def echo_command(command):
    actions = command.split(maxsplit=1)
    redirection = actions[-1].split(">>")

    if len(redirection) == 2:
      content = redirection[0].strip()
      file_name = redirection[-1].strip()

      content = re.sub(r"[\'\"]", "", content)

      global cwd
      for obj in cwd:
        if repr(obj) == file_name:
          obj.cat(content + "\n")
          break
      else:
        created_file = File(file_name)
        cwd.append(created_file)

        obj.content = content

      ls_command()
    else:
      for i in range(1, len(actions)):
        actions[i] = re.sub(r"[\'\"]", "", actions[i])

      write_response(' '.join(actions[1:]))

  def touch_command(command):
    actions = command.split()
    files = actions[1:]

    global cwd
    for f in files:
      for obj in cwd:
        if repr(obj) == f:
          break
      else:
        cwd.append(File(f))

    ls_command()

  def mkdir_command(command):
    actions = command.split()
    dirs = actions[1:]

    global cwd
    for directory in dirs:
      for obj in cwd:
        if repr(obj) == directory:
          break
      else:
        cwd.append(Directory(directory))

    ls_command()

  def cd_command(command):
    actions = command.split()
    global cwd, path

    if 2 < len(actions):
      write_response("cd: too many arguments")
      return

    if len(actions) == 1 or actions[-1] == "~":
      # `cd` or `cd ~`
      for _ in range(len(path) - 1):
        path.pop(-1)
      
      cwd = path[0].children
      return

    if actions[-1] == "..":
      # `cd ..`
      if len(path) != 1:
        path.pop()
        cwd = path[-1].children
      return
  
    cd_dir = actions[-1]
    for obj in cwd:
      # `cd {cd_dir}`
      if repr(obj) == cd_dir:
        cwd = obj.children
        path.append(obj)
        break
    else:
      write_response("cd: no such file or directory: " + cd_dir)

  def cat_command(command):
    actions = command.split(maxsplit=1)
    file_name = actions[-1]

    global cwd
    for obj in cwd:
      if repr(obj) == file_name:
        write_response(obj.content)
        break
    else:
      write_response("psh: file does not exist: " + file_name)

  def rm_command(command):
    actions = command.split(maxsplit=2)
    dir_name = actions[-1]
    i = 0

    if len(actions) == 2:
      # `rm {dir_name}`
      global cwd
      while i < len(cwd):
        if repr(cwd[i]) != dir_name:
          i += 1
        else:
          if isinstance(cwd[i], Directory):
            write_response("rm: cannot remove " + "'" +  repr(cwd[i]) + "' : Is a directory")
          else:
            cwd.pop(i)
            ls_command()
          break
    else:
      pass

  def rmdir_command(command):
    actions = command.split()
    dir_name = actions[-1]
    i = 0

    global cwd
    while i < len(cwd):
      if repr(cwd[i]) != dir_name:
        i += 1
      else:
        if cwd[i].children == []:
          cwd.pop(i)
          ls_command()
        else:
          write_response("rmdir: " + repr(cwd[i]) + ": Directory not empty")
        break


  def up_history(entry):
    global pointer
    if 0 < pointer:
      pointer -= 1

      cmd.delete(0, tk.END)
      cmd.insert(0, history[pointer])
  
  def down_history(entry):
    global pointer
    if pointer < (len(history) - 1):
      pointer += 1

      cmd.delete(0, tk.END)
      cmd.insert(0, history[pointer])

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

  response = tk.Text(root,
                     width=66,
                     font=("Courier", 14))
  response.place(anchor=tk.NW,
                 x=17,
                 y=35,
                 height=283)
  
  response.tag_config('is_directory', foreground="blue")
  response.tag_config('is_file', foreground="black")

  cmd = tk.Entry(root,
                 width=70,
                 font=("Courier", 14),
                 highlightthickness=0,
                 borderwidth=0)
  cmd.place(anchor=tk.NW, x=20, y=23)

  label = tk.Label(root, 
                   text=f"Last login: {last_login} on ttys",
                   font=("Courier", 14))
  label.place(anchor=tk.NW, x=0, y=0)

  prompt = tk.Label(root,
                    text=">",
                    font=("Courier", 14))
  prompt.place(anchor=tk.NW, x=0, y=21)

  home = Directory("~")
  public, private = Directory("public"), Directory("private")
  history, pointer = [], 0
  
  home.add_child(public)
  home.add_child(private)

  cwd = [public, private]
  path = [home]

  cmd.focus_set()
  cmd.bind("<Return>", execute)
  cmd.bind("<Up>", up_history)
  cmd.bind("<Down>", down_history)
  
  root.mainloop()