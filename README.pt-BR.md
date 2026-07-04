# NoteBook FanControl GUI

[English](README.md)

Uma interface gráfica pequena, feita em Python e GTK, para o [nbfc-linux](https://github.com/nbfc-linux/nbfc-linux). Ela oferece uma janela de desktop para alternar modos de controle da ventoinha sem digitar comandos `nbfc` manualmente.

O aplicativo permite:

- Ativar o controle automático da ventoinha.
- Definir a ventoinha na velocidade máxima.
- Aplicar uma velocidade manual por porcentagem.
- Ler o status atual do `nbfc` quando o aplicativo inicia.

![Captura de tela do aplicativo](/assets/main.png "Captura de tela do aplicativo")

## Requisitos

- Python 3.11 ou mais recente.
- Poetry.
- Pacotes de runtime do GTK 4, libadwaita e PyGObject para a sua distribuição Linux.
- `nbfc-linux` instalado e configurado.
- `pkexec`, usado ao aplicar mudanças privilegiadas no `nbfc`.

Este projeto é apenas uma interface gráfica. Perfis de ventoinha, configuração do serviço e suporte de hardware dependem do próprio `nbfc-linux`.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/Andre0n/nbfc-linux-gui
cd nbfc-linux-gui
```

Instale as dependências Python:

```bash
poetry install
```

## Execução

Inicie o aplicativo a partir do diretório do projeto:

```bash
poetry run python nbfc_linux_gui.py
```

Também é possível usar o ponto de entrada do pacote:

```bash
poetry run nbfc_linux_gui
```

Ao clicar em **Aplicar**, o aplicativo executa `pkexec nbfc ...`, então o seu ambiente de desktop pode solicitar autenticação de administrador.

## Desenvolvimento

Comandos úteis:

```bash
poetry run python -m nbfc_linux_gui
poetry run blue nbfc_linux_gui tests
poetry run isort nbfc_linux_gui tests
```

O módulo `nbfc_linux_gui.nbfc` é um wrapper simples para a CLI do `nbfc`. O código da interface fica em `nbfc_linux_gui/objects`.

## Licença

Este projeto está licenciado sob a LGPL-3.0. Consulte [LICENSE](LICENSE) para mais detalhes.
