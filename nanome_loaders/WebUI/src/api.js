const API = {
  list(path) {
    return fetch('/files' + path).then(res => res.json())
  },

  async getFolder(path) {
    const folder = {
      path: '',
      parent: '',
      files: [],
      folders: []
    }

    if (path.slice(-1) !== '/') {
      path += '/'
    }

    if (path !== '/') {
      const lastSlash = path.slice(0, -1).lastIndexOf('/')
      folder.parent = path.substring(0, lastSlash) + '/'
    }

    const data = await API.list(path)
    if (!data.success) throw new Error(data.error)
    folder.path = path

    folder.folders = data.folders
    folder.files = data.files.map(f => {
      const [full, name, ext] = /^(.+?)(?:\.(\w+))?$/.exec(f)
      return { full, name, ext }
    })

    return folder
  },

  upload(path, files) {
    if (!files || !files.length) return

    const data = new FormData()
    for (const file of files) {
      data.append('file', file)
    }

    return fetch('/files' + path, {
      method: 'POST',
      body: data
    })
  },

  delete(path) {
    return fetch('/files' + path, {
      method: 'DELETE'
    })
  },

  create(path) {
    return fetch('/files' + path, {
      method: 'POST'
    })
  }
}

export default API
