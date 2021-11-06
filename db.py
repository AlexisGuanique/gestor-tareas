from tkinter import *
import sqlite3

root = Tk()
root.title('Gestos de Tareas')
root.geometry('400x400')

#################################################################################################################
#Base da datos

conn = sqlite3.connect('todo.db')
c = conn.cursor()

c.execute(
    """
        CREATE TABLE IF NOT EXISTS tarea(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL
        );
    """
)

conn.commit()

#################################################################################################################
#Interfaz grafica

# c.execute('delete from tarea')
# conn.commit()

#########################################
#Esto se conoce como CURRYING!

def remove(id):
    def _remove():
        c.execute('DELETE FROM tarea WHERE id = ?', (id, ))
        conn.commit()
        render_todos()
    return _remove


def complete(id):
    def _complete():
        todo = c.execute("SELECT * FROM tarea WHERE id = ?", (id, )).fetchone()
        c.execute("UPDATE tarea SET completed = ? WHERE id = ?", (not todo[3], id))
        conn.commit()
        render_todos()
        
    return _complete

############################


def render_todos():
    rows = c.execute("SELECT * FROM tarea").fetchall()

    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = '#888888' if completed else '#000000'
        l = Checkbutton(frame, text=description, fg=color, width=42, anchor='w', command= complete(id))
        l.grid(row=i, column=0, sticky='w')
        boton = Button(frame, text='Eliminar', command=remove(id))
        boton.grid(row=i, column=1)
        l.select() if completed else l.deselect()


def addTodo():
    e.get()
    todo = e.get()
    if todo:
        c.execute("""
            INSERT INTO tarea(description, completed) VALUES(?, ?)
        """, (todo, False))
        conn.commit()
        e.delete(0, END)
        render_todos()
    else:
        pass



l = Label(root, text='Tarea')
l.grid(row=0, column=0)

e = Entry(root, width=40, borderwidth=3)
e.grid(row=0, column=1)

boton = Button(root, text='Agregar', command=addTodo)
boton.grid(row=0, column=2)

frame = LabelFrame(root, text='Mis Tareas', padx=5, pady=5)
frame.grid(row=1, columnspan=3, sticky='nswe', padx=5)


e.focus()
root.bind('<Return>', lambda x: addTodo())

render_todos()

root.mainloop()



