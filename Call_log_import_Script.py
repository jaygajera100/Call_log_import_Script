from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from pathlib import Path
import pandas as pd
gui = Tk()
gui.geometry("400x400")
gui.title("FC")


def getFolderPath():
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)


def getSavePath():
    folder_selected = filedialog.askdirectory()
    savePath.set(folder_selected)


def doStuff():
    # From Path
    folder = folderPath.get()
    splitt = folder.split('/')
    folder_path = "\\".join(splitt)
    path = Path(folder_path)

    # Save Path
    save = savePath.get()
    splitt = save.split('/')
    save_path = "\\".join(splitt)
    save_path = Path(save_path)

    # Get All CSV file from the folder
    csv_file = [p for p in path.glob("*.csv")]
    csv_files = [str(x) for x in csv_file]

    # Editing One by One CSV FILE
    for file in csv_files:
        data = pd.read_csv(file)
        # Drop First 4 Row Which is the header of the data
        data1 = data.drop([0, 1, 2, 3], axis=0).copy()
        data1.iloc[0, 2] = 'Jay'
        data1.columns = data1.iloc[0]
        df = data1.drop(4, axis=0)
        # Making Key Column
        df["Key"] = " "
        df.fillna(' ', inplace=True)
        for x in range(0, len(df)-1):
            if x == 0:
                df.iloc[x, -1] = f"{df.iloc[x, 0]} | {df.iloc[x, 3]}"

            elif df.iloc[x, 0] == " ":
                df.iloc[x, -1] = f"{df.iloc[x-1, 0]} | {df.iloc[x, 3]}"
                df.iloc[x, 0] = df.iloc[x-1, 0]

            else:
                df.iloc[x, -1] = f"{df.iloc[x, 0]} | {df.iloc[x, 3]}"

        dff = list(df['Key'])
        df = df.drop(['Key'], axis=1)
        df.insert(0, 'Key', dff)
        df.insert(1, 'Missing?', "")
        df.reset_index(drop=True, inplace=True)

        # Delete Reason which contain "Was Joined"
        reason = list(df.Reason)
        count = 0
        result = []
        for i in reason:
            if "was join" in i:
                result.append(count)
            count = count + 1
        df.drop(df.index[result], inplace=True)
        df.reset_index(drop=True, inplace=True)

        # Delete the unwanted column
        df.drop('Jay', axis=1, inplace=True)
        for i in range(2):
            df.drop([df.index[-1]], inplace=True)
        df.drop_duplicates(subset="Key", inplace=True)
        df.drop(['Play'], axis=1, inplace=True)
        df.insert(11, "Play", "")

        # Making Save path and Save the file
        name = file.split('\\')
        f = f"{save_path}\\{name[-1]}"
        df.to_csv(f, index=False)
        print("Done")

    messagebox.showinfo("Information", "Done")
    gui.quit()


folderPath = StringVar()
a = Label(gui, text="From :")
a.grid(row=0, column=0)
E = Entry(gui, textvariable=folderPath)
E.grid(row=0, column=1)
btnFind = ttk.Button(gui, text="Browse Folder", command=getFolderPath)
btnFind.grid(row=0, column=2)

savePath = StringVar()
a = Label(gui, text="Save to :")
a.grid(row=1, column=0)
E = Entry(gui, textvariable=savePath)
E.grid(row=1, column=1)
btnFind = ttk.Button(gui, text="Browse Folder", command=getSavePath)
btnFind.grid(row=1, column=2)

c = ttk.Button(gui, text="find", command=doStuff)
c.grid(row=4, column=0)
gui.mainloop()


print('Done')
