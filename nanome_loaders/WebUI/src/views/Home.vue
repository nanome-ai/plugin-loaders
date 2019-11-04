<template>
  <div class="home min-h-full container m-auto bg-white flex flex-col">
    <header class="pt-10 mx-auto">
      <h1 class="inline-flex items-baseline">
        <img class="mr-4" src="@/assets/logo.png" /> Vault
      </h1>
      <h2>Upload files to make them available in Nanome!</h2>
    </header>

    <p class="text-lg pt-2 pb-4">
      Drag and drop or click the new file button to upload files.<br />
      Supports <b>{{ extensions.join(' ') }}</b>
    </p>

    <div class="text-left">
      <div class="text-lg text-left px-4 py-2 ml-4 rounded bg-gray-200 inline">
        <template v-if="$store.state.name">
          Welcome <b>{{ $store.state.name }}!</b>&nbsp;
          <a @click="$store.dispatch('logout')" class="link text-red-500"
            >log out</a
          >
        </template>
        <template v-else>
          Welcome!
          <a @click="$modal.login()" class="link text-blue-500">log in</a>
        </template>
      </div>
    </div>

    <file-explorer />
  </div>
</template>

<script>
import FileExplorer from '@/components/FileExplorer'
import extensions from '@/helpers/extensions'

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
