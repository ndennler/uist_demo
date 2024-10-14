import tkinter as tk
from tkinter import ttk
from pylips.speech import RobotFace
from pylips.face import FacePresets

# Create two RobotFace objects
face1 = RobotFace(robot_name='actor1', voice_id="com.apple.voice.compact.en-GB.Daniel")
face2 = RobotFace(robot_name='actor2', voice_id="com.apple.voice.premium.en-US.Zoe")


def run_script():
    output_label.config(text=f"Actors are Performing! Please respect their Theater!")
    disable_interface()



    # Get script and actor details
    script = text_box.get("1.0", "end-1c")
    
    actor1_name = actor1_name_var.get()
    actor1_appearance = actor1_appearance_var.get()
    actor1_voice = actor1_voice_var.get()
    face1.robot_name = actor1_name  # Set the name for Actor 1
    face1.set_appearance(get_preset(actor1_appearance))
    face1.voice_id = actor1_voice

    actor2_name = actor2_name_var.get()
    actor2_appearance = actor2_appearance_var.get()
    actor2_voice = actor2_voice_var.get()
    face2.robot_name = actor2_name  # Set the name for Actor 2
    face2.set_appearance(get_preset(actor2_appearance))
    face2.voice_id = actor2_voice

    if actor1_name == '' or actor2_name == '':
        output_label.config(text="Please enter names for both actors.")
        enable_interface()
        return
    
    
    for line in script.split('\n'):
        if ':' not in line:
            continue
        actor, content = line.split(':', 1)
        if actor.strip() == actor1_name:
            face1.say(content.strip())
            face1.wait()
        elif actor.strip() == actor2_name:
            face2.say(content.strip())
            face2.wait()

    output_label.config(text=f"Performance finished!")
    enable_interface()


def get_preset(preset):
    if preset == 'default':
        return FacePresets.default
    elif preset == 'high_contrast':
        return FacePresets.high_contrast
    elif preset == 'chili':
        return FacePresets.chili
    elif preset == 'gingerbreadman':
        return FacePresets.gingerbreadman
    elif preset == 'cutie':
        return FacePresets.cutie
    else:
        return FacePresets.default


def disable_interface():
    # Disable text box
    text_box.config(state='disabled')

    # Disable name fields and drop-downs
    actor1_name_entry.config(state='disabled')
    actor1_appearance_dropdown.config(state='disabled')
    actor1_voice_dropdown.config(state='disabled')
    actor2_name_entry.config(state='disabled')
    actor2_appearance_dropdown.config(state='disabled')
    actor2_voice_dropdown.config(state='disabled')

    # Disable run button
    run_button.config(state='disabled')


def enable_interface():
    # Enable text box
    text_box.config(state='normal')

    # Enable name fields and drop-downs
    actor1_name_entry.config(state='normal')
    actor1_appearance_dropdown.config(state='normal')
    actor1_voice_dropdown.config(state='normal')
    actor2_name_entry.config(state='normal')
    actor2_appearance_dropdown.config(state='normal')
    actor2_voice_dropdown.config(state='normal')

    # Enable run button
    run_button.config(state='normal')


# Create the main window
root = tk.Tk()
root.title("Script Runner with Actor Selection")

# Text box for script input
text_box_label = tk.Label(root, text="Enter Script:")
text_box_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

text_box = tk.Text(root, height=10, width=90)
text_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Actor 1 Name entry (Left side)
actor1_name_label = tk.Label(root, text="Actor 1 Name:")
actor1_name_label.grid(row=2, column=0, padx=10, pady=5, sticky="W")

actor1_name_var = tk.StringVar()
actor1_name_entry = tk.Entry(root, textvariable=actor1_name_var)
actor1_name_entry.grid(row=3, column=0, padx=10, pady=5, sticky="W")

# Actor 1 Appearance drop-down (Left side)
actor1_appearance_label = tk.Label(root, text="Actor 1 Appearance:")
actor1_appearance_label.grid(row=4, column=0, padx=10, pady=5, sticky="W")

actor1_appearance_var = tk.StringVar()
actor1_appearance_dropdown = ttk.Combobox(root, textvariable=actor1_appearance_var)
actor1_appearance_dropdown['values'] = ['default', 'high_contrast', 'chili', 'gingerbreadman', 'cutie']
actor1_appearance_dropdown.current(0)
actor1_appearance_dropdown.grid(row=5, column=0, padx=10, pady=5, sticky="W")

# Actor 1 Voice drop-down (Left side)
actor1_voice_label = tk.Label(root, text="Actor 1 Voice:")
actor1_voice_label.grid(row=6, column=0, padx=10, pady=5, sticky="W")

actor1_voice_var = tk.StringVar()
actor1_voice_dropdown = ttk.Combobox(root, textvariable=actor1_voice_var)
actor1_voice_dropdown['values'] = ["Justin", "Kendra"]
actor1_voice_dropdown.current(0)
actor1_voice_dropdown.grid(row=7, column=0, padx=10, pady=5, sticky="W")

# Actor 2 Name entry (Right side)
actor2_name_label = tk.Label(root, text="Actor 2 Name:")
actor2_name_label.grid(row=2, column=1, padx=10, pady=5, sticky="W")

actor2_name_var = tk.StringVar()
actor2_name_entry = tk.Entry(root, textvariable=actor2_name_var)
actor2_name_entry.grid(row=3, column=1, padx=10, pady=5, sticky="W")

# Actor 2 Appearance drop-down (Right side)
actor2_appearance_label = tk.Label(root, text="Actor 2 Appearance:")
actor2_appearance_label.grid(row=4, column=1, padx=10, pady=5, sticky="W")

actor2_appearance_var = tk.StringVar()
actor2_appearance_dropdown = ttk.Combobox(root, textvariable=actor2_appearance_var)
actor2_appearance_dropdown['values'] = ['default', 'high_contrast', 'chili', 'gingerbreadman', 'cutie']
actor2_appearance_dropdown.current(0)
actor2_appearance_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="W")

# Actor 2 Voice drop-down (Right side)
actor2_voice_label = tk.Label(root, text="Actor 2 Voice:")
actor2_voice_label.grid(row=6, column=1, padx=10, pady=5, sticky="W")

actor2_voice_var = tk.StringVar()
actor2_voice_dropdown = ttk.Combobox(root, textvariable=actor2_voice_var)
actor2_voice_dropdown['values'] = ["Justin", "Kendra"]
actor2_voice_dropdown.current(0)
actor2_voice_dropdown.grid(row=7, column=1, padx=10, pady=5, sticky="W")

# Run button (below the text box and drop-downs)
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Output label to display feedback
output_label = tk.Label(root, text="")
output_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
