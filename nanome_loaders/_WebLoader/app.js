'use strict'

new Vue({
  el: '#app',

  data: {
    files: [],
    numDropping: 0,
    isDroppable: false,
    isUploading: false,
    validExt: ['.pdb', '.sdf', '.cif', '.ppt', '.pptx', '.pdf']
  },

  created() {
    document.body.addEventListener('dragenter', e => {
      this.numDropping = e.dataTransfer.items.length
      this.isDroppable = true
    })

    this.requestList()
  },

  methods: {
    async requestList() {
      const res = await fetch('/list')
      const json = await res.json()
      const files = json.file_list.map(name => ({ name }))

      this.files = []
      for (const file of files) {
        const [full, name, ext] = /^(.+)\.(\w+)$/.exec(file.name)
        this.files.push({ full, name, ext })
      }
    },

    async deleteFile(filename) {
      await fetch(`/${filename}`, { method: 'DELETE' })
      await this.requestList()
    },

    onChange(e) {
      this.upload(e.target.files)
      e.target.value = null
    },

    drop(e) {
      const files = e.dataTransfer.files
      this.upload(files)
      this.isDroppable = false
    },

    async upload(files) {
      this.isUploading = true

      const numBefore = files.length
      files = Array.from(files).filter(f => {
        const [, ext] = /(\.\w+)$/.exec(f.name)
        return this.validExt.includes(ext)
      })

      const numRemoved = numBefore - files.length
      if (numRemoved) {
        alert(`${numRemoved} unsupported files skipped`)
      }

      // only post if we have valid files
      if (files.length) {
        const data = new FormData()
        for (const file of files) {
          data.append('files[]', file)
        }

        await fetch('/', {
          method: 'POST',
          body: data
        })
        await this.requestList()
      }

      this.isUploading = false
    }
  }
})
