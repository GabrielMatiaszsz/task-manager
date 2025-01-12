import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import json
import os
import pyaudio
import wave

TASKS_FILE = "tasks.json"
AUDIO_DIR = "audio_tasks"


# Verifica e cria o diretório de áudios
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas com Áudio")
        self.root.geometry("500x600")

        # Armazena as tarefas
        self.tasks = self.load_tasks()

        # Criação dos widgets
        ttk.Label(root, text="Gerenciador de Tarefas", font=("Helvetica", 20, "bold")).pack(pady=10)

        # Usando Treeview para exibir tarefas
        self.task_tree = ttk.Treeview(root, columns=("task", "status"), show="headings", height=15, bootstyle="info")
        self.task_tree.heading("task", text="Tarefa")
        self.task_tree.heading("status", text="Status")
        self.task_tree.column("task", width=300, anchor="w")
        self.task_tree.column("status", width=100, anchor="center")
        self.task_tree.pack(pady=10)

        self.entry = ttk.Entry(root, width=40, font=("Helvetica", 12))
        self.entry.pack(pady=5)

        # Botões estilizados
        ttk.Button(root, text="Adicionar Tarefa", command=self.add_task, bootstyle="success-outline").pack(pady=5)
        ttk.Button(root, text="Adicionar Tarefa em Áudio", command=self.add_audio_task, bootstyle="primary-outline").pack(pady=5)
        ttk.Button(root, text="Reproduzir Tarefa Selecionada", command=self.play_audio, bootstyle="info-outline").pack(pady=5)
        ttk.Button(root, text="Remover Tarefa", command=self.delete_task, bootstyle="danger-outline").pack(pady=5)
        ttk.Button(root, text="Salvar Tarefas", command=self.save_tasks, bootstyle="success").pack(pady=10)

        # Atualiza a lista inicial
        self.update_task_list()

    def add_task(self):
        task = self.entry.get()
        if task:
            self.tasks.append({"task": task, "status": "pendente", "audio": None})
            self.entry.delete(0, tk.END)
            self.update_task_list()
        else:
            messagebox.showwarning("Erro", "Digite uma tarefa válida.")

    def add_audio_task(self):
        task = self.entry.get()
        if not task:
            messagebox.showwarning("Erro", "Digite uma descrição para a tarefa antes de gravar o áudio.")
            return

        audio_path = os.path.join(AUDIO_DIR, f"{len(self.tasks)}.wav")
        self.record_audio(audio_path)

        self.tasks.append({"task": task, "status": "pendente", "audio": audio_path})
        self.entry.delete(0, tk.END)
        self.update_task_list()

    def record_audio(self, audio_path):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        messagebox.showinfo("Gravação", "Gravação de áudio iniciada. Fale algo!")
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(audio_path, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        messagebox.showinfo("Gravação", f"Áudio salvo em {audio_path}")

    def play_audio(self):
        selected_task = self.get_selected_task()
        if not selected_task:
            return

        audio_path = selected_task.get("audio")
        if not audio_path:
            messagebox.showwarning("Erro", "Esta tarefa não possui áudio associado.")
            return

        CHUNK = 1024
        wf = wave.open(audio_path, "rb")
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)
        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def delete_task(self):
        selected_task_index = self.get_selected_task_index()
        if selected_task_index is not None:
            task = self.tasks.pop(selected_task_index)
            if task.get("audio") and os.path.exists(task["audio"]):
                os.remove(task["audio"])
            self.update_task_list()
        else:
            messagebox.showwarning("Erro", "Selecione uma tarefa para remover.")

    def update_task_list(self):
        for row in self.task_tree.get_children():
            self.task_tree.delete(row)

        for index, task in enumerate(self.tasks):
            status = "✔" if task["status"] == "concluído" else "Pendente"
            self.task_tree.insert("", "end", iid=index, values=(task["task"], status))

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f)
        messagebox.showinfo("Sucesso", "Tarefas salvas com sucesso!")

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                try:
                    tasks = json.load(f)
                    if isinstance(tasks, list):
                        return tasks
                except json.JSONDecodeError:
                    return []
        return []

    def get_selected_task_index(self):
        selected = self.task_tree.focus()
        return int(selected) if selected else None

    def get_selected_task(self):
        index = self.get_selected_task_index()
        if index is not None:
            return self.tasks[index]
        messagebox.showwarning("Erro", "Selecione uma tarefa.")
        return None

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = TaskManagerApp(root)
    root.mainloop()
