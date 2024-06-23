# Remote Terminal

Remote Terminal is a Python-based application that allows clients to connect to a server and send terminal commands to be executed on that server. This project aims to provide an easy-to-use and secure way to manage remote servers from any terminal. The application leverages socket programming to facilitate real-time communication between clients and the server. Multiple clients can connect and interact with the server simultaneously.

## Features

- **Terminal-to-Terminal Interface**: Connect and control the server directly from your terminal.
- **Secure**: Uses authentication to ensure only authorized users can access the terminal.
- **Real-time Command Execution**: Execute shell commands in real-time and view the output instantly.
- **Multiple Client Support**: Multiple clients can connect and send commands simultaneously.
- **Platform Independent**: Works on any system with Python.

## Actions Performed on the Server

- **Create Directory**: Make new directories on the server.
- **Delete Directory**: Remove directories from the server.
- **Edit Directory**: Modify existing directories.
- **Upload Data**: Upload files to the server.
- **Download Data**: Download files from the server.

## Installation

### Prerequisites

- `pydoc`: Provides the `cli` module for command line interface utilities.
- `select`: Allows monitoring multiple file descriptors, waiting until one or more of the file descriptors become "ready" for some class of I/O operation.
- `socket`: Provides low-level networking interface.
- `random`: Implements pseudo-random number generators for various distributions.
- `threading`: Allows running multiple threads (tasks, function calls) at the same time.
- `os`: Provides a way of using operating system dependent functionality like reading or writing to the file system.
- `shutil`: Offers a number of high-level operations on files and collections of files.
- `pathlib`: Offers classes representing filesystem paths with semantics appropriate for different operating systems.

### Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/varun30300/Remote-Terminal.git
    cd Remote-Terminal
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**

    ```bash
    python server.py
    ```

4. **Connect Client**

    Open a new terminal window and run:

    ```bash
    python client.py
    ```
