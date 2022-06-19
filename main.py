#importing needed libraries
from tkinter import Entry, Tk, END
import tkinter.font as font
from collections import defaultdict
import random
from word_list import words
from tkinter import messagebox as mb

#Defining a few functions and coding the word part of the day.
def next_row():
  global track_row
  track_row = track_row + 1
  next_row = entry_dict[track_row]
  ## also enable row
  for inp in next_row:
    inp.config(state= "normal")
  ## set the focus on the first one
  next_row[0].focus_set()
  
def caps(event):
  selected = root.focus_get()
  current_text = selected.get()

  if current_text:
    selected.delete(0,END)
    selected.insert(0,current_text.upper())
    if selected.col + 1 < wcolumn:
      next_entry = entry_dict[track_row][selected.col + 1]
      next_entry.focus_set()
            
def enter_pressed(event):
  check_word()

def delete_pressed(event):
  def clear(entry):
    current_text = entry.get()
    if current_text:
      entry.delete(0,END)

  ## get current focused entry & clear
  selected = root.focus_get()
  clear(selected)

  ## check if previous entry can be cleaned 
  if selected.col - 1 >= 0:
    last_entry = entry_dict[track_row][selected.col - 1]
    clear(last_entry)
    last_entry.focus_set()

def reset_grid():
  global track_row
  track_row = 0
  for r_entries in entry_dict.values():
    for c_entry in r_entries:
      c_entry.config(state= "normal")
      c_entry.delete(0,END)
  entry_dict[0][0].focus_set()
  
def check_word():
  current_entries = entry_dict[track_row]
  ## check if all the enteries have some text
  for inp in current_entries:
      if not inp.get():
        mb.showinfo("Fill all", "Please fill all the sections.")
        return
  ## check if its a valid word
  entered_word = ""
  for inp in current_entries:
    entered_word += inp.get().lower()
    
  all_correct_entries = True
  ## now check all the entered text
  for index, inp in enumerate(current_entries):
      current_value = inp.get().lower()
      ## when letter matches
      if current_value == today_word[index]:
        inp.configure({"disabledbackground": "lightgreen",                                 "disabledforeground" : "black",
                      })
      else:
        all_correct_entries = False
        ## check if its in the today's word
        if current_value in today_word:
          inp.configure({"disabledbackground": "lightyellow", 
                         "disabledforeground" : "black",
                        })
        else:
          # letter is not in the word at all
          inp.configure({"disabledbackground": "lightgrey",
                         "disabledforeground" : "black",
                        })
      ## make text bold & disable
      inp.configure(font=font.Font(weight="bold"))
      inp.config(state= "disabled")

  ## if all the entries are not correct then move to next row
  if not all_correct_entries:
    if track_row + 1 < wrow:
      next_row()
    else:
      mb.showerror("TryAgain", "Sorry, Try Again")
      reset_grid()
  else:
    mb.showinfo('YouWon', 'Congratulations! You won!')
    #print("You won !!!")

#---------------------------------------------------------

def main():
  for row in range(wrow):
    for col in range(wcolumn):
      
      entry = Entry(root, 
                    width=4,
                    justify='center', 
                    font=(14), 
                    bd=4)
      
      ## tracking the entry
      entry.row=row
      entry.col=col
      
      ## change entred text to caps
      entry.bind("<KeyRelease>", caps)
      ## when Enter is hit
      entry.bind("<Return>", enter_pressed)
      ## when backspace is hit
      entry.bind("<BackSpace>", delete_pressed)
      
      entry_dict[row].append(entry)
  
      entry.grid(row=row, column=col + 1, padx=10,
                  pady=10, ipady=5)
      
      ## disable rows except first one
      if row > 0:
        entry.config(state= "disabled")
      ## set the focus on the first row and first column
      if row == 0 and col == 0:
        entry.focus_set()
      entry.icursor(0)
  # root.mainloop()

#------------------------------------------------------------
      #CODE START BELOW
#------------------------------------------------------------

if __name__ == "__main__":
  # Choose a word random from list
  today_word = random.choice(words)
  print(today_word)
  # variables for number of letters in word and 
  # letters per column/row
  wrow = 6
  wcolumn = 5
  track_row = 0

  #Creating the screen for Wordle.
  root = Tk()
  root.title("Wordle")
  root.geometry("550x550")
  root.resizable(0, 0)
  
  entry_dict = defaultdict(list)

  # Defining variables needed later on.

  main()