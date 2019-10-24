<template>
  <div class="toolbar flex text-lg items-center">
    <div class="toggle relative mr-2 flex">
      <input
        @input="$emit('display-mode', $event.target.value)"
        checked
        value="grid"
        type="radio"
        name="display-mode"
        id="display-mode-grid"
      />
      <label for="display-mode-grid" class="btn rounded-l">
        <fa-icon icon="th" />
      </label>
      <input
        @input="$emit('display-mode', $event.target.value)"
        value="list"
        type="radio"
        name="display-mode"
        id="display-mode-list"
      />
      <label for="display-mode-list" class="btn rounded-r">
        <fa-icon icon="bars" />
      </label>
    </div>
    <button class="btn rounded mr-2" @click="$emit('new-folder')">
      <fa-layers>
        <fa-icon icon="folder" />
        <fa-icon icon="plus" transform="down-1 shrink-10" class="text-white" />
      </fa-layers>
      <span class="hidden lg:inline"> new folder</span>
    </button>
    <button class="btn rounded" @click="$emit('show-upload')">
      <fa-icon icon="cloud-upload-alt" />
      <span class="hidden lg:inline"> upload</span>
    </button>
    <div class="flex-grow"></div>
    <div class="search relative">
      <input
        type="search"
        @input="$emit('search', $event.target.value)"
        class="border rounded py-2 px-3"
        placeholder="search..."
      />
      <fa-icon icon="search" class="absolute text-gray-400 icon" />
    </div>
  </div>
</template>

<style lang="scss">
.toolbar {
  .toggle {
    input {
      position: absolute !important;
      clip: rect(0, 0, 0, 0);
      height: 1px;
      width: 1px;
      border: 0;
      overflow: hidden;
    }

    label {
      cursor: pointer;
    }

    input:checked + label {
      @apply bg-gray-700 text-white;
    }
  }

  .search {
    .icon {
      top: 50%;
      left: 0.5em;
      transform: translateY(-50%);
    }

    input {
      padding-left: 2em;

      &:focus {
        outline: none;
      }

      &:focus + .icon {
        @apply text-gray-700;
      }
    }
  }
}
</style>
