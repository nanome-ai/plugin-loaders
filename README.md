# Nanome - Loaders

### A linux-only molecule loader plugin for Nanome through a URL or a Drag-and-Drop Web Interface.

This works for both Nanome & Nanome Curie (Quest edition).


- URL Loader will load a molecule from RCSB, by its molecular code
- Web Loader will start a web server. Other people can upload molecules to it, and they will appear in Nanome

### Installation

```sh
$ pip install nanome-loaders
```

### Usage

To start the plugin:

```sh
$ nanome-url-loader -a plugin_server_address
```

```sh
$ nanome-web-loader -a plugin_server_address
```

In Nanome:

- Activate Plugin
- Click Run
- For URL Loader: Enter a molecular code (for instance "1YUI"), and click "Load"
- For Web Loader: The list of molecule should be empty. Open your web browser, go to "127.0.0.1" (or your computer's IP address from another computer), and add molecular files (.pdb, .sdf, or .cif). Your files will appear in Nanome

### License

MIT
