import store from '@/store'
const LOGIN_API = 'https://api.nanome.ai/user'

function replaceAccount(path) {
  return path.replace(/^\/account/, '/' + store.state.unique)
}

function request(url, options) {
  return fetch(url, options).then(res => res.json())
}

const API = {
  login({ username, password }) {
    const body = {
      login: username,
      pass: password,
      source: 'web:webloader-plugin'
    }

    return request(`${LOGIN_API}/login`, {
      headers: {
        'Content-Type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify(body)
    })
  },

  refresh() {
    const token = store.state.token
    if (!token) return {}

    return request(`${LOGIN_API}/session`, {
      headers: {
        Authorization: `Bearer ${token}`
      },
      method: 'GET'
    })
  },

  list(path) {
    if (path === '/') {
      return {
        success: true,
        files: [],
        folders: ['shared']
      }
    }

    path = replaceAccount(path)
    return request('/files' + path)
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

    path = replaceAccount(path)
    return request('/files' + path, {
      method: 'POST',
      body: data
    })
  },

  delete(path) {
    path = replaceAccount(path)
    return request('/files' + path, {
      method: 'DELETE'
    })
  },

  create(path) {
    path = replaceAccount(path)
    return request('/files' + path, {
      method: 'POST'
    })
  }
}

export default API
