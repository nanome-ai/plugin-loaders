# Nanome - Loaders

### A Web-Loader plugin for Nanome to load files through a URL or a Drag-and-Drop Web Interface.

This works for both Nanome & Nanome Curie (Quest edition).


- URL Loader will load a molecule from RCSB, by its molecular code
- Web Loader will start a web server. Other people can upload molecules or other files to it, and they will appear in Nanome.

Web Loader currently supports:
- Molecules: .pdb, .cif, .sdf
- Presentations: .pptx, .ppt, .odp
- Documents: .pdf

### Installation

```sh
$ pip install nanome-loaders
```

In order to load non-molecular files with Web Loader, the following applications/packages should be installed on the computer running the plugin:
- ImageMagick
- LibreOffice
- Ghostscript

For Windows especially, make sure that these applications are in the PATH environment variable (the folder containing simpress.exe should be in PATH for LibreOffice)

### Usage

To start the plugin:

```sh
$ nanome-url-loader -a plugin_server_address
```

```sh
$ nanome-web-loader -a plugin_server_address
```

On Linux, you might have to start the nanome-web-loader as sudo to listen on port 80.

In Nanome:

- Activate Plugin
- Click Run
- For URL Loader: Enter a molecular code (for instance "1YUI"), and click "Load"
- For Web Loader: The list of molecule should be empty. Open your web browser, go to "127.0.0.1" (or your computer's IP address from another computer), and add supported files. Your files will appear in Nanome

### License

MIT
