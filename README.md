Criei o código com uma janela (Tkinter). Ao clicar em ▶ Play, ele gera uma senha aleatória com no mínimo 16 caracteres.


Como usar:
Instalar o a biblioteca "import bcrypt"; e
instalar o bcrypt no Python 3.14.
pip install bcrypt
python gerador_senhas.py

O que ele faz:

Gera a senha com o módulo secrets, que é seguro para esse fim. Ela sempre tem letras minúsculas, maiúsculas, números e, opcionalmente, símbolos.
O tamanho mínimo é 16. Se alguém digitar menos, o código ajusta para 16. O máximo é 64, porque o bcrypt só considera os primeiros 72 bytes.
Reproduz o seu exemplo com bcrypt para a senha gerada. Ele mostra que salt_a == salt_b dá False, que os dois hashes são diferentes e que checkpw retorna True para ambos com a senha correta.
Tem um botão Copiar para levar a senha à área de transferência.

