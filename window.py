import tkinter as tk
from datetime import date, datetime

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

  root = tk.Tk()
  root.geometry("569x343")
  root.title("User — client@users — ~ — -psh — 80x24")
  root.resizable(False, False)

  entry = tk.Entry(root,
                   width=70,
                   font=("Courier", 14),
                   highlightthickness=0,
                   borderwidth=0)
  entry.place(anchor=tk.NW, x=20, y=22)

  label = tk.Label(root, 
                   text=f"Last login: {last_login} on ttys",
                   font=("Courier", 14))
  label.place(anchor=tk.NW, x=0, y=0)

  prompt = tk.Label(root,
                    text=">",
                    font=("Courier", 14))
  prompt.place(anchor=tk.NW, x=0, y=22)

  root.mainloop()