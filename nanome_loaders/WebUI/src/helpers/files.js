const IGNORE_FILES = ['.DS_Store', 'Thumbs.db']

function getFile(item) {
  return new Promise(resolve => {
    item.file(file => resolve(file))
  })
}

function getEntries(item) {
  const reader = item.createReader()
  return new Promise(resolve => {
    reader.readEntries(entries => resolve(entries))
  })
}

async function traverseDir(item, path = '') {
  const tree = []
  if (item.isFile && !IGNORE_FILES.includes(item.name)) {
    const f = await getFile(item)
    const file = new File([f], path + item.name, { type: f.type })
    tree.push(file)
  } else if (item.isDirectory) {
    path += item.name + '/'
    const entries = await getEntries(item)
    const promises = entries.map(entry => traverseDir(entry, path))
    const list = await Promise.all(promises)
    tree.push(...list)
  }

  return tree
}

export async function getFiles(event) {
  const tree = []
  const items = event.dataTransfer.items
  for (const item of items) {
    const entry = item.webkitGetAsEntry()
    if (entry) {
      const list = await traverseDir(entry)
      tree.push(...list)
    }
  }
  return tree.flat(Infinity)
}
