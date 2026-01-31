import os
import file_organization
import gui

gui = gui.GUI()
folder_list = gui.run_gui()

print(folder_list)

# root.mainloop()
# source_file_path = os.path.join(os.getcwd(), "Source Files")
# destination_folder = os.path.join(os.getcwd(), "Modified Files")

# source_file_path = os.path.join(os.getcwd(), "Test Source Files")
# destination_folder = os.path.join(os.getcwd(), "Test Modified Files")

file_organization.FileOrganization(folder_list[0], folder_list[1])