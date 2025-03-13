## This is desktop application for ZePark project

# Instructions to run the project
- Ensure the the `uv` is installed
    ```powershell
    uv -V
    ```

- If `uv` not found in your system then follow the instruction to install `uv` into your system
    - For Windows
        ```powershell
        powershell -c "irm https://astral.sh/uv/install.ps1 | more"
        ```
    - For macOS and Linux
        ```powershell
        curl -LsSf https://astral.sh/uv/install.sh | less
        ```
    - Also can use `pip` to install `uv` in any system if you already have python installed
        ```powershell
        pip install uv
        ```

- To sync the project and install the dependency
    ```powershell
    uv sync --no-dev
    ```
- Now run the project using this line
    ```powershell
    uv run app/main.py
    ```
