<template>
  <div class="home min-h-full container m-auto bg-white flex flex-col">
    <header class="pt-10 mx-auto">
      <h1 class="inline-flex items-baseline">
        <img class="mr-4" src="@/assets/logo.png" /> Vault
      </h1>
      <h2>Upload files to make them available in Nanome!</h2>
    </header>

    <p class="text-lg py-5">
      Drag and drop or click the new file button to upload files.<br />
      Supports <b>{{ extensions.join(' ') }}</b>
    </p>

    <file-explorer />
  </div>
</template>

<script>
import FileExplorer from '@/components/FileExplorer'
import extensions from '@/extensions'

export default {
  components: { FileExplorer },
  data: () => ({ extensions })
}
</script>

<style lang="scss">
header {
  img {
    height: 1em;
  }
}
</style>
