"""
Gerador de senhas com janela (Tkinter) + demonstração de bcrypt.

Instalação:  pip install bcrypt
Execução:    python gerador_senhas.py
"""

import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox

import bcrypt

TAMANHO_MIN = 16
TAMANHO_MAX = 64  # bcrypt só considera os primeiros 72 bytes


def gerar_senha(tamanho: int, simbolos: bool = True) -> str:
    """Gera uma senha aleatória segura com pelo menos 1 de cada tipo."""
    tamanho = max(tamanho, TAMANHO_MIN)
    conjuntos = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if simbolos:
        conjuntos.append("!@#$%&*?-_.+=")

    # garante pelo menos um caractere de cada conjunto
    senha = [secrets.choice(c) for c in conjuntos]
    todos = "".join(conjuntos)
    senha += [secrets.choice(todos) for _ in range(tamanho - len(senha))]
    secrets.SystemRandom().shuffle(senha)
    return "".join(senha)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Senhas")
        self.geometry("620x420")
        self.resizable(False, False)

        self.tamanho = tk.IntVar(value=TAMANHO_MIN)
        self.simbolos = tk.BooleanVar(value=True)
        self.senha = tk.StringVar()

        self._montar_interface()

    def _montar_interface(self):
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        # Opções
        opcoes = ttk.Frame(frame)
        opcoes.pack(fill="x")
        ttk.Label(opcoes, text=f"Tamanho (mín. {TAMANHO_MIN}):").pack(side="left")
        ttk.Spinbox(
            opcoes, from_=TAMANHO_MIN, to=TAMANHO_MAX,
            textvariable=self.tamanho, width=5,
        ).pack(side="left", padx=8)
        ttk.Checkbutton(
            opcoes, text="Incluir símbolos", variable=self.simbolos
        ).pack(side="left", padx=15)

        # Botão play
        ttk.Button(
            frame, text="▶  Play (gerar senha)", command=self.on_play
        ).pack(pady=12, fill="x")

        # Senha gerada
        ttk.Label(frame, text="Senha gerada:").pack(anchor="w")
        linha = ttk.Frame(frame)
        linha.pack(fill="x", pady=4)
        ttk.Entry(
            linha, textvariable=self.senha,
            font=("Consolas", 13), state="readonly",
        ).pack(side="left", fill="x", expand=True)
        ttk.Button(linha, text="Copiar", command=self.copiar).pack(side="left", padx=6)

        # Saída do bcrypt
        ttk.Label(frame, text="Demonstração bcrypt:").pack(anchor="w", pady=(12, 0))
        self.saida = tk.Text(
            frame, height=10, wrap="word", font=("Consolas", 9), state="disabled"
        )
        self.saida.pack(fill="both", expand=True, pady=4)

    def on_play(self):
        try:
            tamanho = int(self.tamanho.get())
        except (tk.TclError, ValueError):
            messagebox.showerror("Erro", "Tamanho inválido.")
            return

        if tamanho < TAMANHO_MIN:
            tamanho = TAMANHO_MIN
            self.tamanho.set(TAMANHO_MIN)
        if tamanho > TAMANHO_MAX:
            tamanho = TAMANHO_MAX
            self.tamanho.set(TAMANHO_MAX)

        senha = gerar_senha(tamanho, self.simbolos.get())
        self.senha.set(senha)
        self.demonstrar_bcrypt(senha)

    def demonstrar_bcrypt(self, senha: str):
        """Mesma lógica do seu exemplo: dois salts diferentes -> dois hashes."""
        senha_b = senha.encode("utf-8")

        salt_a = bcrypt.gensalt()
        salt_b = bcrypt.gensalt()

        hash_a = bcrypt.hashpw(senha_b, salt_a)
        hash_b = bcrypt.hashpw(senha_b, salt_b)

        linhas = [
            f"salt_a == salt_b ?  {salt_a == salt_b}",
            f"hash_a: {hash_a.decode()}",
            f"hash_b: {hash_b.decode()}",
            f"checkpw(senha, hash_a) -> {bcrypt.checkpw(senha_b, hash_a)}",
            f"checkpw(senha, hash_b) -> {bcrypt.checkpw(senha_b, hash_b)}",
            f"checkpw(senha errada, hash_a) -> {bcrypt.checkpw(b'errada', hash_a)}",
        ]

        self.saida.config(state="normal")
        self.saida.delete("1.0", "end")
        self.saida.insert("end", "\n".join(linhas))
        self.saida.config(state="disabled")

    def copiar(self):
        if self.senha.get():
            self.clipboard_clear()
            self.clipboard_append(self.senha.get())


if __name__ == "__main__":
    App().mainloop()
