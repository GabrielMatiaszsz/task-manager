# Gerenciador de Tarefas com Áudio

![image](https://github.com/user-attachments/assets/be8ec984-1736-4641-a837-b10a8e94fed0)


Este é um projeto de gerenciamento de tarefas com suporte para adicionar tarefas de texto e tarefas em áudio. Ele permite que os usuários gravem e reproduzam áudios relacionados às suas tarefas. A interface foi construída com a biblioteca `ttkbootstrap`, proporcionando uma aparência moderna e limpa.

## Funcionalidades

- **Adicionar tarefas de texto:** Você pode adicionar tarefas digitadas.
- **Adicionar tarefas em áudio:** Permite gravar uma mensagem de áudio associada a uma tarefa.
- **Reproduzir tarefas em áudio:** Tarefas com áudios gravados podem ser reproduzidas diretamente pela interface.
- **Excluir tarefas:** Tarefas, tanto de texto quanto de áudio, podem ser removidas.
- **Salvar e carregar tarefas:** As tarefas são salvas em um arquivo `tasks.json` e podem ser carregadas ao iniciar o programa.
- **Interface moderna:** Estilo visual inspirado nos designs da Apple, com o tema `flatly` do `ttkbootstrap`.

## Pré-requisitos

Certifique-se de ter as seguintes bibliotecas Python instaladas:

- `ttkbootstrap`
- `pyaudio`
- `wave`
- `json`
- `os`
- `tkinter` (já incluso no Python)

Para instalar as dependências necessárias, execute o seguinte comando:

```bash
pip install ttkbootstrap pyaudio
